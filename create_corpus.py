
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions, iterate_questions_in_mongo
from preprocess.txt_preprocess import create_corpus


if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    corpus_out_dir = config['corpus_dir']
    #copy_into_qa_documents(data_dir, mongo_connection)
    #split_qa_documents_into_questions(mongo_connection)
    corpus = create_corpus(iterate_questions_in_mongo(mongo_connection))
    corpus.save(corpus_out_dir+'/qa_questions.corpus')
    print(corpus)
