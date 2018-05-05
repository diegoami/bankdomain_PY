
import yaml
from repository import MongoRepository


if __name__ == '__main__':
    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    mongo_repository = MongoRepository(mongo_connection)

    with open('data/questions.txt', 'w') as f:
        f.writelines(mongo_repository.iterate_questions(collection=mongo_repository.questions, separator=True))

    with open('data/preprocessed_questions.txt', 'w') as f:
        f.writelines(mongo_repository.iterate_questions(collection=mongo_repository.preprocessed_questions, separator=True))

    with open('data/processed_questions.txt', 'w') as f:
        f.writelines(mongo_repository.iterate_questions(collection=mongo_repository.processed_questions, separator=True))
