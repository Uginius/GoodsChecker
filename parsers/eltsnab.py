from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items


class ParserEltsnab(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'eltsnab'

    def generate_url(self):
        search_page = f'&p={self.page_pos}' if self.pag else ''
        self.current_url = f'https://eltsnab.ru/catalogue?filter_proizv={self.search_phrase.upper()}{search_page}'
        print('connect to', self.current_url)

    def get_last_page_number(self):
        self.pag = int(self.soup.find('div', class_='pagination').find_all('li')[-1].text)

    def get_goods_list(self):
        try:
            self.goods_list = self.soup.find('div', class_='table-content').find_all('tr')
        except AttributeError:
            self.goods_list = None

    def parse_product(self):
        self.cp = Product()
        link = self.html_product.find('h3').a
        self.cp.name = link['title']
        self.cp.url = 'https://eltsnab.ru' + link['href'][2:]
        self.set_price_and_status()
        self.cp.id = self.html_product.find('span', class_='data').text.split(': ')[1]
        self.check_brand()

    def set_price_and_status(self):
        try:
            self.cp.price = float(self.html_product.find('td', class_='price').find('div', class_='new').text)
        except ValueError:
            self.cp.price = None
        try:
            div_status = self.html_product.find('div', class_='main-product-item-qty-block')
            self.cp.status = div_status.find('div', class_='qty').text.split('-')[0]
        except AttributeError:
            self.cp.status = 'НЕТ В НАЛИЧИИ'

    def check_brand(self):
        name = self.cp.name.upper()
        brandlist = ['ФОТОН', 'РЕКОРД', 'КОНТАКТ', 'SafeLine']
        for brand in brandlist:
            if brand.upper() in name:
                self.cp.trade_mark = brand
                break
        if not self.cp.trade_mark:
            self.cp.trade_mark = ''
