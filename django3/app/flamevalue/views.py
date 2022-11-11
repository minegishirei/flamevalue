from .careerJet import clear_jnet,mock_getCareerJet, row_converter, getCareerJet
from .wikipedia_list import get_wikipedia_list
from .JsonIO import JsonDictionalyManager, JsonIO
from .my_tools import del_dub_dict_list
from django.shortcuts import render, redirect, HttpResponse
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
from .my_mecab import getMeishiList
from .my_Qiita import getQiitaInfo
from .my_Qiita import getQiitaTags

from functools import reduce
from operator import add
import datetime
import pprint
import wikipedia
# 言語を日本語に設定
wikipedia.set_lang("jp")
from .my_tools import calc_distance
from multiprocessing import Process

            
jsonDictionalyManager = JsonDictionalyManager()
FLAMEWORKDICT = jsonDictionalyManager.generate_all_flameworkdict()





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
        "remote" : round(average_data(origin, "リモート率")),
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
    "age" : 60,
    "count" : 10000,
    "size" : 1000,
    "remote" : 70,
    "qiita_score" : 20000,
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
    assert timetable[1], "error : TEST_split_timetable"

"""
TEST_average_data()
TEST_scoring()
TEST_split_timetable()
"""


def get_money_countlist(origin, column, steps = None):
    origin = sorted(origin, key=lambda row:row[column])
    steps = range(0, 1000, 100)
    count_list = [0 for row in steps]
    for row in origin:
        for i, step in enumerate(steps):
            if row[column] < step and step < row[column] + 100:
                count_list[i] += 1
    return count_list


def get_wiki_explain(name):
    words = wikipedia.search(name)
    page = wikipedia.page(words[0], auto_suggest=False)
    return {
        "explain" : "。".join(page.summary.split("。")[:4]),
        "comments" : (page.summary.split("。")[4:7]),
        "image" : page.images[0]
    }



def get_qiita_comments(name, word):
    def get_good_comment(name, markdown):
        hit_word = re.findall(name+'.?' + word, markdown)[0]
        text1 =  hit_word + "\n" + hit_word.join( markdown.split(hit_word)[1:] )
        text2 = text1[:500]
        new_tag = '#### '
        text2 = re.sub('#+', new_tag, text2)
        text3 = new_tag + "\n" + new_tag.join( text2.split(new_tag)[:1] )
        return text3
    feature_include_list = filter( lambda x: re.findall(name+'.?'+word, x["body"]),getQiitaInfo("title:"+name+word, 100) )
    qiita_comments = []
    for row in feature_include_list:
        target_text = row["body"]
        new_text = get_good_comment(name, target_text)
        row.update({
            "body" : new_text,
            "origin_body" : row["body"],
            "rendered_body" : ""
        })
        if len(new_text) > 100:
            qiita_comments.append(row)
    return qiita_comments



import re
def build_param(name_original):
    name = name_original.replace("(IT)", "").replace("言語", "")
    origin = getCareerJet(name.replace("(プログラミング言語)", ""))
    jobs = origin["jobs"]
    hits = origin["hits"]
    origin = row_converter(clear_jnet(jobs))
    basic_info = basic(origin)

    qiita_info = getQiitaInfo(name, 100)
    basic_info.update({
        "count" : hits,
        #"qiita_score" : reduce(lambda a, b: a + int(b["user"]["followees_count"]), qiita_info, 0) / len(qiita_info)
    })
    qiita_tags = getQiitaTags(name.replace("言語",""))
    basic_info.update({
        "qiita_score" : qiita_tags["followers_count"]
    })
    total_score = round( sum(scoring(basic_info).values())/len(scoring(basic_info)), 2)
    total_score_int = int(round(total_score) )
    data_param = {
        "name" : name,
        "explain" : "Django（ジャンゴ）は、Pythonで実装されたWebアプリケーションフレームワーク"
    }

    wordcount_list =  getMeishiList("。".join([row["description"] for row in jobs]))
    data_param.update({
        "date" : datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        "total_score" :  total_score,
        "stars" : "★"*total_score_int + "☆"*(5-total_score_int),
        "basic" : basic_info,
        "score" : scoring(basic_info),
        "score_100" : scoring_100(basic_info),
        "basic_graph" : [ {row["date"]: basic(row["origin"])} for row in split_timetable(origin) ],
        "score_graph" : [ {row["date"]: scoring(basic(row["origin"]))} for row in split_timetable(origin) ],
        "score_graph_json" : json.dumps([ {"date": row["date"], "values" : scoring(basic(row["origin"]))} for row in split_timetable(origin) ]),
        "money_sorted" : sorted(origin, key=lambda row:row["年収"]),
        "jobs" : clear_jnet(jobs),
        "min_salary" : sorted( clear_jnet(jobs), key=lambda row:row["salary_min"]),
        "wordcloud_json" : json.dumps(wordcount_list, ensure_ascii=False ),
        "money_countlist" : json.dumps( {'lower' : get_money_countlist(origin, "年収"), 'upper' : get_money_countlist(origin, "残業時間")} ),
        "qiita_acounts" : sorted( del_dub_dict_list([ row["user"] for row in getQiitaInfo(name, 100) ]) , key=lambda x: x["items_count"], reverse=True )[:5],
        "qiita_comments" : get_qiita_comments(name, "メリット") + get_qiita_comments(name, "特徴")+ get_qiita_comments(name, "とは")
    })
    html_param = {
        "title" : f"{name} 「年収/採用企業」 フレームワークの転職評価 FlameValue",
        "description" : f"{name}の「年収/採用企業情報」。就職・転職前に{name}の働く環境、年収・求人数などをリサーチ。就職・転職のための「{name}」の価値分析チャート、求人情報、フレームワークランキングを掲載。"
    }
    
    wikipedia_param = get_wiki_explain(name_original+"(IT)")
    related_word = [ row_v2["word"] for row_v2 in wordcount_list]
    wikipedia_related = {"wikipedia_related": list(filter(lambda row : (row["name"] in related_word) , FLAMEWORKDICT) )}
    
    param = {}
    param.update(data_param)
    param.update(html_param)
    param.update(wikipedia_param)
    param.update({
        "image" : qiita_tags["icon_url"]
    })
    param.update(wikipedia_related)
    return param


