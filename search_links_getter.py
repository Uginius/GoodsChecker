from config import trade_platforms, search_phrases
from parsers.parsers import MaxidomLinksGetter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SearchLinksGetter:
    def __init__(self, platform):
        self.platform = platform
        self.url = trade_platforms[self.platform]
        self.current_phrase = None
        self.browser = None

    def run(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        for self.current_phrase in search_phrases:
            parser = MaxidomLinksGetter(self.current_phrase, driver)
            parser.run()
            break
        driver.close()
