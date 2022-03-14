from product import Product


class PlatformParser:
    def __init__(self, soup):
        self.soup = soup
        self.last_page = None
        self.html_cp = None

    def run(self):
        pass

    def get_last_page(self):
        pass

    def get_goods(self):
        pass


class Maxidom(PlatformParser):

    def get_last_page(self):
        li = self.soup.find('div', class_='pager-catalogue__search').find_all('li')
        self.last_page = int(li[-2].text.strip())

    def get_goods(self):
        articles = self.soup.find('div', class_='item-list-inner').find_all('article')
        for self.html_cp in articles:
            self.get_data_from_html_article()

    def get_data_from_html_article(self):
        cp = self.html_cp
        product = Product()
        product.id = int(cp.find('small').text.split()[1])
        link = cp.find(attrs={"itemprop": "name"})
        product.name = link.text
        product.url = 'https://www.maxidom.ru/' + link['href']
        product.status = cp.find('div', class_='item-controls').span.text.strip()
        product.price = int(cp.find('span', class_='price-list').text.split(',-')[0].strip().replace(' ', ''))
        print(product.out_items())
