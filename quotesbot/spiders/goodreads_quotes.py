# -*- coding: utf-8 -*-
import scrapy


class GoodreadsQuotesSpider(scrapy.Spider):
    name = 'goodreads_quotes'
    allowed_domains = ['goodreads.com']
    start_urls = ['https://www.goodreads.com/quotes']

    def parse(self, response):
        for quote in response.css('div.quote'):
            image_src = quote.css('img::attr(src)').extract_first()
            text = quote.css('div.quoteText::text').extract_first().strip()
            author_or_title = quote.css('span.authorOrTitle::text').extract_first().strip()
            tags = quote.css('div.quoteFooter div.greyText a::text').extract()
            yield dict(
                image_src=image_src,
                text=text,
                author_or_title=author_or_title,
                tags=tags,
            )

        # next_page = response.css('a.next_page::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

        # for tag_link in response.css('ul.listTagsTwoColumn li.greyText'):
        #     tag_page = tag_link.css('a.gr-hyperlink::attr(href)').extract_first()
        #     yield response.follow(tag_page, callback=self.parse)
