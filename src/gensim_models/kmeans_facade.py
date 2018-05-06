from sklearn import cluster
from sklearn import metrics

class KMeansFacade:




    def do_cluster(self, model, num_clusters=50):
        X = model[model.wv.vocab]
        kmeans = cluster.KMeans(n_clusters=num_clusters)
        kmeans.fit(X)

        labels = kmeans.labels_

        words = list(model.wv.vocab)
        all_cluster = dict()
        for i, word in enumerate(words):
            if (labels[i] not in all_cluster):
                all_cluster[labels[i]] = []
            all_cluster[labels[i]].append(word)
        return all_cluster