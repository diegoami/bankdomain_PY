from .custom_words import remove_words
from .custom_stopwords import CUSTOM_STOP_WORDS, add_stop_words
from .custom_lemmas import CUSTOM_REMOVES, CUSTOM_LOOKUP
import spacy
class NlpWrapper():

    def __init__(self):
        self.nlp = spacy.load('de')
        self.modify()

    def __call__(self, text):
        return self.nlp(text)

    def modify(self):
        remove_words(self.nlp)
        map(self.nlp.Defaults.lemma_lookup.pop, CUSTOM_REMOVES)

        self.nlp.Defaults.lemma_lookup.update(CUSTOM_LOOKUP)
        add_stop_words(self.nlp)