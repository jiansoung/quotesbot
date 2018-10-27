# quotesbot

Let's Play with Scrapy !


## Run all spiders

```shell
./run_spider.sh
```


## Scrapy in quotesbot

### Spiders

- goodreads_quotes: spider for crawling quotes on goodreads.


### Items

- QuoteItem

### Pipelines

- 'scrapy.pipelines.images.ImagesPipeline'
- 'quotesbot.pipelines.QuotePipeline'
- 'quotesbot.pipelines.DuplicatesPipeline'
- 'quotesbot.pipelines.JsonWriterPipeline' (disabled)
- 'quotesbot.pipelines.MongoPipeline' (disabled)


## TODO

- [Settings](https://doc.scrapy.org/en/latest/topics/settings.html)
- [AutoThrottle extension](https://doc.scrapy.org/en/latest/topics/autothrottle.html)
- SQLitePipeline
- MySQLPipeline
- PostgreSQLPipeline
- RedisPipeline
- ORM (Peewee / SQLAlchemy)
- Login / Logout
- Auto HTTP Proxy Switch
- [Deploying Spiders](https://doc.scrapy.org/en/latest/topics/deploy.html)
- [Signals](https://doc.scrapy.org/en/latest/topics/signals.html)
- [Jobs: pausing and resuming crawls](https://doc.scrapy.org/en/latest/topics/jobs.html)
- [Spiders Contracts](https://doc.scrapy.org/en/latest/topics/contracts.html)
- More Spiders
