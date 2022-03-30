from platforms_and_phrases import PlatformSearcher
from utilites import json_corrector


def get_links():
    # maxidom = SearchLinksGetter('maxidom')
    # maxidom.run()

    # dns = PlatformSearcher('dns')
    # dns.run()

    # bau = PlatformSearcher('baucenter')
    # bau.run()

    akson = PlatformSearcher('akson')
    akson.run()
    json_corrector(akson.json_filename)

    # etm = PlatformSearcher('etm')
    # etm.run()
    # json_corrector(etm.json_filename)


if __name__ == '__main__':
    get_links()
