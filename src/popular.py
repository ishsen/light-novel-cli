import requests
from bs4 import BeautifulSoup
import re

from src.chapters import ChapterRequester


class Book(object):
    def __init__(self, title, link, description, views, rating):

        self.title = title
        self.link = link
        self.description = description
        self.views = views
        self.rating = rating

class PopularRequester(ChapterRequester):

    def __init__(self,  amount, query='popular'):
        self.query = query
        self.amount = amount
        super().__init__(self)

    def construct_search(self):
        self.search_term = str(self.query)

        return self

    def retrieve_contents(self):
        books_wrapper = self.soup.select(".list > .book-item")

        self.books = []
        for book_item in books_wrapper:

            #print(book_item)
            title = book_item.select(
                ".book-detailed-item .title a")[0].getText()
            link = self.site + \
                book_item.select(".book-detailed-item .title a")[0]['href'][1:]
            rating = book_item.select(
                ".book-detailed-item .rating")[0].getText()
            views = book_item.select(
                ".book-detailed-item .views span")[0].getText()
            description = book_item.select(
                ".book-detailed-item .summary")[0].getText() + '...'

            self.books.append(Book(title, link, description, views, rating))

        self.books = self.books[:self.amount]

        print(self.books)

        return self