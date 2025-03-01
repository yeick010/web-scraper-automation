import scrapy
import json
from scrapy.crawler import CrawlerProcess

class QuoteScraper(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = "https://quotes.toscrape.com/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "quote": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get()
            }

process = CrawlerProcess()
process.crawl(QuoteScraper)
process.start()

