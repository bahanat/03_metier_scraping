# Projet de scraping et de structuration de données

## AVERTISSEMENT

Ce projet a été réalisé dans un objectif strictement **pédagogique** d'apprentissage du scraping avec la bibliothèque Scrapy en Python.

**AUCUN CONTENU ISSU DU SITE UTILISÉ À DES FIN DE TEST DANS CE PROJET N'EST ENREGISTRÉ DANS CE DÉPOT.**

Les scripts ont été écrits pour démontrer des compétences techniques (requests, parsing, orchestration, stockage, etc.).

Toute personne qui utiliserait ces scripts est seule responsable du respect :
- des Conditions Générales d’Utilisation (CGU) et mentions légales des sites ciblés ;
- des fichiers robots.txt ;
- du RGPD et, plus largement, des lois applicables en matière de protection des données personnelles ;
- du droit sui generis des bases de données (Code de la propriété intellectuelle, art. L341-1 s.) et de toute autre règle relative à l’extraction/réutilisation de données.

Sur simple demande d’un ayant droit, tout contenu problématique sera retiré ou modifié.

## Objectifs

- Concevoir et développer un système de scraping capable de collecter les données tarifaires sur une large gamme de produits sur un site de vente en ligne d'articles du domaine du bricolage.
- Assurer la conformité légale et éthique du processus de collecte, en respectant les conditions d'utilisation du site web ciblé et en mettant en place des mesures pour éviter toute surcharge du serveur.
- Nettoyer et structurer les données collectées pour garantir leur qualité et leur fiabilité.

## Structure du projet

```
 bricoscraper
 ├── .gitignore
 ├── bricoscraper
 │  ├── bricoscraper
 │  │  ├── __init__.py
 │  │  ├── items.py
 │  │  ├── middlewares.py
 │  │  ├── pipelines.py
 │  │  ├── settings.py
 │  │  ├── spiders
 │  │  │  ├── __init__.py
 │  │  │  ├── categories.py
 │  │  │  └── produits.py
 │  │  └── utils.py
 │  └── scrapy.cfg
 ├── LICENSE
 └── README.md
```

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/bahanat/03_metier_scraping.git
   cd 03_metier_scraping
   ```

2. Créez et activez un environnement virtuel (script fourni pour le gestionnaire *venv*) :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Exécution

Il faut d'abord récupérer les catégories au moins une fois avant de récupérer les produits.

### Commandes pour démarrer le scraping :

```bash
cd bricoscraper # on se place dans le sous-dossier bricoscraper
scrapy crawl categories # récupération des catégories
scrapy crawl produits # récupération des produits
```

Chaque commande *scrapy crawl* génère un fichier CSV placé dans le répertoire **data**.

### Fichiers générés :
- categories.csv
- produits.csv

# Auteurs

- [Anatole Bahurel](https://github.com/bahanat)
- [César Gattano](https://cesargattano.github.io/)
- [Alexis Halbot-Schoonaert](https://github.com/alexishs)
- [Harley Rueda](https://github.com/harleyrueda)

## Licence

Ce projet est sous licence MIT.
