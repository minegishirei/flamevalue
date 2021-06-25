#オタク統計学
#ターゲット
from bs4 import BeautifulSoup
from urllib.request import urlopen


def niconicoRanking():
    url = "https://dic.nicovideo.jp/rank/hours/3/20/all/all"
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    tableObj = bsObj.find("table",{"class":"rank-list"})
    name_list = []
    for column in tableObj.findAll("td"):
        name_list.append(column)
    return name_list


