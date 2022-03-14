import time
import requests
from bs4 import BeautifulSoup
from config import trade_platforms, headers
from product import Product
from utilites import select_parser


class LinksGetter:
    def __init__(self, phrase, platform):
        self.platform = platform
        self.parser = select_parser(platform)
        self.search_url = trade_platforms[platform] + f'search/catalog/?q={phrase}&category_search=0&amount=12'
        self.soup = None
        self.last_page = None

    def run(self):
        self.get_first_page()
        self.get_other_pages()

    def get_first_page(self):
        # r = requests.get(url=self.search_url, headers=headers)
        # with open('maxi.html', 'w', encoding='utf8') as write_file:
        #     write_file.write(r.text)
        # self.soup = (r.text, 'lxml')
        self.read_html()
        page_goods = self.parser(self.soup)
        page_goods.get_last_page()
        self.last_page = page_goods.last_page
        page_goods.get_goods()

    def read_html(self):
        with open('maxi.html', 'r', encoding='utf8') as read_file:
            src = read_file.read()
        self.soup = BeautifulSoup(src, 'lxml')

    def get_other_pages(self):
        pass
