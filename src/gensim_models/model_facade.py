from .gram_facade import GramFacade
from .doc2vec_facade import Doc2VecFacade
from .tfidf_facade import TfidfFacade
from .kmeans_facade import KMeansFacade
from .tf2wv_mapper import Tf2WvMapper
import logging
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
class ModelFacade:

    def __init__(self, mongo_repository, models_dir):
        self.mongo_repository = mongo_repository
        self.models_dir = models_dir
        self.gramFacade = GramFacade(self.models_dir, bigrams_threshold=0.88, trigrams_threshold=0.88 )
        self.doc2vecFacade = Doc2VecFacade(self.models_dir, window=9, min_count=4, sample=0, epochs=35, alpha=0.01,vector_size=300, batch_size=10000)
        self.kmeansFacade = KMeansFacade()
        self.tfidfFacade = TfidfFacade(self.models_dir, no_below=3, no_above=0.9, num_topics=400 )
        self.tf2wv = Tf2WvMapper(models_dir, self.gramFacade, self.tfidfFacade, self.doc2vecFacade )

    def create_model(self):
        self.mongo_repository.load_all_documents()
        all_questions_processed = self.mongo_repository.get_all_questions()
        self.gramFacade.create_model( all_questions_processed )

        bigrams = self.gramFacade.export_bigrams(all_questions_processed)
        trigrams = self.gramFacade.export_trigrams(bigrams)

        self.doc2vecFacade.create_model(trigrams)
        self.tfidfFacade.create_all_models(trigrams)
        self.load_models_for_create()
        self.tf2wv.create_weighted_vector_docs()

    def load_models_for_create(self):
        self.gramFacade.load_models()
        self.doc2vecFacade.load_models()
        self.tfidfFacade.load_models()
        self.tf2wv.remap()

    def load_models(self):
        self.load_models_for_create()
        self.tf2wv.load_weighted_vector()

    def find_documents_with_tokens(self, tokens_not_found):
        questions, answers = self.mongo_repository.questions_no_answer, self.mongo_repository.questions_with_answer
        found_in_questions, found_in_answers = 0, 0
        found_with_tokens = []
        for token in tokens_not_found:
            found_in_questions = [i  for i, x in enumerate(questions) if token in x ]
            found_in_answers = [i - len(found_in_questions) + 1 for i, x in enumerate(answers) if token in x]
            found_with_tokens += found_in_questions
            found_with_tokens += found_in_answers
        logging.info("Ids for tokens : Questions {}, Answers {} ".format(found_in_questions, found_in_answers))
        return found_with_tokens


    def similar_doc(self, trigrams, tokens_not_found):
        min_level =  self.mongo_repository.num_questions
        scores_wv = self.similar_doc_wv(trigrams)


        scores_tfidf = self.similar_doc_tfidf(trigrams)
        idx_with_tokens_nf = self.find_documents_with_tokens(tokens_not_found)
        scores_map = {}
        for idx, score_wv in scores_wv:
            ridx = int(idx if idx >= min_level else idx+min_level)
            dict_score = scores_map.get(ridx, {"idx": idx})
            if not "wv" in dict_score:
                dict_score.update({"wv" : score_wv, "total" : score_wv  })
                scores_map[ridx] = dict_score
        for idx in idx_with_tokens_nf:
            ridx = int(idx if idx >= min_level else idx + min_level)
            dict_score = scores_map.get(ridx, {"idx": idx})
            dict_score["token_nf"] = dict_score.get("token_nf", 0) + 1
            dict_score["total"] = dict_score.get("total", 0) + 1
            logging.info("Word not found: {}".format(dict_score))
            scores_map[ridx] = dict_score
        for idx, score_tfidf in scores_tfidf:
            ridx = int(idx if idx >= min_level else idx + min_level)
            dict_score = scores_map.get(ridx,{"idx": idx})
            if not "tfidf" in dict_score:
                dict_score["tfidf"] = score_tfidf
                dict_score["total"] = dict_score.get("total", 0) + score_tfidf
                scores_map[ridx] = dict_score

        scores = sorted([(ridx, dict_score.get("idx",0), dict_score.get("total",0), dict_score.get("tfidf",0), dict_score.get("wv",0)) for ridx, dict_score in scores_map.items()], key=lambda x: x[2], reverse=True)
        return scores

    def similar_doc_wv(self, trigrams, topn=None):
        logging.info("Processing trigrams : {}".format(trigrams))
        weighted_list = self.tf2wv.get_weighted_list(trigrams)

        if len(weighted_list) > 0:
            logging.info("Weighted list of length: {}".format(len(weighted_list)))
            arg_scores = self.doc2vecFacade.model.docvecs.most_similar(weighted_list, topn=topn)
            arr_range = np.expand_dims(np.arange(len(arg_scores)), axis=1)
            arr_score = np.expand_dims(arg_scores, axis=1)
            arr_total = np.concatenate([arr_range, arr_score], axis=1)
            arsorted = np.argsort(-arg_scores)
            arr_result = arr_total[arsorted]
            scores = arr_result.tolist()
            return scores
        else:
            return []
    def similar_id_wv(self, id, topn=None):
        scores = self.doc2vecFacade.model.docvecs.most_similar([int(id)], topn=topn)
        return scores

    def similar_doc_tfidf(self, trigrams):
        vector = self.tfidfFacade.get_vec_from_tokenized(trigrams)
        scores = self.tfidfFacade.get_scores_from_vec(vector)
        return  scores

    def similar_id_tfidf(self, id):
        vector = self.tfidfFacade.get_vec_docid(id)
        scores = self.tfidfFacade.get_scores_from_vec(vector)
        return scores

    def retrieve_clusters(self, num_clusters=50):
        return self.kmeansFacade.do_cluster(self.doc2vecFacade.model, num_clusters=num_clusters)

    def get_similar_questions(self, tokens):
        trigrams = self.gramFacade.phrase(tokens)
        sim_matrx = self.tf2wv.get_similarity_matrix(trigrams)
        sort_index = np.argsort(sim_matrx)
        return self.mongo_repository.panda.iloc[sort_index]


    def words_report(self, min_count, language_facade):
        logging.info("Retrieving words for min count {}".format(min_count))
        words = self.doc2vecFacade.retrieve_words()
        wps = []
        logging.info("Retrieved {} words".format(len(words)))
        for index, word_count in enumerate(words):
            word, count = word_count
            if (count >= min_count):
                sim_w = self.doc2vecFacade.pull_scores_word(word, threshold=0.78, topn=20)
                forms = language_facade.retrieve_forms_for_lemma(word)
                wps.append({"word": word, "count": count,
                            "forms": ", ".join([f for f in forms]),
                            "n_forms": len(forms),
                            "simw": ", ".join([v[0] + " (" + str(round(v[1], 2)) + ")" for v in sim_w])

                            })
                if (len(wps) % 100 == 0):
                    logging.info("{}:  Added {} words".format(index, len(wps)))
        logging.info("Finished retrieving words")
        return wps
