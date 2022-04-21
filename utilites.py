import json
import time
from pprint import pprint


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\nФункция работала {elapsed} секунд(ы)')
        return result

    return surrogate


def write_json_items(filename, data):
    with open(filename, "a") as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')


def json_correct_doubles(json_filename):
    json_data = {}
    with open(json_filename, "r", encoding='utf8') as file:
        for line in file:
            loads = json.loads(line.strip())
            json_data.update(loads)
    with open(json_filename, 'w'):
        pass
    for element in json_data:
        data_line = {element: json_data[element]}
        write_json_items(json_filename, data_line)


def write_html(src, filename):
    with open(filename, 'w', encoding='utf8') as write_file:
        write_file.write(src)
