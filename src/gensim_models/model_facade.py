from repository import MongoRepository
from .gram_facade import GramFacade
from .doc2vec_facade import Doc2VecFacade
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
class ModelFacade:

    def __init__(self, mongo_repository, models_dir):
        self.mongo_repository = mongo_repository
        self.models_dir = models_dir
        self.gramFacade = GramFacade(self.models_dir, 10, 10)
        self.doc2vecFacade = Doc2VecFacade(self.models_dir, window=8, min_count=6, sample=0.001, epochs=45, alpha=0.01,
                                      vector_size=300, batch_size=10000)

    def create_model(self):

        all_questions = list(self.mongo_repository.iterate_questions(
            collection=self.mongo_repository.processed_questions, separator=False))
        self.gramFacade.create_model(all_questions)

        bigrams = self.gramFacade.export_bigrams(all_questions)
        trigrams = self.gramFacade.export_trigrams(bigrams)

        self.doc2vecFacade.create_model(trigrams)

    def load_models(self):
        self.gramFacade.load_models()
        self.doc2vecFacade.load_models()

    def similar_doc(self, text):
        trigrams = self.gramFacade.phrase(text)
        logging.info("Trigrams : {}".format(trigrams))
        vector = self.doc2vecFacade.get_vector_from_phrase(trigrams)
        logging.info("vector : {}".format(vector))
        scores = self.doc2vecFacade.get_most_similar(vector)
