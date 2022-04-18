import urllib.parse
from parsers.platform_finder import Searcher
from product import Product


class ParserMaxidom(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'maxidom'

    def generate_url(self):
        query = urllib.parse.quote_plus(self.search_phrase)
        link = f'https://www.maxidom.ru/search/catalog/?q={query}&category_search=0&amount=12'
        self.current_url = link
        if self.page_pos > 1:
            self.current_url = link + f'&PAGEN_2={self.page_pos}'
        print('connect to', self.current_url)

    def get_last_page_number(self):
        try:
            li = self.soup.find('div', class_='pager-catalogue__search').find_all('li')
            self.pag = int(li[-2].text.strip())
        except Exception as ex:
            self.pag = None
            print(ex)

    def get_goods_list(self):
        try:
            self.goods_list = self.soup.find('div', class_='item-list-inner').find_all('article')
        except Exception as ex:
            self.goods_list = None
            print(ex)

    def parse_product(self):
        self.cp = Product()
        art_block = self.html_product.find_all('small', class_="sku")
        split_id = art_block[0].text.split()[1].replace('.', '')
        if '/' in split_id:
            split_id = split_id.split('/')[0]
        try:
            self.cp.id = int(split_id)
        except ValueError:
            self.cp.id = None
        self.cp.trade_mark = art_block[2].text.split(':')[1].strip()
        link = self.html_product.find(attrs={'itemprop': 'name'})
        self.cp.name = link.text
        self.cp.url = 'https://www.maxidom.ru' + link['href']
        self.cp.status = self.html_product.find('div', class_='item-controls').span.text.strip()
        self.cp.price = int(
            self.html_product.find('span', class_='price-list').text.split(',-')[0].strip().replace(' ', ''))
        print(self.cp.json_items())
