import scrapy
import scrapy.http
from ..items import CategorieItem


class CategoriesSpider(scrapy.Spider):
    """
    Spider pour extraire la hiérarchie des catégories depuis le site venessens-parquet.com.

    Ce spider parcourt le menu principal du site pour identifier les liens vers les catégories de produits.
    Pour chaque catégorie trouvée, il visite la page de la catégorie, puis le premier article de cette catégorie,
    afin d'extraire la hiérarchie complète des catégories à partir du fil d'Ariane (breadcrumb).
    La catégorie n'est prise en compte que s'il y a concordance entre la catégorie traitée et celle du produit.
    Car en cas de non concordance, la catégorie est une catégorie secondaire qui permet juste de regrouper des produits
    qui possèdent leur propre catégorie. Dans ce cas, la catégorie traitée est à ignorer.

    Attributs de classe :
        name (str): Nom du spider.
        allowed_domains (list): Liste des domaines autorisés.
        start_urls (list): Liste des URLs de départ.
        custom_settings (dict): Paramètres personnalisés pour l'export des données.

    Méthodes :
        parse(response):
            Extrait les liens du menu susceptibles de pointer vers une catégorie et lance la requête sur chaque catégorie trouvée.

        parse_page_categorie(response):
            Extrait le lien du premier article de la catégorie et lance la requête pour extraire la hiérarchie des catégories.

        parse_premier_article(response):
            Extrait la hiérarchie des catégories à partir du fil d'Ariane du premier article et génère les items de catégorie.
    """
    name = "categories"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com"]

    custom_settings = {
        "FEEDS": {f"data/{name}.csv": {"format": "csv", "overwrite": True}}
    }

    def parse(self, response: scrapy.http.Response):
        """
        Analyse la page d'accueil pour extraire les liens du menu pointant vers les catégories.

        Args:
            response (scrapy.http.Response): La réponse HTTP de la page d'accueil.

        Yields:
            scrapy.Request: Requêtes vers les pages de catégories trouvées dans le menu.
        """

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
        """
        Analyse la page de catégorie pour extraire le lien du premier article.

        Args:
            response (scrapy.http.Response): La réponse HTTP de la page de catégorie.

        Yields:
            scrapy.Request: Requête vers la page du premier article de la catégorie.
        """
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
        """
        Analyse la page d'un premier article pour extraire la hiérarchie des catégories.
        Cette méthode récupère les liens et libellés des catégories à partir du fil d'Ariane
        (breadcrumb) de la page. Elle vérifie que la dernière catégorie correspond à la catégorie traitée
        (qui correspond au référent de la requête pour s'assurer que la catégorie est principale.
        Si ce n'est pas le cas, la catégorie est ignorée.
        Pour chaque catégorie trouvée, un objet CategorieItem est généré avec :
            - l'identifiant de la catégorie (extrait de l'URL),
            - le libellé de la catégorie,
            - l'identifiant du parent (None pour la racine),
            - un indicateur si la catégorie contient des produits,
            - l'URL de la catégorie.
        Args:
            response (scrapy.http.Response): La réponse HTTP de la page à analyser.
        Yields:
            CategorieItem: Un objet représentant une catégorie extraite de la hiérarchie.
        """

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
