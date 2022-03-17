from parsers.platform_finder import Searcher


class ParserSdvor(Searcher):
    def __init__(self, phrase):
        super().__init__(phrase)
