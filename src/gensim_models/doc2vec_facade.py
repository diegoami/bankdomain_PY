from gensim.models import Doc2Vec
from gensim import matutils


#

MODEL_FILENAME = 'doc2vec'

import numpy as np
from gensim.models.doc2vec import TaggedDocument
from datetime import timedelta
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


class LabeledLineSentence(object):
    def __init__(self, idxlist, texts):
        self.doc_list = idxlist
        self.texts = texts

    def __iter__(self):
        for idx, text in zip(self.doc_list, self.texts):
            wtok = text
            tags = [idx]

            yield TaggedDocument(words=wtok, tags=tags)


class Doc2VecFacade:

    def __init__(self, model_dir,  window=10, min_count=5, sample=0.001, epochs=30, alpha=0.1, vector_size=400, batch_size=10000, queue_factor=2, workers=8, version=1):

        self.model_dir = model_dir
        self.name="DOC2VEC-V"+str(version)

        self.window=window
        self.min_count=min_count
        self.sample = sample
        self.epochs = epochs
        self.alpha = alpha
        self.vector_size = vector_size
        self.batch_size = batch_size
        self.queue_factor = queue_factor
        self.workers = workers

    def load_models(self):
        model_filename = self.model_dir+'/'+MODEL_FILENAME
        self.model = Doc2Vec.load(model_filename)

    def get_vector_from_phrase(self, phrase):
        infer_vector = self.model.infer_vector(phrase, alpha=self.alpha, steps=self.epochs)
        return infer_vector

    def get_most_similar(self, vector, topn=20):
        return self.model.docvecs.most_similar([vector], topn=topn)

    def create_model(self, texts):
        it = LabeledLineSentence(range(len(texts)), texts)
        logging.info("Creating model with {} texts".format(len(texts)))
        self.model = Doc2Vec(size=self.vector_size, window=self.window, workers=self.workers, alpha=self.alpha, min_alpha=0.0001,
                             epochs=self.epochs, min_count=self.min_count, sample=self.sample, batch_words=self.batch_size)  # use fixed learning rate
        self.model.build_vocab(it)

        logging.info("Starting to train......")

        self.model.train(it, total_examples=self.model.corpus_count, epochs=self.epochs, queue_factor=self.queue_factor)

        logging.info("Training completed, saving to  " + self.model_dir)
        self.model.save(self.model_dir + MODEL_FILENAME)

    def retrieve_words(self):
        cw_l = []
        for word, vocab_obj in self.model.wv.vocab.items():
            cw_l.append((word, vocab_obj.count))
        cw_s = sorted(cw_l, key=lambda x: x[1], reverse=True)
        return cw_s

    def pull_scores_word(self, criteria, threshold, topn=15):
        scores = self.model.most_similar(criteria, topn=topn)
        found_scores = [score for score in scores if score[1] > threshold]
        return found_scores

    def retrieve_similar_words(self, arg_tokens, threshold = 0.9, topn=15):
        tokens_map = {}
        tokens =[ token for token in arg_tokens if token in self.model.wv.vocab]
        for token in tokens:
            tokens_map[token] = self.pull_scores_word(token, threshold, topn)
        if (len(tokens) > 0):
            tokens_map["ALL"] = self.pull_scores_word(tokens, threshold, topn)

        return tokens_map
