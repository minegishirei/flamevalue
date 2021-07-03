# Create your views here.
from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
dt_now = datetime.datetime.now()

all_ranking_static = "/static/engineer/data/"
all_ranking_folder = "/app/static/engineer/data/"
all_ranking_filename = "access_ranking" + dt_now.strftime('%Y%m%d') +".json"

repo = "engineer_rank"

favicon = "http://fanstatic.short-tips.info/static/dashboard/img2/static.png"
img =     "http://fanstatic.short-tips.info/static/dashboard/img2/thumbnail2.png"
site_explain = "エンジニアのためのツイートランキングサイト"
site_name = "テック・ツイ・ランク"



tag_list = Github.seach_page_list(repo)


def sitemap(request):
    return render(request,f"fanstatic/sitemap.xml")

def about(request):
    htmlname = "about.html"
    params = {
        "title" : "エンジニア・ツイッターランキング | " + site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
        "tag_list" : tag_list
    }
    return render(request,f"ranking/{htmlname}",params)


def index(request,):
    htmlname = "index.html"
    tag_list = Github.seach_page_list(repo)
    if not Statichub.does_exists(all_ranking_folder + all_ranking_filename):
        min_retweet = 300
        pop_list = []
        for tag in tag_list:
            try:
                json_string = Github.load(repo, tag)
            except:
                continue
            tweet_list = json.loads( json_string)["tweet_list"]
            for tweet in tweet_list:
                if tweet["retweet_count"] > min_retweet:
                    pop_list.append(tweet)
        text = json.dumps(pop_list, ensure_ascii=False, indent=4)
        Statichub.write(all_ranking_folder + all_ranking_filename, text)
        
    params = {
        "title" : "エンジニア・ツイッターランキング | " + site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
        "tag_list" : tag_list,
        "all_ranking_file" : all_ranking_static + all_ranking_filename
    }
    return render(request,f"ranking/{htmlname}",params)


def all_page(request, htmlname, pagetype):
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
    return render(request, f'engineer_rank/top/', params)

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



