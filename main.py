from config import GET_FROM_WEB_AND_WRITE
from platforms_and_phrases import PlatformSearcher
from utilites import json_correct_doubles


def runner(platform_name):
    product_getter = PlatformSearcher(platform_name)
    product_getter.run()
    json_correct_doubles(product_getter.json_filename)


def get_links():
    # runner('sdvor')
    # runner('votonia')
    # runner('eltsnab')
    # runner('maxidom')
    # runner('dns')
    # runner('baucenter')
    # runner('akson')
    runner('etm')


if __name__ == '__main__':
    get_links()
