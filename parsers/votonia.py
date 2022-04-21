import time

from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items


class ParserVotonia(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'votonia'
        self.blocklist = ['контакт', 'рекорд', 'safeline']

    def generate_url(self):
        self.current_url = f'https://www.votonia.ru/search/{self.search_phrase}/'
        print('connect to', self.current_url)

    def scroll_down(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        while True:
            try:
                self.browser.find_element_by_css_selector('.pager-info-block').click()
            except Exception as ex:
                print(ex)
            time.sleep(1)
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            if new_height == last_height:
                break
            last_height = new_height

    def get_goods_list(self):
        self.goods_list = self.soup.find_all('div', class_='wfloat cat_product_box is-product')
        # ,attrs={'data-id': 'product'}

    def parse_product(self):
        product = self.html_product
        self.cp = Product()
        self.cp.id = product['data-id']
        self.search_index_number += 1
        self.cp.index = self.search_index_number
        link = product.find('a', class_='product_link')
        self.cp.name = link.text.strip()
        self.cp.url = 'https://www.votonia.ru' + link['href']
        self.cp.price = float(product['data-market'])
        self.cp.trade_mark = 'Фотон'
        self.cp.status = product.find('div', class_='reach_line reach1').text.strip()
