import requests
from colorama import Fore, Style
import json

wolfreeAlpha_url_list = [
    "https://gqq.gitlab.io",
    "https://jqq.gitlab.io",
    "https://rqq.gitlab.io",
    "https://sqq.gitlab.io",
    "https://uqq.gitlab.io"
]


def wolfreeAlpha(mightyList):
    global wolfreeAlpha_url_list_i
    frontend = 'wolfreeAlpha'
    for instance in wolfreeAlpha_url_list:
        try: 
            r = requests.get(instance+"/instances.json")
            if r.status_code != 200:
                continue
            else:
                rJson = json.loads(r.text)
                networks = rJson['wolfree']
                _list = {}
                for i in networks.keys():
                    _list[i] = networks[i]
                mightyList[frontend] = _list
                print(Fore.GREEN + 'Fetched ' + Style.RESET_ALL + frontend)
                break
        except:
            wolfreeAlpha_url_list_i += 1
            wolfreeAlpha(wolfreeAlpha_url_list_i)