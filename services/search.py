import requests
from colorama import Fore, Style
import json
import re
from .utils import torRegex, i2pRegex, fetchRegexList, fetchJsonList
import yaml


def searxng(mightyList):
    r = requests.get(
        'https://searx.space/data/instances.json')
    rJson = json.loads(r.text)
    searxngList = {}
    searxngList['clearnet'] = []
    searxngList['tor'] = []
    searxngList['i2p'] = []
    searxngList['loki'] = []

    for item in rJson['instances']:
        if re.search(torRegex, item[:-1]) and rJson['instances'][item].get('generator') == 'searxng':
            searxngList['tor'].append(item[:-1])
        elif re.search(i2pRegex, item[:-1]) and rJson['instances'][item].get('generator') == 'searxng':
            searxngList['i2p'].append(item[:-1])
        elif rJson['instances'][item].get('generator') == 'searxng':
            searxngList['clearnet'].append(item[:-1])

    mightyList['searxng'] = searxngList
    print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + 'SearXNG')


def searx(mightyList):
    searxList = {}
    searxList['clearnet'] = []
    searxList['tor'] = []
    searxList['i2p'] = []
    searxList['loki'] = []
    r = requests.get(
        'https://raw.githubusercontent.com/searx/searx-instances/master/searxinstances/instances.yml')
    data = yaml.safe_load(r.text)
    for key in data:
        searxList['clearnet'].append(key)
        if 'additional_urls' in data[key]:
            for additional_url in data[key]['additional_urls']:
                if data[key]['additional_urls'][additional_url] == "Hidden Service":
                    searxList['tor'].append(additional_url)
    mightyList['searx'] = searxList
    print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + 'SearX')


def whoogle(mightyList):
    fetchRegexList(
        'whoogle',
        'https://raw.githubusercontent.com/benbusby/whoogle-search/main/README.md',
        r"\| \[https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\) \| ",
        mightyList
    )
