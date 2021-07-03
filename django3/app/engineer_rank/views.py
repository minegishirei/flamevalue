# Create your views here.
from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github

import datetime

dt_now = datetime.datetime.now()

repo = "engineer_rank"

favicon = "http://fanstatic.short-tips.info/static/dashboard/img2/static.png"
img =     "http://fanstatic.short-tips.info/static/dashboard/img2/thumbnail2.png"
site_explain = "エンジニアのためのツイートランキングサイト"
site_name = "テック・ツイ・ランク"

tag_list = Github.seach_page_list(repo)


def sitemap(request):
    return render(request,f"fanstatic/sitemap.xml")

def index(request):
    htmlname = "index.html"
    params = {
        "title" : "エンジニア・ツイッターランキング | " + site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    return render(request,f"engineer_rank/top/{htmlname}",params)



# Create your views here.
def page(request, htmlname, pagetype):
    params = {
        "title" : htmlname + " | "+site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
        "explain": site_explain,
        "tag_list" : tag_list
    }
    if Github.has_already_created(repo, htmlname):
        return render(request,f"ranking/{pagetype}",params)
    else:
        #処理は次のページに任せて、まずは飛ぶ
        return render(request,f"ranking/data_loading.html",params)


def data_loading(request, htmlname):
    
    params = {
        "title" : htmlname + " | " + site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
        "explain": site_explain,
        "tag_list" : tag_list
    }
    

    if not Github.has_already_created(repo, htmlname):
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list('"'+ htmlname+ '"' + " lang:ja min_faves:100", amount=50)
        
        git_json = {}
        git_json.update({
            "tweet_list" : tweet_list
        })

        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.upload(repo, htmlname, text)
    return render(request,f"ranking/ranking.html",params)



