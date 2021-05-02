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
    "Dialogue" : {
        "listinfo" : SpreadSheet.main("Dialogue"),
        "indextitle" : "対話と音声学",
        "description" : "「あはいより大きいーー」音声学を元にした言葉と印象の記録"
    },
    "WordDesign" : {
        "listinfo" : SpreadSheet.main("WordDesign"),
        "indextitle" : "言葉の道具箱",
        "description" : "操作可能な範囲の限界ギリギリを攻める道具達"
    },
}



def index(request):
    return redirect("index.html")

def sitemap(request):
    return render(request, 'meta/sitemap.xml') 

def robots(request):
    return render(request, 'meta/robots.txt') 


def shortcutkey_page(request, htmlpage):
    category = "ShortCutKey"
    return page(request, category, htmlpage)


def design_page(request, htmlpage):
    category = "Design"
    return page(request, category, htmlpage)


def dialogue_page(request, htmlpage):
    category = "Dialogue"
    return page(request, category, htmlpage)

def page(request, category, htmlpage):
    if "--" in htmlpage:
        return registar(request,htmlpage)
    
    category_info = category_dict[category]
    listinfo = category_info["listinfo"]
    #params処理
    params = {
        "lilist" : listinfo,
        "title" : category_info["indextitle"]
    }
    pageinfo = get_pageinfo(htmlpage, listinfo)
    params.update(pageinfo)
    if htmlpage == "index.html":
        params.update({
            "seo_title" : category_info["indextitle"],
            "title" : category_info["indextitle"],
            "description" : category_info["description"]
        })
        return render(request, 'index.html', params)
    else:
        params.update({
            "seo_title" :  pageinfo["title"] + " - "+category_info["indextitle"],
            "title" : pageinfo["title"],
        })
    return render(request, 'parts/applebase.html', params)


def dialog_uml(request):
    lilist = []
    """
    category = "Dialogue"
    category_info = category_dict[category]
    lilist.extend(category_info["listinfo"])
    """
    category = "WordDesign"
    category_info = category_dict[category]
    lilist.extend(category_info["listinfo"])


    umlBuilder = UmlBuilder()
    for page in lilist:
        classComposit = ClassComposit(page)
        umlBuilder.add(classComposit)
    umlBuilder.build()
    umlcode = umlBuilder.dump()
    param = {
        "lilist" : lilist,
        "umlcode" : umlcode
    }
    return render(request, "umlpage.html",  param)


def registar(request ,context):
    SpreadSheet.registar(context.split("--"))
    return render(request, '404NotFound.html')


def get_pageinfo(title, listinfo):
    for info in listinfo:
        print(info["title"])
        if info["title"] ==title:
            return info
    return {}






class Composit():
    def add(self):
        pass

    def dump(self):
        pass



class UmlBuilder():
    def __init__(self):
        self.code = """classDiagram
{}
"""
        self.classDefCode = ""
        self.classDefList = []

    def add(self, classComposit):
        self.classDefList.append(classComposit)

    def build(self):
        for classDef in self.classDefList:
            classDef.build()
            self.classDefCode += (classDef.dump() +"\n") 
    
    def dump(self):
        return self.code.format(self.classDefCode)
    



class ClassComposit(Composit):
    def __init__(self, infoDict):
        self.code = f"""
class {infoDict["title"]}"""+ "{"
        self.code += f"""
.
.
.
.
.
.
.
.
----------------------------------
-ans {infoDict["ans"]}
    -description 
    {infoDict["description"]}
        """
        self.code += "}"
    
    def build(self):
        pass

    def dump(self):
        return self.code

