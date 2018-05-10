from sklearn import cluster
from sklearn import metrics
import spacy
from language import NlpWrapper

class LanguageFacade:

    def __init__(self):
        self.nlp_wrapper = NlpWrapper()


    def retrieve_forms_for_lemma(self, lemma):
        return self.nlp_wrapper.retrieve_forms_for_lemma(lemma)