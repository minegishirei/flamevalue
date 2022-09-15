import requests
import json
import pprint



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



