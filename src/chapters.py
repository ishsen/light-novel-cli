import requests
from bs4 import BeautifulSoup
import re
import click


class Chapter(object):
    def __init__(self, text_content, author, title, nxt, prv):

        self.text_content = text_content
        self.author = author
        self.title = title
        self.nxt = nxt
        self.prv = prv

class ChapterRequester:
    def __init__(self, title="Dragon-Marked War God", number=2914, site="https://novelkiss.com/"):
        self.title = title
        self.number = number
        self.site = site
        self.construct_search()
        self.request_page()
        self.retrieve_contents()

    def construct_search(self):
        self.search_term = str(self.title).strip().lower().replace(
            " ", "-") + "/chapter-" + str(self.number)

        #print(self.search_term)


        return self

    def request_page(self):
        self.page = requests.get(self.site + self.search_term)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

        return self

    def retrieve_contents(self):
        def retrieve_buttons(bs_soup):

            nxt = self.site + bs_soup.select(
                "#btn-next")[0]['href'][1:] if bs_soup.select("#btn-next") else None
            prv = self.site + bs_soup.select(
                "#btn-prev")[0]['href'][1:] if bs_soup.select("#btn-prev") else None

            return (nxt, prv)

        def retreive_text(bs_soup):

            text_wrapper = bs_soup.select(".content-inner > p")
            title_wrapper = bs_soup.select(".content-inner > h3")

            title = str(title_wrapper[0].getText()
                        ).strip() if title_wrapper else ""

            author = str(text_wrapper.pop(0).getText()).strip()

            text_content = " ".join([str(elem.getText()).strip()
                                    for elem in text_wrapper])

            return (author, text_content, title)

        nxt, prv = retrieve_buttons(self.soup)
        author, text_content, title = retreive_text(self.soup)
        #print(text_content, author, title, nxt,prv)
        #t = TextConverter(text= text_content, title = title, author = author)
        self.chapter = Chapter(text_content, author, title, nxt, prv)
        



        return self

