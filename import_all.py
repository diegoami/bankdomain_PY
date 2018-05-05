
import yaml
from repository import MongoRepository


if __name__ == '__main__':
    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    mongo_repository = MongoRepository(mongo_connection)
    mongo_repository.import_questions(data_dir)