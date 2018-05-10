
import yaml
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
from query import QueryExecutor
def doc2vec_similar(query_executor):

    while True:
        st = input('--> ')
        query_executor.process_input(st)
if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    models_dir = config['models_dir']
    mongo_connection = config['mongo_connection']
    query_executor = QueryExecutor(mongo_connection, models_dir)
    doc2vec_similar(query_executor)


