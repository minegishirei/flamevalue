import requests
import json
import pprint
import time


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



def calc_distance(a, b):
    if a == b: return 0
    a_k = len(a)
    b_k = len(b)
    if a == "": return b_k
    if b == "": return a_k
#1---格納するための表
    matrix = [[] for i in range(a_k+1)]
#2---初期化
    for i in range(a_k+1):
        matrix[i] = [0 for j in range(b_k+1)]
#3---0時の初期値を設定
    for i in range(a_k+1):
        matrix[i][0] = i
    for j in range(b_k+1):
        matrix[0][j] = j
#4---表を埋める
    for i in range(1, a_k+1):
        ac = a[i-1]
        for j in range(1, b_k+1):
            bc = b[j-1]
            cost = 0 if (ac == bc) else 1
            matrix[i][j] = min([
                matrix[i-1][j] + 1,
                matrix[i][j-1] + 1,
                matrix[i-1][j-1] + cost
            ])
    return matrix[a_k][b_k]


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
