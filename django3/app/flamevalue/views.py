from .careerJet import clear_jnet,mock_getCareerJet, row_converter, getCareerJet
from .wikipedia_list import get_wikipedia_list
from .JsonIO import JsonDictionalyManager, JsonIO
from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
from .my_mecab import getMeishiList


from functools import reduce
from operator import add
import datetime
import pprint
import wikipedia
# 言語を日本語に設定
wikipedia.set_lang("jp")


            
jsonDictionalyManager = JsonDictionalyManager()
FLAMEWORKDICT = jsonDictionalyManager.generate_all_flameworkdict()


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
        "money" : round(average_data(origin, "年収")),
        "overtime" : round(average_data(origin, "残業時間")),
        "age" : round(average_data(origin, "年齢")),
        "size" : round(average_data(origin, "規模")),
        "count" : len(origin)
    }
def TEST_average_data():
    expect = 470
    actual = basic(origin)["money"]
    assert expect == actual , f"error : test_average_data expected : {expect}, actual: {actual}" 


def scoring_cuury(score):
    def inside_cuury(basic_dict):
        return {key: score(key, value) for key, value in basic_dict.items()}
    return inside_cuury

def score_currey(max_score, max_values):
    def score(key,value):
        result =  (value/max_values[key])*max_score 
        if result > max_score:
            return max_score
        else:
            return result
    return score

max_values = {
    "money" : 700,
    "overtime" : 1000,
    "age" : 30,
    "count" : 10000,
    "size" : 1000
}
score       = score_currey(5, max_values)
score_100   = score_currey(100, max_values)

scoring = scoring_cuury(score)
scoring_100 = scoring_cuury(score_100)
def TEST_scoring():
    expect = 30
    result = scoring(basic(origin))
    actual = result["money"]
    assert  actual < expect , f"error : test_average_data expected : {expect}, actual: {actual}, result {result}" 


def split_timetable(origin):
    sorted_origin = sorted(origin, key=lambda row:datetime.datetime.strptime(row["日付"], '%Y-%m-%d'))
    date_list = [datetime.datetime.now() + datetime.timedelta(days=i) for i in range(-3,-60,-3)]
    return_timetable = [{ "date": i.strftime("%Y-%m-%d"), "origin":[]} for i in date_list]
    for i_job in sorted_origin:
        for i, i_date in enumerate(date_list):
            date1 = datetime.datetime.strptime(i_job["日付"], '%Y-%m-%d')
            date2 = datetime.datetime.strptime(i_job["日付"], '%Y-%m-%d') - datetime.timedelta(days=7)
            if  date2 < i_date and i_date < date1:
                return_timetable[i]["origin"].append(i_job)
    return_timetable = list(reversed(return_timetable))
    return return_timetable
def TEST_split_timetable():
    timetable = split_timetable(origin)
    pprint.pprint(timetable)
    assert timetable[1], "error : TEST_split_timetable"


TEST_average_data()
TEST_scoring()
TEST_split_timetable()




def get_wiki_explain(name):
    words = wikipedia.search(name)
    page = wikipedia.page(words[0], auto_suggest=False)
    return {
        "explain" : "。".join(page.summary.split("。")[:4]),
        "comments" : (page.summary.split("。")[4:7]),
        "image" : page.images[0]
    }

def build_param(name):
    origin = getCareerJet(name.replace("(プログラミング言語)", ""))
    jobs = origin["jobs"]
    hits = origin["hits"]
    origin = row_converter(clear_jnet(jobs))
    total_score = round( sum(scoring(basic(origin)).values())/len(scoring(basic(origin))), 2)
    total_score_int = int(round(total_score) )
    data_param = {
        "name" : name,
        "explain" : "Django（ジャンゴ）は、Pythonで実装されたWebアプリケーションフレームワーク"
    }
    basic_info = basic(origin)
    basic_info.update({
        "count" : hits
    })
    wordcount_list =  getMeishiList("。".join([row["description"] for row in jobs]))
    data_param.update({
        "total_score" :  total_score,
        "stars" : "★"*total_score_int + "☆"*(5-total_score_int),
        "icons" : "...png",
        "basic" : basic_info,
        "score" : scoring(basic_info),
        "score_100" : scoring_100(basic_info),
        "basic_graph" : [ {row["date"]: basic(row["origin"])} for row in split_timetable(origin) ],
        "score_graph" : [ {row["date"]: scoring(basic(row["origin"]))} for row in split_timetable(origin) ],
        "score_graph_json" : json.dumps([ {"date": row["date"], "values" : scoring(basic(row["origin"]))} for row in split_timetable(origin) ]),
        "money_sorted" : sorted(origin, key=lambda row:row["年収"]),
        "jobs" : clear_jnet(jobs),
        "min_salary" : sorted( clear_jnet(jobs), key=lambda row:row["salary_min"]),
        "wordcloud_json" : json.dumps(wordcount_list, ensure_ascii=False )
    })
    html_param = {
        "title" : f"{name} 「年収/採用企業」 フレームワークの転職評価 FlameValue",
        "description" : f"{name}の「年収/採用企業情報」。就職・転職前に{name}の働く環境、年収・求人数などをリサーチ。就職・転職のための「{name}」の価値分析チャート、求人情報、フレームワークランキングを掲載。"
    }
    wikipedia_param = get_wiki_explain(name)
    related_word = [ row_v2["word"] for row_v2 in wordcount_list]
    wikipedia_related = {"wikipedia_related": list(filter(lambda row : (row["name"] in related_word) , FLAMEWORKDICT) )}
    
    param = {}
    param.update(data_param)
    param.update(html_param)
    param.update(wikipedia_param)
    param.update(wikipedia_related)
    return param

def page(request, htmlname):
    name = htmlname
    param = {}
    jsonIO = JsonIO()
    if jsonIO.exists(name) and (not request.GET.get("reload") ):
        param = jsonIO.read(name)
    else:
        param = build_param(name)
        jsonIO.write(param["name"],param)
    return render(request, f"jobstatic/page.html", param)

def index(request):
    global FLAMEWORKDICT
    if request.GET.get("reload"):
        FLAMEWORKDICT = jsonDictionalyManager.generate_all_flameworkdict()
    name = "フレームワーク"
    param = {
        "title" : "「年収/採用企業」FlameValue フレームワークの転職評価",
        "description" : f"「年収/採用企業情報」。就職・転職前に{name}の働く環境、年収・求人数などをリサーチ。就職・転職のための「{name}」の価値分析チャート、求人情報、フレームワークランキングを掲載。",
        "FLAMEWORKDICT" : sorted(FLAMEWORKDICT, key=lambda x: x["total_score"], reverse=True)
    }
    return render(request, f"jobstatic/index.html", param)

def sitemap(request):
    param = {
        "pop_page_list" : jsonDictionalyManager.generate_all_flameworkdict(),
    }
    return render(request, f"jobstatic/sitemap.xml", param)

def robots(request):
    return render(request, f"robots.txt")

def reverse_index(request):
    return redirect("/")

