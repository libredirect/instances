import pandas
import re


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
