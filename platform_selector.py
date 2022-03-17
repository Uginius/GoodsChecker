from parsers.baucenter import ParserBau
from parsers.dns import ParserDns
from parsers.maxidom import ParserMaxidom


def select_platform(platform):
    match platform:
        case 'maxidom':
            return ParserMaxidom
        case 'dns':
            return ParserDns
        case 'baucenter':
            return ParserBau
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