import requests
from bs4 import BeautifulSoup
import re

from src.chapters import ChapterRequester

class Page(object):
    def __init__(self, status, updated, genres, chapters, rating, title, latest_chapters, authors, description):
        self.status = status
        self.updated = updated
        self.genres = genres
        self.chapters = chapters
        self.rating = rating
        self.title = title
        self.latest_chapters = latest_chapters
        self.authors = authors
        self.description = description

        
class HomePageRequester(ChapterRequester):

    def __init__(self, query='Battle Through The Heavens'):
        self.query = query
        super().__init__(self)

    def construct_search(self):
        self.search_term = str(self.query).lower().replace(
            " ", "-")

        return self

    def retrieve_contents(self):

        title = self.soup.select(
            ".detail .name")[0].getText().replace('\n', " ").strip()

        rating = str(self.soup.select(
            ".rating")[0].getText()).strip().replace('\n', "")

        content_items = self.soup.select(
            ".detail .meta p")

        description = self.soup.select(
            "#info p.content")[0].getText().strip()

        

        latest_chapters_container = self.soup.select(
            ".latest-chapters a")

        latest_chapters = {}
        for chat in latest_chapters_container:

            latest_chapters[chat.getText().strip()] = self.site + chat['href'][1:]

        authors = {}
        status, updated, genres, chapters = None, None, {}, None
        for elem in content_items:
            #print(elem)
            if "author" in str(elem.getText()).lower():
                authors_container = elem.select('a')
                for author_item in authors_container:
                    
                    authors[author_item.find('span').getText()] = author_item['href']

            if "genre" in str(elem.getText()).lower():
                genres_container = elem.select('a')
                for genre_item in genres_container:
                    genres[genre_item.getText().replace(
                        ",", "").strip()] = self.site + genre_item['href'][1:]

            if "update" in str(elem.getText()).lower():
                updated = elem.find('span').getText()

            if "status" in str(elem.getText()).lower():
         
                status = elem.select('a')[0].find('span').getText()

            if "chapter" in str(elem.getText()).lower():
                chapters = elem.find('span').getText()


        
        self.homepage = Page(status, updated, genres, chapters, rating, title, latest_chapters, authors, description)
        #print(self.homepage.status, self.homepage.updated)

        return self
