import time
import requests
from bs4 import BeautifulSoup
from config import search_phrases, headers
from parsers.search_maxidom import Maxidom
from parsers.url_functions import url_maxidom
from utilites import write_html


def select_parser(platform):
    match platform:
        case 'maxidom':
            return Maxidom, url_maxidom
        case _:
            print('not found platform in list')


class SearchLinksGetter:
    def __init__(self, platform):
        self.platform = platform
        self.current_phrase = None
        self.parser, self.url_func = select_parser(platform)
        self.soup = None
        self.last_page = None

    def run(self):
        for self.current_phrase in search_phrases:
            self.get_first_page()
            if self.last_page:
                self.get_other_pages()

    def get_first_page(self):
        filename = f'htmls/{self.platform}_{self.current_phrase}_001.html'
        link = self.url_func(self.current_phrase)
        print('connect to', link)
        r = requests.get(url=link, headers=headers)
        write_html(r.text, filename)
        self.read_html(filename)
        page_goods = self.parser(self.soup)
        page_goods.get_last_page()
        self.last_page = page_goods.last_page
        page_goods.get_goods()

    def read_html(self, filename):
        with open(filename, 'r', encoding='utf8') as read_file:
            src = read_file.read()
        self.soup = BeautifulSoup(src, 'lxml')

    def get_other_pages(self):
        for i in range(2, self.last_page + 1):
            url = self.url_func(self.current_phrase, i)
            print('connect to', url)
            r = requests.get(url=url, headers=headers)
            filename = f'htmls/{self.platform}_{self.current_phrase}_{i:03d}.html'
            write_html(r.text, filename)
            time.sleep(3)

            self.read_html(filename)
            page_goods = self.parser(self.soup)
            page_goods.get_goods()
