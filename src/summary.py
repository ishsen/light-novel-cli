import requests
from bs4 import BeautifulSoup
import re



from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from multiprocessing.dummy import Pool as Threadpool
from itertools import chain

from src.chapters import ChapterRequester





class SummaryGenerator:
    def __init__(self, site="https://novelkiss.com/", number=2914, title="Dragon-Marked War God", go_back=3, summary_type="LSA"):
        self.site = site
        self.number = number
        self.title = title
        self.go_back = go_back
        self.summary_type = summary_type
        self.LANGUAGE = "english"
        self.SENTENCES_COUNT = 5
        #self.collect_text()
        self.NUM_THREADS = 4
        self.multithreaded_collect()
        self.collect_summary()

    def collect_text(self):
        count = 0
        self.collected_text = []

        while count < self.go_back:
            c = ChapterRequester(
                number=(self.number - count), site=self.site, title=self.title)

            self.collected_text.append(c.chapter.text_content)
            count += 1

        self.collected_text = " ".join(self.collected_text)

        return self

    def multithreaded_collect(self):
        print('Processing with threads...')

        self.num_list = list(range(self.number - self.go_back,self.number))
       
        def read_data(num):
            c = ChapterRequester(
            number=num, site=self.site, title=self.title)

            self.collected_text.append(c.chapter.text_content)

        threadpool = Threadpool(processes = self.NUM_THREADS)
        self.collected_text = []

        results = threadpool.map(read_data, self.num_list)

        #print(self.collected_text)

        self.collected_text = " ".join(self.collected_text)

        return self






     


    def collect_summary(self):

        if self.summary_type == "LSA":
            #print("Retrieving a lsa summary")
            self.lsa_summarize()

        elif self.summary_type == "GENERAL":
            print("Retrieving a general summary")
            #t = TextCleaner(self.collected_text)
            #doc, word_freq = t.doc, t.word_freq

            #self.general_summarize(doc, word_freq)

    def lsa_summarize(self):

        parser = PlaintextParser.from_string(
            self.collected_text, Tokenizer(self.LANGUAGE))
        stemmer = Stemmer(self.LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(self.LANGUAGE)

        self.sentences = []
        for sentence in summarizer(parser.document, self.SENTENCES_COUNT):
            #print(sentence)
            self.sentences.append(str(sentence))

        self.summary = " ".join(self.sentences)
        #print(self.summary)

        return self

        """     def general_summarize(self, doc, word_freq):
        sent_score = {}
        sent_tokens = [sent for sent in doc.sents]

        for sent in sent_tokens:
            for word in sent:
                if word.text.lower() in word_freq.keys():
                    if sent not in sent_score.keys():
                        sent_score[sent] = word_freq[word.text.lower()]
                    else:
                        sent_score[sent] += word_freq[word.text.lower()]

        largest_summary = nlargest(
            n=7, iterable=sent_score, key=sent_score.get)
        final_summary = [word.text for word in largest_summary]
        self.summary = " ".join(final_summary)
        print(self.summary)

        return self """