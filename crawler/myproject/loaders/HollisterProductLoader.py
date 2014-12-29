# -*- coding: utf-8 -*-

import scrapy
import json

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars, replace_entities

class HollisterProductLoader(ItemLoader):

    def strip_dollar_sign(x):
        return  x.strip("$")
    
    def strip_whitespace(x):
        return x.strip()
    
    def add_http(x):
        y = "http:" + x +""
        return y
    
    def append_retailer(x):
        y = "hollister/" + x +""
        return y

    default_output_processor = TakeFirst()

    name_in = MapCompose(unicode.title)
    name_out = Join()

    description_in = MapCompose(replace_escape_chars, strip_whitespace, remove_tags)

    price_in = MapCompose(strip_dollar_sign)

    image_urls_in = MapCompose(add_http)
    image_urls_out = Join()

    categories_in = MapCompose(remove_tags, replace_escape_chars, replace_entities, strip_whitespace, append_retailer)