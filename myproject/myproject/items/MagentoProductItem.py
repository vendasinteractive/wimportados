# -*- coding: utf-8 -*-

import scrapy
import json

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars, replace_entities


#handle configurable products
#map to magmi importer file spec


class MagentoBaseProductItem(scrapy.Item):

    #old values
    #sku = scrapy.Field()
    #name = scrapy.Field()
    #description = scrapy.Field()
    #price = scrapy.Field()
    size = scrapy.Field()
    #category = scrapy.Field()

    color = scrapy.Field()
    
    sizes = scrapy.Field()
    store = scrapy.Field()
    categories = scrapy.Field()
    websites = scrapy.Field()
    attribute_set = scrapy.Field()
    type = scrapy.Field()
    sku = scrapy.Field()
    has_options = scrapy.Field()
    name = scrapy.Field()
    meta_title = scrapy.Field()
    image = scrapy.Field()
    small_image = scrapy.Field()
    thumbnail = scrapy.Field()
    page_layout = scrapy.Field()
    options_container = scrapy.Field()
    msrp_enabled = scrapy.Field()
    msrp_display_actual_price_type = scrapy.Field()
    gift_message_available = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    visibility = scrapy.Field()
    tax_class_id = scrapy.Field()
    description = scrapy.Field()
    short_description = scrapy.Field()
    qty = scrapy.Field()
    min_qty = scrapy.Field()
    use_config_min_qty = scrapy.Field()
    is_qty_decimal = scrapy.Field()
    backorders = scrapy.Field()
    use_config_backorders = scrapy.Field()
    min_sale_qty = scrapy.Field()
    use_config_min_sale_qty = scrapy.Field()
    max_sale_qty = scrapy.Field()
    use_config_max_sale_qty = scrapy.Field()
    is_in_stock = scrapy.Field()
    use_config_notify_stock_qty = scrapy.Field()
    manage_stock = scrapy.Field()
    use_config_manage_stock = scrapy.Field()
    stock_status_changed_auto = scrapy.Field()
    use_config_qty_increments = scrapy.Field()
    qty_increments = scrapy.Field()
    use_config_enable_qty_inc = scrapy.Field()
    enable_qty_increments = scrapy.Field()
    is_decimal_divided = scrapy.Field()
    stock_status_changed_automatically = scrapy.Field()
    use_config_enable_qty_increments = scrapy.Field()
    product_name = scrapy.Field()
    store_id = scrapy.Field()
    product_type_id = scrapy.Field()
    weight = scrapy.Field()
    
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()


    store = "admin"
    websites = "base"
    has_options = 0
    page_layout = "No layout updates"
    options_container = "Product Info Column"
    msrp_enabled = "Use config"
    msrp_display_actual_price_type = "Use config"
    gift_message_available = "No"
    min_qty = 0
    use_config_min_qty = 1
    is_qty_decimal = 0
    backorders = 0
    use_config_backorders = 1
    min_sale_qty = 1
    use_config_min_sale_qty = 1
    max_sale_qty = 0
    use_config_max_sale_qty = 1
    use_config_notify_stock_qty = 1
    manage_stock = 0
    use_config_manage_stock = 1
    stock_status_changed_auto = 0
    use_config_qty_increments = 1
    qty_increments = 0
    use_config_enable_qty_inc = 1
    enable_qty_increments = 0
    is_decimal_divided = 0
    stock_status_changed_automatically = 0
    use_config_enable_qty_increments = 1
    store_id = 0
    product_type_id = "simple"
    weight = 1
    qty = 100
    is_in_stock = 1
    status = "Disabled"









class MagentoConfigurableProductItem(MagentoBaseProductItem):
    visibility = "Not Visible Individually"
    type = "configurable"

class MagentoSimpleProductItem(MagentoBaseProductItem):
    visibility = "Catalog, Search"
    type = "simple"


#    def loadDefaultValues(self):
#        self["store"] = "admin"
#        self["websites"] = "base"
#        self["has_options"] = 0
#        self["page_layout"] = "No layout updates"
#        self["options_container"] = "Product Info Column"
#        self["msrp_enabled"] = "Use config"
#        self["msrp_display_actual_price_type"] = "Use config"
#        self["gift_message_available"] = "No"
#        self["min_qty"] = 0
#        self["use_config_min_qty"] = 1
#        self["is_qty_decimal"] = 0
#        self["backorders"] = 0
#        self["use_config_backorders"] = 1
#        self["min_sale_qty"] = 1
#        self["use_config_min_sale_qty"] = 1
#        self["max_sale_qty"] = 0
#        self["use_config_max_sale_qty"] = 1
#        self["use_config_notify_stock_qty"] = 1
#        self["manage_stock"] = 0
#        self["use_config_manage_stock"] = 1
#        self["stock_status_changed_auto"] = 0
#        self["use_config_qty_increments"] = 1
#        self["qty_increments"] = 0
#        self["use_config_enable_qty_inc"] = 1
#        self["enable_qty_increments"] = 0
#        self["is_decimal_divided"] = 0
#        self["stock_status_changed_automatically"] = 0
#        self["use_config_enable_qty_increments"] = 1
#        self["store_id"] = 0
#        self["product_type_id"] = "simple"
#        self["weight"] = 1
#        self["qty"] = 100
#        self["is_in_stock"] = 1
#        item["status"] = "Disabled"



#type = "simple"

#sku
#name
#product_name
#description
#short_description
#meta_title
#color
#size
#categories
#tax_class_id = "Taxable Goods"
#image
#small_image
#thumbnail

#price
#status ="Enabled"
#visibility = "Catalog, Search" #only for Simple Product Types
#qty = 1
#is_in_stock = 1

#    def set_configurable_product():
#        set_default_values()





