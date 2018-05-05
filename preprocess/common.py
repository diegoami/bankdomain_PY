def replace_strings(text, banks, bank_name):
    for bank in banks:
        if bank in text:
            text = text.replace(bank, bank_name)
    return text


def map_products(text, map_product):
    for key, value in map_product.items():
        if key in text:
            text = text.replace(key, value)
    return text

