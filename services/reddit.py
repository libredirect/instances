from .utils import fetchJsonList


def redlib(mightyList):
    fetchJsonList(
        'redlib',
        'https://github.com/redlib-org/redlib-instances/raw/main/instances.json',
        {
            'clearnet': 'url',
            'tor': 'onion',
            'i2p': 'i2p',
            'loki': None
        },
        True,
        mightyList
    )
