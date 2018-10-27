# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import pymongo
from scrapy.exceptions import DropItem


# class QuotesbotPipeline(object):
#     def process_item(self, item, spider):
#         return item

def sanitize_item(item):
    item['text'] = item['text'].strip().strip('\u201c\u201d')
    item['author_or_title'] = item['author_or_title'].strip()


class QuotePipeline(object):
    # This method is called for every item pipeline component. process_item()
    # must either: return a dict with data, return an Item (or any descendant
    # class) object, return a Twisted Deferred or raise DropItem exception.
    # Dropped items are no longer processed by further pipeline components.
    def process_item(self, item, spider):
        sanitize_item(item)
        text = item['text']
        if text == '':
            raise DropItem("Missing text in %s" % item)
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.items_seen = set()

    def process_item(self, item, spider):
        unique_key = item['author_or_title'] + item['text']
        if unique_key in self.items_seen:
            raise DropItem("Duplicate item found: %s" % item)
        self.items_seen.add(unique_key)
        return item


# The purpose of JsonWriterPipeline is just to introduce how to write item
# pipelines. If you really want to store all scraped items into a JSON file you
# should use the Feed exports.
class JsonWriterPipeline(object):

    # This method is called when the spider is opened.
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    # This method is called when the spider is closed.
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # If present, this classmethod is called to create a pipeline instance from
    # a Crawler. It must return a new instance of the pipeline. Crawler object
    # provides access to all Scrapy core components like settings and signals;
    # it is a way for pipeline to access them and hook its functionality into
    # Scrapy.
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
