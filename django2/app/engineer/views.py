import os

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, "engineer/index.html")

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

    params = {
        "lilist" : lilist
    }

    print(params)
    return render(request, 'engineer/' + htmlpage, params)


from bs4 import BeautifulSoup
class HtmlInfo():
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]
        self.html = ""
        self.title = ""
        self.bsObj = None
        with open(filepath) as f:
            self.html = f.read()
        self.bsObj = BeautifulSoup(self.html)
        self.__grep_title__()

    
    def __grep_title__(self):
        self.title = self.bsObj.find("title").get_text()
    