from .utils import fetchJsonList, fetchRegexList


def libreTranslate(mightyList):
    fetchRegexList(
        'libreTranslate',
        'https://raw.githubusercontent.com/LibreTranslate/LibreTranslate/main/README.md',
        r"\[(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\)\|",
        mightyList
    )

def mozhi(mightyList):
        fetchJsonList(
        'mozhi',
        'https://codeberg.org/aryak/mozhi/raw/branch/master/instances.json',
        {
            'clearnet': 'link',
            'tor': 'onion',
            'i2p': 'i2p',
            'loki': None
        },
        False,
        mightyList
    )

def simplytranslate(mightyList):
        fetchJsonList(
        'simplyTranslate',
        'https://codeberg.org/ManeraKai/simplytranslate/raw/branch/main/instances.json',
        'url',
        False,
        mightyList
    )
