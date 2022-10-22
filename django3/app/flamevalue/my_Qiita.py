import requests
import json
import pprint
import time
from .my_tools import calc_distance


def getQiitaInfo(query, per_page):
    token = "5798518994eec676de3272cc9c15405cf3b697d5"
    headers = {
        "Authorization": "Bearer " + token
    }
    params = {
        "query" : f'{query}',
        "page": "1",
        "per_page": per_page,
    }
    res = requests.get('https://qiita.com/api/v2/items', params=params, headers=headers)
    jsondata = json.loads(res.text)
    return jsondata






def getQiitaTags(tag_name):
    def getAllQiitaTag():
        token = "5798518994eec676de3272cc9c15405cf3b697d5"
        headers = {
            "Authorization": "Bearer " + token
        }
        origin = []
        for i in range(0, 2):
            params = {
                "page": i+1,
                "per_page": "100",
                "sort" : "count"
            }
            res = requests.get('https://qiita.com/api/v2/tags', params=params, headers=headers)
            jsondata = json.loads(res.text)
            time.sleep(1)
            return jsondata
    
    all_qiita_tags = getAllQiitaTag()
    for row in all_qiita_tags:
        if (row["id"] == tag_name):
            return row
    return list(sorted(all_qiita_tags, key=lambda x: calc_distance(x["id"], tag_name) ))[0]

if __name__ == "__main__":
    print( getQiitaTags("Ruby on Rails")  )
