
from careerJet import clear_jnet,mock_getCareerJet, row_converter, getCareerJet
from functools import reduce
from operator import add
import datetime
import pprint
import wikipedia
# 言語を日本語に設定
wikipedia.set_lang("jp")
from my_tools import calc_distance
from multiprocessing import Process
import random
import math            
from my_mecab import getMeishiList
from my_Qiita import getQiitaInfo
from my_Qiita import getQiitaTags
from my_Qiita import putQiitaArticle

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



import re
def build_param(name_original):
    print("start")
    name = name_original
    origin = getCareerJet(name.replace("(プログラミング言語)", ""))
    jobs = origin["jobs"]
    hits = origin["hits"]
    origin = row_converter(clear_jnet(jobs))
    basic_info = basic(origin)
    qiita_info = getQiitaInfo(name, 100)
    basic_info.update({
        "count" : hits,
        "qiita_score" : reduce(lambda a, b: a + int(b["user"]["followees_count"]), qiita_info, 0) / len(qiita_info)
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
    print(data_param)

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
        # Administrator用のコメント
        #"admin_comment" : getAdminMarkdown(name),
        # 本当はここに書きたいが、Goodを押した後の時差の関係で後ほどupdate
        #"goodness_count" : SQLiteFlamevalueControl().get_goodness_count(flamework_name = name)[0][0]
    })
    html_param = {
        "title" : f"{name} 「年収/採用企業」 フレームワークの転職評価 FlameValue",
        "description" : f"{name}の「年収/採用企業情報」。就職・転職前に{name}の働く環境、年収・求人数などをリサーチ。就職・転職のための「{name}」の価値分析チャート、求人情報、フレームワークランキングを掲載。"
    }
    print(data_param)

    wikipedia_param = get_wiki_explain(name_original+"(IT)")
    related_word = [ row_v2["word"] for row_v2 in wordcount_list]
    wikipedia_related = {"wikipedia_related": list(filter(lambda row : (row["name"] in related_word) , FLAMEWORKDICT) )}

    comments = []
    try:
        FLAMEVALUE_DATABASE_REPO = "flamevalue_database"
        category = f"comments/{name}"
        for htmlname in Github.seach_page_list(FLAMEVALUE_DATABASE_REPO, category):
            row_json = Github.load(FLAMEVALUE_DATABASE_REPO, category + "/" +htmlname)
            comments.append( json.loads(row_json) )
    except:
        pass

    param = {}
    comments_param = {
        "user_comments" : comments
    }
    param.update(comments_param)
    param.update(data_param)
    param.update(html_param)
    param.update(wikipedia_param)
    param.update({
        "image" : qiita_tags["icon_url"]
    })
    param.update(wikipedia_related)
    return param

if __name__=="__main__":
    build_param("Java")