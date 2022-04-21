import json
import os
import csv
from pprint import pprint

json_dir = 'results'
files = os.listdir(json_dir)
csv_file = 'final_data.csv'
json_title = ['platform', 'shop id', 'brand', 'name', 'url', 'status', 'price', 'rating', 'votes']


def write_data(data):
    with open(csv_file, 'a', newline='') as out_csv:
        writer = csv.writer(out_csv)  # <_csv.writer object at 0x03B0AD80>
        writer.writerow(data)


def convert_data(read_file):
    for line in read_file:
        jsn = json.loads(line)
        product_id = list(jsn.keys())[0]
        items = jsn[product_id]
        el = [
            items['shop'],
            product_id,
            items['brand'],
            items['name'],
            items['url'],
            items['status'],
            items['price'],
            items['vote_rating'],
            items['vote_qt']
        ]
        write_data(el)


write_data(json_title)
for filename in files:
    with open(f'{json_dir}/{filename}', 'r') as json_file:
        convert_data(json_file)
