
import yaml
from repository.mongo_ops import copy_into_qa_documents, split_qa_documents_into_questions, print_all_questions, iterate_questions_in_mongo
from preprocess.txt_preprocess import create_corpus, load_corpus, print_corpus
from components.custom_lemmas import CUSTOM_LOOKUP
from textacy.corpus import Corpus
import spacy
if __name__ == '__main__':

    config = yaml.safe_load(open("config.yml"))
    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    corpus_out_dir = config['corpus_dir']
    corpus_filename = config['corpus_filename']
    corpus_proc_filename = config['corpus_proc_filename']



    corpus = load_corpus(corpus_out_dir+'/'+corpus_proc_filename)
    new_corpus = Corpus('de')
    new_corpus.spacy_lang.Defaults.lemma_lookup.update(CUSTOM_LOOKUP)
    new_corpus.add_texts([doc.text for doc in corpus] )

    # corpus.spacy_vocab
    count_res = new_corpus.word_doc_freqs(normalize=u'lemma',  as_strings=True)
    #count_res = corpus.word_doc_freqs(normalize=u'lemma',  as_strings=True)
    with open('data/all_terms.txt', 'w') as fw:
        for key, value in sorted(count_res.items(), key=lambda x: x[1], reverse = True):
            print("{}: {}".format(key, value), file=fw)
