from config import trade_platforms, search_phrases, browser_path
from parsers.parsers import MaxidomLinksGetter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class SearchLinksGetter:
    def __init__(self, platform):
        self.platform = platform
        self.url = trade_platforms[self.platform]
        self.current_phrase = None
        self.browser = None

    def run(self):
        driver = webdriver.Chrome(service=Service(executable_path=browser_path))
        for self.current_phrase in search_phrases:
            parser = MaxidomLinksGetter(self.current_phrase, driver)
            parser.run()
            break
        driver.close()
