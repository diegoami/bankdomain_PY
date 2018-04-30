
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions, iterate_questions_in_mongo, iterate_proc_questions_in_mongo



if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    #copy_into_qa_documents(data_dir, mongo_connection)
    #split_qa_documents_into_questions(mongo_connection)
    with open('data/all_questions.txt', 'w') as f:
        f.writelines(iterate_questions_in_mongo(mongo_connection, separator=True))

    with open('data/proc_questions.txt', 'w') as f:
        f.writelines(iterate_proc_questions_in_mongo(mongo_connection, separator=True))

