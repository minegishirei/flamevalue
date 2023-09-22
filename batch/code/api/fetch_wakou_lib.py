import requests
from bs4 import BeautifulSoup
import time
import uuid
import re

def myuuid(target):
    return uuid.uuid3(uuid.uuid1(), target)

url = "https://www.wakolib.jp"
base_url = "https://www.wakolib.jp"

def fetch_lib_event_list():
    print(url)
    r = requests.get(url + "/eventnews/")
    bsObj = BeautifulSoup(r.content, 'html.parser')
    eventBsObj = bsObj.find("div", {"id" : "link_contents_news"} )
    event_list = []
    for li in  eventBsObj.find_all("li"):
        event = {
            "date" : li.find("span", { "class":"update_date"}).getText(),
            "split_date" : re.split('[年月日]', li.find("span", { "class":"update_date"}).getText())[:3],
            "title" : "和光図書館" + li.find("span", { "class":"news_description"}).getText(),
            "detail_link" : url + li.find("span", { "class":"news_description"}).find("a").get("href"),
        }
        event.update({
            "id" : str(myuuid(event["detail_link"]))
        })
        event_list.append(event)
    return event_list



def fetch_event_details(url):
    time.sleep(1)
    r = requests.get(url)
    bsObj = BeautifulSoup(r.content, 'html.parser')
    main_containt = bsObj.find("div", {"class": "content_wrap"})
    event_details = {
        "description": main_containt.getText(),
        "location" : "和光市図書館",
        "fee" : "詳細から確認をお願いします",
        "powerd_by" : "和光市図書館",
        "ask" : "和光市図書館",
        "images" : ["https://1.bp.blogspot.com/-7DsADfq2BX4/Xlyf7aSybcI/AAAAAAABXq8/ut72jfLtCuo8ZvRGp1kqCYEbeQ0dOR8pgCNcBGAsYHQ/s1600/no_image_tate.jpg"]
    }
    if main_containt.find_all("img"):
        event_details.update({"images" : [ base_url + img.get("src") for img in main_containt.find_all("img")] })
    if main_containt.find_all("a"):
        event_details.update({
            "pdfs" : list(set(list(filter(lambda href: href.endswith(".pdf"), [ base_url + img.get("href") for img in main_containt.find_all("a")]))))
        })
    return event_details

