def url_maxidom(phrase, i=None):
    link = f'https://www.maxidom.ru/search/catalog/?q={phrase}&category_search=0&amount=12'
    if i:
        link = link + f'&PAGEN_2={i}'
    return link


def url_dns(phrase, i=None):
    link = f'https://www.dns-shop.ru/search/?q={phrase}'
    if i:
        link = link + f'&p={i}'
    return link
