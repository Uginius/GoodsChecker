from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items


class ParserEtm(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'etm'
        self.blocklist = ['контакт']

    def generate_url(self):
        self.current_url = f'https://www.etm.ru/catalog?searchValue={self.search_phrase}&page={self.page_pos}&rows=12'
        print('connect to', self.current_url)

    def get_last_page_number(self):
        self.pag = int(self.soup.find('div', class_='MuiBox-root').find_all('span')[0].text.split()[1])

    def get_goods_list(self):
        goods = self.soup.find('div', class_='MuiPaper-rounded').div.find_all('div', recursive=False)
        for self.html_product in goods:
            self.parse_product()

    def parse_product(self):
        self.cp = Product()
        links = self.html_product.find_all('a')
        brand_list = ['ФОТОН', 'SafeLine', 'К2']
        brand = links[-1].text
        if brand not in brand_list:
            return
        self.cp.trade_mark = brand
        self.cp.id = links[-1].parent.parent.parent.p.text
        self.cp.name = links[-2].text.replace("'", "")
        self.cp.url = 'https://www.etm.ru' + links[-2]['href']
        try:
            buy = self.html_product.find('div', text='Покупка от').parent.find_all('p')
            self.cp.status = ' '.join([buy[0].text, buy[1].text])
        except AttributeError:
            self.cp.status = 'Отсутствуют в продаже'
        try:
            price = self.html_product.find('div', text='Розничная цена').parent.parent.find_all('div')[-1].text
            self.cp.price = float(price.replace(',', ''))
        except Exception as ex:
            self.cp.price = f'Цена отсутствует {ex}'
        write_json_items(f'{self.json_file}', self.cp.json_items())
