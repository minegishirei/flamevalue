import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint


import sys
import sys
sys.path.append('/God')
import SpreadSheet
import RediusManeger
import json
import random
import threading



category_dict = {
    "Design" : { 
        "listinfo" : SpreadSheet.main("Design"),
        "indextitle" : "1分で分かる デザイン逆引き集",
        "description" : "すぐに使えるデザインテクニックを厳選！"
    },
    "ShortCutKey" : { 
        "listinfo" : SpreadSheet.main("ShortCutKey"),
        "indextitle" : "1分で分かる ショートカットキー集",
        "description" : "すぐに使えるショートカットキーを厳選！"
    },
}


def index(request):
    return redirect("index.html")

def sitemap(request):
    return render(request, 'meta/sitemap.xml') 

def shortcutkey_page(request, htmlpage):
    category = "ShortCutKey"
    return page(request, category, htmlpage)


def design_page(request, htmlpage):
    category = "Design"
    return page(request, category, htmlpage)


def page(request, category, htmlpage):
    if "--" in htmlpage:
        return registar(request,htmlpage)
    
    category_info = category_dict[category]
    listinfo = category_info["listinfo"]
    params = {
        "lilist" : listinfo,
        "title" : category_info["indextitle"]
    }
    pageinfo = get_pageinfo(htmlpage, listinfo)
    params.update(pageinfo)
    if htmlpage == "index.html":
        params.update({
            "title" : category_info["indextitle"],
            "description" : category_info["description"]
        })
        return render(request, 'index.html', params)
    return render(request, 'parts/applebase.html', params)



def registar(request ,context):
    SpreadSheet.registar(context.split("--"))
    return render(request, '404NotFound.html')


def get_pageinfo(title, listinfo):

    for info in listinfo:
        print(info["title"])
        if info["title"] ==title:
            return info
    return {}