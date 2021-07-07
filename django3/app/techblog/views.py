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



favicon = "/static/engineer/img/twitter_profile_image.png"
img =     "http://techtweetrank.short-tips.info/static/engineer/img/twitter_profile_image.png"
site_explain = "エンジニアのためのツイートランキングサイト"
site_name = "社内SE雑記ブログ"


repo = "techblog"

def sitemap(request):
    return render(request,f"ranking/sitemap.xml")


def index(request):
    params = {
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "htmlname" : htmlname,
        "tag_list" : tag_list,
        "all_ranking_file" : all_ranking_static + all_ranking_filename
    }
    return render(request,f"ranking/{htmlname}",params)



# Create your views here.
def page(request, htmlname):
    mk = Github.load(repo, htmlname)
    md = markdown.Markdown()
    htmltext = md.convert(mk)
    params = {
        "mk" : mk,
        "htmltext" : htmltext,
        "site_name" : site_name
    }
    params.update(grep_param(mk, ["title", "description"]))
    return render(request,f"blog/techblog/page/mkpage.html", params)


def grep_param(mk, taglist):
    params = {}
    for tag in taglist:
        for line in mk.split("\n"):
            if line.startswith(tag+":"):
                params.update({
                    tag : line.replace(tag + ":", "" )
                })
    return params