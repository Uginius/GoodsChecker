from config import trade_platforms, search_phrases, browser_path
from parsers.parsers import LinksGetter


class SearchLinksGetter:
    def __init__(self, platform):
        self.platform = platform
        self.url = trade_platforms[self.platform]
        self.current_phrase = None
        self.browser = None

    def run(self):
        for self.current_phrase in search_phrases:
            parser = LinksGetter(self.current_phrase, self.platform)
            parser.run()
            break
