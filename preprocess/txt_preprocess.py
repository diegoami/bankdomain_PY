from textacy.corpus import Corpus
from textacy.preprocess import preprocess_text




def create_corpus(text_stream):
    corpus = Corpus('de', texts=text_stream)
    return corpus

def load_corpus( filename):
    corpus = Corpus.load(filename)
    return corpus

def print_corpus(corpus):
    for text in corpus:
        print(text)

def custom_preprocess(text):
    processed_text = preprocess_text(text, fix_unicode = True, lowercase = False, no_urls = True, no_emails = True, no_phone_numbers = True, no_punct = True, no_numbers=True)
    return processed_text