from config import GET_FROM_WEB_AND_WRITE
from platforms_and_phrases import PlatformSearcher
from utilites import json_corrector


def runner(platform_name):
    product_getter = PlatformSearcher(platform_name)
    product_getter.run()
    # if not GET_FROM_WEB_AND_WRITE:
    #     json_corrector(product_getter.json_filename)


def get_links():
    # maxidom = SearchLinksGetter('maxidom')
    # maxidom.run()

    # dns = PlatformSearcher('dns')
    # dns.run()

    # bau = PlatformSearcher('baucenter')
    # bau.run()

    # akson = PlatformSearcher('akson')
    # akson.run()
    # json_corrector(akson.json_filename)

    # etm = PlatformSearcher('etm')
    # etm.run()
    # json_corrector(etm.json_filename)

    # runner('sdvor')
    # runner('votonia')
    # runner('eltsnab')
    runner('maxidom')


if __name__ == '__main__':
    get_links()
