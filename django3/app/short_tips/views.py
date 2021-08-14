#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint

import sys
import sys
if '/God' not in sys.path:
    sys.path.append('/God')

import SpreadSheet
import os
import threading
import random
import json

from DAO import DAO, InsertableDAO, TableCreatableDAO, CmdDAO, create_newTable



meta_info = {
    "design": {
        "category" : "design",
        "indextitle": "デザイン逆引き集",
        "description": "すぐに使えるデザインテクニックを厳選！"
    },
    "shortcutkey": {
        "category":"shortcutkey",
        "indextitle": "1分で分かる ショートカットキー集",
        "description": "すぐに使えるショートカットキーを厳選！"
    },
    "dialogue": {
        "category":"dialogue",
        "indextitle": "対話と音声学",
        "description": "「あはいより大きいーー」音声学を元にした言葉と印象の記録"
    },
    "wordeffect": {
        "category" : "wordeffect",
        "indextitle": "言葉の心理学図鑑",
        "description": "操作可能な範囲の限界ギリギリを攻める道具達"
    },
    "stock": {
        "category" : "stock",
        "indextitle": "SEメモ",
        "description": "SEメモ"
    },
    "shogi": {
        "category" : "shogi",
        "indextitle": "将棋のケアレスミスメモ",
        "description": "将棋にケアレスミスはつきもの。だがそれも魅力の一つ。"
    },
        "psy": {
        "category" : "psy",
        "indextitle": "将棋のケアレスミスメモ",
        "description": "将棋にケアレスミスはつきもの。だがそれも魅力の一つ。"
    }
}



def init_sql(category):
    tagzip,list_info  = SpreadSheet.main(category)
    column = " ,".join([ str(tag) + " " + str(type_) for  tag, type_ in tagzip])

    with InsertableDAO(category, column) as dao:
        for li in list_info:
            try:
                statement = 'insert into ' + category + ' VALUES (' + ', '.join(['"'+str(v) + '"' for v in li.values()]) + ')'
                dao.run(statement)
            except:
                import traceback
                traceback.print_exc()



init_sql("psy")
init_sql("localtheorem")
init_sql("wordeffect")

init_sql("furniture")
init_sql("individuality")

init_sql("design")
init_sql("shortcutkey")

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

    def index(self, request):
        category_name = request.get_host().split(".")[0]
        indexParamFactory  = IndexParamFactory()
        params = indexParamFactory.build(category_name)
        return render(request, "index.html", params)

    def robots(self, request):
        return render(request, 'meta/robots.txt')

    def sitemap(self, request):
        category_name = request.get_host().split(".")[0]
        return render(request, f'meta/{category_name}.xml')

    def table_index(self, request):
        ParamFactory = ParamFactory(request, "table_index.html")
        ParamFactory.set_lilist()
        ParamFactory.page()
        return render(request,  'table_index.html', ParamFactory.params)

    def page(self, request, htmlpage):
        category_name = request.get_host().split(".")[0]
        paramFactory = PageParamFactory()
        params = paramFactory.build(category_name, htmlpage)
        return render(request, "parts/applebase.html",params)
    
    def sql(self, request):
        category_name = request.get_host().split(".")[0]
        paramFactory = SQLParamFactory()
        sentence = request.POST.get("sql")
        if sentence is None:
            sentence = f"select * from {category_name}"
        params = paramFactory.build(category_name, sentence)
        return render(request, "sql.html", params)




class ParamComponent():
    def __init__(self):
        self.comdict ={}
        super().__init__()
    
    def getComdict(self):
        return self.comdict


class TitleComponent(ParamComponent):
    def __init__(self, title):
        super().__init__()
        self.comdict.update({
            "title" : title 
        })

class MetaTitleComponent(ParamComponent):
    def __init__(self, category_name,  title):
        super().__init__()
        self.comdict.update({
            "title" : title + " | " +meta_info[category_name]["indextitle"]
        })

class RelationComponent(ParamComponent):
    def __init__(self, category_name, page_name):
        super().__init__()
    
class AllRelationComponent(ParamComponent):
    def __init__(self, category_name):
        super().__init__()
        with DAO(category_name) as dao:
            result = dao.select_all()
            self.comdict.update({"all_relation": result})

class PageComponent(ParamComponent):
    def __init__(self, category_name, page_name):
        super().__init__()
        with DAO(category_name) as dao:
            result_list = dao.run(f'select * from {category_name} where title = "{page_name}"')
            result = result_list[0]
            self.comdict.update(result)

class SQLComponent(ParamComponent):
    def __init__(self, category_name, cmd):
        super().__init__()
        with DAO(category_name) as dao:
            result = dao.run(cmd)
            self.comdict.update({"all_relation": result})
            self.comdict.update({"sql" : cmd})


###############################

class ParamFactory():
    def __init__(self):
        self.params = {}
        self.category_name = ""
        super().__init__()
    
    def getFactory(self, factoryType):
        pass

class IndexParamFactory(ParamFactory):
    def __init__(self):
        self.factoryType = "index"
        super().__init__()
    
    def build(self, category_name):
        self.category_name = category_name
        componentList = [
            TitleComponent(category_name +meta_info[category_name]["indextitle"] ),
            AllRelationComponent(category_name)
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params

class PageParamFactory(ParamFactory):
    def __init__(self):
        super().__init__()
    
    def build(self, category_name, page_name):
        self.category_name = category_name
        componentList = [
            PageComponent(category_name, page_name),
            AllRelationComponent(category_name),
            MetaTitleComponent(category_name, page_name)
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params

class SQLParamFactory(ParamFactory):
    def __init__(self):
        super().__init__()
    
    def build(self, category_name, cmd):
        self.category_name = category_name
        componentList = [
            MetaTitleComponent(category_name, category_name),
            SQLComponent(category_name,cmd)
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params


