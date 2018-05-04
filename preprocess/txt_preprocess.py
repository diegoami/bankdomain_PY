from textacy.corpus import Corpus
from textacy.preprocess import preprocess_text
import spacy
from components.custom_lemmas import CUSTOM_LOOKUP, CUSTOM_REMOVES, remove_lemmas
from components.custom_stopwords import CUSTOM_STOP_WORDS, add_stop_words
import regex
REGEXES = [regex.compile('\b\d+\b'),regex.compile('\b\d+\.\b'), regex.compile('\b\d+\.\d+\b')]
POS_IGNORE = ["CONJ", "CCONJ", "DET", "NUM", "PRON", "PUNCT", "SYM", "PART",  ]

PUNKT_PREPROCESS = ["/", "<", ">", "*", "=", "–", "+", "·", "|",  "1", "2", "3", "t", "x", "4", "5", "…", "#", "[", "]", "_"]

first_banks = ["PostBank", "PSD", "EthikBank", "TARGOBANK", "Triodos", "Sparda-Bank", "targobank", "FerratumBank", "GarantiBank", "Hanseatic Bank", "Keytrade Bank", "Deutsche Bank", "MERKUR BANK", "Skatbank", "VR-Bank", "norisbank", "Skatbank", "BLKB", "ABN AMRO", "Austrian Anadi Bank", "De Nederlandsche Bank", "HypoVereinsbank", "L-Bank", "Deutschen Handelsbank","schlau-finanziert.at", "Ikano Bank AB", "KSK Köln", "FIL Fondsbank"]
second_banks  = ["solarisBank AG", "solarisBank","SWK Bank", "DNB", "ING DiBa","ING-DiBa" ,"RCI Banque", "Commerzbank","Postbank", "AmExCo", "DB PGK", "UnionInvestment","FinReach", "Crédit Mutuel", "CIC Bank", "Unicredit", "Tigerstarker", "RBd", "Shell", "Ikano Bank", "Svenska Handelsbanken", "Yapı Kredi Bank", "DekaBank", "FGDL", "FFB"]
companies = ["comdirect","CIM","Volkswagen", "Opel", "Renault", "Dacia", "Nissan","GRENKE", "Santander", "Fidor", "Credit Europe", "DKB", "HOB", "IKEA" ,"OKB", "Rabo",  "Ferratum", "NIBC", "Shaufelonline", "EdB", "GLS", "HVB", "PayPal" ,"East West Direkt", "COMPEON", "DHB", "FINAVI", "Finavi", "Fiducia GAD", "Fiducia & GAD", "AMRO", "Anadi", "MLP", "Interhyp", "Ikano",  "Deka", "LBS", "BBVA", "Netcetera AG"]


products_map = {
    "Kash Reserv" : "DidiRahmenkredit",
    "ROBIN" : "DidiVermögen",
    "VR-FinanzPlan" : "DidiVermögen",
    "NIBCard" : "DidiCard",
    "SpardaSecure" : "DidiSecure",
    "Sparkassen-Card" : "DidiCard",
    "RaboSpar90" : "DidiSuperSparkonto",
    "RaboSpar30" : "DidiSparkonto",
    "Kash Borgen" : "DidiRatenkredit",
    "DispoEasy" : "DidiDispo",
    "maxblue" : "DidiInvestor",
    "SpardaNet" : "DidiOnline",
    "S-Card" : "DidiCard",
    "SparkassenCard": "DidiCard",

    "Kleeblatt" : "Didi",
    "sparSmart" : "DidiSuperSparkonto",
    "TWINT" : "DidiPay",
    "easyKonto" :"DidiEasy",
    "SpardaApp" : "DidiApp",
    "EB-Banking App": "DidiApp",
    "Fleks Horten" : "DidiTagesgeld",
    "Anadi-Konto" : "DidiKonto",
    "CrontoPush" : "DidiLogin",
    "VRNetKey" : "DidiLogin",
    "boon." : "DidiPay",
    "Anadi mobilePAY" :  "DidiApp",
    "ZOIN" : "DidiPay",
    "MLP-Konto" : "DidiKonto",
    "S-direkt" : "DidiInvestor",
    "girogo-Funktion": "DidiPay",
    "girogo" : "DidiEasy",
    "S-Depot" : "DidiVermögen",
    "S-Broker" : "DidiBroker",
    "SPG-Verein" : "DidiVerein",
    "SFirm" : "DidiApp",
    "sfirm" : "didiapp",
    "S-Tagesgeld" : "DidiTagesgeld",
    "meine.deutsche-bank.de" : "DidiApp",
    "netsp@r_konto" : "DidiSparKonto",
    "SpardaMobil-Banking" : "DidiApp",
    "VERIMI" : "DidiLogin",
    "SIX Paynet AG" : "DidiPay",
    "PostFinance AG" : "DidiEasy",
    "CrontoSign Swiss App": "DidiApp"


}
countries = ["Deutschland", "Schweiz", "Österreich", "Luxembourg", "Malta", "Belgien", "Ruhr", "Hessen", "España", "Spanien", "Niederlanden", "Niederlande", "Island", "Lichtenstein", "Australien", "Finnland", "Norwegen", "Luxemburg", "Thüringen", "Bayern", "Frankreich", "Türkei", "Italien"]
towns = ["Berlin", "München", "Frankfurt am Main", "Hamburg", "Hannover", "Karlsruhe", "Stuttgart", "Köln", "Düsseldorf", "Duisburg", "Mannheim", "Dresden", "Ingolstadt", "Münster", "Amsterdam", "Helsinki", "Freiburg", "Hannover", "Zürich"]
first_bank_name = "DidiBank"
second_bank_name = "AmbiBank"


