import sys

GET_FROM_WEB_AND_WRITE = False

wait_time = 3
shops = {'maxidom': 'https://www.maxidom.ru/',
         'dns': 'https://www.dns-shop.ru/',
         'baucenter': 'https://baucenter.ru/',
         'akson': 'https://akson.ru/',
         'etm': 'https://www.etm.ru/',
         'sdvor': 'https://www.sdvor.com/moscow',
         'eltsnab': 'https://eltsnab.ru/',
         'toledo24': 'https://www.toledo24.pro/',
         'votonia': 'https://www.votonia.ru/'}

search_phrases = [
    'фотон',
    'контакт',
    'рекорд',
    'safeline'
]

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
selenium_arguments = [
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    '--disable-blink-features=AutomationControlled'
]

chromedriver_mac_path = 'drivers/chromedriver'
chromedriver_linux_path = 'drivers/chromedriver_linux64_99.0.4844.51/chromedriver'
match sys.platform:
    case 'linux':
        browser_path = chromedriver_linux_path
    case 'darwin':
        browser_path = chromedriver_mac_path
    case 'win32':
        browser_path = 'drivers/chromedriver_win32/chromedriver.exe'
    case _:
        print("ERROR: can't found selenium driver")
