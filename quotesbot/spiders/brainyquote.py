# -*- coding: utf-8 -*-
import scrapy
from quotesbot.items import QuoteItem


class BrainyQuoteSpider(scrapy.Spider):
    name = 'brainyquote'
    allowed_domains = ['brainyquote.com']
    start_urls = ['https://www.brainyquote.com/topics']

    def parse(self, response):
        for a in response.css('a.topicIndexChicklet'):
            yield response.follow(a, callback=self.parse_quotes_list)

    def parse_quotes_list(self, response):
        for item in response.css('div[class="m-brick grid-item boxy bqQt"]'):
            text = item.css('a.b-qt::text').extract()
            author = item.css('a.bq-aut::text').extract_first()
            tags = item.css('div.kw-box a::text').extract()
            yield QuoteItem(
                text=text,
                author_or_title=author,
                tags=tags,
                image_urls=[],
            )

        query = '//ul[@class="pagination "]/li[@class="active"]/following-sibling::li[1]/a'
        for a in response.xpath(query):
            yield response.follow(a, callback=self.parse_quotes_list)
