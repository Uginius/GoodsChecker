import time
import requests
from bs4 import BeautifulSoup
from config import trade_platforms, search_phrases, headers


class MaxidomLinksGetter:
    def __init__(self, phrase, driver):
        self.platform = 'maxidom'
        self.search_url = trade_platforms[self.platform] + f'search/catalog/?q={phrase}&category_search=0&amount=12'
        self.browser = driver
        self.soup = None

    def run(self):
        self.get_first_page()

    def get_first_page(self):
        try:
            r = requests.get(url=self.search_url, headers=headers)
            time.sleep(6)
            self.soup = BeautifulSoup(r.text, 'lxml')
        except Exception as ex:
            print(ex)
        print(self.soup)
        time.sleep(6)

