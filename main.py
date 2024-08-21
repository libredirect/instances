import json
from colorama import Fore, Style
from services.from_file import *
from services.medium import *
from services.other import *
from services.reddit import *
from services.search import *
from services.translate import *
from services.utils import *
from services.wolfram import *
from services.youtube import *
from services.pixiv import *

mightyList = {}

invidious(mightyList)
materialious(mightyList)
piped(mightyList)
pipedMaterial(mightyList)
cloudtube(mightyList)
proxitok(mightyList)
send(mightyList)
nitter(mightyList)
libreddit(mightyList)
redlib(mightyList)
teddit(mightyList)
scribe(mightyList)
quetre(mightyList)
libremdb(mightyList)
simplytranslate(mightyList)
linvgatranslate(mightyList)
libreTranslate(mightyList)
searxng(mightyList)
searx(mightyList)
whoogle(mightyList)
librex(mightyList)
rimgo(mightyList)
pixivFe(mightyList)
safetwitch(mightyList)
hyperpipe(mightyList)
osm(mightyList)
breezeWiki(mightyList)
binternet(mightyList)
privateBin(mightyList)
neuters(mightyList)
ruralDictionary(mightyList)
libMedium(mightyList)
dumb(mightyList)
anonymousOverflow(mightyList)
wikiless(mightyList)
biblioReads(mightyList)
suds(mightyList)
poketube(mightyList)
gothub(mightyList)
mikuInvidious(mightyList)
wolfreeAlpha(mightyList)
jiti(mightyList)
proxigram(mightyList)
tent(mightyList)
laboratory(mightyList)
twineo(mightyList)
priviblur(mightyList)
mozhi(mightyList)


mightyList = filterLastSlash(mightyList)
mightyList = idnaEncode(mightyList)

cloudflare = []
for k1, v1 in mightyList.items():
    if type(mightyList[k1]) is dict:
        for k2, v2 in mightyList[k1].items():
            for instance in mightyList[k1][k2]:
                if not isValid(instance):
                    mightyList[k1][k2].remove(instance)
                    print("removed " + instance)
                else:
                    if not instance.endswith('.onion') and not instance.endswith('.i2p') and not instance.endswith('.loki') and is_cloudflare(instance):
                        cloudflare.append(instance)
blacklist = {
    'cloudflare': cloudflare
}

json_object = json.dumps(mightyList, ensure_ascii=False, indent=2)
with open('./data.json', 'w') as outfile:
    outfile.write(json_object)
print(Fore.BLUE + 'wrote ' + Style.RESET_ALL + 'instances/data.json')

json_object = json.dumps(blacklist, ensure_ascii=False, indent=2)
with open('./blacklist.json', 'w') as outfile:
    outfile.write(json_object)
print(Fore.BLUE + 'wrote ' + Style.RESET_ALL + 'instances/blacklist.json')
