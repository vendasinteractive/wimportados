# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import SitemapSpider
from scrapy.contrib.loader import ItemLoader
from myproject.items.MagentoProductItem import MagentoSimpleProductItem
from myproject.loaders.HollisterProductLoader import HollisterProductLoader

from myproject.items.MagentoProductItem import MagentoSimpleProductItem, MagentoConfigurableProductItem, MagentoBaseProductItem
from myproject.loaders.TJMaxxSimpleProductLoader import TJMaxxSimpleProductLoader

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

import json
import time

from myproject.items.ProductFactory import ProductFactory


class HollisterSpider(SitemapSpider):
    name = 'HollisterSpider'
    sitemap_urls = ['http://www.hollisterco.com/sitemap_10251_-1.xml.gz']
    sitemap_rules = [ ('/shop/us/p/', 'parse_shop')]

    item_fields = {
        "sku": '//div[@class="skus"]//li[@class="web-item-number"]//span[contains(@class, "number")]/text()',
        "name": '//span[@class="product__description--name"]/text()',
        "price": '//span[contains(@class, "product-price--offer")]/text()',
        "description": '//section[@class="product__details"]/p',
        "image_urls": '//section[contains(@class, "product__images")]//img[contains(@class, "product__images--image")]/@src',
        "categories": '//div[@class="product__breadcrumb--content"]'
    }

    #"sizes": '//li[@class="product-sizes__size-wrapper"]//div[@class="product-sizes__size"]/text()',


    def parse_shop(self, response):

        #Create BaseItem
        BaseItem = ProductFactory.CreateMangentoProduct()

        SimpleItem = MagentoSimpleProductItem(BaseItem)
        SimpleItem["type"] = "simple"
        #SimpleItem["attribute_set"] = "Default"
        SimpleItem["visibility"] = "Catalog, Search"

        loader = HollisterProductLoader(item=MagentoSimpleProductItem(BaseItem), response=response)
        
        for field, xpath in self.item_fields.iteritems():
            loader.add_xpath(field, xpath)
        return loader.load_item()
