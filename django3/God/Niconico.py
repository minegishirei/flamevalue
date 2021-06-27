#オタク統計学
#ターゲット
from bs4 import BeautifulSoup
from urllib.request import urlopen, quote
import time

def niconicoRanking():
    url = "https://dic.nicovideo.jp/rank/hours/3/20/all/all"
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    tableObj = bsObj.find("table",{"class":"rank-list"})
    niconico_info_dict = []
    for column in tableObj.findAll("td"):
        column = column.get_text()
        print(column)
        if "\n\n" in column:
            continue
        description = getPageInfo(column)
        niconico_info_dict.append({
            "name" :column,
            "description" : description
        })
    return niconico_info_dict



def getPageInfo(htmlname):
    time.sleep(1)
    try:
        url = f"https://dic.nicovideo.jp/a/{ quote(htmlname)}"
        html = urlopen(url)
        bsObj = BeautifulSoup(html)
        content = bsObj.find("div", {"class","a-contents"})
        for p_tag in content.findAll("p"):
            text = p_tag.get_text()
            if len(text) >100:
                return ""
            if "とは、" in text:
                return text
        return bsObj.get_text()
    except Exception as error:
        return ""
    return ""


