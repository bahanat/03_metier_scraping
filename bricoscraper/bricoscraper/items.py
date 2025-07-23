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
    id_parent: str|None = scrapy.Field()
    libelle: str = scrapy.Field()
    contient_produits: bool = scrapy.Field()