# -*- coding: utf-8 -*-

# Scrapy settings for myproject project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'myproject'

SPIDER_MODULES = ['myproject.spiders']
NEWSPIDER_MODULE = 'myproject.spiders'
EDITOR = "open -a gedit"

ITEM_PIPELINES = {  'myproject.pipelines.DuplicatesPipeline': 300,
                    'myproject.pipelines.MyImagesPipeline': 400
                 }
#IMAGES_STORE = '/Users/michaelwhalen/Documents/Vendas Interactive/wimportados/myproject/data/images'

IMAGES_STORE = '/Library/WebServer/Documents/magento/media/import'
IMAGES_THUMBS = {
    'small': (100, 100),
    'big': (498, 498),
}

CLOSESPIDER_ITEMCOUNT = 100


#UPDATE WITH DYNAMIC SPIDER AND TIME STAMP
#FEED_URI = '/Users/michaelwhalen/Documents/Vendas Interactive/wimportados/myproject/data/%(name)s/%(time)s.csv'
FEED_URI = '/Library/WebServer/Documents/magento/var/import/%(name)s_%(time)s.csv'
FEED_FORMAT = 'csv'



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'myproject (+http://www.yourdomain.com)'
