import re
from bs4 import BeautifulSoup


class KaggleWord2VecUtility(object):
    """KaggleWord2VecUtility is a utility class for processing raw HTML text into segment for further learning"""
    @staticmethod
    def review_to_wordlist(review, lang, remove_stopwords=False):
        review_text = BeautifulSoup(review).get_text()
        review_text = re.sub("[^a-zA-Z]", " ", review_text)
        review_text.decode('utf8')
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

    # Define a function to split a review into parsed sentence
    @staticmethod
    def review_to_sentences(review, tokenizer, lang, remove_stopwords=False):
        raw_sentences = tokenizer.tokenize(review.decode('utf8').strip())
        sentences = []
        for raw_sentence in raw_sentences:
            if len(raw_sentence) > 0:
                sentences.append(KaggleWord2VecUtility.review_to_wordlist(raw_sentence, lang, remove_stopwords))
        return sentences
