
import yaml
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from query import QueryExecutor
from gensim_models import LanguageFacade
import threading, time

class Application:
    def __init__(self, config):
        models_dir = config['models_dir']
        mongo_connection = config['mongo_connection']
        self.query_executor = QueryExecutor(mongo_connection, models_dir)
        self.model_facade = self.query_executor.model_facade
        self.mongo_repository = self.query_executor.mongo_repository

        self.language_facade = LanguageFacade()
        self.wps = None

        if config['preload_words'] and config['preload_words'].strip() == 'True':
            thread = threading.Thread(target=self.preload_words)
            thread.start()
        else:
            logging.info("Not preloading words....")

    def preload_words(self):

        words = self.model_facade.doc2vecFacade.retrieve_words()
        wps = []
        logging.info("Retrieving {} words".format(len(words)))
        for word, count in words:
            if (count >= 8):
                sim_w = self.model_facade.doc2vecFacade.pull_scores_word(word, threshold=0.78, topn=20)
                forms = self.language_facade.retrieve_forms_for_lemma(word)
                wps.append({"word": word, "count": count,
                            "forms": ", ".join([f for f in forms]),
                            "simw": ", ".join([v[0] + " (" + str(round(v[1], 2)) + ")" for v in sim_w])

                            })
        logging.info("Finished retrieving words")
        self.wps = wps