import scrapy
import json
import random
import pandas as pd
from scrapy.crawler import CrawlerProcess

# Lista di proxy per evitare blocchi
PROXY_LIST = [
    "http://proxy1.example.com:8000",
    "http://proxy2.example.com:8000",
    "http://proxy3.example.com:8000"
]

# Funzione per selezionare un proxy casuale
def get_random_proxy():
    return random.choice(PROXY_LIST)

class QuoteScraper(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        url = "https://quotes.toscrape.com/"
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={"proxy": get_random_proxy()}  # Assegna un proxy casuale
        )

    def parse(self, response):
        data = []
        for quote in response.css("div.quote"):
            item = {
                "quote": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get()
            }
            data.append(item)

        # Creazione del dataset CSV
        df = pd.DataFrame(data)
        df.to_csv("quotes_dataset.csv", index=False)  # Salva il dataset

# Avvio dello scraper
process = CrawlerProcess()
process.crawl(QuoteScraper)
process.start()

