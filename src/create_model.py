
import yaml

import argparse
import logging
import os


from language import NlpWrapper

from feature_extract import FeatureProcessor

from repository import MongoRepository
from preprocess import Preprocessor
from gensim_models import ModelFacade


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


def process_documents(data_dir, output_dir, do_import, do_process, do_print_files):
    logging.info("Processing documents: {}, {}, {}, {}, {}".format(data_dir, output_dir, do_import, do_process, do_print_files))
    nlp = NlpWrapper()
    if do_import:
        mongo_repository.import_questions(data_dir)
    if do_process:
        preprocessor = Preprocessor()
        mongo_repository.process_questions(source_collection=mongo_repository.questions,
                                           target_collection=mongo_repository.preprocessed_questions,
                                           processor=preprocessor)
        feature_processor = FeatureProcessor(nlp)
        mongo_repository.process_questions(source_collection=mongo_repository.preprocessed_questions,
                                           target_collection=mongo_repository.processed_questions,
                                           processor=feature_processor)
    if do_print_files:
        mongo_repository.print_all_files(output_dir)
    logging.info("Finished processing documents")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--import_qa', dest="import_qa", action = 'store_true')
    parser.add_argument('--process', dest="process", action = 'store_true')
    parser.add_argument('--print_files', dest="print_files", action = 'store_true')
    parser.add_argument('--model',  dest="model", action = 'store_true')

    parser.set_defaults(import_qa=False, process=False, print_files=False, model=False)

    args = parser.parse_args()
    config = yaml.safe_load(open("../config.yml"))
    model_dir = config['models_dir']
    output_dir = config['output_dir']
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    data_dir = config['data_dir']
    mongo_connection = config['mongo_connection']
    mongo_repository = MongoRepository(mongo_connection)

    process_documents(data_dir, output_dir, do_import=args.import_qa, do_process=args.process,
                      do_print_files=args.print_files)

    if args.model:
        logging.info("Started creation of model...")
        model_facade = ModelFacade(mongo_repository, model_dir)
        model_facade.create_model()
        logging.info("Finished started creation of model...")
