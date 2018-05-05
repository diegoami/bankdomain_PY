
import yaml
from language import NlpWrapper
from repository import MongoRepository
from feature_extract import FeatureProcessor

if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    mongo_repository = MongoRepository(mongo_connection )
    nlp = NlpWrapper()
    feature_processor = FeatureProcessor(nlp)
    mongo_repository.process_questions(source_collection=mongo_repository.preprocessed_questions,
                                       target_collection=mongo_repository.processed_questions, processor=feature_processor)

