
import yaml
import logging
from language import NlpWrapper

from feature_extract import FeatureProcessor

from repository import MongoRepository
from preprocess import Preprocessor
from gensim_models import ModelFacade

PER_PAGE = 20

class QueryExecutor:


    def __init__(self, mongo_connection, models_dir):
        self. mongo_repository = MongoRepository(mongo_connection)
        self.mongo_repository.load_all_documents()
        nlp = NlpWrapper()
        self.feature_processor = FeatureProcessor(nlp)
        self.model_facade = ModelFacade(self.mongo_repository, models_dir)
        self.model_facade.load_models()

    def process_input(self, text):
        scores_tfidf, token_map = self.retrieve_answers(text)

        self.print_documents_for(scores_tfidf)
        self.print_similar_words(token_map)


    def retrieve_answers(self, text):

        text = self.feature_processor(text)
        tokens = text.lower().split()

        trigrams, scores_tfidf = self.model_facade.similar_doc(tokens)

        token_map = self.model_facade.retrieve_similar_words(trigrams, threshold = 0.85, topn=20)

        return scores_tfidf, token_map

    def retrieve_similar_words(self, tokens, threshold=0.85, topn=30):
        token_map = self.model_facade.retrieve_similar_words(tokens, threshold=threshold, topn=topn)
        return token_map

    def retrieve_documents(self,  all_scores, page_id):
        all_documents = []
        scores = all_scores[PER_PAGE*page_id:PER_PAGE*(page_id+1)]
        for id, score in scores:
            mongo_document = self.mongo_repository.get_preprocessed_question(id)
            lines_answer = mongo_document.split('\n')
            all_documents.append({"question" : lines_answer[0],
                                  "answer" : "\n".join(lines_answer[1:]) if score > 0.2 else "", "score" : score})
        return all_documents

    def print_documents_for(self, scores):
        for id, score in scores:
            mongo_document = self.mongo_repository.get_preprocessed_question(id)
            print("======"+str(id)+"============================")
            print(mongo_document)

    def print_similar_words(self, tokenmap):
        print(" ============= SIMILAR WORDS ======W===============")
        for key, values in tokenmap.items():
            print(key, ", ".join([v[0] for v in values]))
