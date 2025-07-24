import scrapy
import scrapy.http
from ..items import CategorieItem


class CategoriesSpider(scrapy.Spider):
    name = "categories"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com"]

    custom_settings = {
        "FEEDS": {f"data/{name}.csv": {"format": "csv", "overwrite": True}}
    }

    def parse(self, response: scrapy.http.Response):

        # On récupère les liens du menu susceptibles de pointer vers une catégorie.
        liens_menu = response.css(
            "div[data-elementor-type=header] > section:nth-child(2) .elementor-shortcode > nav > ul > li > a::attr(href), div[data-elementor-type=header] > section:nth-child(2) .elementor-shortcode nav > ul > li > ul > li > ul > li > ul > li nav:nth-child(1) a::attr(href)"
        ).getall()
        liens_categories_dans_menu = [
            lien
            for lien in liens_menu
            if lien.startswith("https://venessens-parquet.com/collection/")
        ]
        for lien_categorie in liens_categories_dans_menu:
            yield scrapy.Request(lien_categorie, callback=self.parse_page_categorie)
        return

    def parse_page_categorie(self, response: scrapy.http.Response):
        lien_premier_article = response.css(
            "ul.products li.product a.woocommerce-LoopProduct-link::attr(href)"
        ).get()
        if lien_premier_article:
            yield scrapy.Request(
                lien_premier_article, callback=self.parse_premier_article
            )
        else:
            self.logger.error(
                "Lien du premier article non trouvé. Catégorie non prise en compte."
            )

    def parse_premier_article(self, response: scrapy.http.Response):
        liste_liens_categories = response.css(
            ".woocommerce-breadcrumb > a:not(:first-child)::attr(href)"
        ).getall()

        if not liste_liens_categories:
            self.logger.error(
                "Liens de catégories non trouvés sur premier article ! Catégorie non prise en compte."
            )
            return

        if not (
            liste_liens_categories[-1]
            == response.request.headers.get("Referer").decode("utf-8")
        ):
            # les catégories ne concordent pas.
            # La catégorie est une catégorie secondaire.
            # On l'ignore.
            return

        id_categories = []
        libelles_categories = response.css(
            ".woocommerce-breadcrumb > a:not(:first-child)::text"
        ).getall()

        for lien_categorie in liste_liens_categories:
            # on récupère l'avant dernier élément du split (le dernier élément est une chaine vide car l'url finit par /)
            id_categories.append(lien_categorie.split("/")[-2])

        # on enregistre la hiérarchie des catégories trouvées…
        for index_categorie in range(len(id_categories)):
            item_categorie = CategorieItem()
            item_categorie["id"] = id_categories[index_categorie]
            item_categorie["libelle"] = libelles_categories[index_categorie]
            if index_categorie == 0:
                item_categorie["id_parent"] = None
            else:
                item_categorie["id_parent"] = id_categories[index_categorie - 1]
            if index_categorie == (len(id_categories) - 1):
                item_categorie["contient_produits"] = True
            else:
                item_categorie["contient_produits"] = False
            item_categorie["url"] = liste_liens_categories[index_categorie]
            yield item_categorie
