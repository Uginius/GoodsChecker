from platforms_and_phrases import PlatformSearcher


def get_links():
    # maxidom = SearchLinksGetter('maxidom')
    # maxidom.run()
    dns = PlatformSearcher('dns')
    dns.run()


if __name__ == '__main__':
    get_links()
