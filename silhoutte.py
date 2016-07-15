from __future__ import print_function
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

print(__doc__)


def number_clusters(X, range_n_clusters):
    avg_sil_score = []
    for n_clusters in range_n_clusters:
        clusterer = KMeans(n_clusters=n_clusters)
        cluster_labels = clusterer.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        avg_sil_score.append(silhouette_avg)
    max_sil_score = np.max(avg_sil_score)
    n_cls = avg_sil_score.index(max_sil_score)
    return range_n_clusters[n_cls]
