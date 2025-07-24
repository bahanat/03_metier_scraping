# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BricoscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CategorieItem(scrapy.Item):
    id: str = scrapy.Field()
    id_parent: str | None = scrapy.Field()
    libelle: str = scrapy.Field()
    contient_produits: bool = scrapy.Field()
    url: str = scrapy.Field()


class ProduitItem(scrapy.Item):
    id: str = scrapy.Field()
    ref_interne: str = scrapy.Field()
    label: str = scrapy.Field()
    id_categorie: str = scrapy.Field()
    url: str = scrapy.Field()
    url_image: str | None = scrapy.Field()
    devise: str = scrapy.Field()
    prix_ht: float = scrapy.Field()
    prix_ttc: float = scrapy.Field()
    type_prix: str = scrapy.Field()
    description: str | None = scrapy.Field()
    disponibilite: str | None = scrapy.Field()
    origine: str | None = scrapy.Field()
    normes: str | None = scrapy.Field()
    compatibilite_cas: bool | None = scrapy.Field()
    teinte: str | None = scrapy.Field()
    essence: str | None = scrapy.Field()
    caractere: str | None = scrapy.Field()
    finition: str | None = scrapy.Field()
    epaisseur_mm: float | None = scrapy.Field()
    largeur_mm: float | None = scrapy.Field()
    couche_usure_mm: float | None = scrapy.Field()
    type_lame: str | None = scrapy.Field()
    chanfrein: str | None = scrapy.Field()
