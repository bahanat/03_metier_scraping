import scrapy


class ProduitSpider(scrapy.Spider):
    name = "produitspider"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = [
        "https://venessens-parquet.com/collection/les-parquets-dinterieur/parquet-semi-massif/"
    ]

    def parse(self, response):
        produits = response.css("ul.products li.product")

        for produit in produits:

            yield {
                "label": produit.css("h2::text").get(),
                "prix_ht": produit.css("span.price bdi::text").get(),
                "prix_ttc": produit.css("span.priceRight bdi::text").get(),
                "url": produit.css('a::attr("href")').get(),
            }

        page_suivante = response.css("a.next::attr(href)").get()

        if page_suivante is not None:
            yield response.follow(page_suivante, callback=self.parse)
