
import yaml
import logging
from language import NlpWrapper

from feature_extract import FeatureProcessor

from repository import MongoRepository
from preprocess import Preprocessor
from gensim_models import ModelFacade
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def doc2vec_similar(mongo_repository, feature_processor, model_facade):

    while True:
        st = input('--> ').lower()
        text = feature_processor(st)
        tokens = text.split()
        logging.info("Split to {}".format(tokens))
        scores = model_facade.similar_doc(tokens)
        print(scores)



if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    data_dir = config['data_dir']
    models_dir = config['models_dir']
    mongo_connection = config['mongo_connection']
    mongo_repository = MongoRepository(mongo_connection)
    nlp = NlpWrapper()
    feature_processor = FeatureProcessor(nlp)
    model_facade = ModelFacade(mongo_repository, models_dir)
    model_facade.load_models()
    doc2vec_similar(mongo_repository, feature_processor, model_facade)