import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint

def index(request):
    return redirect("index.html")

def page(request, htmlpage):
    lilist = []
    folder = "/app/engineer/templates/engineer/"
    for filename in os.listdir(folder):
        filepath = os.path.join(folder ,filename)
        print(filepath)
        if os.path.isfile(filepath):
            try:
                htmlInfo = HtmlInfo(filepath)
                lilist.append({
                    "title": htmlInfo.title,
                    "href" : htmlInfo.filename
                })
            except:
                pass
    print("uooooooooooo")
    
    htmlInfo = HtmlInfo(os.path.join(folder, htmlpage))
    htmlInfo.asign_to_dict("description")
    htmlInfo.asign_to_dict("title")
    htmlInfo.asign_to_dict("sidecolumn")
    htmlInfo.asign_to_dict("ans")
    params = {
        "htmlpage" : htmlpage,
        "lilist" : lilist
    }
    params.update(htmlInfo.elements)

    print(params)
    return render(request, 'parts/applebase.html', params)


from bs4 import BeautifulSoup
class HtmlInfo():
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]
        self.html = ""
        self.title = ""
        self.elements = {}
        self.bsObj = None
        with open(filepath) as f:
            self.html = f.read()
        self.bsObj = BeautifulSoup(self.html)
        self.__grep_title__()

    
    def __grep_title__(self):
        self.title = self.bsObj.find("title").get_text()
    
    def asign_to_dict(self, tag):
        self.elements.update({
            tag : self.__simple_grep__(tag).get_text()
        }) 

    def __simple_grep__(self, tag):
        return self.bsObj.find(tag)