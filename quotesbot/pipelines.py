# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import json

import pymongo
import MySQLdb
from scrapy.exceptions import DropItem


# class QuotesbotPipeline(object):
#     def process_item(self, item, spider):
#         return item

def sanitize_item(item):
    item['text'] = normalize_text(item['text'])
    item['author_or_title'] = normalize_name(item['author_or_title'])
    item['tags'] = normalize_tags(item['tags'])

def normalize_text(text):
    _text = text.strip()
    # TODO
    return _text

def normalize_name(name):
    _name = name.strip()
    # TODO: do more to make _name more identical.
    return _name

def normalize_tag(tag):
    _tag = tag.strip()
    # TODO
    return _tag

def normalize_tags(tags):
    return list(set([normalize_tag(tag) for tag in tags]))

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
        unique_key = item['author_or_title'] + ': ' + item['text']
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


class MySQLPipeline(object):

    def __init__(self, user, passwd, db, host, port, **options):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.host = host
        self.port = port
        self.options = options

    @classmethod
    def from_crawler(cls, crawler):
        mysql_settings = crawler.settings.get('MYSQL_SETTINGS')
        return cls(
            user=mysql_settings['user'],
            passwd=mysql_settings['passwd'],
            db=mysql_settings['db'],
            host=mysql_settings.get('host', 'localhost'),
            port=mysql_settings.get('port', 3306),
            **mysql_settings.get('options', {})
        )

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            host=self.host,
            port=self.port,
            **self.options,
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        if not self.save_item(item):
            raise DropItem('item: {} insert failed'.format(item))
        return item

    def save_item(self, item):
        tag_ids = self.insert_tags(item)
        quote_id = self.insert_quote(item)
        return self.insert_quote_tag_assoc(quote_id, tag_ids)

    def insert_author(self, item):
        name, image_path = item['author_or_title'], self.image_path(item)
        if name == '':
            return None
        sql_statement = 'INSERT INTO authors (name, image_path) VALUES (%s, %s);'
        params = (name.encode('utf-8'), image_path)
        try:
            self.cursor.execute(sql_statement, params)
            author_id = self.cursor.lastrowid
            self.conn.commit()
        except MySQLdb.MySQLError as _:
            self.conn.rollback()
            result = self.search_author_by_name(name)
            author_id = result[0] if result else None
        return author_id

    def search_author_by_name(self, name):
        sql_statement = 'SELECT * FROM authors WHERE name = %s LIMIT 1;'
        self.cursor.execute(sql_statement, (name.encode('utf-8'), ))
        return self.cursor.fetchone()

    def insert_tags(self, item):
        tag_ids = []
        tags = item['tags']
        sql_statement = 'INSERT INTO tags (name) VALUES (%s);'
        for tag in tags:
            try:
                self.cursor.execute(sql_statement, (tag.encode('utf-8'), ))
                tag_ids.append(self.cursor.lastrowid)
                self.conn.commit()
            except MySQLdb.MySQLError as _:
                self.conn.rollback()
                result = self.search_tag_by_name(tag)
                if result: tag_ids.append(result[0])
        return tag_ids

    def search_tag_by_name(self, name):
        sql_statement = 'SELECT * FROM tags WHERE name = %s LIMIT 1;'
        self.cursor.execute(sql_statement, (name.encode('utf-8'), ))
        return self.cursor.fetchone()

    def insert_quote(self, item):
        author_id, text = self.insert_author(item), item['text']
        sql_statement = 'INSERT INTO quotes (author_id, text) VALUES (%s, %s);'
        params = (author_id, text.encode('utf-8'))
        try:
            self.cursor.execute(sql_statement, params)
            lastrowid = self.cursor.lastrowid
            self.conn.commit()
        except MySQLdb.MySQLError as _:
            self.conn.rollback()
            result = self.search_quote_by_unique_key(author_id, text)
            lastrowid = result[0] if result else None
        return lastrowid

    def search_quote_by_unique_key(self, author_id, text):
        sql_statement = 'SELECT * FROM quotes WHERE author_id=%s AND text=%s LIMIT 1;'
        self.cursor.execute(sql_statement, (author_id, text.encode('utf-8')))
        return self.cursor.fetchone()

    def insert_quote_tag_assoc(self, quote_id, tag_ids):
        if not (quote_id and tag_ids):
            return False
        insert_ok = False
        sql_statement = 'INSERT INTO quote_tag_assoc (quote_id, tag_id) VALUES (%s, %s);'
        for tag_id in tag_ids:
            try:
                self.cursor.execute(sql_statement, (quote_id, tag_id))
                self.conn.commit()
                insert_ok = True
            except MySQLdb.MySQLError as _:
                self.conn.rollback()
                insert_ok = insert_ok or False
        return insert_ok

    def image_path(self, item):
        return item['images'][0]['path'] if item['images'] else ''
