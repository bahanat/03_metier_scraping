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

    id = scrapy.Field()
    ref_interne = scrapy.Field()
    label = scrapy.Field()
    id_categorie = scrapy.Field()
    url = scrapy.Field()
    url_image = scrapy.Field()
    devise = scrapy.Field()
    prix_ht = scrapy.Field()
    prix_ttc = scrapy.Field()
    type_prix = scrapy.Field()
    description = scrapy.Field()
    disponibilite = scrapy.Field()
    origine = scrapy.Field()
    normes = scrapy.Field()
    compatibilite_cas = scrapy.Field()
    teinte = scrapy.Field()
    essence = scrapy.Field()
    caractere = scrapy.Field()
    finition = scrapy.Field()
    epaisseur_mm = scrapy.Field()
    largeur_mm = scrapy.Field()
    couche_usure_mm = scrapy.Field()
    type_lame = scrapy.Field()
    chanfrein = scrapy.Field()
