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

        # Traitement des produits
        if isinstance(item, ProduitItem):
            id_produit = item["id"]
            if isinstance(id_produit, str):
                id_produit = id_produit.strip().lower()
                if id_produit.startswith("nom-du-produit"):
                    raise DropItem(f"Produit aberrant nettoyé: id={id_produit}")

            else:
                raise DropItem(f"Produit nettoyé: non-string id={id_produit}")

        return item


class BricoScraperTransformPipeline:

    def process_item(self, item, spider: Spider):

        adapter = ItemAdapter(item)
        self.mise_en_minuscule(adapter)
        self.type_de_prix_non_vide(adapter)

        return item

    def mise_en_minuscule(self, adapter: ItemAdapter):
        """Mise en minuscules de certains champs de données:
        - id
        - id_parent
        - id_categorie
        - ref_interne
        - type_prix

        Args:
            adapter (ItemAdapter): L'item passant à travers le pipeline
        """

        champs_minuscules = [
            "id",
            "id_parent",
            "id_categorie",
            "ref_interne",
            "type_prix",
        ]
        for champ_minuscule in champs_minuscules:
            valeur = adapter.get(champ_minuscule)
            if isinstance(valeur, str):
                adapter[champ_minuscule] = valeur.lower()

    def type_de_prix_non_vide(self, adapter: ItemAdapter):
        """Assure que le champ type_prix ne soit pas vide.
        Par défaut ce champ doit contenir 'u' pour prix à l'unité

        Args:
            adapter (ItemAdapter): L'item passant à travers le pipeline
        """

        valeur = adapter.get("type_prix")
        if isinstance(valeur, str) and not valeur:
            adapter["type_prix"] = "u"
