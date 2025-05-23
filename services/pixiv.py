import pandas
import re
import requests
from .utils import fetchRegexList

def pixivFe(mightyList):
    df = pandas.read_csv(
        'https://gitlab.com/pixivfe/pixivfe-docs/-/raw/master/data/instances.csv?ref_type=heads')

    clearnet = []
    for value in df['URL']:
        r = re.findall(r"\((.*?)\)", value)
        if r:
            clearnet.append(r[0])

    mightyList['pixivFe'] = {
        "clearnet": clearnet,
        "tor": [],
        "i2p": [],
        "loki": []
    }

def vixipy(mightyList):
    res = requests.get(
        "https://maid.zone/vixipy/instances.json",
        # set user agent for transparency sake
        headers={
            "User-Agent": "https://codeberg.org/libredirect/instances"
        }
    ).json()

    tor = []
    i2p = []
    clearnet = []

    for i in res:
        if i["URL"] != "":
            clearnet.append(i["URL"])
        if i["I2P"] != "":
            i2p.append(i["I2P"])
        if i["Onion"] != "":
            tor.append(i["Onion"])
    
    mightyList['vixipy'] = {
        "clearnet": clearnet,
        "tor": tor,
        "i2p": i2p,
        "loki": []
    }

def litexiv(mightyList):
    fetchRegexList(
        'liteXiv',
        'https://codeberg.org/LiteXiv/LiteXiv/raw/branch/v2/README.md',
        r"\| (https?:\/{2}.*?) +\|.*?\n",
        mightyList
    )
