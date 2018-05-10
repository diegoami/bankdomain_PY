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
        self.doc2vecFacade = Doc2VecFacade(self.models_dir, window=8, min_count=4, sample=0, epochs=35, alpha=0.01,vector_size=300, batch_size=10000)
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

    def similar_doc_wv(self, tokens, topn=20):
        trigrams = self.gramFacade.phrase(tokens)
        vector = self.doc2vecFacade.get_vector_from_phrase(trigrams)
        scores = self.doc2vecFacade.get_most_similar(vector, topn=topn)
        return scores

    def similar_id_wv(self, id, topn=20):
        scores = self.doc2vecFacade.model.docvecs.most_similar([int(id)], topn=topn)
        return scores

    def similar_doc(self, tokens):
        trigrams = self.gramFacade.phrase(tokens)
        vector = self.tfidfFacade.get_vec_from_tokenized(trigrams)
        scores = self.tfidfFacade.get_scores_from_vec(vector)
        return trigrams, scores

    def similar_id(self, id):
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
