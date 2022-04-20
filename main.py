from config import GET_FROM_WEB_AND_WRITE
from platforms_and_phrases import PlatformSearcher
from utilites import json_corrector


def runner(platform_name):
    product_getter = PlatformSearcher(platform_name)
    product_getter.run()


def get_links():
    # akson = PlatformSearcher('akson')
    # akson.run()
    # json_corrector(akson.json_filename)

    # etm = PlatformSearcher('etm')
    # etm.run()
    # json_corrector(etm.json_filename)

    # runner('sdvor')
    # runner('votonia')
    # runner('eltsnab')
    # runner('maxidom')
    runner('dns')
    # runner('baucenter')


if __name__ == '__main__':
    get_links()
