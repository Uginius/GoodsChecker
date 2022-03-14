from search_links_getter import SearchLinksGetter


def get_links():
    maxidom = SearchLinksGetter('maxidom')
    maxidom.run()


if __name__ == '__main__':
    get_links()
