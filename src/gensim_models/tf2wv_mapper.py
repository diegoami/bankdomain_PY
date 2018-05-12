from gensim import matutils
import numpy as np
DOCS_NUMPY_ARRAY = 'docs_numpy_array'
import logging
from gensim.matutils import unitvec

class Tf2WvMapper:
    def __init__(self, model_dir, gram_facade, tfidf_facade, doc2vec_facade, doc_shape=300):
        self.model_dir = model_dir
        self.gram_facade = gram_facade
        self.tfidf_facade = tfidf_facade
        self.doc2vec_facade = doc2vec_facade
        self.doc_shape =doc_shape

    def remap(self):
        self.dictionary = self.tfidf_facade.dictionary

        self.tfidf = self.tfidf_facade.tfidf
        self.idfs = self.tfidf.idfs
        self.id2word = self.tfidf_facade.lsi.id2word
        self.wv = self.doc2vec_facade.model.wv


    def get_wv(self, word):
        return self.wv.word_vec(word)

    def get_idf(self, word):
        return self.idfs[self.self.dictionary.token2id[word]]


    def get_weighted_vector(self, trigrams):
        vec_bow = self.dictionary.doc2bow(trigrams)
        return self.get_vec_bow(vec_bow)

    def get_weighted_vector_id(self, doc_id):
        vec_bow = self.tfidf_facade.corpus[ doc_id]
        return self.get_vec_bow(vec_bow)

    def get_vec_bow(self, vec_bow):
        vec_sum = np.zeros((1,self.doc_shape))

        for token_id, token_count in vec_bow:
            idf = self.idfs[token_id]
            token = self.dictionary[token_id]
            try:
                vec = self.get_wv(token)
                vec_sum = vec_sum + (token_count * idf) * vec
            except KeyError:
                logging.info("Ignoring token {} - not found in WV".format(token))
                continue
        vec_norm = unitvec(vec_sum )
        return vec_norm

    def get_vec_list(self, vec_bow):
        vec_list = []

        for token_id, token_count in vec_bow:
            idf = self.idfs[token_id]
            token = self.dictionary[token_id]
            try:
                vec = self.get_wv(token)
                vec_weight_tuple = (vec, idf * token_count)
                if (idf > 0 ):
                    vec_list.append(vec_weight_tuple )
            except KeyError:
                logging.info("Ignoring token {} - not found in WV".format(token))
                continue
        return vec_list

    def get_weighted_list(self, trigrams):
        vec_bow = self.dictionary.doc2bow(trigrams)
        return self.get_vec_list(vec_bow)

    def create_weighted_vector_docs(self):
        for index, doc_bow in enumerate(self.tfidf_facade.corpus):
            if (index % 100 == 0):
                logging.info("Processed {} documents".format(index))
            wv_id = self.get_vec_bow(doc_bow)
            if (index > 0):
                np_all_docs = np.concatenate([np_all_docs, wv_id], axis=0)
            else:
                np_all_docs = wv_id
        self.weighted_vector = np_all_docs
        np.save(self.model_dir+'/'+DOCS_NUMPY_ARRAY, self.weighted_vector)

    def load_weighted_vector(self):
        self.weighted_vector = np.load(self.model_dir+'/'+DOCS_NUMPY_ARRAY+".npy")

    def get_similarity_matrix(self, tokens):
        wei_vec = self.get_weighted_vector(tokens)
        wei_n = unitvec(wei_vec)
        res_vec = np.dot(self.weighted_vector, wei_n.T)
        s_matrix = res_vec.T[0]
        return s_matrix


"""
    def get_weighted_vector(self, tokens):
        trigrams = self.gram_facade.phrase(tokens)
        vec_sum = np.zeros((self.doc_shape,))
        for token in trigrams :
            idf = self.get_idf(token)
            vec = self.get_wv(token)
            vec_sum = vec_sum + idf * vec
        vec_avg = vec_sum / len (tokens)
        return vec_avg
"""