from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def page(request, htmlpage):
    return render(request, 'engineer/' + htmlpage)

