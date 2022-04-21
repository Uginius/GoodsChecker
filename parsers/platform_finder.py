import datetime
import os
import time

from bs4 import BeautifulSoup
from config import browser_path, wait_time, selenium_arguments, GET_FROM_WEB_AND_WRITE
from utilites import write_html, write_json_items
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Searcher:
    def __init__(self, phrase):
        super().__init__()
        self.shop = None
        self.search_phrase = phrase
        self.browser = None
        self.current_url = None
        self.html_data = None
        self.soup = None
        self.page_pos = 1
        self.goods_list = None
        self.pag = None
        self.html_product = None
        self.json_file = None
        self.blocklist = []
        self.brand_list = ['ФОТОН', 'КОНТАКТ', 'РЕКОРД', 'SAFELINE']
        self.html_dir = None
        self.cp = None
        self.search_index_number = 0

    def run(self):
        self.set_json_filename()
        self.check_htmls_dir()
        self.initiate_browser()
        self.get_first_page()
        if self.pag:
            self.get_other_pages()
        if self.browser:
            self.browser.close()
        self.footer()

    def initiate_browser(self):
        if GET_FROM_WEB_AND_WRITE:
            options = webdriver.ChromeOptions()
            options.add_argument(selenium_arguments[0])
            options.add_argument(selenium_arguments[1])
            self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)

    def soup_page_getter(self):
        if GET_FROM_WEB_AND_WRITE:
            self.generate_url()
            try:
                self.browser.get(url=self.current_url)
            except Exception as ex:
                pass
            self.scroll_down()
            time.sleep(wait_time)
            self.html_data = self.browser.page_source
            self.write_page()
            self.soup = BeautifulSoup(self.html_data, 'lxml')
        else:
            self.read_page()

    def scroll_down(self):
        pass

    def generate_url(self):
        pass

    def get_first_page(self):
        self.soup_page_getter()
        try:
            self.get_last_page_number()
        except IndexError:
            self.pag = None
        self.get_and_parse_goods_list()

    def get_other_pages(self):
        for self.page_pos in range(2, self.pag + 1):
            self.soup_page_getter()
            self.get_and_parse_goods_list()

    def get_and_parse_goods_list(self):
        if not GET_FROM_WEB_AND_WRITE:
            self.get_goods_list()
            if not self.goods_list:
                return
            for self.html_product in self.goods_list:
                self.parse_product()
                if self.cp.url:
                    write_json_items(self.json_file, self.cp.json_items())

    def check_htmls_dir(self):
        self.html_dir = f'htmls/{self.shop}'
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)

    def write_page(self):
        write_html(self.html_data, f'{self.html_dir}/{self.shop}_{self.search_phrase}_{self.page_pos:03d}.html')

    def clear_result_filename(self):
        with open(self.json_file, 'w', encoding='utf8'):
            pass

    def read_page(self):
        filename = f'{self.html_dir}/{self.shop}_{self.search_phrase}_{self.page_pos:03d}.html'
        print('opening', filename)
        with open(filename, 'r', encoding='utf8') as read_file:
            src = read_file.read()
        self.soup = BeautifulSoup(src, 'lxml')

    def get_last_page_number(self):
        pass

    def get_goods_list(self):
        pass

    def parse_product(self):
        pass

    def set_json_filename(self):
        self.json_file = f'results/{self.shop}_{datetime.datetime.now().strftime("%d-%m-%Y")}.json'

    def footer(self):
        pass
