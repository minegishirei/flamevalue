from .careerJet import clear_jnet,mock_getCareerJet, row_converter, getCareerJet
from .wikipedia_list import get_wikipedia_list
from .JsonIO import JsonDictionalyManager, JsonIO
from .my_tools import del_dub_dict_list
from django.shortcuts import render, redirect, HttpResponse
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
from .my_Admin_Markdown import getAdminMarkdown
from .my_mecab import getMeishiList
from .my_Qiita import getQiitaInfo
from .my_Qiita import getQiitaTags
from .my_Qiita import putQiitaArticle
from .my_SQLite_FlamevalueControl import SQLiteFlamevalueControl
from .my_SQLite_LoginControl import SQLiteLoginControl
from .my_SQLite_UserInfoControl import UserInfoCollector
from .my_SQLite_Profile import SQLiteProfileImage

# .dbファイルの初期化
SQLiteFlamevalueControl().end()
SQLiteLoginControl().end()
UserInfoCollector().end()
SQLiteProfileImage().end()

from functools import reduce
from operator import add
import datetime
import pprint
import wikipedia
# 言語を日本語に設定
wikipedia.set_lang("jp")
from .my_tools import calc_distance
from multiprocessing import Process
import random
import math            

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
    name = name_original
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
        "qiita_comments" : get_qiita_comments(name, "メリット") + get_qiita_comments(name, "特徴")+ get_qiita_comments(name, "とは"),
        # Administrator用のコメント
        "admin_comment" : getAdminMarkdown(name),
        # 本当はここに書きたいが、Goodを押した後の時差の関係で後ほどupdate
        #"goodness_count" : SQLiteFlamevalueControl().get_goodness_count(flamework_name = name)[0][0]
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
        "title" : f"{name}の転職評価 - Flamevalue",
        "description" : f"{description}"
    })



def page(request, htmlname):
    if htmlname == "robots.txt":
        return robots(request)
    
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
    
    # Goodを追加時の処理
    if request.GET.get("active-add-good"):
        has_session_logininfo = (request.session.get("e_mail") and request.session.get("hashed_password") )
        is_certification_ok = SQLiteLoginControl().certification_by_hashed_password(request.session.get("e_mail") , request.session.get("hashed_password", ""))
        if (has_session_logininfo) and (is_certification_ok) :
            SQLiteFlamevalueControl().add_one_good(request.session["e_mail"], htmlname)
        else:
            return redirect("/login.html")
    # Goodカウントを即時反映させるための処理
    param.update({
        "goodness_count" : SQLiteFlamevalueControl().get_goodness_count(flamework_name=htmlname)[0][0]
    })
    
    # 5割の確率でページを再構成する
    if random.random() < 0.5:
        p = Process(target = reload_subprocess, args=(name,))
        p.start()
    
    # コメントや仕事タブを開いた時の処理
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
        param.update(titleProduction()(name,param["explain"].replace("\n","") ))
    return render(request, f"jobstatic_pages/page.html", param)



def ranking(request):
    e_mail = request.session.get("e_mail")
    hashed_password = request.session.get("hashed_password") 
    username = request.session.get("username")
    has_session_info = ("e_mail" in request.session) and ("hashed_password" in request.session)
    is_certification_ok = SQLiteLoginControl().certification_by_hashed_password(request.session.get("e_mail") , request.session.get("hashed_password", ""))
    if has_session_info and (is_certification_ok) :
        pass
    else:
        return redirect("/login.html")
    params = {
        "title" : f"プログラミング言語 年収ランキング {datetime.datetime.now().strftime('%Y年%m月%d日')} 最新版",
        "description" : f"{datetime.datetime.now().strftime('%Y年%m月%d日')}更新 Flamevalue プログラミング言語やフレームワークを年収ごとにランキング化。技術選定や学習するプログラミング言語選びにFlamevalue",
        "img" : "https://github.com/kawadasatoshi/minegishirei/blob/main/flamevalue/flamevalue.png?raw=true"
    }
    params.update({
        "ranking_list" : sorted(FLAMEWORKDICT, key=lambda x: x["basic"]["money"], reverse=True),
    })
    if request.GET.get("active"):
        params.update({
            "ranking_list" : sorted(FLAMEWORKDICT, key=lambda x: x["basic"][request.GET.get("active")], reverse=True)
        })
    
    # テストコード
    #putQiitaArticle("工事中...",  ,"article", "", True)
    print(build_Qiita_context(FLAMEWORKDICT, sort_function = (lambda x: x["basic"]["money"]) ))

    # プログラミング言語年収ランキング
    if random.random() < 0.5:
        putQiitaArticle(
            title = "フレームワーク/プログラミング言語 下方年収ランキング", 
            markdown = build_Qiita_context(FLAMEWORKDICT) ,
            tags = list(map(lambda row:{"name":row["name"]}, sorted(FLAMEWORKDICT, key=lambda x: x["basic"]["money"], reverse=True) ))[:5],
            path = "article", 
            id = "",
            is_private = False
        )
        """
        putQiitaArticle(
            title = "プログラミング言語 転職市場ランキングTop15", 
            markdown = build_Qiita_context(FLAMEWORKDICT) ,
            tags = list(map(lambda row:{"name":row["name"]}, sorted(FLAMEWORKDICT, key=lambda x: x["stars"], reverse=True) ))[:5],
            path = "article", 
            id = "c2acb400a27ab78c22b6",
            is_private = False
        )
        """
    return render(request, f"jobstatic_pages/ranking.html", params)


