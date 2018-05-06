
import yaml
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from query import QueryExecutor

class Application:
    def __init__(self, config):
        models_dir = config['models_dir']
        mongo_connection = config['mongo_connection']
        self.query_executor = QueryExecutor(mongo_connection, models_dir)
        self.model_facade = self.query_executor.model_facade

