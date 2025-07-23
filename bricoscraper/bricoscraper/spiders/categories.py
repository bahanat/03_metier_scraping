import scrapy


class CategoriesSpider(scrapy.Spider):
    name = "categories"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com"]

    def parse(self, response):
        pass
