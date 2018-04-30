
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions, iterate_questions_in_mongo, process_questions
from preprocess.txt_preprocess import create_corpus, load_corpus, print_corpus
from textacy.preprocess import preprocess_text
import spacy


if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    corpus_out_dir = config['corpus_dir']
    corpus_filename = config['corpus_filename']
    corpus_proc_filename = config['corpus_proc_filename']
    nlp = spacy.load('de')
    all_texts = process_questions(mongo_connection,  preprocess_text, fix_unicode=True, lowercase=False, no_urls=True,
                      no_emails=True, no_phone_numbers=True, no_punct=True)
    new_corpus = create_corpus(all_texts)
    new_corpus.save(corpus_out_dir+'/'+corpus_proc_filename)
