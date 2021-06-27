from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Niconico
import datetime

dt_now = datetime.datetime.now()

repo = "twitter_json"
filename = "access_ranking" + dt_now.strftime('%Y%m%d')

favicon = "http://fanstatic.short-tips.info/static/dashboard/img2/static.png"
img =     "http://fanstatic.short-tips.info/static/dashboard/img2/thumbnail2.png"
site_explain = "アニメ、漫画のコミュニティをtwitterの検索結果から分析します。"
ranking_list = []#Niconico.niconicoRanking()


def sitemap(request):
    return render(request,f"fanstatic/sitemap.xml")

def index(request):
    writeNicoRank(filename)
    ranking_list = readNicoRank(filename)
    result = seach(request)
    if result:
        return result
    htmlname = "index.html"
    params = {
        "title" : "コミュニティ分析サイト",
        "description" : "アニメ、漫画のコミュニティをtwitterの検索結果から分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    params.update({
        "ranking_list":ranking_list
    })
    return render(request,f"fanstatic/dashboard/top/{htmlname}",params)


def pop_page(request):
    writeNicoRank(filename)
    ranking_list = readNicoRank(filename)
    result = seach(request)
    if result:
        return result
    htmlname = "pop_page.html"
    params = {
        "title" : "人気ランキング | コミュニティ分析サイト",
        "description" : "アニメ、漫画のコミュニティをtwitterの検索結果から分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    params.update({
        "ranking_list":ranking_list
    })
    return render(request,f"fanstatic/dashboard/top/{htmlname}",params)



def all_page(request):
    result = seach(request)
    if result:
        return result
    writeNicoRank(filename)
    #ranking_list = readNicoRank(filename)
    page_list = Github.seach_page_list(repo)
    htmlname = "all_page.html"
    params = {
        "title" : "ページ一覧 | コミュニティ分析サイト",
        "description" : "アニメ、漫画のコミュニティをtwitterの検索結果から分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    params.update({
        "ranking_list":page_list
    })
    return render(request,f"fanstatic/dashboard/top/{htmlname}",params)


# Create your views here.
def page(request, htmlname, pagetype):
    writeNicoRank(filename)
    ranking_list = readNicoRank(filename)
    explain = ""
    metadata = {}
    for content in ranking_list:
        if content["name"] == htmlname:
            metadata = content
            explain = metadata["description"]
    if explain == "":
        explain = site_explain
    result = seach(request)
    if result:
        return result
    params = {
        "title" : htmlname + " | コミュニティ分析",
        "description" : explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
        "explain": explain
    }
    if Github.has_already_created(repo, htmlname):
        return render(request,f"fanstatic/dashboard/{pagetype}",params)
    else:
        #処理は次のページに任せて、まずは飛ぶ
        return render(request,f"fanstatic/dashboard/data_loading.html",params)

def creation_page(request, htmlname, pagetype):
    result = seach(request)
    if result:
        return result
    params = {
        "title" : htmlname + " | コミュニティ分析",
        "description" : "アニメ、漫画のコミュニティをtwitterの検索結果から分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }


def data_loading(request, htmlname):
    result = seach(request)
    if result:
        return result
    params = {
        "title" : "コミュニティ分析サイト",
        "description" : "アニメ、漫画のコミュニティをtwitterの検索結果から分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    if not Github.has_already_created(repo, htmlname):
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list(htmlname, amount=50)
        text= json.dumps(tweet_list, ensure_ascii=False, indent=4)
        Github.upload("twitter_json", htmlname, text)
    return render(request,f"fanstatic/dashboard/dashboard.html",params)


def seach(request):
    if "request_word" in request.GET:
        request_word = request.GET["request_word"]
        return redirect(f"/page/{request_word}/dashboard.html")
    return False

import os
def writeNicoRank(filename):
    filepath = f"/app/static/dashboard/database/{filename}"
    if not os.path.exists(filepath):
        ranking_list = Niconico.niconicoRanking()
        text = json.dumps(ranking_list, ensure_ascii=False, indent=4)
        with open(filepath, "w") as f:
            f.write(text)


def readNicoRank(filename):
    filepath = f"/app/static/dashboard/database/{filename}"
    with open(filepath, "r") as f:
        return json.load(f)