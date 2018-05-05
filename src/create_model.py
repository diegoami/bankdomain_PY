
import yaml
import logging
from language import NlpWrapper

from feature_extract import FeatureProcessor

from repository import MongoRepository
from preprocess import Preprocessor
from gensim_models import ModelFacade


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
if __name__ == '__main__':
    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    mongo_repository = MongoRepository(mongo_connection)

    nlp = NlpWrapper()
    mongo_repository.import_questions(data_dir)
    preprocessor = Preprocessor()
    mongo_repository.process_questions(source_collection=mongo_repository.questions,
                                       target_collection=mongo_repository.preprocessed_questions,
                                       processor=preprocessor)
    feature_processor = FeatureProcessor(nlp)
    mongo_repository.process_questions(source_collection=mongo_repository.preprocessed_questions,
                                           target_collection=mongo_repository.processed_questions, processor=feature_processor)
    mongo_repository.print_all_files()

    model_facade = ModelFacade(mongo_repository, data_dir)
    model_facade.create_model()
