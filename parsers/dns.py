import datetime
from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items


class ParserDns(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'dns'
        self.result_filename = f'results/{self.shop}_{phrase}_{datetime.datetime.now().strftime("%d-%m-%Y")}.json'
        self.blocklist = ['контакт', 'safeline', 'рекорд']

    def generate_url(self):
        self.current_url = f'https://www.dns-shop.ru/search/?q={self.search_phrase}&p={self.page_pos}'
        print('connect to', self.current_url)

    def get_last_page_number(self):
        try:
            pag_block = self.soup.find('ul', class_='pagination-widget__pages')
            self.pag = int(pag_block.find_all('li')[-1]['data-page-number'])
        except AttributeError:
            self.pag = 1

    def get_goods_list(self):
        try:
            self.goods_list = self.soup.find_all('div', attrs={'data-id': 'product'})
        except AttributeError:
            self.goods_list = None

    def parse_product(self):
        product = Product()
        product.id = int(self.html_product['data-code'])
        product.name = self.html_product.find('span').text
        product.url = f"https://www.dns-shop.ru{self.html_product.find('a')['href']}"
        try:
            product.status = self.html_product.find('div', class_='order-avail-wrap').text.strip()
        except AttributeError:
            product.status = 'Отсутствуют в продаже'
        try:
            product.price = int(self.html_product.find('div', class_='product-buy__price').text.split()[0])
        except AttributeError:
            product.price = 'Продажи прекращены'
        if 'ФОТОН' in product.name.upper():
            product.trade_mark = 'ФОТОН'
        votes = self.html_product.find('a', class_='catalog-product__rating ui-link ui-link_black')
        product.vote_rating = votes['data-rating']
        product.vote_qt = votes.text.strip()
        self.cp = product
