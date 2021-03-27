from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, "engineer/index.html")

def page(request, htmlpage):
    lilist = [
        {
            "title" : "apple",
            "href" : "app2.html"
        },
        {
            "title" : "portfolio",
            "href" : "portfolio.html"
        }
    ]

    params = {
        "lilist" : lilist
    }
    return render(request, 'engineer/' + htmlpage, params)

