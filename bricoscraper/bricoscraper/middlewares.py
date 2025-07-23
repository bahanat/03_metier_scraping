# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from dotenv import load_dotenv
from scrapy import signals
from urllib.parse import urlencode
import requests
from random import randint

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

load_dotenv()


class BricoscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BricoscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapeOpsFauxEnTeteNavigateurMiddleware:

    def __init__(self, settings):
        """Construit l'instance à partir d'un dictionnaire de configuration

        Args:
            settings (dict): Les paramètres de configuration
        """
        # Clé API depuis le fichier .env
        self.scrapeops_cle_api = os.getenv("SCRAPEOPS_API_KEY")
        # Autres informations depuis settings.py
        self.scrapeops_cible = settings.get("SCRAPEOPS_FAUX_ENTETE_NAVIGATEUR_CIBLE")
        self.scrapeops_active = settings.get(
            "SCRAPEOPS_FAUX_ENTETE_NAVIGATEUR_ACTIVE", False
        )
        self.scrapeops_nb_resultats = settings.get("SCRAPEOPS_NB_RESULTATS")
        self.faux_entetes_navigateur = []
        self._get_faux_entetes_navigateur()
        self._scrapeops_faux_entetes_navigateur_active()

    @classmethod
    def from_crawler(cls, crawler):
        """Constructeur alternatif à partir d'un crawler

        Args:
            crawler (?): Le crawler
        """
        return cls(crawler.settings)

    def _get_faux_entetes_navigateur(self):
        """Fais la requete à scrapeops.io d'une liste de faux
        en-tetes de navigateur. Le résultat est intégré à **self**.
        """

        # Récupération des parametres
        parametres = {"api_key": self.scrapeops_cle_api}
        if self.scrapeops_nb_resultats is not None:
            parametres["num_results"] = self.scrapeops_nb_resultats

        # Envoi de la requete à scrapeops.io
        reponse = requests.get(self.scrapeops_cible, params=urlencode(parametres))
        json_reponse = reponse.json()
        self.faux_entetes_navigateur = json_reponse.get("result", [])

    def _get_faux_entete_navigateur_aleatoire(self) -> dict:
        """Retourne un faux en-tete de navigateur aléatoire parmi
        la liste de faux en-tetes contenue dans **self**.

        Returns:
            dict: Le faux en-tete de navigateur aléatoire
        """
        random_index = randint(0, len(self.faux_entetes_navigateur) - 1)
        return self.faux_entetes_navigateur[random_index]

    def _scrapeops_faux_entetes_navigateur_active(self):
        """Vérifie les parametres ScrapeOps et modifie l'activation
        de l'utilisation de faux en-tetes de navigation en fonction de leur cohérence.
        """

        if (
            self.scrapeops_cle_api is None
            or self.scrapeops_cle_api == ""
            or self.scrapeops_active == False
        ):
            self.scrapeops_active = False
        else:
            self.scrapeops_active = True

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        """Lance la requête avec un en-tete de navigateur généré
        aléatoirement par scrapeops.io

        Args:
            request (Request): La requête a exécuter
            spider (Spider): La spider réalisant le scraping
        """
        entete_navigateur_aleatoire = self._get_faux_entete_navigateur_aleatoire()

        # Utilisation de la totalité d'un faux en-tete de navigateur, ou ...
        # request.headers = entete_navigateur_aleatoire
        # ... Utilisation partielle de certains champs d'un faux en-tete de navigateur
        request.headers["sec-fetch-user"] = entete_navigateur_aleatoire.get(
            "sec-fetch-user"
        )
        request.headers["sec-fetch-mod"] = entete_navigateur_aleatoire.get(
            "sec-fetch-mod"
        )
        request.headers["sec-fetch-site"] = entete_navigateur_aleatoire.get(
            "sec-fetch-site"
        )
        request.headers["sec-ch-ua-platform"] = entete_navigateur_aleatoire.get(
            "sec-ch-ua-platform"
        )
        request.headers["sec-ch-ua-mobile"] = entete_navigateur_aleatoire.get(
            "sec-ch-ua-mobile"
        )
        request.headers["sec-ch-ua"] = entete_navigateur_aleatoire.get("sec-ch-ua")
        request.headers["accept"] = entete_navigateur_aleatoire.get("accept")
        request.headers["accept-language"] = entete_navigateur_aleatoire.get(
            "accept-language"
        )
        request.headers["accept-encoding"] = entete_navigateur_aleatoire.get(
            "accept-encoding"
        )
        request.headers["user-agent"] = entete_navigateur_aleatoire.get("user-agent")
        request.headers["upgrade-insecure-requests"] = entete_navigateur_aleatoire.get(
            "upgrade-insecure-requests"
        )

        print("*******Nouvel en-tête de navigateur intégré à la requête*******")
        print(request.headers)


## TEST ## TEST ## TEST ## TEST ## TEST ## TEST ## TEST ## TEST ## TEST ## TEST ##


def test():
    settings = {
        "SCRAPEOPS_FAUX_ENTETE_NAVIGATEUR_CIBLE": "https://headers.scrapeops.io/v1/browser-headers",
        "SCRAPEOPS_FAUX_ENTETE_NAVIGATEUR_ACTIVE": True,
        "SCRAPEOPS_NB_RESULTATS": 10,
    }

    # Test du constructeur (avec liste de faux en-tetes de navigateur)
    test1 = ScrapeOpsFauxEnTeteNavigateurMiddleware(settings)
    print(test1.scrapeops_cle_api)
    print(test1.scrapeops_cible)
    print(test1.scrapeops_active)
    print(test1.scrapeops_nb_resultats)
    for entete in test1.faux_entetes_navigateur:
        print(entete)

    # Test de la sélection aléatoire d'un faux en-tete de navigateur
    print("\n************\n")
    print(test1._get_faux_entete_navigateur_aleatoire())
    print(test1._get_faux_entete_navigateur_aleatoire())
    print(test1._get_faux_entete_navigateur_aleatoire())
    print(test1._get_faux_entete_navigateur_aleatoire())
    print(test1._get_faux_entete_navigateur_aleatoire())

    # Test de la sélection aléatoire d'un faux en-tete de navigateur
    print("\n************\n")
    print(test1._scrapeops_faux_entetes_navigateur_active())
    print(test1.scrapeops_active)


if __name__ == "__main__":
    test()
