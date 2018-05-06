

import yaml
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from query import QueryExecutor

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    models_dir = config['models_dir']
    mongo_connection = config['mongo_connection']
    query_executor = QueryExecutor(mongo_connection, models_dir)
    doc2vec_similar(query_executor)


X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()