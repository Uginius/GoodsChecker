import datetime

from parsers.platform_finder import Searcher


class ParserEtm(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'etm'
        self.result_filename = f'results/{self.shop}_{phrase}_{datetime.datetime.now().strftime("%d-%m-%Y")}.json'
        self.blocklist = ['контакт', 'safeline']

    def generate_url(self):
        self.current_url = f'https://www.etm.ru/catalog?searchValue={self.search_phrase}&page={self.page_pos}&rows=12'
        print('connect to', self.current_url)

    def get_last_page_number(self):
        try:
            pag_block = self.soup.find('ul', class_='pagination-widget__pages')
            self.pag = int(pag_block.find_all('li')[-1]['data-page-number'])
        except AttributeError:
            self.pag = 1