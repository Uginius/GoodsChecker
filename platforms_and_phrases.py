from config import search_phrases
from platform_selector import select_platform
from utilites import time_track


class PlatformSearcher:
    def __init__(self, shop):
        self.parser = select_platform(shop)
        self.json_filename = None

    @time_track
    def run(self):
        for current_phrase in search_phrases:
            parser = self.parser(current_phrase)
            parser.run()
            self.json_filename = parser.json_file
