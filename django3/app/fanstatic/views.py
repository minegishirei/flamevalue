from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import datetime
import NatureLang

dt_now = datetime.datetime.now()

repo = "twitter_json"
filename = "access_ranking" + dt_now.strftime('%Y%m%d')

favicon = "http://fanstatic.short-tips.info/static/dashboard/img2/static.png"
img =     "http://fanstatic.short-tips.info/static/dashboard/img2/thumbnail2.png"
site_explain = "あなたのアカウントを可能な限り分析します"
ranking_list = []


def get_pagetype_title(key):
    pagetype_title_dict = {
        "dashboard.html" : " | コミュニティ分析",
        "charts.html" : " | 市場調査ツール",
        "word_cloud.html" : "が一目で分かる！"
    }
    if key in pagetype_title_dict:
        return pagetype_title_dict[key]
    return " | コミュニティ分析"


def sitemap(request):
    return render(request,f"fanstatic/sitemap.xml")

def index(request):
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
        "title" : htmlname + get_pagetype_title(pagetype),
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
        "description" : site_explain,
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
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    if not Github.has_already_created(repo, htmlname):
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list(htmlname, amount=50)
        
        git_json = {}
        git_json.update({
            "tweet_list" : tweet_list
        })

        git_json.update({
            "wordcloud" : genWordList(tweet_list)
        })

        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.upload("twitter_json", htmlname, text)
    return render(request,f"fanstatic/dashboard/dashboard.html",params)


def seach(request):
    if "request_word" in request.GET:
        request_word = request.GET["request_word"]
        return redirect(f"/page/{request_word}/dashboard.html")
    return False



def genWordList(tweet_list):
    all_text = ""
    for tweet in tweet_list:
        text = tweet["text"]
        all_text += text
    
    return_list = []
    for text in all_text[: :400]:
        return_list.extend( NatureLang.get_wordlist(text) )
    0/0
    return return_list


