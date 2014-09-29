# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import SitemapSpider
from scrapy.contrib.loader import ItemLoader
from myproject.items.MagentoProductItem import MagentoSimpleProductItem
from myproject.loaders.HollisterProductLoader import HollisterProductLoader

class HollisterSpider(SitemapSpider):
    name = 'HollisterSpider'
    sitemap_urls = ['http://www.hollisterco.com/sitemap_10251_-1.xml.gz']
    sitemap_rules = [ ('/shop/us/p/', 'parse_shop')]

    item_fields = {
        "sku": '//div[@class="skus"]//li[@class="web-item-number"]//span[contains(@class, "number")]/text()',
        "name": '//span[@class="product__description--name"]/text()',
        "price": '//span[contains(@class, "product-price--offer")]/text()',
        "description": '//section[@class="product__details"]/p',
        "sizes": '//li[@class="product-sizes__size-wrapper"]//div[@class="product-sizes__size"]/text()',
        "image_urls": '//section[contains(@class, "product__images")]//img[contains(@class, "product__images--image")]/@src',
        "categories": '//div[@class="product__breadcrumb--content"]'
    }


    def parse_shop(self, response):

        loader = HollisterProductLoader(item=MagentoProductItem(), response=response)
        
        for field, xpath in self.item_fields.iteritems():
            loader.add_xpath(field, xpath)
        return loader.load_item()

