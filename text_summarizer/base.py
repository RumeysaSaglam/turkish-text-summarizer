"""
Original Implementation

Author: Gaetano Rossiello
Email: gaetano.rossiello@uniba.it


Implementation for Turkish Language

Author: Houssem MENHOUR
Email: husmen93@gmail.com
"""
import re
import string
import unidecode
import numpy as np
from nltk.tokenize import sent_tokenize as nltk_sent_tokenize
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
from scipy.spatial.distance import cosine
from gensim.summarization.textcleaner import split_sentences as gensim_sent_tokenize
import flashtext

from text_summarizer.zemberek import Zemberek
#from zemberek import sent_tokenize as zmbrk_sent_tokenize
#from zemberek import word_tokenize as zmbrk_word_tokenize
#from zemberek import stopwords as zmbrk_stopwords

def similarity(v1, v2):
    score = 0.0
    if np.count_nonzero(v1) != 0 and np.count_nonzero(v2) != 0:
        score = ((1 - cosine(v1, v2)) + 1) / 2
    return score


class BaseSummarizer:

    extra_stopwords = ["''", "``", "'s"]

    def __init__(self,
                 language='turkish',
                 preprocess_type='zemberek',
                 stopwords_remove=True,
                 length_limit=10,
                 debug=False):
        self.language = language
        #Restrict Zemberek usage to only Turkish language
        self.preprocess_type = preprocess_type if (self.language == "turkish" or preprocess_type != 'zemberek') else 'nltk'
        self.zmbrk = Zemberek() if self.preprocess_type == 'zemberek' else None
        self.stopwords_remove = stopwords_remove
        self.length_limit = length_limit
        self.debug = debug
        if stopwords_remove:
            stopword_remover = flashtext.KeywordProcessor()
            if self.preprocess_type == "zemberek":
                for stopword in self.zmbrk.stopwords.words():
                    stopword_remover.add_keyword(stopword, '')
            else:
                for stopword in nltk_stopwords.words(self.language):
                    stopword_remover.add_keyword(stopword, '')
            self.stopword_remover = stopword_remover
        return

    def sent_tokenize(self, text):
        if self.preprocess_type == 'zemberek':
            sents = self.zmbrk.sent_tokenize(text)
        elif self.preprocess_type == 'nltk':
            sents = nltk_sent_tokenize(text, self.language)
        else:
            sents = gensim_sent_tokenize(text)
        sents_filtered = []
        for s in sents:
            if s[-1] != ':' and len(s) > self.length_limit:
                sents_filtered.append(s)
            # else:
            #   print("REMOVED!!!!" + s)
        return sents_filtered

    def preprocess_text_zemberek(self, text):
        sentences = self.sent_tokenize(text)
        sentences_cleaned = []
        for sent in sentences:
            if self.stopwords_remove:
                self.stopword_remover.replace_keywords(sent)
            words = self.zmbrk.word_tokenize(sent, self.language)
            words = [w for w in words if w not in string.punctuation]
            words = [w for w in words if w not in self.extra_stopwords]
            words = [w.lower() for w in words]
            sentences_cleaned.append(" ".join(words))
        return sentences_cleaned
    
    def preprocess_text_nltk(self, text):
        sentences = self.sent_tokenize(text)
        sentences_cleaned = []
        for sent in sentences:
            if self.stopwords_remove:
                self.stopword_remover.replace_keywords(sent)
            words = nltk_word_tokenize(sent, self.language)
            words = [w for w in words if w not in string.punctuation]
            words = [w for w in words if w not in self.extra_stopwords]
            words = [w.lower() for w in words]
            sentences_cleaned.append(" ".join(words))
        return sentences_cleaned

    def preprocess_text_regexp(self, text):
        sentences = self.sent_tokenize(text)
        sentences_cleaned = []
        for sent in sentences:
            sent_ascii = unidecode.unidecode(sent)
            cleaned_text = re.sub("[^a-zA-Z0-9]", " ", sent_ascii)
            if self.stopwords_remove:
                cleaned_text = self.stopword_remover.replace_keywords(cleaned_text)
            words = cleaned_text.lower().split()
            sentences_cleaned.append(" ".join(words))
        return sentences_cleaned

    def preprocess_text(self, text):
        if self.preprocess_type == 'zemberek':
            self.preprocess_text_zemberek(text)
        elif self.preprocess_type == 'nltk':
            return self.preprocess_text_nltk(text)
        else:
            return self.preprocess_text_regexp(text)

    def summarize(self, text, limit_type='word', limit=100):
        raise NotImplementedError("Abstract method")
