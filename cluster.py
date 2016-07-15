import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import SpectralClustering, KMeans
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations
import itertools
import silhoutte


def review_to_wordlist(review, lang, remove_stopwords=True):
        review_text = re.sub("[^a-zA-Z]", " ", review)
        words = review_text.lower().split()
        if remove_stopwords:
            if lang == "en":
                with open("./stopwords/english.txt") as f:
                    stoplist = f.readlines()
                    stoplist = [x.strip('\n') for x in stoplist]
            elif lang == "nl":
                with open("./stopwords/dutch.txt") as f:
                    stoplist = f.readlines()
                    stoplist = [x.strip('\n') for x in stoplist]
            else:
                with open("./stopwords/greek.txt") as f:
                    stoplist = f.readlines()
                    stoplist = [x.strip('\n') for x in stoplist]

            words = [w for w in words if not w in stoplist]
        return words


def clustering(list_perproblem, lang):
    vectorizer = TfidfVectorizer(analyzer="char", tokenizer=None, preprocessor=None, stop_words=None,
                                 max_features=5000, min_df=2, ngram_range=(3, 8))
    clean_text = []
    for j in xrange(0, len(list_perproblem)):
        clean_text.append(list_perproblem[j])

    data_features = vectorizer.fit_transform(clean_text)
    data_features = data_features.toarray()
    
    n_start = int(len(data_features)/2)
    n_stop = len(data_features)-5
    step = 5
    n_cls_range = range(n_start, n_stop, step)
    n_cls = silhoutte.number_clusters(data_features, n_cls_range)
    spectral = KMeans(n_clusters=n_cls).fit(data_features)
    label = spectral.fit_predict(data_features)
    return data_features, label


def clustering_word2vec(data_features):
    n_start = int(len(data_features)/2)
    n_stop = len(data_features)-5
    step = 5
    n_cls_range = range(n_start, n_stop, step)
    n_cls = silhoutte.number_clusters(data_features, n_cls_range)
    spectral = KMeans(n_clusters=n_cls).fit(data_features)
    label = spectral.fit_predict(data_features)
    return label


def similarity_score(list_all, dict_features):
    list_all_comb = []
    for i in xrange(len(list_all)):
        list_comb_percluster = []
        if len(list_all[i]) > 1:
            for j in xrange(len(list_all[i])):
                list_comb_percluster.append(list_all[i][j]["document"])
            list_all_comb.append(list_comb_percluster)
    combs = []
    for i in xrange(len(list_all_comb)):
        comb = list(combinations(list_all_comb[i], 2))
        combs.append(comb)
    comb_list = list(itertools.chain(*combs))
    all_sim = []
    for i in xrange(len(comb_list)):
        doc1 = comb_list[i][0].split(".")
        doc2 = comb_list[i][1].split(".")
        vec1 = dict_features[doc1[0]]
        vec2 = dict_features[doc2[0]]
        sim = cosine_similarity(vec1, vec2)
        all_sim.append(sim)
    return comb_list, all_sim


