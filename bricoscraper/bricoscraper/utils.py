import re


def extract_devise(price_str):
    if not price_str:
        return None
    match = re.search(r"([€$£])", price_str)
    return match.group(1) if match else None


def extract_float(str):
    if not str:
        return None
    match = re.search(r"[\d.,]+", str)
    return float(match.group().replace(",", ".")) if match else None


def extract_int(str):
    if not str:
        return None
    match = re.search(r"[\d.,]+", str)
    return int(match.group().replace(",", ".")) if match else None


def remove_substring(full_string, to_remove):
    if not full_string or not to_remove:
        return full_string
    return full_string.replace(to_remove, "")


def convert_str_to_bool(str):
    if str is None:
        return None
    str = str.strip().lower()
    if str == "oui":
        return True
    if str == "non":
        return False
    return None


def number_in_range(value, min_value=None, max_value=None):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return None
    if min_value is not None and value < min_value:
        return None
    if max_value is not None and value > max_value:
        return None
    return value
