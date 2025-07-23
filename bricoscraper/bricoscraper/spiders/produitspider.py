import scrapy


class ProduitspiderSpider(scrapy.Spider):
    name = "produitspider"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com/"]

    def parse(self, response):
        pass
