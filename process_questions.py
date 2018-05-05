
import yaml
from repository import MongoRepository

from repository import MongoRepository
from preprocess import Preprocessor


if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    mongo_repository = MongoRepository(mongo_connection)
    preprocessor = Preprocessor()
    mongo_repository.process_questions(source_collection=mongo_repository.questions, target_collection= mongo_repository.preprocessed_questions, processor=preprocessor)
