import logging
from parsers.outmode.search_parsers import PlatformParser
from product import Product
from utilites import write_json_items


class Maxidom(PlatformParser):

    def __init__(self, soup):
        super().__init__(soup)
        self.platform = 'maxidom'

    def get_last_page(self):
        try:
            li = self.soup.find('div', class_='pager-catalogue__search').find_all('li')
            self.last_page = int(li[-2].text.strip())
        except Exception as ex:
            self.last_page = None
            logging.info('Not pagination pages', ex)

    def get_goods(self):
        try:
            articles = self.soup.find('div', class_='item-list-inner').find_all('article')
            for self.html_cp in articles:
                self.get_data_from_html_article()
        except Exception as ex:
            logging.warning('Not found goods', ex)

    def get_data_from_html_article(self):
        cp = self.html_cp
        product = Product()
        split_id = cp.find('small').text.split()[1].replace('.', '')
        if '/' in split_id:
            split_id = split_id.split('/')[0]
        product.id = int(split_id)
        link = cp.find(attrs={'itemprop': 'name'})
        product.name = link.text
        product.url = 'https://www.maxidom.ru' + link['href']
        product.status = cp.find('div', class_='item-controls').span.text.strip()
        product.price = int(cp.find('span', class_='price-list').text.split(',-')[0].strip().replace(' ', ''))
        write_json_items('results/maxidom.json', product.json_items())


