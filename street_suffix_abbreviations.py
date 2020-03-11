import json

import requests
from bs4 import BeautifulSoup

base_url = 'https://pe.usps.com/text/pub28/28apc_002.htm'

session = requests.Session()
session.headers['User-Agent'] = \
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
    'Chrome/34.0.1847.131 ' \
    'Safari/537.36'
response = session.get(base_url)
bs = BeautifulSoup(response.text, 'lxml')
rows = bs.select('.Basic_no_title tr')

current_abbreviation = ''
res_dict = {}

for row in rows:
    cols = row.select('td')

    if len(cols) == 1:
        res_dict[current_abbreviation].append(cols[0].text.strip())

    if len(cols) == 3:
        current_abbreviation = cols[2].text.strip()  # change 2 to 0 for
        # primary street suffix name instead of abbreviation
        res_dict[current_abbreviation] = [cols[1].text.strip()]

    if len(cols) not in [1, 3]:
        raise Exception(f'length {len(cols)} in {row}')

with open('result.json', 'w') as f:
    json.dump(res_dict, f)
