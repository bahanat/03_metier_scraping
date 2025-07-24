import scrapy

from ..utils import (
    extraire_devise,
    extraire_float,
    extraire_int,
    supprimer_substring,
    convert_str_en_bool,
    nombre_compris_entre,
)


class ProduitsSpider(scrapy.Spider):
    name = "produits"
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
        url_produit = response.url
        url_categories = response.xpath(
            '//nav[@class="woocommerce-breadcrumb"]/a/@href'
        ).getall()

        # Extraction des données de la table des détails en un dictionnaire
        details = {
            th.get(): td.get()
            for th, td in zip(
                response.xpath('//div[@class="accordionContent"]//th/text()'),
                response.xpath('//div[@class="accordionContent"]//td/text()'),
            )
        }

        yield {
            "url": url_produit,
            "label": details.get("nom du produit"),
            "id": url_produit.rstrip("/").split("/")[-1],
            "ref_interne": supprimer_substring(
                response.css("span.reference::text").get(), "Ref: "
            ),
            "id_categorie": url_categories[-1].rstrip("/").split("/")[-1],
            "url_image": response.css(
                'div.woocommerce-product-gallery__image a::attr("href")'
            ).get(),
            "prix_ht": extraire_float(response.css("span.prix::text").get()),
            "prix_ttc": extraire_float(response.css("span.tva::text").get()),
            "devise": extraire_devise(response.css("span.prix::text").get()),
            "type_prix": response.css("span.prix::text").get().split("/")[-1],
            "description": response.css(
                "div.elementor-widget-woocommerce-product-content p::text"
            ).get(),
            "disponibilite": supprimer_substring(
                response.css("span.disponibilite::text").get(), "Disponibilité "
            ),
            "origine": details.get("fabrication"),
            "normes": details.get("normes"),
            "compatibilite_cas": convert_str_en_bool(
                details.get("compatible sol chauffant")
            ),
            "teinte": details.get("teinte"),
            "essence": details.get("essence de bois"),
            "caractere": details.get("caractere"),
            "finition": details.get("finition"),
            "epaisseur_mm": nombre_compris_entre(
                extraire_int(details.get("epaisseur")), 0, 100
            ),  # On renvoie -1 si l'épaisseur n'est pas comprise entre 0 et 100mm
            "largeur_mm": nombre_compris_entre(
                extraire_int(details.get("largeur")), 30
            ),  # On renvoie -1 si la largeur n'est pas supérieure à 30mm
            "couche_usure_mm": nombre_compris_entre(
                extraire_int(details.get("couche dusure")), 0, 30
            ),  # On renvoie -1 si la couche d'usure est supérieur à 30mm
            "type_lame": details.get("type de lame"),
            "chanfrein": details.get("chanfrein"),
        }
