import requests
from colorama import Fore, Style
import json
import re
from .utils import torRegex, i2pRegex, fetchRegexList, fetchJsonList, fetchCache
import logging
import traceback


def searxng(mightyList):
    try:
        r = requests.get(
            'https://searx.space/data/instances.json')
        rJson = json.loads(r.text)
        searxngList = {}
        searxngList['clearnet'] = []
        searxngList['tor'] = []
        searxngList['i2p'] = []
        searxngList['loki'] = []

        for item in rJson['instances']:
            if re.search(torRegex, item[:-1]):
                searxngList['tor'].append(item[:-1])
            elif re.search(i2pRegex, item[:-1]):
                searxngList['i2p'].append(item[:-1])
            else:
                searxngList['clearnet'].append(item[:-1])

        mightyList['searxng'] = searxngList
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + 'SearXNG')
    except Exception:
        fetchCache('searxng', mightyList)
        logging.error(traceback.format_exc())


def whoogle(mightyList):
    fetchRegexList(
        'whoogle',
        'https://raw.githubusercontent.com/benbusby/whoogle-search/main/README.md',
        r"\| \[https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\) \| ",
        mightyList
    )


def degoog(mightyList):
    fetchJsonList(
        'degoog',
        'https://raw.githubusercontent.com/degoog-org/degoog/main/instances.json',
        {
            'clearnet': 'clearnet',
            'tor': 'tor',
            'i2p': 'i2p',
            'loki': None
        },
        True,
        mightyList
    )


def librey(mightyList):
    fetchJsonList(
        'librey',
        'https://raw.githubusercontent.com/Ahwxorg/librey/main/instances.json',
        {
            'clearnet': 'clearnet',
            'tor': 'tor',
            'i2p': 'i2p',
            'loki': None
        },
        True,
        mightyList
    )
