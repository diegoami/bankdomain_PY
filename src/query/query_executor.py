
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
        self.model_facade.tf2wv.load_weighted_vector()


    def process_input(self, text):

        answers = self.retrieve_answers(text, threshold=0.78)
        scores, token_map, tokens_not_found = answers["scores"], answers["token_map"], answers["tokens_not_found"]
        self.print_documents_for(scores)
        self.print_similar_words(token_map)


    def retrieve_answers(self, text, threshold=0.78, topn=20):
        logging.info("Retrieving answers for {}".format(text))
        text = self.feature_processor(text)
        tokens = text.lower().split()
        logging.info("Tokens after preprocessing : {}".format(tokens))
        trigrams = self.model_facade.gramFacade.phrase(tokens)
        token_map = {}
        dc_token_map = self.model_facade.doc2vecFacade.retrieve_similar_words(trigrams, threshold=threshold, topn=topn)
        dc_tokens_not_found = [word for word in trigrams if word not in dc_token_map]
        token_map.update(dc_token_map )
        tf_tokens_not_found = self.model_facade.tfidfFacade.retrieve_words_not_found(trigrams)

        tokens_not_found = set(dc_tokens_not_found + tf_tokens_not_found)
        scores = self.model_facade.similar_doc(trigrams, tokens_not_found )
        if (len(scores) > 0):
            return {"scores" : scores, "token_map" : token_map, "tokens_not_found" : tokens_not_found }
        else:
            return {"scores" : [], "token_map" : {}, "tokens_not_found" :  trigrams }

    def retrieve_similar_words(self, tokens, threshold=0.78, topn=30):
        token_map = self.model_facade.doc2vecFacade.retrieve_similar_words(tokens, threshold=threshold, topn=topn)
        return token_map

    def retrieve_documents(self,  all_scores, page_id):
        all_documents = []
        scores = all_scores[PER_PAGE*page_id:PER_PAGE*(page_id+1)]
        for ridx, idx, score, tfidf_score, wv_score in scores:
            mongo_document = self.mongo_repository.get_preprocessed_question(ridx)
            lines_answer = mongo_document.split('\n')
            all_documents.append({"idx": idx, "ridx": ridx, "question" : lines_answer[0],
                                  "answer" : "\n".join(lines_answer[1:]), "score" : score, "tfidf_score" : tfidf_score, "wv_score" : wv_score})
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
