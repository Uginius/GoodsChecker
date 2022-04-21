import time
from parsers.platform_finder import Searcher
from product import Product
from utilites import write_json_items


class ParserAkson(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'akson'
        self.blocklist = ['рекорд']

    def generate_url(self):
        self.current_url = f'https://akson.ru/search/?q={self.search_phrase}'
        print('connect to', self.current_url)

    def scroll_down(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(1)
        for i in range(1, 5):
            self.browser.execute_script(f"window.scrollTo(0, {last_height - 500 * i});")
            time.sleep(1)
        while True:
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            if new_height == last_height:
                break
            last_height = new_height

    def get_goods_list(self):
        html_goods = self.soup.find('div', class_='goods-list__content')
        self.goods_list = html_goods.find_all('div', class_='product-matrix goods-list__matrix')
        # ,attrs={'data-id': 'product'}

    def check_brand(self):
        name = self.cp.name.upper()
        brandlist = ['ФОТОН', 'РЕКОРД', 'КОНТАКТ', 'SafeLine']
        for brand in brandlist:
            if brand.upper() in name:
                self.cp.trade_mark = brand
                break
        stop_words = ['Бетон', 'Планка', 'Профиль', 'Фотообои', 'Очаг', 'Разъем', 'Фоторамка', 'Портал']
        for word in stop_words:
            no_our_brand = word.upper() in name
            if no_our_brand:
                return True
        return False

    def parse_product(self):
        self.cp = Product()
        self.cp.name = self.html_product.find('div', class_='product-info__title').text
        if self.check_brand():
            self.cp.__init__()
            return
        self.cp.id = int(self.html_product.find('div', class_='product-info__code').text.split()[1])
        self.cp.url = f"https://akson.ru{self.html_product.find('a')['href']}"
        try:
            button_text = self.html_product.find('button').text
            if button_text == 'В корзину':
                self.cp.status = 'В наличии'
        except AttributeError:
            self.cp.status = 'Отсутствуют в продаже'
        try:
            price = self.html_product.find('div', class_='current-price').text.replace(' ', '').split('руб')[0]
            self.cp.price = price
        except AttributeError:
            self.cp.price = 'Продажи прекращены'
        rate = self.html_product.find('span', class_='rating')
        stars = rate.find('span', class_='stars__block stars__block_fill')['style']
        percent = int(stars.split(':')[1][:-2])
        self.cp.vote_rating = (percent * 5) / 100
        self.cp.vote_qt = rate.text.split('(')[1].split(')')[0]

