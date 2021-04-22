import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint


def index(request):
    return redirect("index.html")


def page(request, category, htmlpage):
    lilist = []
    folder = "/app/engineer/templates/" + category
    for filename in os.listdir(folder):
        filepath = os.path.join(folder ,filename)
        if os.path.isfile(filepath):
            try:
                htmlInfo = HtmlInfo(filepath)
                htmlInfo.asign_to_dict("img")
                elements = {
                    "title": htmlInfo.title,
                    "href" : htmlInfo.filename,
                    "img" : "https://i.ytimg.com/vi/84f8ItPV1Mg/maxresdefault.jpg"
                }
                elements.update(htmlInfo.elements)
                lilist.append(elements)
            except:
                import traceback
                traceback.print_exc()
                pass

    htmlInfo = HtmlInfo(os.path.join(folder, htmlpage))
    htmlInfo.asign_to_dict("description")
    htmlInfo.asign_to_dict("title")
    htmlInfo.asign_to_dict("sidecolumn")
    htmlInfo.asign_to_dict("ans")
    htmlInfo.asign_to_dict("img")
    htmlInfo.asign_to_dict("xmp")

    headerlist = [
        "engineer/",
        "design/",
        "shortcuts/"
    ]
    params = {
        "htmlpage" : htmlpage,
        "lilist" : lilist,
        "headerlist" : headerlist
    }
    params.update(htmlInfo.elements)
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
