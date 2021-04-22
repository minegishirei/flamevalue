import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint

import redis
cache = redis.StrictRedis(host='redis', port=6379, db=0)

import sys
import sys
sys.path.append('/God')
import SpreadSheet
import json
import random
import threading

def index(request):
    return redirect("index.html")


def page(request, category, htmlpage):
    if category == "dog":
        row = registar(htmlpage)
        SpreadSheet.registar(row)
        return render(request, '404NotFound.html')

    listinfo = SpreadSheet.main(category)
    pageinfo = {}
    for info in listinfo:
        print(info["title"])
        if info["title"] == htmlpage:
            pageinfo = info
            break
    print(htmlpage)

    params = {
        "pageinfo" : pageinfo,
        "lilist" : listinfo
    }
    params.update(pageinfo)
    if htmlpage == "index.html":
        return render(request, 'index.html', params)
    return render(request, 'parts/applebase.html', params)




def registar(context):
    row = context.split("--")
    return row



class htmlManeger():
    def main(self, folder):
        directoryInfo = DirectoryInfo(folder)
        directoryInfo.seach()
        return directoryInfo


        


class Compose():
    def __init__(self, path):
        self.path = path
        self.elements = {}
        self.nextComposeList = []
        super().__init__()
    
    def next(self, nextpath):
        if os.path.isfile(nextpath):
            return HtmlInfo(nextpath)
        else:
            return DirectoryInfo(nextpath)

    def seach(self):
        pass

    def get(self):
        return self.nextComposeList
    
    def add(self, compose):
        self.nextComposeList.append(compose)



class DirectoryInfo(Compose):
    def __init__(self, path):
        super().__init__(path)
    
    def seach(self):
        for filename in os.listdir(self.path):
            nextpath = os.path.join(self.path ,filename)
            nextCompse = self.next(nextpath)
            self.add(nextCompse)
            nextCompse.seach()






from bs4 import BeautifulSoup
class HtmlInfo(Compose):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]
        self.elements.update({
            "href" : self.filename
        })
        self.html = ""
        self.title = ""
        self.bsObj = None
        with open(filepath) as f:
            self.html = f.read()
        self.bsObj = BeautifulSoup(self.html)
        #self.__grep_title__()
    
    def seach(self):
        self.asign_to_dict("description")
        self.asign_to_dict("title")
        self.asign_to_dict("sidecolumn")
        self.asign_to_dict("ans")
        self.asign_to_dict("img")
        self.asign_to_dict("xmp")

    def __grep_title__(self):
        self.title = self.bsObj.find("title").get_text()
    
    def asign_to_dict(self, tag):
        tagobj = self.__simple_grep__(tag)
        if tagobj is None:
            return
        if tag=="img":
            self.elements.update({
                tag : tagobj["src"]
            })
        elif tag=="xmp":
            self.elements.update({
                tag : str(tagobj)
            }) 
        else:
            self.elements.update({
                tag : tagobj.get_text()
            }) 

    def __simple_grep__(self, tag):
        return self.bsObj.find(tag)
