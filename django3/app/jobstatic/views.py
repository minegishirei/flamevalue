from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')



from functools import reduce
from operator import add
import datetime
import pprint
import wikipedia
# 言語を日本語に設定
wikipedia.set_lang("jp")

origin = [
    {
        "会社名":"yahoo株式会社",
        "規模" : 400,
        "年収": 800,
        "残業時間": 30,
        "年齢": 20,
        "日付" : "2022-09-08"
    },
    {
        "会社名":"パーソルキャリア",
        "規模" : 300,
        "年収": 500,
        "残業時間": 0,
        "年齢": 30,
        "日付" : "2022-08-01"
    },
        {
            
        "会社名":"パナソニック",
        "規模" : 400,
        "年収": 350,
        "残業時間": 60,
        "年齢": 30,
        "日付" : "2022-08-22"
    },
        {
            
        "会社名":"アクセンチュア",
        "規模" : 400,
        "年収": 300,
        "残業時間": 70,
        "年齢": 30,
        "日付" : "2022-07-31"
    },
        {
            
        "会社名":"ニトリHD",
        "規模" : 400,
        "年収": 400,
        "残業時間": 50,
        "年齢": 45,
        "日付" : "2022-07-30"
    },
]

def row_converter(row):
    """
    一列の辞書→指定の配列
    """
    return {
        "money" : row["年収"],
        "overtime" : row["残業時間"],
        "age" : row["年齢"]
    }


def grep(column):
    def no_name(row):
        return row[column]
    return no_name
def average_data(origin, column):
    grep_column = grep(column)
    return reduce(lambda value, i_dict: value + grep_column(i_dict), origin, 0)/len(origin)


def basic(origin):
    if len(origin) < 1:
        return {
            "money" : 0,
            "overtime" : 0,
            "age" : 0,
            "count" : 0,
            "size" : 0
        }
    return {
        "money" : average_data(origin, "年収"),
        "overtime" : average_data(origin, "残業時間"),
        "age" : average_data(origin, "年齢"),
        "size" : average_data(origin, "規模"),
        "count" : len(origin)
    }
def TEST_average_data():
    expect = 470
    actual = basic(origin)["money"]
    assert expect == actual , f"error : test_average_data expected : {expect}, actual: {actual}" 

"""
def scoring(basic_dict):
    def score(key,value):
        # TODO:外に出してもいい
        max_values = {
            "money" : 800,
            "overtime" : 50,
            "age" : 65,
            "count" : 10,
            "size" : 400
        }
        return (value/max_values[key])*5
    return {key: score(key, value) for key, value in basic_dict.items()}
"""
def scoring_cuury(score):
    def inside_cuury(basic_dict):
        return {key: score(key, value) for key, value in basic_dict.items()}
    return inside_cuury

def score(key,value):
    # TODO:外に出してもいい
    max_values = {
        "money" : 800,
        "overtime" : 50,
        "age" : 65,
        "count" : 10,
        "size" : 400
    }
    return (value/max_values[key])*5
def score_100(key,value):
    # TODO:外に出してもいい
    max_values = {
        "money" : 800,
        "overtime" : 50,
        "age" : 65,
        "count" : 10,
        "size" : 400
    }
    return int((value/max_values[key])*100)

scoring = scoring_cuury(score)
scoring_100 = scoring_cuury(score_100)
def TEST_scoring():
    expect = 30
    result = scoring(basic(origin))
    actual = result["money"]
    assert  actual < expect , f"error : test_average_data expected : {expect}, actual: {actual}, result {result}" 


def split_timetable(origin):
    sorted_origin = sorted(origin, key=lambda row:datetime.datetime.strptime(row["日付"], '%Y-%m-%d'))
    date_list = [datetime.datetime.now() + datetime.timedelta(days=i) for i in range(0,-60,-7)]
    return_timetable = [{ "date": i.strftime("%Y-%m-%d"), "origin":[]} for i in date_list]
    for i_job in sorted_origin:
        for i, i_date in enumerate(date_list):
            if i_date < datetime.datetime.strptime(i_job["日付"], '%Y-%m-%d'):
                return_timetable[i]["origin"].append(i_job)
                break
    return return_timetable
