
from xml.etree import ElementTree

import requests


def get_wikipedia_list():
    url = "https://ja.wikipedia.org/w/api.php?format=json&callback=foobar&action=query&list=categorymembers&cmlimit=500&cmtitle=Category:%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9E&format=xml"
    res = requests.get(url)
    res_text = res.text
    elem = ElementTree.fromstring(res_text)
    wiki_list = []
    for child in elem[1][0]:
        wiki_list.append(wiki)
    return wiki_list