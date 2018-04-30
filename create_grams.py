
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions, iterate_questions_in_mongo, iterate_proc_questions_in_mongo, process_questions, question_for_model
from preprocess.txt_preprocess import create_corpus, load_corpus, print_corpus,preprocess_text, model_process
from components.custom_lemmas import CUSTOM_LOOKUP
from textacy.corpus import Corpus
import textacy
import spacy
if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    corpus_out_dir = config['corpus_dir']
    corpus_filename = config['corpus_filename']
    corpus_proc_filename = config['corpus_proc_filename']
    corpus_mod_filename = config['corpus_mod_filename']

    corpus = load_corpus(corpus_out_dir+'/'+corpus_mod_filename)
