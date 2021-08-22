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
import markdown


all_ranking_static = "/static/engineer/data/"
all_ranking_folder = "/app/static/engineer/data/"



favicon = "/static/techblog/img/feature.png"
img =     ""#"/static/techblog/img/feature.png"#"http://techtweetrank.short-tips.info/static/engineer/img/twitter_profile_image.png"
site_explain = "社内SEの業務内容を可能な限りリアルに記しました。これから目指す人も、そうでないエンジニアも楽しめるように書きます！"
site_name = "社内SE雑記ブログ"


repo = "techblog"


def robots(request):
    return render(request, f"robots.txt")

def grep_param(mk, taglist):
    params = {}
    for tag in taglist:
        for line in mk.split("\n"):
            if line.startswith(tag+":"):
                params.update({
                    tag : line.replace(tag + ":", "" )
                })
    return params


def genPageDict():
    page_dict = {}
    for category in ["python", "inhouse_se", "design", "developper", "os", "programming","powershell", "else"]:
        category_dict = {}
        for htmlname in Github.seach_page_list(repo, category):
            mk = Github.load(repo, category + "/" +htmlname)
            md = markdown.Markdown()
            htmltext = md.convert(mk)
            params =  grep_param(mk, ["title", "description", "img"])
            params.update({
                "category" : category,
                "htmlname" : htmlname,
                "htmltext" : htmltext
            })
            category_dict[htmlname] = params

        page_dict[category] = category_dict
    return page_dict

clock = 0
page_dict = genPageDict()

def checkandrenew():
    global clock
    global page_dict
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d%H')
    if clock != now:
        clock = now
        page_dict = genPageDict()
        return True
    return False



def sitemap(request):
    return render(request,f"blog/techblog/page/sitemap.xml")

def sitemap(request):
    pop_page_list = []
    for category_key in page_dict.keys():
        category_dict = page_dict[category_key]
        for html_key in category_dict.keys():
            pop_page_list.append({
                "category" : category_key,
                "htmlname" : html_key
            })

    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d%H')
    pop_page_list_copy = pop_page_list.copy()
    for page in pop_page_list_copy:
        page["lastmod"] = f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    params = {
        "pop_page_list" : pop_page_list_copy
    }
    return render(request,f"blog/techblog/page/sitemap.xml", params)


def index(request):
    global page_dict
    if request.GET.get("reload"):
        page_dict = genPageDict()
    page_list = []
    for category, category_list in page_dict.items():
        for page in category_list.values():
            page_list.append(page)
    params = {
        "page_list" : page_list,
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name
    }
    return render(request,f"blog/techblog/page/index.html",params)


def about(request):
    params = {
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name
    }
    return render(request,f"blog/techblog/page/about.html",params)


# Create your views here.
def page(request, category, htmlname):
    mk = Github.load(repo, category + "/" +htmlname)
    md = markdown.Markdown()
    htmltext = md.convert(mk)
    params = {
        "mk" : mk,
        "htmltext" : htmltext,
        "site_name" : site_name,
        "category" : category,
        "favicon" : favicon
    }
    params.update(grep_param(mk, ["title", "description", "img"]))
    if category=="slides":
        return render(request, "blog/non_base.html",params)

    return render(request,f"blog/techblog/page/mkpage.html", params)


def category_page(request, category_name):
    page_list=[]
    category_dict = page_dict[category_name]
    for category in category_dict.values():
        page_list.append(category)
    params = {
        "page_list" : page_list,
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name,
        "category" : category_name
    }
    
    return render(request,f"blog/techblog/page/category.html", params)


