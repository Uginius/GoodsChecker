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
        goods = html_goods.find_all('div', class_='product-matrix goods-list__matrix')  # ,attrs={'data-id': 'product'}
        for self.html_product in goods:
            self.parse_product()

    def check_brand(self):
        stop_words = ['Бетон', 'Планка', 'Профиль', 'Фотообои',  'Очаг', 'Разъем', 'Фоторамка', 'Портал']
        for word in stop_words:
            no_our_brand = word.upper() in self.cp.name.upper()
            # print(word.upper(), self.cp.name.upper(), no_our_brand)
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
            if button_text =='В корзину':
                self.cp.status = 'В наличии'
        except AttributeError:
            self.cp.status = 'Отсутствуют в продаже'
        try:
            price = self.html_product.find('div', class_='current-price').text.replace(' ', '').split('руб')[0]
            self.cp.price = price
        except AttributeError:
            self.cp.price = 'Продажи прекращены'
        write_json_items(f'{self.json_file}', self.cp.json_items())
