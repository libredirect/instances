from .utils import fetchJsonList, fetchRegexList


def linvgatranslate(mightyList):
    fetchJsonList(
        'lingva',
        'https://raw.githubusercontent.com/TheDavidDelta/lingva-translate/main/instances.json',
        None,
        False,
        mightyList
    )


def libreTranslate(mightyList):
    fetchRegexList(
        'libreTranslate',
        'https://raw.githubusercontent.com/LibreTranslate/LibreTranslate/main/README.md',
        r"\[(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\)\|",
        mightyList
    )
