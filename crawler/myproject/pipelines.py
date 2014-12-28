# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        #Sprint "item['image_urls']: %s", item['image_urls']
        yield scrapy.Request(item['image_urls'])
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        item['image'] = image_paths
        item['small_image'] = image_paths
        item['thumbnail'] = image_paths
        return item


#Insert Duplicate Pipeline here
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    
    def __init__(self):
        self.ids_seen = set()
    
    def process_item(self, item, spider):
        if item['sku'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['sku'])
            return item