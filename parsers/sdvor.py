from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items


class ParserSdvor(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'sdvor'
        self.blocklist = ['контакт', 'рекорд']

    def generate_url(self):
        self.current_url = f'https://www.sdvor.com/moscow/search/{self.search_phrase}'
        print('connect to', self.current_url)

    def get_last_page_number(self):
        self.pag = None

    def get_goods_list(self):
        self.goods_list = self.soup.find_all('sd-product-grid-item', class_='product-grid-item')

    def parse_product(self):
        self.search_index_number += 1
        self.cp = Product()
        self.cp.index = self.search_index_number
        self.cp.id = int(self.html_product.find('span', class_='code-value').text)
        link = self.html_product.find('a', class_='product-name')
        name = link.text.strip().split()
        self.cp.name = ' '.join(name)
        self.cp.url = 'https://www.sdvor.com' + link['href']
        try:
            price = self.html_product.find('div', class_='price').text.strip().split()[:-1]
            self.cp.price = float(''.join(price))
        except AttributeError:
            self.cp.price = None
        if 'Фотон'.upper() in self.cp.name.upper():
            self.cp.trade_mark = 'ФОТОН'
        elif 'Изолента'.upper() in self.cp.name.upper():
            self.cp.trade_mark = 'SafeLine'
        try:
            status = self.html_product.find('span', class_='shops-text check-availability').text
            if status == 'Проверить наличие':
                self.cp.status = 'Есть в наличии'
            else:
                self.cp.status = 'Нет данных'
        except Exception as ex:
            self.cp.status = 'Нет в наличии'
