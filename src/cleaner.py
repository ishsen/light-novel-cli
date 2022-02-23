import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


class TextCleaner:
    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")
        self.get_frequencies()
        self.normalize_frequencies()

    def get_frequencies(self):

        self.text = self.text.replace("x91", "'")
        self.text = self.text.replace("x92", "'")

        self.doc = self.nlp(self.text)
        self.tokens = [token.text for token in self.doc]

        self.word_freq = {}
        stop_words = list(STOP_WORDS)
        for word in self.doc:
            if word.text.lower() not in stop_words:
                if word.text.lower() not in punctuation:
                    if word.text not in self.word_freq.keys():
                        self.word_freq[word.text] = 1
                    else:
                        self.word_freq[word.text] += 1
        return self

    def normalize_frequencies(self):
        x = (self.word_freq.values())
        a = list(x)
        a.sort()
        max_freq = a[-1]

        for word in self.word_freq.keys():
            self.word_freq[word] = self.word_freq[word]/max_freq

        return self