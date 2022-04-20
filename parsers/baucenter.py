import datetime
from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items


class ParserBau(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'baucenter'
        self.result_filename = f'results/{self.shop}_{phrase}_{datetime.datetime.now().strftime("%d-%m-%Y")}.json'

    def generate_url(self):
        shop = 'https://baucenter.ru/'
        pagination = f'&PAGEN_1={self.page_pos}' if self.page_pos > 1 else ''
        self.current_url = f'{shop}search/?q={self.search_phrase}{pagination}'
        print('connect to', self.current_url)

    def get_last_page_number(self):
        try:
            self.pag = int(self.soup.find('nav', class_='pagination').find_all('a')[-2].text)
        except AttributeError:
            self.pag = 1

    def get_goods_list(self):
        catalog = self.soup.find('div', class_='catalog-list')
        self.goods_list = catalog.find_all('div', class_='catalog_item with-tooltip')

    def parse_product(self):
        product = Product()
        product.id = int(self.html_product['data-article'])
        product.name = self.html_product['data-name']
        link = self.html_product.find('a', attrs={'data-gtm-event': 'product_click'})['href']
        product.url = f"https://baucenter.ru{link}"
        try:
            stock = self.html_product.find('div', class_='stock-list').p.text
            product.status = ' '.join(stock.split())
        except AttributeError:
            product.status = 'Отсутствуют в продаже'
        try:
            product.price = float(self.html_product['data-price'])
        except AttributeError:
            product.price = 'Нет данных'
        product.trade_mark = self.html_product['data-brand']
        votes = self.html_product.find('div', class_='catalog_item_rating')
        if votes.text.strip():
            product.vote_qt = votes.text.strip()
            percent = int(votes.find('div', class_='raiting-votes')['style'].split(':')[1][:-2])
            product.vote_rating = (percent * 5) / 100
        self.cp = product
