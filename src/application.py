
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
        self.wps_count = None
        self.grams = None
        self.loading_words_thread = None
        self.config = config
        logging.info("Application config: {}".format(config))

        if config['preload_words'] and config['preload_words'] == True:
            self.start_load_words()
        else:
            logging.info("Not preloading words....")

    def start_load_words(self, min_count = 8):
        if not self.loading_words_thread or not self.loading_words_thread.is_alive():
            self.loading_words_thread = threading.Thread(name='load_words', target=self.load_words, kwargs={'min_count':min_count})
            self.loading_words_thread.start()

    def load_words(self, min_count=8):
        wps = self.model_facade.words_report(min_count)
        self.wps = wps
        self.wps_count = min_count


    def load_grams(self):
        if not self.grams:
            logging.info("Retrieving grams...")
            grams = self.model_facade.gramFacade.retrieve_grams()
            logging.info("Finished retrieving")
            self.grams = grams
        return self.grams