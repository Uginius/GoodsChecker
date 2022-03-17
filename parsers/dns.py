import datetime
from bs4 import BeautifulSoup
from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items, write_html


class ParserDns(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'dns'
        self.result_filename = f'results/{self.shop}_{phrase}_{datetime.datetime.now().strftime("%d-%m-%Y")}.json'
        self.blocklist = ['контакт', 'safeline']

    def generate_url(self):
        self.current_url = f'https://www.dns-shop.ru/search/?q={self.current_phrase}&p={self.page_pos}'
        print('connect to', self.current_url)

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
            product.status = self.html_product.find('div', class_='order-avail-wrap').text.strip()
        except AttributeError:
            product.status = 'Отсутствуют в продаже'
        try:
            product.price = int(self.html_product.find('div', class_='product-buy__price').text.split()[0])
        except AttributeError:
            product.price = 'Продажи прекращены'
        write_json_items(f'{self.result_filename}', product.json_items())
