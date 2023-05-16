#!/usr/bin/python3

import traceback
import logging
import requests
import json
from urllib.parse import urlparse
import re
from colorama import Fore, Style
import socket
import yaml

mightyList = {}
networks = {}

startRegex = r"https?:\/{2}(?:[^\s\/]+\.)*"
endRegex = "(?:\/[^\s\/]+)*\/?"
torRegex = startRegex + "onion" + endRegex
i2pRegex = startRegex + "i2p" + endRegex
lokiRegex = startRegex + "loki" + endRegex
authRegex = r"https?:\/{2}\S+:\S+@(?:[^\s\/]+\.)*[a-zA-Z0-9]+" + endRegex

with open('networks.json', 'rt') as tmp:
    networks = json.load(tmp)


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


def ip2bin(ip): return "".join(
    map(
        str,
        [
            "{0:08b}".format(int(x)) for x in ip.split(".")
        ]
    )
)


def get_cloudflare_ips():
    r = requests.get('https://www.cloudflare.com/ips-v4')
    return r.text.split('\n')


cloudflare_ips = get_cloudflare_ips()


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


def fetchCache(frontend):
    try:
        with open('./data.json') as file:
            mightyList[frontend] = json.load(file)[frontend]
        print(Fore.YELLOW + 'Failed' + Style.RESET_ALL + ' to fetch ' + frontend)
    except Exception:
        print(Fore.RED + 'Failed' + Style.RESET_ALL +
              ' to get cached ' + frontend)


def fetchFromFile(frontend):
    with open('./fixed/' + frontend + '.json') as file:
        mightyList[frontend] = json.load(file)
    print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)


def fetchJsonList(frontend, url, urlItem, jsonObject):
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
        fetchCache(frontend)
        logging.error(traceback.format_exc())


def fetchRegexList(frontend, url, regex):
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


def invidious():
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
        fetchCache(frontend)
        logging.error(traceback.format_exc())


def piped():
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
                url = requests.get(item, timeout=5).url
                if url.strip("/") == item:
                    continue
                else:
                    _list['clearnet'].append(url)
            except Exception:
                logging.error(traceback.format_exc())
                continue
        mightyList[frontend] = _list
        _list['clearnet'].remove("https://piped.video")
        print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
    except Exception:
        fetchCache(frontend)
        logging.error(traceback.format_exc())


def pipedMaterial():
    fetchRegexList('pipedMaterial', 'https://raw.githubusercontent.com/mmjee/Piped-Material/master/README.md',
                   r"\| (https?:\/{2}(?:\S+\.)+[a-zA-Z0-9]*) +\| Production")


def cloudtube():
    fetchFromFile('cloudtube')


def proxitok():
    fetchRegexList('proxiTok', 'https://raw.githubusercontent.com/wiki/pablouser1/ProxiTok/Public-instances.md',
                   r"\| \[.*\]\(([-a-zA-Z0-9@:%_\+.~#?&//=]{2,}\.[a-z]{2,}\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)\)(?: \(Official\))? +\|(?:(?: [A-Z]*.*\|.*\|)|(?:$))")


def send():
    fetchRegexList('send', 'https://gitlab.com/timvisee/send-instances/-/raw/master/README.md',
                   r"- ([-a-zA-Z0-9@:%_\+.~#?&//=]{2,}\.[a-z0-9]{2,}\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)\)*\|*[A-Z]{0,}")


def nitter():
    fetchRegexList('nitter', 'https://raw.githubusercontent.com/wiki/zedeus/nitter/Instances.md',
                   r"(?:(?:\| )|(?:-   ))\[(?:(?:\S+\.)+[a-zA-Z0-9]+)\/?\]\((https?:\/{2}(?:\S+\.)+[a-zA-Z0-9]+)\/?\)(?:(?: (?:\((?:\S+ ?\S*)\) )? *\| [^❌]{1,4} +\|(?:(?:\n)|(?: ❌)|(?: ✅)|(?: ❓)|(?: \[)))|(?:\n))")


def libreddit():
    fetchJsonList('libreddit', 'https://github.com/libreddit/libreddit-instances/raw/master/instances.json',
                  {'clearnet': 'url', 'tor': 'onion', 'i2p': 'i2p', 'loki': None}, True)


