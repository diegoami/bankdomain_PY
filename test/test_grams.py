from language import NlpWrapper
from feature_extract import FeatureProcessor
import yaml
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from query import QueryExecutor

if __name__ == '__main__':
    config = yaml.safe_load(open("../config.yml"))
    key_config = yaml.safe_load(open(config["key_file"]))
    config.update(key_config)

    models_dir = config['models_dir']
    mongo_connection = config['mongo_connection']

    query_executor = QueryExecutor(mongo_connection, models_dir)
    model_facade = query_executor.model_facade
    mongo_repository = query_executor.mongo_repository
    words_report = model_facade.words_report(min_count=3)