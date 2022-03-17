import time
from bs4 import BeautifulSoup
from config import browser_path, wait_time, selenium_arguments
from utilites import write_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

GET_FROM_WEB_AND_WRITE = False


class Searcher():
    def __init__(self, phrase):
        super().__init__()
        self.shop = None
        self.current_phrase = phrase
        self.browser = None
        self.current_url = None
        self.html_data = None
        self.soup = None
        self.page_pos = 1
        self.pag = None
        self.html_product = None
        self.result_filename = None
        self.blocklist = []

    def run(self):
        if self.current_phrase in self.blocklist:
            return
        if GET_FROM_WEB_AND_WRITE:
            options = webdriver.ChromeOptions()
            options.add_argument(selenium_arguments[0])
            options.add_argument(selenium_arguments[1])
            self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)
        self.get_first_page()
        self.get_other_pages()
        if self.browser:
            self.browser.close()

    def soup_page_getter(self):
        if GET_FROM_WEB_AND_WRITE:
            self.generate_url()
            self.browser.get(url=self.current_url)
            time.sleep(wait_time)
            self.html_data = self.browser.page_source
            self.write_page()
            self.soup = BeautifulSoup(self.html_data, 'lxml')
        else:
            self.read_page()

    def generate_url(self):
        pass

    def get_first_page(self):
        self.soup_page_getter()
        self.get_last_page_number()
        if not GET_FROM_WEB_AND_WRITE:
            self.get_goods_list()

    def get_other_pages(self):
        for self.page_pos in range(2, self.pag + 1):
            self.soup_page_getter()
            if not GET_FROM_WEB_AND_WRITE:
                self.get_goods_list()

    def write_page(self):
        filename = f'htmls/{self.shop}_{self.current_phrase}_{self.page_pos:03d}.html'
        write_html(self.html_data, filename)

    def read_page(self):
        filename = f'htmls/{self.shop}_{self.current_phrase}_{self.page_pos:03d}.html'
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
