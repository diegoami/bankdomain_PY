from gensim import matutils
import numpy as np

class Tf2WvMapper:
    def __init__(self, tfidf_facade, doc2vec_facade, doc_shape=300):
        self.tfidf_facade = tfidf_facade
        self.doc2vec_facade = doc2vec_facade
        self.doc_shape =doc_shape

    def remap(self):
        self.dictionary = self.tfidf_facade.dictionary
        self.token2id = self.dictionary.token2id
        self.tfidf = self.tfidf_facade.tfidf
        self.idfs = self.tfidf.idfs
        self.id2word = self.tfidf_facade.lsi.id2word
        self.wv = self.doc2vec_facade.model.wv

    def get_wv(self, word):
        return self.wv.word_vec(word)

    def get_idf(self, word):
        return self.idfs[self.token2id[word]]

    def get_weighted_vector(self, tokens):
        vec_sum = np.zeros((self.doc_shape,))
        for token in tokens:
            idf = self.get_idf(token)
            vec = self.get_wv(token)
            vec_sum = vec_sum + idf * vec
        vec_avg = vec_sum / len (tokens)
        return vec_avg