company_name = "Didi "
country = "Poltawien"

town = "Oglietzen"

possible_integrator = ["girokonto",  "konto", "einlagen", "behörden", "einstellung", "auszahlung", "verzeichnis","name", "namens", "bank","banken","prozess","verhältnisse","vereinbarungen", "checks", "check", "fristen", "beratung", "kunde", "kunden", "adresse", "daten", "informationen", "spanne", "sprachen", "sprache", "planung", "bescheid", "situation", "verwaltung", "amt", "schulden", "zahlung", "gefühle", "beratungsstelle", "stunden", "beschluss", "schaden", "pfändung", "versicherung", "vertrag", "abtretung", "anteil", "verfahren", "gesellschaft", "datum", "kosten", "kurs", "transaktion", "order" , "verbot", "freiheit", "nummer", "gremium", "kammer", "unabhängig", "system", "limit", "eingang", "ausgang", "gang", "Verfahren", "posten", "vereinbarung", "form", "phase", "teile", "teil"]

characters_to_space = ['/', "*", "(", ")", "+", "·"]
characters_spaced = [" / ", " * ", " ( ", " ) ", " + ", " · "]
GERMAN_SEPARABLE = ["an", "ab", "auf", "aus", "ein", "bei", "heim", "her", "heraus", "herein", "herauf", "hin", "hinauf", "hinaus", "hinein", "los", "mit", "nach", "vor", "weg", "zu", "zurück", "durch", "über", "um", "unter", "wider", "wieder"]

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
    text = map_products(text, products_map)

    text = replace_strings(text, first_banks, first_bank_name)
    text = replace_strings(text, second_banks, second_bank_name)
    text = replace_strings(text, companies, company_name)
    text = replace_strings(text, countries, country)
    text = replace_strings(text, towns, town)
    return text

def replace_characters_to_space(text):
    for index, ctos in enumerate(characters_to_space):
        text = text.replace(ctos , characters_spaced[index])
    return text


def custom_preprocess(text):

    text = replace_bank_names(text)
    text = preprocess_text(text, fix_unicode = True, lowercase = False, no_urls = True, no_emails = True, no_phone_numbers = True, no_punct = False, no_numbers=False)
    text = replace_characters_to_space(text)
    return text


