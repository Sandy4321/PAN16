import logging
import numpy as np
from word2vec_utility import KaggleWord2VecUtility


def makeFeatureVec(words, model, num_features):
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0.
    index2word_set = set(model.index2word)
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            featureVec = np.add(featureVec, model[word])
    featureVec = np.divide(featureVec, nwords)
    return featureVec


def getAvgFeatureVecs(reviews, model, num_features):
    counter = 0.
    reviewFeatureVecs = np.zeros((len(reviews), num_features), dtype="float32")
    for review in reviews:
       if counter % 10. == 0.:
           print "Review %d of %d" % (counter, len(reviews))
           logging.debug("Review %d of %d" % (counter, len(reviews)))
       reviewFeatureVecs[counter] = makeFeatureVec(review, model, num_features)
       counter = counter + 1.
    return reviewFeatureVecs


def getCleanReviews(reviews, lang):
    clean_reviews = []
    for review in reviews["article"]:
        clean_reviews.append(KaggleWord2VecUtility.review_to_wordlist(review, lang, remove_stopwords=False))
    return clean_reviews

