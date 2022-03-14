import time

from parsers.search_parsers import Maxidom


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\nФункция работала {elapsed} секунд(ы)')
        return result

    return surrogate


def select_parser(platform):
    match platform:
        case 'maxidom':
            return Maxidom
        case _:
            print('not found platform in list')
