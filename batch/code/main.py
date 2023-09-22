from pprint import pprint 
from api.fetch_wakou import fetch_event_list, fetch_event_details, fetch_more_event_details
from api.fetch_wakou_lib import fetch_lib_event_list
from api.fetch_wakou_lib import fetch_event_details as fetch_lib_event_details
from createfile.sitemap import create_sitemap
from mydate.date import get_next_target_date
import datetime
import json
import re

import hashlib


def unique_list(a):
    b = []
    for x in a:
        if x not in b:
            b.append(x)
    return b

def unique_id(link):
    return hashlib.md5(link.encode()).hexdigest()
    #return hashlib.sha256(text).hexdigest()
    #return "".join(re.findall(r"\d+", link))

def rotate_fetch_eventlist(next_week_amount):
    eventlist = []
    # 現在の日付を取得する。
    today = datetime.date.today()
    next_date = get_next_target_date(today, '月') + datetime.timedelta(days=-14)
    for _ in range(0, next_week_amount):
        eventlist.extend(list(fetch_event_list(
            year=next_date.strftime('%Y'),
            month=next_date.strftime('%m'),
            day=next_date.strftime('%d')
        )))
        next_date = next_date + datetime.timedelta(days=7)
    return eventlist



def wakou_sanzarie(amount):
    searched_link_set = set()
    all_events = {}
    for event in rotate_fetch_eventlist(amount):
        try:
            if event["link"] and (event["link"] not in searched_link_set):
                print(event["link"])
                searched_link_set.add(event["link"])
                event_details = fetch_event_details(event["link"])
                event_details.update(event)
                if "detail_link" in event_details:
                    event_details.update(fetch_more_event_details(event_details["detail_link"]))
                event_details.update({
                    "id" : unique_id(event_details["detail_link"])
                })
                all_events.update({
                    event_details["id"] : event_details
                })
        except Exception as e:
            print(e)
    return all_events
    
    

def wakou_lib(amount):
    event_list = fetch_lib_event_list()
    all_events = {}
    for event in event_list[:amount]:
        print(event["detail_link"])
        event.update(fetch_lib_event_details(event["detail_link"]))
        event.update({
            "id" : unique_id(event["detail_link"])
        })
        all_events.update({
            event["id"] : event
        })
    return all_events

ALL_EVENTS = {}
ALL_EVENTS = wakou_sanzarie(50)
ALL_EVENTS.update(wakou_lib(10))


with open('./output/store.json', 'w') as f:
    json.dump(ALL_EVENTS, f, indent=4, ensure_ascii=False)




