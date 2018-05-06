
from .lists import *
from textacy.preprocess import preprocess_text

from common import map_products, replace_strings


class Preprocessor:
    def __call__(self, text):
        return self.custom_preprocess(text)

    def replace_bank_names(self, text):
        text = map_products(text, products_map)
        text = replace_strings(text, first_banks, first_bank_name)
        text = replace_strings(text, second_banks, second_bank_name)
        text = replace_strings(text, companies, company_name)
        text = replace_strings(text, countries, country)
        text = replace_strings(text, nationalities, nationality)
        text = replace_strings(text, towns, town)
        return text

    def replace_characters_to_space(self, text):
        for index, ctos in enumerate(characters_to_space):
            text = text.replace(ctos , characters_spaced[index])
        return text


    def custom_preprocess(self, text):
        text = self.replace_bank_names(text)
        text = preprocess_text(text, fix_unicode = True, lowercase = False, no_urls = True, no_emails = True, no_phone_numbers = True, no_punct = False, no_numbers=False)
        text = self.replace_characters_to_space(text)
        return text
