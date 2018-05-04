
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions, iterate_questions_in_mongo, iterate_proc_questions_in_mongo, process_questions, question_for_model
from preprocess.txt_preprocess import create_corpus, load_corpus, print_corpus,preprocess_text, model_process
from components.custom_lemmas import CUSTOM_LOOKUP, CUSTOM_REMOVES
from components.custom_stopwords import CUSTOM_STOP_WORDS, add_stop_words

from textacy.corpus import Corpus
import spacy
if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    corpus_out_dir = config['corpus_dir']
    corpus_filename = config['corpus_filename']
    corpus_proc_filename = config['corpus_proc_filename']
    corpus_mod_filename = config['corpus_mod_filename']

    nlp = spacy.load('de')
    map(nlp.Defaults.lemma_lookup.pop, CUSTOM_REMOVES)
    nlp.Defaults.lemma_lookup.update(CUSTOM_LOOKUP)

    add_stop_words(nlp)
    all_texts = question_for_model(mongo_connection, model_process, nlp)
    with open('data/mod_questions.txt', 'w') as f:
        f.writelines(all_texts)

    new_corpus = create_corpus(all_texts)
    new_corpus.save(corpus_out_dir + '/' + corpus_mod_filename)