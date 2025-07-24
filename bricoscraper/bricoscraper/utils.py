import re


def extraire_devise(str: str):
    """
    Extrait le symbole de la devise (€,$,£) contenu dans une chaîne de caractères.

    Args:
        str (str): La chaîne de caractères à analyser.

    Returns:
        str | None: Le symbole de la devise trouvé, ou None s'il n'y en a pas.
    """
    if not str:
        return None
    devise = re.search(r"([€$£])", str)
    return devise.group(1) if devise else None


def extraire_float(str: str):
    """
    Extrait une valeur numérique à virgule flottante depuis une chaîne de caractères.

    Recherche une suite de chiffres, éventuellement avec une virgule ou un point comme séparateur
    décimal, et convertit en float.

    Args:
        str (str): La chaîne de caractères contenant un nombre.

    Returns:
        float | None: La valeur flottante extraite, ou None si aucun nombre trouvé.
    """
    if not str:
        return None
    result = re.search(r"[\d.,]+", str)
    return float(result.group().replace(",", ".")) if result else None


def extraire_int(str: str):
    """
    Extrait un entier depuis une chaîne de caractères.

    Recherche une suite de chiffres éventuellement avec une virgule ou un point (extrait la partie avant conversion),
    puis convertit en int.

    Args:
        str (str): La chaîne de caractères contenant un nombre entier.

    Returns:
        int | None: L'entier extrait, ou None si aucun nombre trouvé.
    """
    if not str:
        return None
    result = re.search(r"[\d.,]+", str)
    return int(float(result.group().replace(",", "."))) if result else None


def extraire_type_prix(str: str):
    """
    Extrait la partie après le dernier "/" dans une chaîne de caractères donnée.

    Si la chaîne est vide, None ou ne contient pas de "/", la fonction
    retourne la valeur par défaut "u" pour "unitaire".

    Args:
        str (str): Chaîne de caractères représentant un prix potentiellement
                   suivi d'un type séparé par un "/".

    Returns:
        str or None: La partie de la chaîne après le dernier "/", ou "u"
                     si cette partie est absente, ou None si la chaîne est None ou vide.
    """
    if not str:
        return None
    parts = str.split("/")
    if len(parts) > 1 and parts[-1].strip():
        return parts[-1].strip()
    else:
        return "u"


def supprimer_substring(str_complete: str, a_supprimer: str):
    """
    Supprime toutes les occurrences d'une sous-chaîne dans une chaîne complète.

    Args:
        str_complete (str): La chaîne de caractères originale.
        a_supprimer (str): La sous-chaîne à supprimer.

    Returns:
        str: La chaîne résultante après suppression.
             Si l'une des chaînes est vide ou None, retourne la chaîne originale.
    """
    if not str_complete or not a_supprimer:
        return str_complete
    return str_complete.replace(a_supprimer, "")


def convert_str_en_bool(str: str):
    """
    Convertit une chaîne de caractères française en booléen.

    "oui" (insensible à la casse et aux espaces) devient True,
    "non" devient False,
    toute autre valeur ou None retourne None.

    Args:
        str (str): La chaîne à convertir.

    Returns:
        bool | None: Le booléen correspondant ou None si indéterminé.
    """
    if str is None:
        return None
    str = str.strip().lower()
    if str == "oui":
        return True
    if str == "non":
        return False
    return None


def nombre_compris_entre(
    nbr: int | float, valeur_min: int | float = None, valeur_max: int | float = None
):
    """
    Vérifie si un nombre est compris entre une valeur minimale et une valeur maximale.

    Args:
        nbr (int | float): Le nombre à vérifier.
        valeur_min (int | float, optionnel): La valeur minimale incluse. Par défaut None (pas de min).
        valeur_max (int | float, optionnel): La valeur maximale incluse. Par défaut None (pas de max).

    Returns:
        float: Le nombre converti en float si dans l'intervalle.
        -1: Si le nombre est hors bornes ou invalide (conversion impossible).
    """
    try:
        nbr = float(nbr)
    except (ValueError, TypeError):
        return None
    if valeur_min is not None and nbr < valeur_min:
        return -1
    if valeur_max is not None and nbr > valeur_max:
        return -1
    return nbr
