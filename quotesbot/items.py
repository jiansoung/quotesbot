# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class QuotesbotItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author_or_title = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

    def __getitem__(self, key):
        if key in self.fields:
            return self[key]
        raise KeyError("%s does not support field: %s" % (self.__class__.__name__, key))

    def __setitem__(self, key, value):
        if key in self.fields:
            self[key] = value
        else:
            raise KeyError("%s does not support field: %s" % (self.__class__.__name__, key))
