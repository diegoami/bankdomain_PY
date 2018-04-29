
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions, iterate_questions_in_mongo
from preprocess.txt_preprocess import create_corpus, load_corpus, print_corpus


if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    corpus_out_dir = config['corpus_dir']
    corpus_filename = config['corpus_filename']

    corpus = load_corpus(corpus_out_dir+'/'+corpus_filename)
    print_corpus(corpus)
    print(corpus)
