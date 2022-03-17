import time
from bs4 import BeautifulSoup
from config import browser_path, wait_time
from parsers.platform_finder import Searcher
from product import Product
from utilites import write_html, write_json_items
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

GET_FROM_WEB_AND_WRITE = False


class ParserDns(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.platform = 'dns'
        self.current_phrase = phrase
        self.browser = None
        self.html_data = None
        self.soup = None
        self.page_pos = 1
        self.blocklist = ['контакт', 'safeline']
        self.pag = None
        self.html_product = None

    def run(self):
        if self.current_phrase in self.blocklist:
            return
        if GET_FROM_WEB_AND_WRITE:
            self.browser = webdriver.Chrome(service=Service(executable_path=browser_path))
        self.get_first_page()
        self.get_other_pages()
        if self.browser:
            self.browser.close()

    def soup_page_getter(self):
        if GET_FROM_WEB_AND_WRITE:
            url = f'https://www.dns-shop.ru/search/?q={self.current_phrase}&p={self.page_pos}'
            print('connect to', url)
            self.browser.get(url=url)
            time.sleep(wait_time)
            self.html_data = self.browser.page_source
            self.write_page()
            self.soup = BeautifulSoup(self.html_data, 'lxml')
        else:
            self.read_page()

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
        filename = f'htmls/dns_{self.current_phrase}_{self.page_pos:03d}.html'
        write_html(self.html_data, filename)

    def read_page(self):
        filename = f'htmls/dns_{self.current_phrase}_{self.page_pos:03d}.html'
        print('opening', filename)
        with open(filename, 'r', encoding='utf8') as read_file:
            src = read_file.read()
        self.soup = BeautifulSoup(src, 'lxml')

    def get_last_page_number(self):
        self.pag = int(self.soup.find('ul', class_='pagination-widget__pages').find_all('li')[-1]['data-page-number'])

    def get_goods_list(self):
        goods = self.soup.find_all('div', attrs={'data-id': 'product'})
        for self.html_product in goods:
            self.parse_product()

    def parse_product(self):
        product = Product()
        product.id = int(self.html_product['data-code'])
        product.name = self.html_product.find('span').text
        product.url = f"https://www.dns-shop.ru{self.html_product.find('a')['href']}"
        print(product.url)
        try:
            product.status = self.html_product.find('div', class_='order-avail-wrap').text
        except AttributeError:
            product.status = 'Отсутствуют в продаже'
        try:
            product.price = int(self.html_product.find('div', class_='product-buy__price').text.split()[0])
        except AttributeError:
            product.price = 'Продажи прекращены'
        write_json_items('results/dns.json', product.json_items())
