from parsers.platform_finder import Searcher


class ParserEltsnab(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
        self.shop = 'eltsnab'

    def generate_url(self):
        self.current_url = f'https://eltsnab.ru/catalogue?q={self.search_phrase}'
        print('connect to', self.current_url)

