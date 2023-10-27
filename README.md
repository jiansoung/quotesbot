# quotesbot

Let's Play with Scrapy !


## Requirement

- MySQL
- Python 3.x


## Create database
```shell
mysql < mysql_schema.sql
```


## Run all spiders

```shell
./run_spider.sh
```

you can also run some spiders with following command:

```shell
./run_spider.sh [spider1] [spider2] ...
```


## Scrapy in quotesbot

### Spiders

- goodreads_quotes: spider for crawling quotes from goodreads.com.
- brainyquote: spider for crawling quotes from brainyquote.com.


## TODO

- Fix brainyquote spider 403 error.
- Add likes to goodreads_quotes spider and database schema.

ps: 
```python
# '169019 likes'
likes = quote.css('div.quoteFooter div.right a::text').extract_first()
```