# -*- coding: utf-8 -*-
import scrapy


class PopularQuotesSpider(scrapy.Spider):
    name = 'popular_quotes'
    allowed_domains = ['https://www.goodreads.com/quotes']
    start_urls = ['http://https://www.goodreads.com/quotes/']

    def parse(self, response):
        pass
