
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions



if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    #copy_into_qa_documents(data_dir, mongo_connection)
    #split_qa_documents_into_questions(mongo_connection)
    print_all_questions(mongo_connection)
