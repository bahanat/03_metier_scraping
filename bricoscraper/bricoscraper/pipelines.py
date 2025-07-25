# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Spider
from scrapy.exceptions import DropItem
from .items import CategorieItem


class BricoscraperPipeline:
    def __init__(self):
        self.liste_urls_categories_traitees = []

    def process_item(self, item, spider: Spider):

        # Traitement des catégories
        if isinstance(item, CategorieItem):
            url = item.get("url")
            if url:
                if url in self.liste_urls_categories_traitees:
                    raise DropItem("Catégorie déjà récupérée. Catégorie supprimée.")
                else:
                    self.liste_urls_categories_traitees.append(url)
            else:
                spider.logger.error("URL non trouvée ! Catégorie supprimée.")
                raise DropItem("URL non trouvée ! Catégorie supprimée.")

        # Traitement des produits
        elif False:  # remplacer False par ProduitItem et continuer…
            pass

        return item

class BricoscraperCleaningPipeline:

    def process_item(self, item, spider: Spider):

        adapter = ItemAdapter(item)

        ## switch some fields to lowercase
        champs_minuscules = ["id", "id_parent", "ref_interne", "id_categorie", "type_prix"]
        for champ_minuscule in champs_minuscules:
            valeur = adapter.get(champ_minuscule)
            if isinstance(valeur, str):
                adapter[champ_minuscule] = valeur.lower()

        ## pas de chaine vide pour le type de prix, u par défaut
        valeur = adapter.get("type_prix")
        if isinstance(valeur, str) and not valeur:
            adapter["type_prix"] = "u"

        return item