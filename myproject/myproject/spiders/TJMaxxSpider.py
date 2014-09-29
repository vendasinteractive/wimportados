# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from myproject.items.MagentoProductItem import MagentoSimpleProductItem, MagentoConfigurableProductItem
from myproject.loaders.TJMaxxSimpleProductLoader import TJMaxxSimpleProductLoader

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

import json

class TjmaxxspiderSpider(CrawlSpider):
    name = "TJMaxxSpider"
    allowed_domains = ["tjmaxx.tjx.com"]
    start_urls = (
        'http://tjmaxx.tjx.com/store/index.jsp',
    )

    rules = (
        Rule(LinkExtractor(allow=("/store/jump/category",))),
        Rule(LinkExtractor(allow=("/store/jump/product", )), callback="parse_item")
    )


    def parse_item(self, response):
        #self.log('Hi, this is an item page! %s' % response.url)

        #determine product type (does it have variants)
        #then load the parent as a configurable product
        
        #if variants exist load them as simple products
        #variants = get_variants(self, response)
        #for variant in variants:
        #    loader = TJMaxxSimpleProductLoader(item=MagentoProductItem(), response=response)
        #    loader.add_xpath("sku", '//body/@id')
        #    loader.add_xpath("name", '//div[@class="product-details"]//h1[@class="product-brand"]')
        #    loader.add_xpath("name", '//div[@class="product-details"]//h1[@class="product-title"]')
        #    loader.add_xpath("price", '//span[contains(@class, "product-price--offer")]')
        #    loader.add_xpath("description", '//div[@class="product-description"]//ul[contains(@class, "description-list")]')
        #    loader.add_xpath("image_urls", '//img[@class="main-image"]/@src')
        #    loader.add_xpath("category", '//script[contains(., "_DataLayer")]')
        #    loader.load_item()


        item_fields = {
            "sku": '//div[@class="skus"]//li[@class="web-item-number"]//span[contains(@class, "number")]/text()',
            "name": '//div[@class="product-details"]//h1[@class="product-brand"]',
            "price": '//span[contains(@class, "product-price--offer")]',
            "description": '//div[@class="product-description"]//ul[contains(@class, "description-list")]',
            "image_urls": '//img[@class="main-image"]/@src',
            "categories": '//script[contains(., "_DataLayer")]'
        }
        
        sel = Selector(response)
        script_data = sel.xpath('//script[contains(., "TJXdata.productData")]//text()')
        variant_list = script_data.extract()
        json_text = variant_list[0].replace("var TJXdata = TJXdata || {};\n\t\tTJXdata.productData =", "")
        data = json.loads(json_text)
        
        list = []
        i = 0
        
        has_a_color = False
        has_a_size = False
        
        #if a single variant then make it simple product
        keys = data.keys()
        parent_sku = keys[0]
        for sku in data[keys[0]]["skus"]:
            vr = Variant()
            for var_key in sku["variants"].keys():
                if(len(sku["variants"][var_key]["displayName"]) <=2):
                    vr.size=sku["variants"][var_key]["displayName"]
                else:
                    vr.color=sku["variants"][var_key]["displayName"]
            
            vr.sku = parent_sku
            if (vr.color is not None):
                vr.sku = vr.sku + "_" + vr.color
                has_a_color = True
            if (vr.size is not None):
                vr.sku = vr.sku + "_" + vr.size
                has_a_size = True
            
            #determine attribute_type
            #attribute_type can be color, size, or colorsize
            if (vr.color is not None and vr.size is None):
                vr.attribute_set = "ColorOnly"
            if (vr.color is None and vr.size is not None):
                vr.attribute_set = "SizeOnly"
            if (vr.color is not None and vr.size is not None):
                vr.attribute_set = "ColorAndSize"
            if (vr.color is None and vr.size is None):
                vr.attribute_set = "Default"
            
            list.append(vr)
        

        if len(list)==1:
            #This is if not a variant
            item = MagentoSimpleProductItem()
            
            simple_loader = TJMaxxSimpleProductLoader(item, response=response)
            simple_loader.add_value("sku", parent_sku)
            simple_loader.add_value("attribute_set", "Default")
            simple_loader.add_xpath("name", item_fields["name"])
            simple_loader.add_xpath("product_name", item_fields["name"])
            simple_loader.add_xpath("description", item_fields["description"])
            simple_loader.add_xpath("short_description", item_fields["description"])
            simple_loader.add_xpath("price", item_fields["price"])
            simple_loader.add_xpath("image_urls", item_fields["image_urls"])
            simple_loader.add_xpath("categories", item_fields["categories"])
            yield simple_loader.load_item()
        else:
            for var in list:
                #loops through all variants (e.g. simple items)
                item = MagentoSimpleProductItem()
                
                simple_loader = TJMaxxSimpleProductLoader(item, response=response)
                simple_loader.add_value("sku", var.sku)
                simple_loader.add_value("attribute_set", var.attribute_set)
                simple_loader.add_value("color", var.color)
                simple_loader.add_value("size", var.size)
                simple_loader.add_xpath("name", item_fields["name"])
                simple_loader.add_xpath("image_urls", item_fields["image_urls"])
                simple_loader.add_xpath("categories", item_fields["categories"])
                yield simple_loader.load_item()
            
            if len(list)>0:
                #this is the parent (e.g. configurable product)
                item = MagentoConfigurableProductItem()

                config_loader = TJMaxxSimpleProductLoader(item, response=response)
                config_loader.add_value("sku", parent_sku)
                simple_loader.add_value("attribute_set", var.attribute_set)
                config_loader.add_xpath("name", item_fields["name"])
                config_loader.add_xpath("description", item_fields["description"])
                config_loader.add_xpath("price", item_fields["price"])
                config_loader.add_xpath("image_urls", item_fields["image_urls"])
                config_loader.add_xpath("categories", item_fields["categories"])
                yield config_loader.load_item()



class Variant():
    sku = None
    color = None
    size = None
    attribute_set = None
