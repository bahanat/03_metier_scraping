import re


def extraire_devise(chaine: str) -> str | None:
    """
    Extrait le symbole de la devise (€,$,£) dans une chaîne.

    Args:
        chaine (str): La chaîne à analyser.

    Returns:
        str ou None: Le symbole de la devise, ou None si absent.
    """
    if not chaine:
        return None
    devise = re.search(r"([€$£])", chaine)
    return devise.group(1) if devise else None


def extraire_float(chaine: str) -> float | None:
    """
    Extrait un nombre décimal depuis une chaîne.

    Args:
        chaine (str): Chaîne contenant un nombre.

    Returns:
        float ou None: La valeur extraite, ou None si absence.
    """
    if not chaine:
        return None
    result = re.search(r"[\d.,]+", chaine)
    return float(result.group().replace(",", ".")) if result else None


def extraire_int(chaine: str) -> int | None:
    """
    Extrait un entier depuis une chaîne.

    Args:
        chaine (str): Chaîne contenant un nombre entier.

    Returns:
        int ou None: L'entier extrait, ou None si absence.
    """
    if not chaine:
        return None
    result = re.search(r"[\d.,]+", chaine)
    return int(float(result.group().replace(",", "."))) if result else None


def extraire_type_prix(chaine: str) -> str | None:
    """
    Extrait la partie après le dernier "/" ou retourne "u".

    Args:
        chaine (str): Chaîne avec un prix suivi optionnellement d'un type.

    Returns:
        str ou None: Partie après "/", "u" si absente, ou None si chaîne vide.
    """
    if not chaine:
        return None
    parts = chaine.split("/")
    if len(parts) > 1 and parts[-1].strip():
        return parts[-1].strip()
    return "u"


def supprimer_substring(str_complete: str, a_supprimer: str) -> str:
    """
    Supprime toutes les occurrences de a_supprimer dans str_complete.

    Args:
        str_complete (str): Chaîne originale.
        a_supprimer (str): Sous-chaîne à supprimer.

    Returns:
        str: Chaîne résultat (identique si args vides).
    """
    if not str_complete or not a_supprimer:
        return str_complete
    return str_complete.replace(a_supprimer, "")


def convert_str_en_bool(chaine: str) -> bool | None:
    """
    Convertit "oui" en True, "non" en False, sinon None.

    Args:
        chaine (str): Chaîne à convertir.

    Returns:
        bool ou None: Booléen correspondant, ou None sinon.
    """
    if chaine is None:
        return None
    chaine = chaine.strip().lower()
    if chaine == "oui":
        return True
    if chaine == "non":
        return False
    return None


def nombre_compris_entre(
    nbr: int | float,
    valeur_min: float = None,
    valeur_max: float = None,
) -> bool:
    """
    Vérifie que nbr est entre valeur_min et valeur_max.

    Args:
        nbr (int | float): Le nombre à vérifier.
        valeur_min (float, optionnel): Min (inclu), par défaut None (pas de min).
        valeur_max (float, optionnel): Max (inclu), par défaut None (pas de max).

    Returns:
        bool: True si nbr est compris entre valeur_min et valeur_max,
              False sinon (hors bornes ou conversion impossible).
    """
    try:
        nbr_float = float(nbr)
    except (ValueError, TypeError):
        return False
    if valeur_min is not None and nbr_float < valeur_min:
        return False
    if valeur_max is not None and nbr_float > valeur_max:
        return False
    return True


def str_finit_par(chaine: str, fin: str) -> bool:
    """
    Vérifie si la chaîne donnée, après suppression des espaces de début et de fin, finit par la chaîne `fin`.

    Args:
        chaine (str): La chaîne à tester.
        fin (str): La sous-chaîne finale attendue.

    Returns:
        bool: True si `chaine.strip()` se termine par `fin`, False sinon.
    """
    if chaine is None or fin is None:
        return False
    return chaine.strip().endswith(fin)
