# -*- coding: utf-8 -*-
import json
import time

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from myproject.items.ProductVariant import ProductVariant
from myproject.loaders.TJMaxxProductLoader import TJMaxxProductLoader
from myproject.items.ProductFactory import ProductFactory

class TjmaxxSpider(CrawlSpider):
    name = "TJMaxxSpider"
    allowed_domains = ["tjmaxx.tjx.com"]
    start_urls = (
        'http://tjmaxx.tjx.com/store/index.jsp',
    )

    rules = (
        Rule(LinkExtractor(allow=("/store/jump/category",))),
        Rule(LinkExtractor(allow=("/store/jump/product", )), callback="parse_item")
    )

    factory = ProductFactory()

    def get_clean_json_data(self, response):
        selector = Selector(response)
        script_data = selector.xpath('//script[contains(., "TJXdata.productData")]//text()')
        variant_list = script_data.extract()
        json_text = variant_list[0].replace("var TJXdata = TJXdata || {};\n\t\tTJXdata.productData =", "")
        clean_json_data = json.loads(json_text)
        return clean_json_data


    def create_tjmaxx_base_product_item(self, item_fields, parent_sku, response):
        # Create tjmaxx_base_product_item
        base_product_item = self.factory.create_base_product_item()
        loader = TJMaxxProductLoader(base_product_item, response=response)
        loader.add_value("sku", parent_sku)
        loader.add_xpath("name", item_fields["name"])
        loader.add_xpath("product_name", item_fields["name"])
        loader.add_xpath("manufacturer", item_fields["manufacturer"])
        loader.add_xpath("description", item_fields["description"])
        loader.add_xpath("short_description", item_fields["description"])
        #loader.add_xpath("price", item_fields["price"])
        loader.add_value("price", "22.22")
        loader.add_xpath("image_urls", item_fields["image_urls"])
        loader.add_xpath("categories", item_fields["categories"])
        loader.add_value("original_url", response.url)
        tjmaxx_base_product_item = loader.load_item()

        return tjmaxx_base_product_item


    def get_variant_list(self, data, keys, parent_sku):
        variant_list = []
        for sku in data[keys[0]]["skus"]:
            variant = ProductVariant()
            for variant_key in sku["variants"].keys():
                if (len(sku["variants"][variant_key]["displayName"]) <= 2):
                    variant.size = sku["variants"][variant_key]["displayName"]
                else:
                    variant.color = sku["variants"][variant_key]["displayName"]
            variant.sku = parent_sku

            # set configurable attributes and attribute set for variants
            if (variant.color is not None and variant.size is None):
                variant.configurable_attributes = "color"
                variant.attribute_set = "ColorOnly"
            if (variant.color is None and variant.size is not None):
                variant.configurable_attributes = "size"
                variant.attribute_set = "SizeOnly"
            if (variant.color is not None and variant.size is not None):
                variant.configurable_attributes = "color, size"
                variant.attribute_set = "ColorAndSize"
            if (variant.color is None and variant.size is None):
                variant.configurable_attributes = ""
                variant.attribute_set = "Default"

            variant_list.append(variant)
        return variant_list


    def parse_item(self, response):
        #self.log('Hi, this is an item page! %s' % response.url)
        
        item_fields = {
            "name": '//div[@class="product-details"]//h2[@class="product-title"]/text()',
            "manufacturer": '//div[@class="product-details"]//h1[@class="product-brand"]/text()',
            "categories": '//script[contains(., "_DataLayer")]',
            "description": '//div[@class="product-description"]//ul[contains(@class, "description-variant_list")]',
            "price": '//p[contains(@class, "price")]//span[contains(@class, "product-price")]',
            "image_urls": '//img[@class="main-image"]/@src'
        }

        data = self.get_clean_json_data(response)
        keys = data.keys()
        parent_sku = keys[0]

        base_item = self.create_tjmaxx_base_product_item(item_fields, parent_sku, response)
        variant_list = self.get_variant_list(data, keys, parent_sku)
        
        if len(variant_list)==1:
            #This is if not a variant
            simple_item = self.factory.create_simple_product_item(base_item)
            yield simple_item
        else:
            for variant in variant_list:
                #loops through all variants (e.g. simple items)
                simple_variant_product_item = self.factory.get_simple_variant_product_item(base_item, variant)
                yield simple_variant_product_item
            
            if len(variant_list)>0:
                #this is the parent (e.g. configurable product)
                configurable_attributes = variant_list[0].configurable_attributes
                attribute_set = variant_list[0].attribute_set
                configurable_item = self.factory.get_configurable_product_item(base_item, attribute_set, configurable_attributes)
                yield configurable_item
