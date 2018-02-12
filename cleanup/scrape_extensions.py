#! /usr/bin/env python3

'''
    Scrapes file extensions for various file types from FileInfo.com
'''

import io
import json
from time import sleep
from urllib.request import urlopen

from bs4 import BeautifulSoup

from constants import BASE_URL, FILE_TYPES

EXTENSIONS_DICT = {}
EXTENSIONS_BY_TYPE = {}


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, 'lxml')


def get_extensions_for(type):
    soup = make_soup(BASE_URL + FILE_TYPES[type]['url'])
    extension_table = soup.find('tbody')

    EXTENSIONS_BY_TYPE[type] = []
    for row in extension_table.find_all('tr'):
        cols = row.find_all('td')
        extension = cols[0].get_text()
        EXTENSIONS_BY_TYPE[type].append(extension)

        EXTENSIONS_DICT[extension] = {}
        EXTENSIONS_DICT[extension]['type'] = type
        EXTENSIONS_DICT[extension]['description'] = cols[1].get_text()


def get_all_extensions():
    for type in FILE_TYPES:
        get_extensions_for(type)
        sleep(1)


def write_dict_to_json_file(dictionary, filename):
    with io.open(filename, 'w', encoding='utf8') as file:
        json_str = json.dumps(dictionary,
                              ensure_ascii=False,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '))
        file.write(json_str)


if __name__ == '__main__':
    get_all_extensions()
    write_dict_to_json_file(EXTENSIONS_DICT, 'extensions.json')
    write_dict_to_json_file(EXTENSIONS_BY_TYPE, 'extensions_by_type.json')
