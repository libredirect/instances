import traceback
import logging
import requests
import json
from urllib.parse import urlparse
import re
from colorama import Fore, Style
import socket


startRegex = r"https?:\/{2}(?:[^\s\/]+\.)*"
endRegex = "(?:\\/[^\\s\\/]+)*\\/?"
torRegex = startRegex + "onion" + endRegex
i2pRegex = startRegex + "i2p" + endRegex
lokiRegex = startRegex + "loki" + endRegex
authRegex = r"https?:\/{2}\S+:\S+@(?:[^\s\/]+\.)*[a-zA-Z0-9]+" + endRegex


def get_cloudflare_ips():
    r = requests.get('https://www.cloudflare.com/ips-v4')
    return r.text.split('\n')


cloudflare_ips = get_cloudflare_ips()


def ip2bin(ip): return "".join(
    map(
        str,
        [
            "{0:08b}".format(int(x)) for x in ip.split(".")
        ]
    )
)


def is_cloudflare(url):
    instance_ip = None
    try:
        instance_ip = socket.gethostbyname(urlparse(url).hostname)
        if instance_ip is None:
            return False
    except Exception:
        return False
    instance_bin = ip2bin(instance_ip)

    for cloudflare_ip_mask in cloudflare_ips:
        cloudflare_ip = cloudflare_ip_mask.split('/')[0]
        cloudflare_bin = ip2bin(cloudflare_ip)

        mask = int(cloudflare_ip_mask.split('/')[1])
        cloudflare_bin_masked = cloudflare_bin[:mask]
        instance_bin_masked = instance_bin[:mask]

        if cloudflare_bin_masked == instance_bin_masked:
            print(url + ' is behind ' + Fore.RED +
                  'cloudflare' + Style.RESET_ALL)
            return True
    return False


is_cloudflare('https://pipedapi-libre.kavin.rocks')


def filterLastSlash(urlList):
    tmp = {}
    for frontend in urlList:
        tmp[frontend] = {}
        for network in urlList[frontend]:
            tmp[frontend][network] = []
            for url in urlList[frontend][network]:
                if url.endswith('/'):
                    tmp[frontend][network].append(url[:-1])
                    print(Fore.YELLOW + "Fixed " + Style.RESET_ALL + url)
                else:
                    tmp[frontend][network].append(url)
    return tmp


def idnaEncode(urlList):
    tmp = {}
    for frontend in urlList:
        tmp[frontend] = {}
        for network in urlList[frontend]:
            tmp[frontend][network] = []
            for url in urlList[frontend][network]:
                try:
                    encodedUrl = url.encode("idna").decode("utf8")
                    tmp[frontend][network].append(encodedUrl)
                    if (encodedUrl != url):
                        print(Fore.YELLOW + "Fixed " + Style.RESET_ALL + url)
                except Exception:
                    tmp[frontend][network].append(url)
    return tmp


def fetchCache(frontend, mightyList):
    try:
        with open('./data.json') as file:
            mightyList[frontend] = json.load(file)[frontend]
        print(Fore.YELLOW + 'Failed' + Style.RESET_ALL + ' to fetch ' + frontend)
    except Exception:
        print(Fore.RED + 'Failed' + Style.RESET_ALL +
              ' to get cached ' + frontend)


def fetchFromFile(frontend, mightyList):
    with open('./fixed/' + frontend + '.json') as file:
        mightyList[frontend] = json.load(file)
    print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)


networks = {}

with open('networks.json', 'rt') as tmp:
    networks = json.load(tmp)


def fetchJsonList(frontend, url, urlItem, jsonObject, mightyList):
    try:
        r = requests.get(url)
        rJson = json.loads(r.text)
        if jsonObject:
            rJson = rJson['instances']
        _list = {}
        for network in networks:
            _list[network] = []
        if type(urlItem) == dict:
            for item in rJson:
                for network in networks:
                    if urlItem[network] is not None:
                        if urlItem[network] in item and item[urlItem[network]] is not None:
                            if type(item[urlItem[network]]) == list:
                                for i in item[urlItem[network]]:
                                    if i.strip() != '':
                                        _list[network].append(i)
                            elif item[urlItem[network]].strip() != '':
                                _list[network].append(item[urlItem[network]])
        else:
            for item in rJson:
                tmpItem = item
                if urlItem is not None:
                    tmpItem = item[urlItem]
                if tmpItem.strip() == '':
                    continue
                elif re.search(torRegex, tmpItem):
                    _list['tor'].append(tmpItem)
                elif re.search(i2pRegex, tmpItem):
                    _list['i2p'].append(tmpItem)
                elif re.search(lokiRegex, tmpItem):
                    _list['loki'].append(tmpItem)
                else:
                    _list['clearnet'].append(tmpItem)

        mightyList[frontend] = _list
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
    except Exception:
        fetchCache(frontend, mightyList)
        logging.error(traceback.format_exc())


def fetchRegexList(frontend, url, regex, mightyList):
    try:
        r = requests.get(url)
        _list = {}
        for network in networks:
            _list[network] = []

        tmp = re.findall(regex, r.text)

        for item in tmp:
            if item.strip() == "":
                continue
            elif re.search(torRegex, item):
                _list['tor'].append(item)
            elif re.search(i2pRegex, item):
                _list['i2p'].append(item)
            elif re.search(lokiRegex, item):
                _list['loki'].append(item)
            else:
                _list['clearnet'].append(item)
        mightyList[frontend] = _list
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
    except Exception:
        fetchCache(frontend)
        logging.error(traceback.format_exc())


def fetchTextList(frontend, url, prepend):
    try:
        _list = {}
        for network in networks:
            _list[network] = []

        if type(url) == dict:
            for network in networks:
                if url[network] is not None:
                    r = requests.get(url[network])
                    tmp = r.text.strip().split('\n')
                    for item in tmp:
                        item = prepend[network] + item
                        _list[network].append(item)
        else:
            r = requests.get(url)
            tmp = r.text.strip().split('\n')

            for item in tmp:
                item = prepend + item
                if re.search(torRegex, item):
                    _list['tor'].append(item)
                elif re.search(i2pRegex, item):
                    _list['i2p'].append(item)
                elif re.search(lokiRegex, item):
                    _list['loki'].append(item)
                else:
                    _list['clearnet'].append(item)
        mightyList[frontend] = _list
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
    except Exception:
        fetchCache(frontend)
        logging.error(traceback.format_exc())


def isValid(url):  # by avanitrachhadiya2155
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