import random
def titleABTest():
    return random.choice([
        lambda name, description: {
            "title" : f"【転職】「{name}の年収って実際どうなの？」 👈",
            "description" : f"{description}"
        },lambda name, description: {
            "title" : f"【転職】{name}の年収は高い",
            "description" : f"{description}"
        }
    ])

def titleProduction():
    return (lambda name, description: {
        "title" : f"【転職】{name}の年収は高い?低い? - Flamevalue",
        "description" : f"{description}"
    })

def page(request, htmlname):
    name = htmlname
    param = {}
    jsonIO = JsonIO()
    if jsonIO.exists(name) and (not request.GET.get("reload") ):
        param = jsonIO.read(name)
    elif request.GET.get("reload"):
        param = build_param(name)
        jsonIO.write(param["name"],param)
    else:
        return redirect("/")
    p = Process(target = reload_subprocess, args=(name,))
    p.start()
    GET_active = request.GET.get("active")
    if GET_active == "jobs":
        param.update({
            "title" : f"{name} の「求人一覧」 FlameValue",
            "description" : f"{name}株式会社の採用情報です。FlameValueは{name}の採用情報・求人情報を掲載しています。"
        })
    elif GET_active == "comments":
        param.update({
            "title" : f"{name}の「すべてのクチコミ」 FlameValue",
            "description" : f"{name}ユーザーによる「すべての開発者クチコミ」のクチコミ・評価レビュー。{name}の採用を検討されている方が、{name}の「すべての開発者クチコミ」を把握するための参考情報として、{name}を使用した開発者から「すべての開発者クチコミ」に関するクチコミを収集し掲載しています。就職・採用活動での一段深めた開発者リサーチにご活用いただけます。"
        })
    else:
        """
        try:
            param.update(titleABTest()(name,param["qiita_comments"][0]["body"].replace("\n","")))
        except:
            param.update(titleABTest()(name,param["explain"].replace("\n","") ) ) 
        """
        param.update(titleProduction()(name,param["explain"].replace("\n","") ))
    return render(request, f"jobstatic_pages/page.html", param)

def ranking(request):
    params = {
        "title" : f"プログラミング言語 年収ランキング {datetime.datetime.now().strftime('%Y年%m月%d日')} 最新版",
        "description" : f"{datetime.datetime.now().strftime('%Y年%m月%d日')}更新 Flamevalue プログラミング言語やフレームワークを年収ごとにランキング化。技術選定や学習するプログラミング言語選びにFlamevalue",
        "ranking_list" : sorted(FLAMEWORKDICT, key=lambda x: x["basic"]["money"], reverse=True),
        "img" : "https://github.com/kawadasatoshi/minegishirei/blob/main/flamevalue/flamevalue.png?raw=true"
    }
    return render(request, f"jobstatic_pages/ranking.html", params)

def index(request):
    global FLAMEWORKDICT
    FLAMEWORKDICT = jsonDictionalyManager.generate_all_flameworkdict()
    if request.GET.get("refresh_all"):
        p = Process(target=refresh_all)
        p.start()
    name = "フレームワーク"
    param = {
        "title" : "「年収/採用企業」FlameValue フレームワークの転職評価",
        "description" : f"「年収/採用企業情報」。就職・転職前に{name}の働く環境、年収・求人数などをリサーチ。就職・転職のための「{name}」の価値分析チャート、求人情報、フレームワークランキングを掲載。",
        "FLAMEWORKDICT" : sorted(FLAMEWORKDICT, key=lambda x: x["total_score"], reverse=True),
        "img" : "https://github.com/kawadasatoshi/minegishirei/blob/main/flamevalue/flamevalue.png?raw=true"
    }
    return render(request, f"jobstatic_pages/index.html", param)

def sitemap(request):
    param = {
        "pop_page_list" : jsonDictionalyManager.generate_all_flameworkdict(),
    }
    return render(request, f"jobstatic_pages/sitemap.xml", param)

def robots(request):
    return render(request, f"robots.txt")

def reverse_index(request):
    return redirect("/")


def api_candidate(request):
    unfinished_title = request.GET.get("unfinished_title")
    sorted_flamework_list = list(map(lambda x: x["name"], sorted(FLAMEWORKDICT, key=lambda x: calc_distance(x["name"], unfinished_title))))
    json_dict = {
        "candidate" : sorted_flamework_list
    }
    json_str = json.dumps(json_dict, ensure_ascii=False, indent=2) 
    return HttpResponse(json_str)

import time
def refresh_all():
    global FLAMEWORKDICT
    jsonIO = JsonIO()
    for row in FLAMEWORKDICT:
        time.sleep(1)
        name = row["name"]
        try:
            param = build_param(name)
            jsonIO.write(param["name"],param)
            print("【reflash】 : ", name)
        except:
            print("【reflash_missed!!!】 : ", name)


def reload_subprocess(name):
    jsonIO = JsonIO()
    param = build_param(name)
    jsonIO.write(param["name"],param)