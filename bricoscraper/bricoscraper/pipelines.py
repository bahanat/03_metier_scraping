# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Spider
from scrapy.exceptions import DropItem

from .items import CategorieItem, ProduitItem


class BricoscraperPipeline:
    def __init__(self):
        self.liste_urls_categories_traitees = set()
        self.liste_ids_produits_recuperes = set()

    def process_item(self, item, spider: Spider):
        adapter = ItemAdapter(item)

        # Traitement des catégories
        if isinstance(item, CategorieItem):
            url = adapter.get("url")
            if url:
                if url in self.liste_urls_categories_traitees:
                    raise DropItem("Catégorie déjà récupérée. Catégorie supprimée.")
                else:
                    self.liste_urls_categories_traitees.add(url)
            else:
                spider.logger.error("URL non trouvée ! Catégorie supprimée.")
                raise DropItem("URL non trouvée ! Catégorie supprimée.")

        # Traitement des produits
        elif isinstance(item, ProduitItem):
            key = adapter.get("id")
            if key:
                if key in self.liste_ids_produits_recuperes:
                    raise DropItem(f"Produit déjà récupéré: {key}. Produit supprimé.")
                else:
                    self.liste_ids_produits_recuperes.add(key)
            else:
                spider.logger.error("ID non trouvé ! Produit supprimé.")
                raise DropItem("ID non trouvé ! Produit supprimé.")
            pass

        return item