def teddit():
    fetchJsonList('teddit', 'https://codeberg.org/teddit/teddit/raw/branch/main/instances.json',
                  {'clearnet': 'url', 'tor': 'onion', 'i2p': 'i2p', 'loki': None}, False)


def scribe():
    fetchJsonList(
        'scribe', 'https://git.sr.ht/~edwardloveall/scribe/blob/main/docs/instances.json', None, False)


def quetre():
    fetchRegexList('quetre', 'https://raw.githubusercontent.com/zyachel/quetre/main/README.md',
                   r"\| \[.*\]\(([-a-zA-Z0-9@:%_\+.~#?&//=]{2,}\.[a-z0-9]{2,}\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)\)*\|*[A-Z]{0,}.*\|.*\|")


def libremdb():
    fetchRegexList('libremdb', 'https://raw.githubusercontent.com/zyachel/libremdb/main/README.md',
                   r"\| \[.*\]\(([-a-zA-Z0-9@:%_\+.~#?&//=]{2,}\.[a-z0-9]{2,}\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)\)*\|*[A-Z]{0,}.*\|.*\|")


def simplytranslate():
    fetchTextList('simplyTranslate', {'clearnet': 'https://simple-web.org/instances/simplytranslate', 'tor': 'https://simple-web.org/instances/simplytranslate_onion',
                  'i2p': 'https://simple-web.org/instances/simplytranslate_i2p', 'loki': 'https://simple-web.org/instances/simplytranslate_loki'}, {'clearnet': 'https://', 'tor': 'http://', 'i2p': 'http://', 'loki': 'http://'})


def linvgatranslate():
    fetchJsonList(
        'lingva', 'https://raw.githubusercontent.com/TheDavidDelta/lingva-translate/main/instances.json', None, False)


def searxng():
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


def searx():
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
    print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + 'SearXNG')


def whoogle():
    fetchRegexList('whoogle', 'https://raw.githubusercontent.com/benbusby/whoogle-search/main/README.md',
                   r"\| \[https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\) \| ")


def librex():
    fetchJsonList('librex', 'https://raw.githubusercontent.com/hnhx/librex/main/instances.json',
                  {'clearnet': 'clearnet', 'tor': 'tor', 'i2p': 'i2p', 'loki': None}, True)


def rimgo():
    fetchJsonList('rimgo', 'https://codeberg.org/video-prize-ranch/rimgo/raw/branch/main/instances.json',
                  {'clearnet': 'url', 'tor': 'onion', 'i2p': 'i2p', 'loki': None}, False)


def beatbump():
    fetchFromFile('beatbump')


def hyperpipe():
    fetchJsonList(
        'hyperpipe', 'https://codeberg.org/Hyperpipe/pages/raw/branch/main/api/frontend.json', 'url', False)


def facil():
    fetchFromFile('facil')


def osm():
    fetchFromFile('osm')


def libreTranslate():
    fetchRegexList('libreTranslate', 'https://raw.githubusercontent.com/LibreTranslate/LibreTranslate/main/README.md',
                   r"\[(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\)\|")


def breezeWiki():
    fetchJsonList(
        'breezeWiki', 'https://docs.breezewiki.com/files/instances.json', 'instance', False)


def privateBin():
    fetchJsonList('privateBin', 'https://privatebin.info/directory/api?top=100&https_redirect=true&min_rating=A&csp_header=true&min_uptime=100&attachments=true', 'url', False)


def neuters():
    fetchFromFile('neuters')


def libMedium():
    fetchRegexList('libMedium', 'https://raw.githubusercontent.com/realaravinth/libmedium/master/README.md',
                   r"\| (https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/? +\|")


def dumb():
    fetchRegexList('dumb', 'https://raw.githubusercontent.com/rramiachraf/dumb/main/README.md',
                   r"\| <(https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?> +\|")


def ruralDictionary():
    fetchJsonList('ruralDictionary',
                  'https://codeberg.org/zortazert/rural-dictionary/raw/branch/master/instances.json',
                  {'clearnet': 'clearnet', 'tor': 'tor',
                      'i2p': 'i2p', 'loki': None},
                  False
                  )


def anonymousOverflow():
    fetchRegexList('anonymousOverflow', 'https://raw.githubusercontent.com/httpjamesm/AnonymousOverflow/main/README.md',
                   r"\| \[(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\) +\|")


