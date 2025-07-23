import scrapy

from ..utils import (
    extract_devise,
    extract_float,
    extract_int,
    remove_substring,
    convert_str_to_bool,
    number_in_range,
)


class ProduitSpider(scrapy.Spider):
    name = "produitspider"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = [
        "https://venessens-parquet.com/collection/les-parquets-dinterieur/parquet-massif/"
    ]

    def parse(self, response):
        produits = response.css("ul.products li.product")

        for produit in produits:
            produit_url = produit.css('a::attr("href")').get()
            yield response.follow(produit_url, callback=self.parse_produit)

        page_suivante = response.css("a.next::attr(href)").get()

        if page_suivante is not None:
            yield response.follow(page_suivante, callback=self.parse)

    def parse_produit(self, response):
        url = response.url

        # Extraction des données de la table des détails en un dictionnaire
        details = {
            th.get(): td.get()
            for th, td in zip(
                response.xpath('//div[@class="accordionContent"]//th/text()'),
                response.xpath('//div[@class="accordionContent"]//td/text()'),
            )
        }

        yield {
            "url": url,
            "label": details.get("nom du produit"),
            "id": url.rstrip("/").split("/")[-1],
            "ref_interne": extract_int(response.css("span.reference::text").get()),
            "categorie": response.xpath(
                '//nav[@class="woocommerce-breadcrumb"]/a[3]/text()'
            ).get(),
            "url_image": response.css(
                'div.woocommerce-product-gallery__image a::attr("href")'
            ).get(),
            "prix_ht": extract_float(response.css("span.prix::text").get()),
            "prix_ttc": extract_float(response.css("span.tva::text").get()),
            "devise": extract_devise(response.css("span.prix::text").get()),
            "type_prix": response.css("span.prix::text").get().split("/")[-1],
            "description": response.css(
                "div.elementor-widget-woocommerce-product-content p::text"
            ).get(),
            "disponibilite": remove_substring(
                response.css("span.disponibilite::text").get(), "Disponibilité "
            ),
            "origine": details.get("fabrication"),
            "normes": details.get("normes"),
            "compatibilite_cas": convert_str_to_bool(
                details.get("compatible sol chauffant")
            ),
            "teinte": details.get("teinte"),
            "essence": details.get("essence de bois"),
            "caractere": details.get("caractere"),
            "finition": details.get("finition"),
            "epaisseur_mm": number_in_range(
                extract_int(details.get("epaisseur")), 0, 100
            ),  # On renvoie None si l'épaisseur n'est pas comprise entre 0 et 100mm
            "largeur_mm": number_in_range(
                extract_int(details.get("largeur")), 30
            ),  # On renvoie None si la largeur n'est pas supérieure à 30mm
            "couche_usure_mm": number_in_range(
                extract_int(details.get("couche dusure")), 0, 30
            ),  # On renvoie None si la couche d'usure est supérieur à 30mm
            "type_lame": details.get("type de lame"),
            "chanfrein": details.get("chanfrein"),
        }
