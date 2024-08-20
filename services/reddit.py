from .utils import fetchJsonList


def libreddit(mightyList):
    fetchJsonList(
        'libreddit',
        'https://github.com/libreddit/libreddit-instances/raw/master/instances.json',
        {
            'clearnet': 'url',
            'tor': 'onion',
            'i2p': 'i2p',
            'loki': None
        },
        True,
        mightyList
    )


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


def teddit(mightyList):
    fetchJsonList(
        'teddit',
        'https://codeberg.org/teddit/teddit/raw/branch/main/instances.json',
        {
            'clearnet': 'url',
            'tor': 'onion',
            'i2p': 'i2p',
            'loki': None
        },
        False,
        mightyList
    )
