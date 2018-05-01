from textacy.corpus import Corpus
from textacy.preprocess import preprocess_text
import spacy
from components.custom_lemmas import CUSTOM_LOOKUP

first_banks = ["PostBank", "PSD", "EthikBank", "TARGOBANK", "Triodos", "Sparda-Bank", "targobank", "FerratumBank", "GarantiBank", "Hanseatic Bank", "Keytrade Bank", "Deutsche Bank", "MERKUR BANK", "Skatbank", "VR-Bank", "norisbank", "Skatbank"]
second_banks  = ["solarisBank" "SWK Bank", "DNB", "ING DiBa", "RCI Banque", "Commerzbank"]
companies = ["comdirect","CIM","Volkswagen", "Opel", "Renault", "Dacia", "Nissan","GRENKE", "Santander", "Fidor", "Credit Europe", "DKB", "HOB", "IKEA" ,"OKB", "Rabo", "Sparda", "Ferratum", "NIBC", "Shaufelonline", "EdB", "GLS", "HVB", "PayPal" ,"East West Direkt", "COMPEON", "DHB", "FINAVI", "Finavi"]
first_products = ["Kash Reserv", "ROBIN", "VR-FinanzPlan", "NIBCard", "SpardaSecure", "Sparkassen-Card"]
second_products = ["Kash Borgen", "maxblue", "SecureGo", "SpardaNet", "Kleeblatt", "S-Card"]
third_products = ["Kash Borgen", "TWINT", "easyKonto", "E-Rechnung", "EB-Banking", "RabDirect"]
countries = ["Deutschland", "Schweiz", "Österreich", "Luxembourg", "Malta", "Belgien"]
towns = ["Berlin", "München", "Frankfurt", "Hamburg", "Hannover", "Karslruhe", "Stuttgart", "Köln", "Düsseldorf", "Duisburg", "Mannheim", "Dresden", "Ingolstadt"]
first_bank_name = "DidiBank"
second_bank_name = "AmbiBank"
first_product_name = "Dodo"
second_product_name = "Bambi"
third_product_name = "Mimi"

company_name = "Didi "
country = "Poltawien"
town = "Oglietzen"

possible_integrator = ["girokonto",  "konto", "einlagen", "behörden", "einstellung","verzeichnis","name", "namens", "bank","banken","prozess","verhältnisse","vereinbarungen", "checks", "check", "fristen", "beratung", "kunde", "kunden", "adresse", "daten", "informationen", "spanne", "sprachen", "sprache", "planung", "bescheid", "situation", "verwaltung", "amt", "schulden", "zahlung", "gefühle", "beratungsstelle", "stunden", "beschluss", "schaden", "pfändung", "versicherung", "vertrag", "abtretung", "anteil", "verfahren", "gesellschaft", "datum", "kosten", "kurs", "transaktion", "order" , "verbot", "freiheit", "nummer", "gremium", "kammer", "unabhängig", "system"]

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
    text = replace_strings(text, companies, company_name)
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
    curr_trunc = None
    keep_toks = []
    for token in doc:
        if (token.pos_ in ["CONJ", "CCONJ", "DET", "NUM", "PRON", "PUNCT", "SYM", "PART"]):
            pass
        elif curr_trunc:
            found_ende = [p for p in possible_integrator if token.lemma_.endswith(p)]
            if (len(found_ende) > 0):
                keep_toks.append(curr_trunc+found_ende[0])
            else:
                keep_toks.append(curr_trunc)
            keep_toks.append(token.lemma_)
            curr_trunc = None
        else:
            if (token.tag_ == "TRUNC"):
                curr_trunc = token.text[:-1]
            elif (token.pos_ in ["VERB", "AUX"]):
                sep_part = [x for x in token.children if x.tag_ == "PTKVZ"]
                if (len(sep_part) > 0):
                    keep_toks.append(sep_part[0].text+token.lemma_)
                elif token.pos_ == "VERB":
                    keep_toks.append(token.lemma_)
            else:
                keep_toks.append(token.lemma_)


    return " ".join(keep_toks)


if __name__ == '__main__':
    nlp = spacy.load('de')
    nlp.Defaults.lemma_lookup.update(CUSTOM_LOOKUP)
    print(model_process("Ferner bieten wir interessante und leistungsstarke Fonds sowie ein wachsendes Angebot attraktiver Fonds von führenden Investmentgesellschaften an.", nlp))
    print(model_process(
        "Was sollte ich tun, wenn ich glaube, dass auf mein Konto zugegriffen wurde?",
        nlp))
    print(model_process(
        "Jedes Mal, wenn Sie auf Kontoinformationen in einem Ihrer sicheren Online-Bereiche zugreifen oder diese mitteilen, werden diese Informationen durch eine Technologie namens Secure Sockets Layer, häufig abgekürzt als SSL verschlüsselt.",
        nlp))
    print(model_process(
        "Das Tagesgeldkonto ist ein kostenfreies, sehr gut verzinstes Anlagekonto mit täglicher Verfügbarkeit.",
        nlp))
    print(model_process(
        "Die Regelung garantiert Sicht- und Spareinlagen sowie registrierte Schuldverschreibungen, Bankobligationen und Sparbriefe.",
        nlp))
    print(model_process(
        "Schutz für Giro- und Sparkonten (Tagesgeld- und Festgeldkonten)",
        nlp))


