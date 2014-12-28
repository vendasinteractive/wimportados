# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from myproject.items.MagentoProductItem import MagentoSimpleProductItem, MagentoConfigurableProductItem, MagentoBaseProductItem
from myproject.loaders.TJMaxxSimpleProductLoader import TJMaxxSimpleProductLoader

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

import json
import time

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
    
    def parse_item(self, response):
        #self.log('Hi, this is an item page! %s' % response.url)
        
        item_fields = {
            "name": '//div[@class="product-details"]//h2[@class="product-title"]/text()',
            "manufacturer": '//div[@class="product-details"]//h1[@class="product-brand"]/text()',
            "categories": '//script[contains(., "_DataLayer")]',
            "description": '//div[@class="product-description"]//ul[contains(@class, "description-list")]',
            "price": '//p[contains(@class, "price")]//span[contains(@class, "product-price")]',
            "image_urls": '//img[@class="main-image"]/@src'
        }
        
        sel = Selector(response)
        script_data = sel.xpath('//script[contains(., "TJXdata.productData")]//text()')
        variant_list = script_data.extract()
        json_text = variant_list[0].replace("var TJXdata = TJXdata || {};\n\t\tTJXdata.productData =", "")
        data = json.loads(json_text)
        
        list = []
        
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
                vr.configurable_attributes = "color"
                vr.attribute_set = "ColorOnly"
            if (vr.color is None and vr.size is not None):
                vr.configurable_attributes = "size"
                vr.attribute_set = "SizeOnly"
            if (vr.color is not None and vr.size is not None):
                vr.configurable_attributes = "color, size"
                vr.attribute_set = "ColorAndSize"
            if (vr.color is None and vr.size is None):
                vr.vr.configurable_attributes = ""
                vr.attribute_set = "Default"
            
            list.append(vr)
        

        #Create BaseItem
        BaseItem = self.CreateMangentoProduct()
        
        simple_loader = TJMaxxSimpleProductLoader(BaseItem, response=response)
        simple_loader.add_value("sku", parent_sku)
        simple_loader.add_xpath("name", item_fields["name"])
        simple_loader.add_xpath("product_name", item_fields["name"])
        simple_loader.add_xpath("manufacturer", item_fields["manufacturer"])
        simple_loader.add_xpath("description", item_fields["description"])
        simple_loader.add_xpath("short_description", item_fields["description"])
        #simple_loader.add_xpath("price", item_fields["price"])
        simple_loader.add_value("price", "22.22")
        simple_loader.add_xpath("image_urls", item_fields["image_urls"])
        simple_loader.add_xpath("categories", item_fields["categories"])
        simple_loader.add_value("original_url", response.url)
        BaseItem = simple_loader.load_item()
        
        if len(list)==1:
            #This is if not a variant
            SimpleItem = MagentoSimpleProductItem(BaseItem)
            SimpleItem["type"] = "simple"
            SimpleItem["attribute_set"] = "Default"
            SimpleItem["visibility"] = "Catalog, Search"
            yield SimpleItem
        else:
            for var in list:
                #loops through all variants (e.g. simple items)
                VariantSimpleItem = MagentoSimpleProductItem(BaseItem)
                VariantSimpleItem["sku"] = var.sku
                VariantSimpleItem["color"] = var.color
                VariantSimpleItem["size"] = var.size
                VariantSimpleItem["type"] = "simple"
                VariantSimpleItem["attribute_set"] = var.attribute_set
                VariantSimpleItem["configurable_attributes"] = var.configurable_attributes
                VariantSimpleItem["visibility"] = "Not Visible Individually"
                yield VariantSimpleItem
            
            if len(list)>0:
                #this is the parent (e.g. configurable product)
                ConfigurableItem = MagentoConfigurableProductItem(BaseItem)
                ConfigurableItem["type"] = "configurable"
                ConfigurableItem["configurable_attributes"] = list[0].configurable_attributes
                ConfigurableItem["attribute_set"] = list[0].attribute_set
                ConfigurableItem["visibility"] = "Catalog, Search"
                yield ConfigurableItem


    #TODO Extract this out into common code
    def CreateMangentoProduct(self):
        current_timestamp = time.strftime("%Y-%m-%d")
        item = MagentoBaseProductItem()
        item["store"] = "admin"
        item["websites"] = "base"
        item["has_options"] = 0
        item["page_layout"] = "No layout updates"
        item["options_container"] = "Product Info Column"
        item["msrp_enabled"] = "Use config"
        item["msrp_display_actual_price_type"] = "Use config"
        item["gift_message_available"] = "No"
        item["min_qty"] = 0
        item["use_config_min_qty"] = 1
        item["is_qty_decimal"] = 0
        item["backorders"] = 0
        item["use_config_backorders"] = 1
        item["min_sale_qty"] = 1
        item["use_config_min_sale_qty"] = 1
        item["max_sale_qty"] = 0
        item["use_config_max_sale_qty"] = 1
        item["use_config_notify_stock_qty"] = 1
        item["manage_stock"] = 0
        item["use_config_manage_stock"] = 1
        item["stock_status_changed_auto"] = 0
        item["use_config_qty_increments"] = 1
        item["qty_increments"] = 0
        item["use_config_enable_qty_inc"] = 1
        item["enable_qty_increments"] = 0
        item["is_decimal_divided"] = 0
        item["stock_status_changed_automatically"] = 0
        item["use_config_enable_qty_increments"] = 1
        item["weight"] = 1
        item["qty"] = 100
        item["is_in_stock"] = 1
        item["status"] = "Disabled"
        
        
        item["feed_updated_date"] = current_timestamp
        item["created_date"] = current_timestamp
        return item        
                
class Variant():
    sku = None
    color = None
    size = None
    attribute_set = None
    configurable_attributes = None