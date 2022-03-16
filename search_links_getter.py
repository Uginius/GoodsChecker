import time
import requests
from bs4 import BeautifulSoup
from config import search_phrases, headers
from parsers.outmode.search_maxidom import Maxidom
from parsers.outmode.url_functions import url_maxidom
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
        self.search_filename = None

    def run(self):
        for self.current_phrase in search_phrases:
            self.get_first_page()
            break
            if self.last_page:
                self.get_other_pages()

    def get_first_page(self):
        self.search_filename = f'htmls/{self.platform}_{self.current_phrase}_001.html'
        self.get_and_write_page_from_url()
        # self.read_and_parse_page()

    def read_html(self):
        with open(self.search_filename, 'r', encoding='utf8') as read_file:
            src = read_file.read()
        self.soup = BeautifulSoup(src, 'lxml')

    def get_other_pages(self):
        for i in range(2, self.last_page + 1):
            url = self.url_func(self.current_phrase, i)
            r = requests.get(url=url, headers=headers)
            self.search_filename = f'htmls/{self.platform}_{self.current_phrase}_{i:03d}.html'
            write_html(r.text, self.search_filename)
            time.sleep(3)
            self.read_and_parse_page()

    def read_and_parse_page(self):
        self.read_html()
        page_goods = self.parser(self.soup)
        if not self.last_page:
            page_goods.get_last_page()
            self.last_page = page_goods.last_page
        page_goods.get_goods()

    def get_and_write_page_from_url(self):
        link = self.url_func(self.current_phrase)
        print('connect to', link)
        r = requests.get(url=link, headers=headers)
        time.sleep(3)
        write_html(r.text, self.search_filename)
