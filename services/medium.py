from .utils import fetchJsonList, fetchRegexList


def scribe(mightyList):
    fetchJsonList(
        'scribe', 'https://git.sr.ht/~edwardloveall/scribe/blob/main/docs/instances.json',
        None,
        False,
        mightyList
    )


def libMedium(mightyList):
    fetchRegexList(
        'libMedium',
        'https://raw.githubusercontent.com/realaravinth/libmedium/master/README.md',
        r"\| (https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/? +\|",
        mightyList
    )