def wikiless():
    fetchFromFile('wikiless')


def biblioReads():
    fetchJsonList(
        'biblioReads',
        'https://raw.githubusercontent.com/nesaku/BiblioReads/main/instances.json',
        {'clearnet': 'url', 'tor': 'onion', 'i2p': 'i2p', 'loki': None},
        False
    )


def suds():
    fetchJsonList(
        'suds', 'https://git.vern.cc/cobra/Suds/raw/branch/main/instances.json',
        {
            'clearnet': 'clearnet',
            'tor': 'tor',
            'i2p': 'i2p',
            'loki': None
        },
        False,
    )


def poketube():
    frontend = 'poketube'
    try:
        r = requests.get(
            'https://codeberg.org/Ashley/poketube/raw/branch/main/instances.json')
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
        fetchCache(frontend)
        logging.error(traceback.format_exc())


def gothub():
    fetchJsonList(
        'gothub',
        'https://codeberg.org/gothub/gothub-instances/raw/branch/master/instances.json',
        {
            'clearnet': 'link',
            'tor': None,
            'i2p': None,
            'loki': None
        },
        False
    )


def mikuInvidious():
    fetchFromFile('mikuInvidious')


def tent():
    fetchFromFile('tent')


wolfreeAlpha_url_list = [
    "https://gqq.gitlab.io",
    "https://jqq.gitlab.io",
    "https://rqq.gitlab.io",
    "https://sqq.gitlab.io",
    "https://uqq.gitlab.io"
]
wolfreeAlpha_url_list_i = 0


def wolfreeAlpha(i):
    global wolfreeAlpha_url_list_i
    frontend = 'wolfreeAlpha'
    try:
        r = requests.get(wolfreeAlpha_url_list[i]+"/instances.json")
        if r.status_code != 200:
            wolfreeAlpha_url_list_i += 1
            wolfreeAlpha(wolfreeAlpha_url_list_i)
        else:
            rJson = json.loads(r.text)
            networks = rJson['wolfree']
            _list = {}
            for i in networks.keys():
                _list[i] = networks[i]
            mightyList[frontend] = _list
            print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
    except:
        wolfreeAlpha_url_list_i += 1
        wolfreeAlpha(wolfreeAlpha_url_list_i)


def isValid(url):  # This code is contributed by avanitrachhadiya2155
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


invidious()
piped()
pipedMaterial()
cloudtube()
proxitok()
send()
nitter()
libreddit()
teddit()
scribe()
quetre()
libremdb()
simplytranslate()
linvgatranslate()
libreTranslate()
searxng()
searx()
whoogle()
librex()
rimgo()
beatbump()
hyperpipe()
facil()
osm()
breezeWiki()
privateBin()
neuters()
ruralDictionary()
libMedium()
dumb()
anonymousOverflow()
wikiless()
biblioReads()
suds()
poketube()
gothub()
mikuInvidious()
wolfreeAlpha(wolfreeAlpha_url_list_i)


mightyList = filterLastSlash(mightyList)
mightyList = idnaEncode(mightyList)

cloudflare = []
for k1, v1 in mightyList.items():
    if type(mightyList[k1]) is dict:
        for k2, v2 in mightyList[k1].items():
            for instance in mightyList[k1][k2]:
                if (not isValid(instance)):
                    mightyList[k1][k2].remove(instance)
                    print("removed " + instance)
                else:
                    if not instance.endswith('.onion') and not instance.endswith('.i2p') and not instance.endswith('.loki') and is_cloudflare(instance):
                        cloudflare.append(instance)
blacklist = {
    'cloudflare': cloudflare
}

# Writing to file
json_object = json.dumps(mightyList, ensure_ascii=False, indent=2)
with open('./data.json', 'w') as outfile:
    outfile.write(json_object)
print(Fore.BLUE + 'wrote ' + Style.RESET_ALL + 'instances/data.json')

json_object = json.dumps(blacklist, ensure_ascii=False, indent=2)
with open('./blacklist.json', 'w') as outfile:
    outfile.write(json_object)
print(Fore.BLUE + 'wrote ' + Style.RESET_ALL + 'instances/blacklist.json')

# print(json_object)