def model_process(text, nlp):

    doc = nlp(text)
    docl = nlp(text.lower())
    curr_trunc = None
    keep_toks = []
    for index, token in enumerate(doc):
        if (token.is_stop):
            pass
        elif (index < len(docl) and docl[index].is_stop):
            pass
        elif any([regex.match(token.text) for regex in REGEXES ]):
            pass
        elif (token.text in PUNKT_PREPROCESS):
            pass
        elif (token.pos_ in POS_IGNORE):
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
            if (token.tag_ == "TRUNC" and token.text[-1] == '-'):
                curr_trunc = token.text[:-1]
            elif (token.pos_ == "VERB"):
                sep_part = [x for x in token.children if x.tag_ == "PTKVZ"
                            and x.text in GERMAN_SEPARABLE ]
                if (len(sep_part) > 0):
                    to_app = sep_part[0].text+token.lemma_.lower()

                    keep_toks.append(to_app)
                else:
                    keep_toks.append(token.lemma_)

            elif (index < len(docl) and docl[index].pos_ == "VERB") and any([x for x in docl[index].children if x.tag_ == "PTKVZ" and x.text in GERMAN_SEPARABLE ]):
                sep_part = [x for x in docl[index].children if x.tag_ == "PTKVZ"
                            and x.text in GERMAN_SEPARABLE]
                if (len(sep_part) > 0):
                    to_app = sep_part[0].text + docl[index].lemma_.lower()

                    keep_toks.append(to_app)
            elif (index < len(docl)      and docl[index].pos_ == "VERB") and (docl[index].lemma_ != docl[index].text):
                keep_toks.append(docl[index].lemma_)
            else:
                keep_toks.append(token.lemma_)


    return " ".join(keep_toks)


if __name__ == '__main__':
    nlp = spacy.load('de')
    remove_lemmas(nlp)
    map(nlp.Defaults.lemma_lookup.pop, CUSTOM_REMOVES)

    nlp.Defaults.lemma_lookup.update(CUSTOM_LOOKUP)
    add_stop_words(nlp)
    print(model_process(
        "Alle Unterlagen senden Sie uns vollständig ausgefüllt und unterschrieben retour.",
        nlp))
    print(model_process(
        "Unten Ein DepotPlus können Sie ausschließlich online unter dem unten genannten Link eröffnen.",
        nlp))
    print(model_process(
        "Bestätigen Sie diesen Auftrag im Anschluss mit einer iTAN oder mTAN",
        nlp))

    print(model_process(
        "Fallen zusätzliche Kosten bei der Nutzung der Versicherungen meiner Karten an?",
        nlp))

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
    print(model_process(
        "Wichtig dabei ist, dass die Gutschrift von Ihrem Arbeitgeber korrekt als Lohn / Gehalt verschlüsselt wurde. Anderenfalls kann diese maschinell nicht als Lohn- / Gehaltseingang erkannt werden.",
        nlp))

    print(model_process(
        "Wenn Sie einen Computer benutzen, an dem auch andere arbeiten und Sie das ungute Gefühl haben, dass diese eventuell versteckte Seiten einsehen könnten, nachdem Sie die Station verlassen haben, beenden / verlassen Sie Ihre Browser-Software.",
        nlp))
    print(model_process(
        "Reichen Sie uns hierzu den Antrag der anderen Bank mit dem Hinweis auf Auszahlung der Niedrigzins-Garantie ein.",
        nlp))
    print(model_process(
        "Ein Dispo Antrag ist bei uns einfacher als bei vielen Filialbanken. Bonität vorausgesetzt, verläuft die Einrichtung Deines Disporahmens schnell und mit nur wenigen Angaben. Der Dispo hilft Dir, wenn Du Dein Konto kurzfristig überziehen möchtest.",
        nlp))


    print(model_process(
        "Häufig reicht es auch, eine längere Laufzeit zu wählen, und dadurch die monatliche Belastung zu reduzieren.",
        nlp))

    print(model_process(
        "Genossenschaftsbanken, Sparkassen und die Groß- und Privatbanken haben ein eigenes Online-Bezahlverfahren \"paydirekt\" entwickelt. Mit paydirekt können Sie mit Ihrem Girokonto im Internethandel direkt, sicher und einfach bezahlen.",nlp))

    print(model_process(
        "Sondertilgungen und vorzeitige Rückzahlungen von Teilbeträgen sind jederzeit kostenfrei möglich.",nlp))
    print(model_process(
        "Wann wird eine Entschädigung für Einlagen gezahlt?", nlp))
    print(model_process(
        "Falls Du Deine Kreditkarte noch nicht bei 3D Secure registriert hast, empfehlen wir, dies vorab über die Website Deiner Bank durchzuführen", nlp))
    print(model_process(
        "Sobald Du DidiPay auf dem neuen Smartphone  ( NFC-fähig, Android 4.4 oder höher )  installiert hast, kannst Du Dich mit Deinen existierenden Zugangsdaten einloggen.", nlp))


