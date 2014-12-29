# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import SitemapSpider
from myproject.loaders.HollisterProductLoader import HollisterProductLoader

from myproject.items.ProductFactory import ProductFactory
from scrapy.selector import Selector

class HollisterSpider(SitemapSpider):
    name = 'HollisterSpider'
    sitemap_urls = ['http://www.hollisterco.com/sitemap_10251_-1.xml.gz']
    sitemap_rules = [ ('/shop/us/p/', 'parse_shop')]

    factory = ProductFactory()

    def create_hollister_base_product_item(self, response):
        # Create hollister_base_product_item
        base_product_item = self.factory.create_base_product_item()
        loader = HollisterProductLoader(base_product_item, response=response)
        loader.add_xpath("sku", '//div[@class="skus"]//li[@class="web-item-number"]//span[contains(@class, "number")]/text()')
        loader.add_xpath("name", '//span[@class="product__description--name"]/text()')
        #loader.add_xpath("product_name", item_fields["name"])
        #loader.add_xpath("manufacturer", item_fields["manufacturer"])
        loader.add_xpath("description", '//section[@class="product__details"]/p')
        #loader.add_xpath("short_description", item_fields["description"])
        loader.add_xpath("price", '//span[contains(@class, "product-price--offer")]/text()')
        #loader.add_value("price", "22.22")
        loader.add_xpath("image_urls", '//section[contains(@class, "product__images")]//img[contains(@class, "product__images--image")]/@src')
        loader.add_xpath("categories", '//div[@class="product__breadcrumb--content"]')
        loader.add_value("original_url", response.url)
        hollister_base_product_item = loader.load_item()

        return hollister_base_product_item


    def parse_shop(self, response):

        #loads initial product
        base_item = self.create_hollister_base_product_item(response)
        simple_item = self.factory.create_simple_product_item(base_item)
        yield simple_item

        #load in variants (start with sizes)
        selector = Selector(response)
        data = selector.xpath('//section[@class="product__sizes product__sizes-api"]//div[@class="product-sizes__size"]/text()')
        self.log('This is slze data %s' % data)