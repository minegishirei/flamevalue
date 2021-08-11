#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint
import datetime
import sys
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Github
import MyJson
import os
import threading
import random
import json
import Oreilly
from django.views.decorators.csrf import csrf_exempt


site_title = "オライリー大図鑑"
site_description = "sample description"
repo = "oreilly"
repo_com = "oreilly_com"




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
        if request.GET.get("reload"):
            gen_page_dict_list()
        indexParamFactory  = IndexParamFactory()
        params = indexParamFactory.build()
        return render(request, "oreilly/index.html", params)

    def robots(self, request):
        return render(request, 'meta/robots.txt')

    def sitemap(self, request):
        page_list = []
        for page in PAGE_DICT_LIST:
            page_list.append("http://oreilly.short-tips.info/"+page["book_id"])
        page_list.append("http://oreilly.short-tips.info/index.html")
        dt_now = datetime.datetime.now()
        params = {
            "page_list" : page_list,
            "lastmod" : f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
        }
        return render(request, f'oreilly/sitemap.xml', params)

    def table_index(self, request):
        ParamFactory = ParamFactory(request, "table_index.html")
        ParamFactory.set_lilist()
        ParamFactory.page()
        return render(request,  'table_index.html', ParamFactory.params)
    
    
    def page(self, request, htmlpage):
        if not Github.has_already_created(repo, htmlpage):
            add_to_github(htmlpage)
        
        paramFactory = PageParamFactory()
        if request.POST.get("title"):
            context = {
                'title': request.POST['title'],
                'comment': request.POST['comment'],
                'good' : 0
            }
            params = paramFactory.build( htmlpage, context)
        else:
            params = paramFactory.build( htmlpage)
        
        return render(request, "oreilly/oreilly_base.html",params)
    
    def sql(self, request):
        category_name = request.get_host().split(".")[0]
        paramFactory = SQLParamFactory()
        sentence = request.POST.get("sql")
        if sentence is None:
            sentence = f"select * from {category_name}"
        params = paramFactory.build(category_name, sentence)
        return render(request, "sql.html", params)

switchPage = SwitchPage()

@csrf_exempt
def page( request, htmlpage):
    return switchPage.page(request, htmlpage)
    


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
    def __init__(self,  title):
        super().__init__()
        self.comdict.update({
            "title" : title 
        })

class RelationComponent(ParamComponent):
    def __init__(self, category_name, page_name):
        super().__init__()
    
class AllRelationComponent(ParamComponent):
    def __init__(self, ):
        super().__init__()
        self.comdict.update({"all_relation": PAGE_DICT_LIST})

class PageComponent(ParamComponent):
    def __init__(self,  page_name):
        super().__init__()
        json_str = Github.load(repo, page_name)
        myJson = MyJson.MyJson()
        self.comdict.update(myJson.read(json_str))

class CommentComponent(ParamComponent):
    def __init__(self,  page_name, new_dict=False):
        super().__init__()
        comment_list = []
        if Github.has_already_created(repo_com, page_name):
            myJson = MyJson.MyJson()
            json_str = Github.load(repo_com, page_name)
            comment_list = myJson.read(json_str)
            if new_dict:
                Github.delete_page(repo_com, page_name)
                comment_list.append(new_dict)
                json_str = myJson.write(comment_list)
                Github.upload(repo_com, page_name, json_str)
        else:
            Github.upload(repo_com, page_name, str(comment_list))
        self.comdict.update({
            "comment_list" : comment_list
        })


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
    
    def build(self):
        componentList = [
            TitleComponent( site_title ),
            AllRelationComponent()
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params

class PageParamFactory(ParamFactory):
    def __init__(self):
        super().__init__()
    
    def build(self,  page_name, new_dict=False):
        componentList = [
            PageComponent(page_name),
            CommentComponent(page_name, new_dict)
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




def add_to_github(book_id):
    oreilly = Oreilly.Oreilly(book_id)
    params = oreilly.get_params()
    myJson = MyJson.MyJson()
    Github.upload(repo, book_id, myJson.write(params))


PAGE_DICT_LIST = []
def gen_page_dict_list():
    global PAGE_DICT_LIST
    PAGE_DICT_LIST = []
    for book_id in Github.seach_page_list(repo):
        json_str = Github.load(repo, book_id)
        myJson = MyJson.MyJson()
        page_dict = myJson.read(json_str)
        PAGE_DICT_LIST.append({
            "title" : page_dict["title"],
            "book_id" : page_dict["book_id"],
            "img" : page_dict["img"]
        })
gen_page_dict_list()