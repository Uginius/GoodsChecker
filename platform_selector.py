from parsers.search_dns import ParserDns


def select_platform(platform):
    match platform:
        case 'maxidom':
            return 'maxidom'
        case 'dns':
            return ParserDns
        case 'baucenter':
            return None
        case 'akson':
            return None
        case 'etm':
            return None
        case 'sdvor':
            return None
        case 'eltsnab':
            return None
        case 'toledo24':
            return None
        case 'votonia':
            return None
        case _:
            print('not found platform in list')