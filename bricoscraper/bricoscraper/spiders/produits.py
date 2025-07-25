import csv
import scrapy
from pathlib import Path

from ..items import ProduitItem
from ..utils import (
    extraire_devise,
    extraire_float,
    extraire_int,
    extraire_type_prix,
    supprimer_substring,
    convert_str_en_bool,
    nombre_compris_entre,
)


class ProduitsSpider(scrapy.Spider):
    """
    Spider Scrapy pour extraire tous les produits présents dans les catégories extraites préalablement.

    Attributs :
        name (str): Nom unique du spider.
        allowed_domains (list): Liste des domaines autorisés à crawler.
        custom_settings (dict): Configuration spécifique au spider (fichier de sortie, format).
    """

    name = "produits"
    allowed_domains = ["venessens-parquet.com"]
    custom_settings = {
        "FEEDS": {f"data/{name}.csv": {"format": "csv", "overwrite": True}}
    }

    def start_requests(self):
        """
        Génère les requêtes initiales à partir des URLs de catégorie extraites dans 'data/categories.csv'.

        Yields:
            scrapy.Request: Une requête Scrapy pour chaque URL de catégorie contenant des produits.
        """
        if Path("data/categories.csv").exists():
            try:
                with open("data/categories.csv", mode="r") as fichier_categories:
                    reader_categories = csv.DictReader(fichier_categories)
                    for categorie in reader_categories:
                        if categorie["contient_produits"] == str(True):
                            yield scrapy.Request(categorie["url"], callback=self.parse)
            except:
                raise Exception("Erreur de lecture du fichier data/categories.csv")
        else:
            raise Exception("Fichier data/categories.csv non trouvé.")

    def parse(self, response):
        """
        Parse la page liste-produit d'une catégorie et génère une requête vers chaque page produit.
        Suit également les liens vers les pages suivantes si la pagination est présente.

        Args:
            response (scrapy.http.Response): Réponse de la page de catégorie.

        Yields:
            scrapy.Request: Une requête vers chaque page produit ou vers la page suivante.
        """
        produits = response.css("ul.products li.product")

        for produit in produits:
            produit_url = produit.css('a::attr("href")').get()
            yield response.follow(produit_url, callback=self.parse_produit)

        page_suivante = response.css("a.next::attr(href)").get()

        if page_suivante is not None:
            yield response.follow(page_suivante, callback=self.parse)

    def parse_produit(self, response):
        """
        Récupère et structure toutes les informations d'un produit à partir de sa page détaillée.

        Args:
            response (scrapy.http.Response): Réponse de la page détail-produit.

        Yields:
            ProduitItem: Item Scrapy contenant toutes les informations structurées du produit.
        """
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

        item = ProduitItem()

        item["url"] = url_produit
        item["label"] = details.get("nom du produit")
        item["id"] = url_produit.rstrip("/").split("/")[-1]
        item["ref_interne"] = supprimer_substring(
            response.css("span.reference::text").get(), "Ref: "
        )
        item["id_categorie"] = url_categories[-1].rstrip("/").split("/")[-1]
        item["url_image"] = response.css(
            'div.woocommerce-product-gallery__image a::attr("href")'
        ).get()
        item["prix_ht"] = extraire_float(response.css("span.prix::text").get())
        item["prix_ttc"] = extraire_float(response.css("span.tva::text").get())
        item["devise"] = extraire_devise(response.css("span.prix::text").get())
        item["type_prix"] = extraire_type_prix(response.css("span.prix::text").get())
        item["description"] = response.css(
            "div.elementor-widget-woocommerce-product-content p::text"
        ).get()
        item["disponibilite"] = supprimer_substring(
            response.css("span.disponibilite::text").get(), "Disponibilité "
        )
        item["origine"] = details.get("fabrication")
        item["normes"] = details.get("normes")
        item["compatibilite_cas"] = convert_str_en_bool(
            details.get("compatible sol chauffant")
        )
        item["teinte"] = details.get("teinte")
        item["essence"] = details.get("essence de bois")
        item["caractere"] = details.get("caractere")
        item["finition"] = details.get("finition")
        item["epaisseur_mm"] = nombre_compris_entre(
            extraire_int(details.get("epaisseur")), 0, 100
        )  # On renvoie -1 si l'épaisseur n'est pas comprise entre 0 et 100mm
        item["largeur_mm"] = nombre_compris_entre(
            extraire_int(details.get("largeur")), 30, 240
        )  # On renvoie -1 si la largeur n'est pas comprise entre 30 et 240mm
        item["couche_usure_mm"] = nombre_compris_entre(
            extraire_int(details.get("couche dusure")), 0, 30
        )  # On renvoie -1 si la couche d'usure est supérieur à 30mm
        item["type_lame"] = details.get("type de lame")
        item["chanfrein"] = details.get("chanfrein")

        yield item