def TEST_split_timetable():
    timetable = split_timetable(origin)
    pprint.pprint(timetable)
    assert timetable[1], "error : TEST_split_timetable"


TEST_average_data()
TEST_scoring()
TEST_split_timetable()



def index(request, htmlname):
    name = htmlname
    total_score = round( sum(scoring(basic(origin)).values())/len(scoring(basic(origin))), 2)
    total_score_int = int(total_score)
    data_param = {
        "name" : name,
        "explain" : "Django（ジャンゴ）は、Pythonで実装されたWebアプリケーションフレームワーク"
    }
    data_param.update({
        "total_score" :  total_score,
        "stars" : "★"*total_score_int + "☆"*(5-total_score_int),
        "icons" : "...png",
        "basic" : basic(origin),
        "score" : scoring(basic(origin)),
        "score_100" : scoring_100(basic(origin)),
        "basic_graph" : [ {row["date"]: basic(row["origin"])} for row in split_timetable(origin) ],
        "score_graph" : [ {row["date"]: scoring(basic(row["origin"]))} for row in split_timetable(origin) ],
        "money_sorted" : sorted(origin, key=lambda row:row["年収"]),
        "raw" : origin
    })
    data_param.update({
        "comments" : [
            "swiftはiosのアプリケーションを動かせるプログラミング言語だ。 androidではkotlinを扱うが、iosではswiftを使って記述する。。",
            "国内のswift求人は上昇傾向ではあり、収入も他言語と比べて高い。",
            "しかしながらswiftはバージョンアップの頻度が高く、全方互換性を保てない点がネックだ。"
        ]
    })
    data_param.update({
        "others" : [
            {},
            {},
            {},
        ]
    })
    html_param = {
        "title" : "Djangoの年収はいくら！？",
        "description" : "~~~~~"
    }
    wikipedia_param = get_wiki_explain(name)
    
    param = {}
    param.update(data_param)
    param.update(html_param)
    param.update(wikipedia_param)
    pprint.pprint(param)
    return render(request, f"jobstatic/index.html", param)


def get_wiki_explain(name):
    words = wikipedia.search(name)
    page = wikipedia.page(words[0], auto_suggest=False)
    return {
        "explain" : "。".join(page.summary.split("。")[:4]),
        "comments" : (page.summary.split("。")[4:7]),
        "image" : page.images[0]
    } 

"""yahoo

dj00aiZpPXVJMVo2SUkyT3lWRyZzPWNvbnN1bWVyc2VjcmV0Jng9ZGE-

https://job.yahooapis.jp/v1/furusato/jobinfo/?appid=dj00aiZpPXVJMVo2SUkyT3lWRyZzPWNvbnN1bWVyc2VjcmV0Jng9ZGE-

https://job.yahooapis.jp/v1/furusato/jobinfo/?appid=dj00aiZpPXVJMVo2SUkyT3lWRyZzPWNvbnN1bWVyc2VjcmV0Jng9ZGE-&title=python

"""


