from platforms_and_phrases import PlatformSearcher


def get_links():
    # maxidom = SearchLinksGetter('maxidom')
    # maxidom.run()

    # dns = PlatformSearcher('dns')
    # dns.run()

    # bau = PlatformSearcher('baucenter')
    # bau.run()

    # akson = PlatformSearcher('akson')
    # akson.run()

    etm = PlatformSearcher('etm')
    etm.run()


if __name__ == '__main__':
    get_links()
