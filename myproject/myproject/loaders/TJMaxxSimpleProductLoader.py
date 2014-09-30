# -*- coding: utf-8 -*-

import scrapy
import json

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars, replace_entities


class TJMaxxSimpleProductLoader(ItemLoader):
    
    def strip_dollar_sign(x):
        return  x.strip("$")
    
    def strip_whitespace(x):
        return x.strip()
    
    def add_http(x):
        y = "http:" + x +""
        return y
    
    def append_retailer(x):
        y = x.replace("home/", "/tjmaxx/")
        return y
    
    def extract_json(x):
        json_text = x.replace("_DataLayer = ", "")
        j_obj = json.loads(json_text)
        cat = j_obj["breadcrumb"]
        formated_cat = cat.replace(">", "/")
        return formated_cat
    
    default_output_processor = TakeFirst()
    
    name_in = MapCompose(unicode.title)
    name_out = Join()
    
    description_in = MapCompose(replace_escape_chars, strip_whitespace, remove_tags)
    
    short_description_in = MapCompose(replace_escape_chars, strip_whitespace, remove_tags)
    
    price_in = MapCompose(remove_tags, strip_whitespace, replace_escape_chars, strip_dollar_sign)
    
    image_urls_in = MapCompose(add_http)
    image_urls_out = Join()
    
    categories_in = MapCompose(remove_tags, replace_escape_chars, strip_whitespace, extract_json, append_retailer)
    
    sku_in = Join()
    sku_out = Join()
