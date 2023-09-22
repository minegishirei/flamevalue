import requests
from bs4 import BeautifulSoup
import time
import re

def fetch_event_list(year=2023, month=8, day=21):
    url = f"""https://www.city.wako.lg.jp/home/kensaku/event.html?wyear13259={year}&wmonth13259={month}&wday13259={day}"""
    time.sleep(1)
    r = requests.get(url)
    bsObj = BeautifulSoup(r.text, 'html.parser')
    result_list = []
    for weekCalendarTr in bsObj.find_all("tr", attrs={ 'class': "weekCalendarTr" }):
        td_list = weekCalendarTr.find_all("td")
        result_list.append({
            "format_date" : td_list[0].text,
            "split_date" : re.split('[年月日]', td_list[0].text)[:3],
            "link" : td_list[1].find("a").get("href") if td_list[1].find("a") else None,
            "title": td_list[1].find("a").text if td_list[1].find("a") else None,
        })
    return result_list


def fetch_event_details(link):
    url = f"""https://www.city.wako.lg.jp{link}"""
    print(url)
    time.sleep(1)
    r = requests.get(url)
    bsObj = BeautifulSoup(r.text, 'html.parser')
    event_details = {}
    for weekCalendarTr in bsObj.find_all("tr"):
        td_list = weekCalendarTr.find_all("td")
        if len(td_list) > 1 and key_clear(td_list[0].getText()):
            event_details.update({
                key_clear(td_list[0].getText()) : value_celar(td_list[1].getText())
            })
    event_details.update({
        "title" : value_celar(bsObj.find("title").getText()),
        "purchase" : "https://p-ticket.jp/sunazalea"
    })
    return event_details


def fetch_more_event_details(link):
    print(link)
    event_more_details = {}
    url = link
    r = requests.get(url)
    content_type_encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
    bsObj = BeautifulSoup(r.content, 'html.parser', from_encoding=content_type_encoding)
    div_photo = bsObj.find("div", attrs={"id": "photo"})
    link_list = []
    for img in div_photo.find_all("img"):
        src = img.get('src')
        if src[0] == ".":
            link_list.append( ("https://www.sunazalea.or.jp/event" + src[1:]).replace(" ", ""))
        else:
            link_list.append(src)
    event_more_details.update({
        "images" : link_list,
        "description" : bsObj.find("h3").getText()
    })
    return event_more_details



def key_clear(origin):
    router = {
        "日付" : "date",
        "開演" : "open_at",
        "場所" : "location",
        "入場方法" : "fee",
        "主催 ・ 後援" : "powerd_by",
        "詳細" : "detail_link",
        "問い合わせ" : "ask"
    }
    for key, value in router.items():
        if key in origin:
            return value

def value_celar(origin):
    router = {
        "\xa0" : " ",
        "\u3000" : " ",
        "\n" : ""
    }
    for key, value in router.items():
        origin = origin.replace(key, value)
    return origin







