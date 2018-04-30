from textacy.corpus import Corpus
from textacy.preprocess import preprocess_text


first_banks = ["PostBank", "PSD", "FINAVI", "EthikBank", "TARGOBANK", "Sparkasse", "Triodos", "Sparda-Bank", "targobank", "FerratumBank", "GarantiBank", "Hanseatic Bank", "Keytrade Bank", "Deutsche Bank", "MERKUR BANK", "Skatbank", "VR-Bank", "norisbank", "Skatbank"]
second_banks  = ["solarisBank" "SWK Bank", "DNB", "ING DiBa", "RCI Banque"]
companies = ["comdirect","CIM","Volkswagen", "Opel", "Renault", "Dacia", "Nissan","GRENKE", "Santander", "Fidor", "Credit Europe", "DKB", "HOB", "IKEA" ,"OKB", "Rabo", "Sparda", "Ferratum", "NIBC", "Shaufelonline", "EdB", "GLS", "HVB","PayPal" ,"East West Direkt"]
first_products = ["Kash Reserv", "ROBIN", "VR-FinanzPlan", "NIBCard", "SpardaSecure", "Sparkassen-Card"]
second_products = ["Kash Borgen", "maxblue", "SecureGo", "SpardaNet", "Kleeblatt", "S-Card"]
third_products = ["Kash Borgen", "TWINT", "easyKonto", "E-Rechnung", "EB-Banking"]
countries = ["Deutschland", "Schweiz", "Österreich", "Luxembourg", "Malta", "Belgien"]
towns = ["Berlin", "München", "Frankfurt", "Hamburg", "Hannover", "Karslruhe", "Stuttgart", "Köln", "Düsseldorf", "Duisburg", "Mannheim", "Dresden", "Ingolstadt"]
first_bank_name = "DidiBank"
second_bank_name = "AmbiBank"
first_product_name = "Dodo"
second_product_name = "Bambi"
third_product_name = "Mimi"

company = "Didi "
country = "Poltawien"
town = "Oglietzen"

def create_corpus(text_stream):
    corpus = Corpus('de', texts=text_stream)
    return corpus

def load_corpus( filename):
    corpus = Corpus.load(filename)
    return corpus

def print_corpus(corpus):
    for text in corpus:
        print(text)

def replace_bank_names(text):

    text = replace_strings(text, first_products, first_product_name)
    text = replace_strings(text, second_products, second_product_name)
    text = replace_strings(text, third_products, third_product_name)
    text = replace_strings(text, first_banks, first_bank_name)
    text = replace_strings(text, second_banks, second_bank_name)
    text = replace_strings(text, countries, country)
    text = replace_strings(text, towns, town)
    return text


def replace_strings(text, banks, bank_name):
    for bank in banks:
        if bank in text:
            text = text.replace(bank, bank_name)
    return text


def custom_preprocess(text):
    text = replace_bank_names(text)
    processed_text = preprocess_text(text, fix_unicode = True, lowercase = False, no_urls = True, no_emails = True, no_phone_numbers = True, no_punct = False, no_numbers=False)
    return processed_text


def model_process(text, nlp):
    doc = nlp(text)
    keep_toks = []
    for token in doc:
        if (token.pos_ in ["AUX", "CONJ", "CCONJ", "DET", "NUM", "PRON", "PUNCT", "SYM"]):
            keep_toks.append(token.pos_)
        else:
            keep_toks.append(token.lemma_)
    return " ".join(keep_toks)

