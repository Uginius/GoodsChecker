from parsers.akson import ParserAkson
from parsers.baucenter import ParserBau
from parsers.dns import ParserDns
from parsers.eltsnab import ParserEltsnab
from parsers.etm import ParserEtm
from parsers.maxidom import ParserMaxidom
from parsers.sdvor import ParserSdvor
from parsers.toledo24 import ParserToledo24
from parsers.votonia import ParserVotonia


def select_platform(platform):
    match platform:
        case 'maxidom':
            return ParserMaxidom
        case 'dns':
            return ParserDns
        case 'baucenter':
            return ParserBau
        case 'akson':
            return ParserAkson
        case 'etm':
            return ParserEtm
        case 'sdvor':
            return ParserSdvor
        case 'eltsnab':
            return ParserEltsnab
        case 'toledo24':
            return ParserToledo24
        case 'votonia':
            return ParserVotonia
        case _:
            print('not found platform in list')