from repository import MongoRepository
from .gram_facade import GramFacade
from .doc2vec_facade import Doc2VecFacade
from .tfidf_facade import TfidfFacade
from .kmeans_facade import KMeansFacade
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
class ModelFacade:

    def __init__(self, mongo_repository, models_dir):
        self.mongo_repository = mongo_repository
        self.models_dir = models_dir
        self.gramFacade = GramFacade(self.models_dir,  min_count_bigrams=8, min_count_trigrams=10)
        self.doc2vecFacade = Doc2VecFacade(self.models_dir, window=8, min_count=4, sample=0, epochs=35, alpha=0.01,vector_size=300, batch_size=10000)
        self.kmeansFacade = KMeansFacade()
        self.tfidfFacade = TfidfFacade(self.models_dir, no_below=3, no_above=0.9, num_topics=400 )

    def create_model(self):

        self.mongo_repository.load_all_documents()

        all_questions_processed = self.mongo_repository.all_processed_splitted_questions
        self.gramFacade.create_model( all_questions_processed )

        bigrams = self.gramFacade.export_bigrams(all_questions_processed)
        trigrams = self.gramFacade.export_trigrams(bigrams)

        self.doc2vecFacade.create_model(trigrams)
        self.tfidfFacade.create_all_models(trigrams)

    def load_models(self):
        self.gramFacade.load_models()
        self.doc2vecFacade.load_models()
        self.tfidfFacade.load_models()

    def similar_doc_wv(self, tokens, topn=20):
        trigrams = self.gramFacade.phrase(tokens)

        vector = self.doc2vecFacade.get_vectorr_from_phrase(trigrams)

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

    def retrieve_similar_words(self, arg_tokens, threshold = 0.9, topn=15):
        tokens_map = {}
        tokens =[ token for token in arg_tokens if token in self.doc2vecFacade.model.wv.vocab]
        for token in tokens:
            tokens_map[token] = self.pull_scores_word(token, threshold, topn)
        if (len(tokens) > 0):
            tokens_map["ALL"] = self.pull_scores_word(tokens, threshold, topn)

        return tokens_map

    def pull_scores_word(self, criteria, threshold, topn=15):
        scores = self.doc2vecFacade.model.most_similar(criteria, topn=topn)
        found_scores = [score for score in scores if score[1] > threshold]
        return found_scores


    def retrieve_clusters(self, num_clusters=50):
        return self.kmeansFacade.do_cluster(self.doc2vecFacade.model, num_clusters=num_clusters)

    def retrieve_words(self):
        cw_l = []
        for word, vocab_obj in self.doc2vecFacade.model.wv.vocab.items():
            cw_l.append((word, vocab_obj.count))
        cw_s = sorted(cw_l, key=lambda x: x[1], reverse=True)
        return cw_s