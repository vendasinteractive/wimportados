# -*- coding: utf-8 -*-

import scrapy
import json

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars, replace_entities


#handle configurable products
#map to magmi importer file spec


class MagentoBaseProductItem(scrapy.Item):

    #def __init__(self):
    #    self["store"] = "store"
    #    self["websites"] = "websites"
    #    self["type"] = "type"
    #    super(scrapy.Item, self ).__init__()

    #item key
    sku = scrapy.Field()
    
    #common items scrapped from product detail page
    name = scrapy.Field(default=None)
    product_name = scrapy.Field(default="product_name")
    manufacturer = scrapy.Field(default="manufacturer")
    description = scrapy.Field(default="description")
    short_description = scrapy.Field(default="short_description")    
    price = scrapy.Field(default="price")
    image_urls = scrapy.Field(default="image_urls")
    categories = scrapy.Field(default="categories")    
    
    #data populated from Image Processor
    images = scrapy.Field(default="images")
    image_paths = scrapy.Field(default="image_paths")
    
    #product variant attributes
    attribute_set = scrapy.Field(default="attribute_set")
    size = scrapy.Field(default="size")
    color = scrapy.Field(default="color")
    
    
    store = scrapy.Field()
    websites = scrapy.Field()
    type = scrapy.Field()
    
    
    has_options = scrapy.Field()
    meta_title = scrapy.Field()
    image = scrapy.Field()
    small_image = scrapy.Field()
    thumbnail = scrapy.Field()
    page_layout = scrapy.Field()
    options_container = scrapy.Field()
    msrp_enabled = scrapy.Field()
    msrp_display_actual_price_type = scrapy.Field()
    gift_message_available = scrapy.Field()
    status = scrapy.Field()
    visibility = scrapy.Field()
    tax_class_id = scrapy.Field()
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
    store_id = scrapy.Field()
    product_type_id = scrapy.Field()
    weight = scrapy.Field()
    
    


class MagentoConfigurableProductItem(MagentoBaseProductItem):
    visibility = "Not Visible Individually"
    type = "configurable"

class MagentoSimpleProductItem(MagentoBaseProductItem):
    visibility = "Catalog, Search"
    type = "simple"






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





