from .utils import fetchRegexList, fetchCache, fetchJsonList
import requests
import json
from colorama import Fore, Style
import logging
import traceback
import re


def invidious(mightyList):
    name = 'Invidious'
    frontend = 'invidious'
    url = 'https://api.invidious.io/instances.json'
    try:
        _list = {}
        _list['clearnet'] = []
        _list['tor'] = []
        _list['i2p'] = []
        _list['loki'] = []
        r = requests.get(url)
        rJson = json.loads(r.text)
        for instance in rJson:
            if instance[1]['type'] == 'https':
                _list['clearnet'].append(instance[1]['uri'])
            elif instance[1]['type'] == 'onion':
                _list['tor'].append(instance[1]['uri'])
            elif instance[1]['type'] == 'i2p':
                _list['i2p'].append(instance[1]['uri'])
        mightyList[frontend] = _list
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + name)
    except Exception:
        fetchCache(frontend, mightyList)
        logging.error(traceback.format_exc())


def piped(mightyList):
    frontend = 'piped'
    try:
        _list = {}
        _list['clearnet'] = []
        _list['tor'] = []
        _list['i2p'] = []
        _list['loki'] = []
        r = requests.get(
            'https://raw.githubusercontent.com/wiki/TeamPiped/Piped/Instances.md')

        tmp = re.findall(
            r' \| (https:\/{2}(?:[^\s\/]+\.)+[a-zA-Z]+) \| ', r.text)
        for item in tmp:
            try:
                print(
                    Fore.GREEN + 'Fetching ' + Style.RESET_ALL + item,
                    end=' '
                )
                url = requests.get(item, timeout=5).url
                if url.strip("/") == item:
                    print(Fore.RED + '𐄂')
                    continue
                else:
                    # Exceptions
                    if url == 'https://piped.video':
                        continue
                    if url.startswith('http://ww25.yapi.vyper.me'):
                        continue
                    
                    print(Fore.GREEN + '✓')
                    _list['clearnet'].append(url)
            except Exception:
                print(Fore.RED + '𐄂')
                continue
        mightyList[frontend] = _list
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
    except Exception:
        fetchCache(frontend, mightyList)
        logging.error(traceback.format_exc())


def materialious(mightyList):
    fetchRegexList(
        'materialious',
        'https://raw.githubusercontent.com/Materialious/Materialious/main/docs/INSTANCES.md',
        r"- \[.*\]\((https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\)",
        mightyList
    )


def pipedMaterial(mightyList):
    fetchRegexList(
        'pipedMaterial',
        'https://raw.githubusercontent.com/mmjee/Piped-Material/master/README.md',
        r"\| (https?:\/{2}(?:\S+\.)+[a-zA-Z0-9]*) +\| Production",
        mightyList
    )


def poke(mightyList):
    frontend = 'poke'
    try:
        r = requests.get(
            'https://codeberg.org/ashley/poke/raw/branch/main/instances.json')
        rJson = json.loads(r.text)
        _list = {
            'clearnet': [],
            'tor': [],
            'i2p': [],
            'loki': []

        }
        for element in rJson:
            _list['clearnet'].append(element[1]['uri'])

        mightyList[frontend] = _list
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
    except Exception:
        fetchCache(frontend, mightyList)
        logging.error(traceback.format_exc())


def hyperpipe(mightyList):
    fetchJsonList(
        'hyperpipe',
        'https://codeberg.org/Hyperpipe/pages/raw/branch/main/api/frontend.json',
        'url',
        False,
        mightyList)
