
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint

import sys
import sys
sys.path.append('/God')

import SpreadSheet
import os
import threading
import random
import json




category_dict = {
    "design": {
        "category" : "design",
        "listinfo": SpreadSheet.main("design"),
        "indextitle": "1分で分かる デザイン逆引き集",
        "description": "すぐに使えるデザインテクニックを厳選！"
    },
    "shortcutkey": {
        "category":"shortcutkey",
        "listinfo": SpreadSheet.main("shortcutkey"),
        "indextitle": "1分で分かる ショートカットキー集",
        "description": "すぐに使えるショートカットキーを厳選！"
    },
    "dialogue": {
        "category":"dialogue",
        "listinfo": SpreadSheet.main("dialog"),
        "indextitle": "対話と音声学",
        "description": "「あはいより大きいーー」音声学を元にした言葉と印象の記録"
    },
    "wordeffect": {
        "category" : "wordeffect",
        "listinfo": SpreadSheet.main("wordeffect"),
        "indextitle": "言葉の道具箱",
        "description": "操作可能な範囲の限界ギリギリを攻める道具達"
    },
    "stock": {
        "category" : "stock",
        "listinfo": SpreadSheet.main("stock"),
        "indextitle": "SEメモ",
        "description": "SEメモ"
    },
    "shogi": {
        "category" : "shogi",
        "listinfo": SpreadSheet.main("shogi"),
        "indextitle": "将棋のケアレスミスメモ",
        "description": "将棋にケアレスミスはつきもの。だがそれも魅力の一つ。"
    },
        "psy": {
        "category" : "psy",
        "listinfo": SpreadSheet.main("psy"),
        "indextitle": "将棋のケアレスミスメモ",
        "description": "将棋にケアレスミスはつきもの。だがそれも魅力の一つ。"
    }
}

def get_category_info(host_name):
    for key in category_dict.keys():
        if host_name.startswith(key):
            return category_dict[key]
    return None

def get_pageinfo(title, listinfo):
    for info in listinfo:
        print(info["title"])
        if info["title"] == title:
            return info
    return {}





class SwitchPage():
    def __init__(self):
        pass

    def main(self, request, htmlpage=""):
        if "--" in htmlpage:
            return registar(request, htmlpage)
        elif "index.html" == htmlpage:
            return self.index(request)
        elif "buildable_index.html" == htmlpage:
            return self.buildable_index(request)
        elif "robots.txt" == htmlpage:
            return self.robots(request)
        elif htmlpage.endswith(".xml"):
            return self.sitemap(request, htmlpage)
        else:
            return self.elsepage(request, htmlpage)

    def buildable_index(self, request):
        paramBuilder = IndexParamBuilder(request, "index.html")
        paramBuilder.set_title()
        paramBuilder.set_lilist()
        paramBuilder.page()
        params = paramBuilder.params
        return render(request, "buildable_index.html", params )

    def sortindex(self, request):
        paramBuilder = IndexSortParamBuilder(request, "index.html")
        paramBuilder.set_sortlilist()
        paramBuilder.set_title()
        paramBuilder.set_lilist()
        paramBuilder.page()
        params = paramBuilder.params
        return render(request, "index.html", params )

    def index(self, request):
        paramBuilder = IndexParamBuilder(request, "index.html")
        paramBuilder.set_title()
        paramBuilder.set_lilist()
        paramBuilder.page()
        params = paramBuilder.params
        return render(request, "index.html", params )

    def robots(self, request):
        return render(request, 'meta/robots.txt')

    def sitemap(self, request, htmlpage):
        return render(request, f'meta/{htmlpage}')

    def table_index(self, request):
        paramBuilder = IndexParamBuilder(request, "table_index.html")
        paramBuilder.set_lilist()
        paramBuilder.page()
        return render(request,  'table_index.html', paramBuilder.params)

    def elsepage(self, request, htmlpage):
        paramBuilder = ParamBuilder(request, htmlpage)
        paramBuilder.set_title()
        paramBuilder.set_lilist()
        paramBuilder.page()
        return render(request, "parts/applebase.html",paramBuilder.params)



class ParamBuilder():
    def __init__(self, request, htmlpage):
        host = request.get_host()
        self.category_info = get_category_info(host)
        self.category = self.category_info["category"]
        self.lilist = self.category_info["listinfo"]
        self.page_info = get_pageinfo(htmlpage, self.lilist)
        self.request = request
        self.htmlpage = htmlpage
        self.params = {}

    def set_title(self):
        self.params.update({
            "title": self.category_info["indextitle"]
        })

    def set_description(self):
        self.params.update({
            "description": self.category_info["description"]
        })

    def set_lilist(self):
        self.params.update({
            "lilist": self.lilist
        })

    def page(self):
        self.params.update(self.page_info)
        self.params.update({
            "seo_title":  self.page_info["title"] + " - "+self.category_info["indextitle"],
            "title": self.page_info["title"],
        })
        


class IndexParamBuilder(ParamBuilder):
    def __init__(self, request, htmlpage):
        super().__init__(request, htmlpage)
    
    def page(self):
        self.params.update({
            "seo_title": self.category_info["indextitle"],
            "title": self.category_info["indextitle"],
            "description": self.category_info["description"]
        })


class IndexSortParamBuilder(IndexParamBuilder):
    def __init__(self):
        super().__init__()
    
    def set_sortlilist(self):
        sorted_lilist = sorted(self.lilist , key=lambda x:x['effect'])




def dialog_uml(request):
    lilist = []
    """
    category = "Dialogue"
    category_info = category_dict[category]
    lilist.extend(category_info["listinfo"])
    """
    category = "WordEffect"
    category_info = category_dict[category]
    lilist.extend(category_info["listinfo"])

    umlBuilder = UmlBuilder()
    for page in lilist:
        classComposit = ClassComposit(page)
        umlBuilder.add(classComposit)
    umlBuilder.build()
    umlcode = umlBuilder.dump()
    param = {
        "lilist": lilist,
        "umlcode": umlcode
    }
    return render(request, "umlpage.html",  param)


def registar(request, context):
    SpreadSheet.registar(context.split("--"))
    return render(request, '404NotFound.html')


def get_pageinfo(title, listinfo):
    for info in listinfo:
        print(info["title"])
        if info["title"] == title:
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
            self.classDefCode += (classDef.dump() + "\n")

    def dump(self):
        return self.code.format(self.classDefCode)


class ClassComposit(Composit):
    def __init__(self, infoDict):
        self.code = f"""
class {infoDict["title"]}""" + "{"
        self.code += f"""
-ans {infoDict["ans"]}
    -description 
    {infoDict["description"]}
        """
        self.code += "}"

    def build(self):
        pass

    def dump(self):
        return self.code
