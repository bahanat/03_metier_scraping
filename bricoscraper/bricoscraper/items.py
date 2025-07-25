# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BricoscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def serialize_string(string: str | None) -> str | None:
    if string:
        return string.strip()


class CategorieItem(scrapy.Item):
    id: str = scrapy.Field(serializer=serialize_string)
    id_parent: str | None = scrapy.Field(serializer=serialize_string)
    libelle: str = scrapy.Field(serializer=serialize_string)
    contient_produits: bool = scrapy.Field()
    url: str = scrapy.Field()


class ProduitItem(scrapy.Item):
    id: str = scrapy.Field(serializer=serialize_string)
    ref_interne: str = scrapy.Field(serializer=serialize_string)
    label: str = scrapy.Field(serializer=serialize_string)
    id_categorie: str = scrapy.Field(serializer=serialize_string)
    url: str = scrapy.Field()
    url_image: str | None = scrapy.Field()
    devise: str = scrapy.Field(serializer=serialize_string)
    prix_ht: float = scrapy.Field()
    prix_ttc: float = scrapy.Field()
    type_prix: str = scrapy.Field(serializer=serialize_string)
    description: str | None = scrapy.Field(serializer=serialize_string)
    disponibilite: str | None = scrapy.Field(serializer=serialize_string)
    origine: str | None = scrapy.Field(serializer=serialize_string)
    normes: str | None = scrapy.Field(serializer=serialize_string)
    compatibilite_cas: bool | None = scrapy.Field(serializer=serialize_string)
    teinte: str | None = scrapy.Field(serializer=serialize_string)
    essence: str | None = scrapy.Field(serializer=serialize_string)
    caractere: str | None = scrapy.Field(serializer=serialize_string)
    finition: str | None = scrapy.Field(serializer=serialize_string)
    epaisseur_mm: float | None = scrapy.Field()
    largeur_mm: float | None = scrapy.Field()
    couche_usure_mm: float | None = scrapy.Field()
    type_lame: str | None = scrapy.Field(serializer=serialize_string)
    chanfrein: str | None = scrapy.Field(serializer=serialize_string)