"""Indeed
client:5cdf0fc3d676bcfaf24dee73c12693db6c313cdf1921a66bfb1db72faa281bc6

s：EEEb4s5SHV9CKncOk7faLSx2h3e3GmksR9vta94b2kP7u5hCNPhsZHY9tlFT1sOu


curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: application/json' \
  -d 'grant_type=client_credentials' \
  -d 'scope=employer_access' \
  -d 'client_id=5cdf0fc3d676bcfaf24dee73c12693db6c313cdf1921a66bfb1db72faa281bc6' \
  -d 'client_secret=EEEb4s5SHV9CKncOk7faLSx2h3e3GmksR9vta94b2kP7u5hCNPhsZHY9tlFT1sOu' \
  https://apis.indeed.com/oauth/v2/tokens/get-job


{"access_token":"eyJraWQiOiIwMjhiOTNmMi1lYzAzLTRmZTAtYmM4NS04OWIxMGU3YWI2MjIiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJhcHA6NWNkZjBmYzNkNjc2YmNmYWYyNGRlZTczYzEyNjkzZGI2YzMxM2NkZjE5MjFhNjZiZmIxZGI3MmZhYTI4MWJjNiIsImFwcF9hY2NvdW50IjoiZDQ2NjA5YWRjYzk4ZDQxZiIsImF6cCI6IjVjZGYwZmMzZDY3NmJjZmFmMjRkZWU3M2MxMjY5M2RiNmMzMTNjZGYxOTIxYTY2YmZiMWRiNzJmYWEyODFiYzYiLCJzY29wZSI6ImVtcGxveWVyX2FjY2VzcyIsImlzcyI6Imh0dHBzOlwvXC9zZWN1cmUuaW5kZWVkLmNvbSIsImV4cCI6MTY2MjU0NzExMywiaWF0IjoxNjYyNTQzNTEzfQ.B7j3eem0nhN4XxBRXDcWugCFfRbHTuAzGX8xGKzM9do_RkKjVEjFrjfj5BonC4_LqTNb3XPGbRunjvv8ik7_Uw","scope":"employer_access","token_type":"Bearer","expires_in":3600}%          


curl -H 'Authorization:Bearer eyJraWQiOiIwMjhiOTNmMi1lYzAzLTRmZTAtYmM4NS04OWIxMGU3YWI2MjIiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJhcHA6NWNkZjBmYzNkNjc2YmNmYWYyNGRlZTczYzEyNjkzZGI2YzMxM2NkZjE5MjFhNjZiZmIxZGI3MmZhYTI4MWJjNiIsImFwcF9hY2NvdW50IjoiZDQ2NjA5YWRjYzk4ZDQxZiIsImF6cCI6IjVjZGYwZmMzZDY3NmJjZmFmMjRkZWU3M2MxMjY5M2RiNmMzMTNjZGYxOTIxYTY2YmZiMWRiNzJmYWEyODFiYzYiLCJzY29wZSI6ImVtcGxveWVyX2FjY2VzcyIsImlzcyI6Imh0dHBzOlwvXC9zZWN1cmUuaW5kZWVkLmNvbSIsImV4cCI6MTY2MjU0NzExMywiaWF0IjoxNjYyNTQzNTEzfQ.B7j3eem0nhN4XxBRXDcWugCFfRbHTuAzGX8xGKzM9do_RkKjVEjFrjfj5BonC4_LqTNb3XPGbRunjvv8ik7_Uw' https://secure.indeed.com/v2/api/appinfo



5cdf0fc3d676bcfaf24dee73c12693db6c313cdf1921a66bfb1db72faa281bc6


http://api.indeed.com/ads/apisearch?publisher=#eyJraWQiOiIwMjhiOTNmMi1lYzAzLTRmZTAtYmM4NS04OWIxMGU3YWI2MjIiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJhcHA6NWNkZjBmYzNkNjc2YmNmYWYyNGRlZTczYzEyNjkzZGI2YzMxM2NkZjE5MjFhNjZiZmIxZGI3MmZhYTI4MWJjNiIsImFwcF9hY2NvdW50IjoiZDQ2NjA5YWRjYzk4ZDQxZiIsImF6cCI6IjVjZGYwZmMzZDY3NmJjZmFmMjRkZWU3M2MxMjY5M2RiNmMzMTNjZGYxOTIxYTY2YmZiMWRiNzJmYWEyODFiYzYiLCJzY29wZSI6ImVtcGxveWVyX2FjY2VzcyIsImlzcyI6Imh0dHBzOlwvXC9zZWN1cmUuaW5kZWVkLmNvbSIsImV4cCI6MTY2MjU0NzExMywiaWF0IjoxNjYyNTQzNTEzfQ.B7j3eem0nhN4XxBRXDcWugCFfRbHTuAzGX8xGKzM9do_RkKjVEjFrjfj5BonC4_LqTNb3XPGbRunjvv8ik7_Uw&format=json&q=ゲーム&l=東京都&radius=20&limit=4&co=jp&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2

https://pubwebapp.indeed.com/jobroll/traffic

https://developer.indeed.com/docs/publisher-jobs/get-job
"""
