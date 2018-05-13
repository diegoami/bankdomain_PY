from .gram_facade import GramFacade
from .doc2vec_facade import Doc2VecFacade
from .tfidf_facade import TfidfFacade
from .kmeans_facade import KMeansFacade
from .tf2wv_mapper import Tf2WvMapper
import logging
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
class ModelFacade:

    def __init__(self, mongo_repository, models_dir):
        self.mongo_repository = mongo_repository
        self.models_dir = models_dir
        self.gramFacade = GramFacade(self.models_dir,  min_count_bigrams=10, min_count_trigrams=11)
        self.doc2vecFacade = Doc2VecFacade(self.models_dir, window=9, min_count=3, sample=0, epochs=35, alpha=0.01,vector_size=300, batch_size=10000)
        self.kmeansFacade = KMeansFacade()
        self.tfidfFacade = TfidfFacade(self.models_dir, no_below=3, no_above=0.9, num_topics=400 )
        self.tf2wv = Tf2WvMapper(models_dir, self.gramFacade, self.tfidfFacade, self.doc2vecFacade )

    def create_model(self):
        self.mongo_repository.load_all_documents()
        all_questions_processed = self.mongo_repository.all_processed_splitted_questions
        self.gramFacade.create_model( all_questions_processed )

        bigrams = self.gramFacade.export_bigrams(all_questions_processed)
        trigrams = self.gramFacade.export_trigrams(bigrams)

        self.doc2vecFacade.create_model(trigrams)
        self.tfidfFacade.create_all_models(trigrams)
        self.load_models_for_create()
        self.tf2wv.create_weighted_vector_docs()

    def load_models_for_create(self):
        self.gramFacade.load_models()
        self.doc2vecFacade.load_models()
        self.tfidfFacade.load_models()
        self.tf2wv.remap()

    def load_models(self):
        self.load_models_for_create()
        self.tf2wv.load_weighted_vector()

    def similar_doc(self, tokens):
        min_level =  self.mongo_repository.num_questions
        trigrams = self.gramFacade.phrase(tokens)
        scores_wv = self.similar_doc_wv(trigrams)
        if len(scores_wv) > 0 :
            scores_tfidf = self.similar_doc_tfidf(trigrams)
            scores_map = {}
            for idx, score_wv in scores_wv:
                ridx = int(idx if idx >= min_level else idx+min_level)
                dict_score = scores_map.get(ridx, {})
                if not "wv" in dict_score:
                    scores_map[ridx] = {"wv" : score_wv  }
            for idx, score_tfidf in scores_tfidf:
                ridx = int(idx if idx >= min_level else idx + min_level)
                dict_score = scores_map.get(ridx,{})
                if not "tfidf" in dict_score:
                    dict_score["tfidf"] = score_tfidf
                    dict_score["total"] = dict_score["tfidf"] + dict_score["wv"]
                    scores_map[ridx] = dict_score
            scores = sorted([(idx, dict_score["total"], dict_score["tfidf"], dict_score["wv"]) for idx, dict_score in scores_map.items()], key=lambda x: x[1], reverse=True)
            return trigrams, scores
        else:
            return trigrams, []

    def similar_doc_wv(self, trigrams, topn=None):
        logging.info("Processing trigrams : {}".format(trigrams))
        weighted_list = self.tf2wv.get_weighted_list(trigrams)

        if len(weighted_list) > 0:
            logging.info("Weighted list of length: {}".format(len(weighted_list)))
            arg_scores = self.doc2vecFacade.model.docvecs.most_similar(weighted_list, topn=topn)
            arr_range = np.expand_dims(np.arange(len(arg_scores)), axis=1)
            arr_score = np.expand_dims(arg_scores, axis=1)
            arr_total = np.concatenate([arr_range, arr_score], axis=1)
            arsorted = np.argsort(-arg_scores)
            arr_result = arr_total[arsorted]
            scores = arr_result.tolist()
            return scores
        else:
            return []
    def similar_id_wv(self, id, topn=None):
        scores = self.doc2vecFacade.model.docvecs.most_similar([int(id)], topn=topn)
        return scores

    def similar_doc_tfidf(self, trigrams):
        vector = self.tfidfFacade.get_vec_from_tokenized(trigrams)
        scores = self.tfidfFacade.get_scores_from_vec(vector)
        return  scores

    def similar_id_tfidf(self, id):
        vector = self.tfidfFacade.get_vec_docid(id)
        scores = self.tfidfFacade.get_scores_from_vec(vector)
        return scores

    def retrieve_clusters(self, num_clusters=50):
        return self.kmeansFacade.do_cluster(self.doc2vecFacade.model, num_clusters=num_clusters)

    def get_similar_questions(self, tokens):
        trigrams = self.gramFacade.phrase(tokens)
        sim_matrx = self.tf2wv.get_similarity_matrix(trigrams)
        sort_index = np.argsort(sim_matrx)
        return self.mongo_repository.panda.iloc[sort_index]