flamevalue_score_ranking_count = 0

def build_Qiita_context(FLAMEWORKDICT, sort_function = ""):
    global flamevalue_score_ranking_count
    flamevalue_score_ranking_count= 0
    def row_context(row):
        def floor(value):
            return math.floor(value * 100) / 100
        global flamevalue_score_ranking_count
        flamevalue_score_ranking_count += 1
        admin_markdown = None
        return f"""
# 第{flamevalue_score_ranking_count}位 : {row["name"]} : {row["stars"]}

スコア : **{row["total_score"]}**/5

| 項目名            | ポイント(5点満点) | 実績 | 
| :---------------- | ----------------- | ---- | 
| 下限年収          |     {floor(row["score"]["money"])}   |       {row["basic"]["money"]}万円   | 
| 上限年収          |     {floor(row["score"]["overtime"])}|       {row["basic"]["overtime"]}万円    | 
| 求人数            |     {floor(row["score"]["count"])}   |       {row["basic"]["count"]}件  | 
| リモート率        |     {floor(row["score"]["remote"])}  |       {row["basic"]["remote"]}%    | 
| Qiitaフォロワー数 |     {floor(row["score"]["qiita_score"])}|   {row["basic"]["qiita_score"]}人   | 

参考ページ

https://flamevalue.short-tips.info/{row["name"]}


{row.get("admin_comment") if row.get("admin_comment") else ""}
        """

    context = f"""
## この記事の説明

この記事は<a href="https://flamevalue.short-tips.info/"> フレームワークの転職評価 Flamevalue</a> のサイトから引用しております、
プログラミング言語/フレームワークのランキングを表示するものです。

プログラミング言語/フレームワークの評価を、次の5つの観点から点数化しております。
転職やエンジニア採用の際の一つの参考までにご活用下さい。

# ランキング

{"".join(map(lambda row:row_context(row),sorted(FLAMEWORKDICT, key= sort_function, reverse=True)[:15]))}

    """
    flamevalue_score_ranking_count = 0
    return context



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

def search(request):
    param = {
        "title" : "FlameValue各種リンク"
    }
    return render(request, f"jobstatic_pages/search.html", param)

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


def login(request):
    param = {}
    if "create_acount" in request.POST:
        if SQLiteLoginControl().create_acount(request):
            pass
        else:
            param = {
                "error_message" : "アカウント作成に失敗しました。"
            }
            return render(request, f"jobstatic_pages/login.html", param)
        request = get_deleted_all_session(request)
        # アカウント作成後 ハッシュ化されていないパスワードから
        # ハッシュ化されたパスワードをセッションに入れる
        user_info = SQLiteLoginControl().fetch_user_info_by_unhashed_password( request.POST.get("e_mail"), request.POST.get("unhashed_password"))
        request.session.update(user_info)
        return redirect("/")
    elif "login_acount" in request.POST:
        if SQLiteLoginControl().certification_by_unhashed_password(request.POST.get("e_mail") , request.POST.get("unhashed_password")):
            # ハッシュ化されたパスワードをセッションに入れる
            user_info = UserInfoCollector().fetch_user_fullinfo( request.POST.get("e_mail"))
            request.session.update(user_info)
            return index(request)
        else:
            return render(request, f"jobstatic_pages/login.html", param)
    elif "logout_acount" in request.POST:
        request = get_deleted_all_session(request)
        return redirect("/")
    return render(request, f"jobstatic_pages/login.html", param)


def useradmin(request):
    param = {}
    if "update_acount" in request.POST:
        message_list = []
        if request.POST.get("unhashed_password") and SQLiteLoginControl().update_acount_password(request.POST.get("e_mail"), request.POST.get("unhashed_password")):
            user_info = SQLiteLoginControl().fetch_user_info_by_unhashed_password( request.POST.get("e_mail"), request.POST.get("unhashed_password"))
            request.session.update(user_info)
            message_list.append("パスワード設定：完了")
        if request.POST.get("profile_image_url") and SQLiteProfileImage().replace(request.POST.get("e_mail"), request.POST.get("profile_image_url")):
            request.session["profile_image_url"] = SQLiteProfileImage().fetch(request.POST.get("e_mail"))["profile_image_url"]
            message_list.append("プロフィールイメージ設定：完了")
        if request.POST.get("e_mail") and SQLiteLoginControl().update_acount(request.POST.get("e_mail"), request.POST.get("username")):
            message_list.append("メール、ユーザー名設定：完了")
        param.update({
            "message_list" : message_list
        })
    param.update({
        "users" : UserInfoCollector().get_users(),
        "user_good_flameworks" : UserInfoCollector().get_user_good_flameworks(request.session.get("e_mail"))
    })
    return render(request, f"jobstatic_pages/profile.html", param)


def get_deleted_all_session(request):
    session_copy = {}
    for key, value in request.session.items():
        session_copy[key] = value
    for key, value in session_copy.items():
        del request.session[key]
    return request









