from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

"""
def index(request, msg, id):
    result = ''
    result = 'Hello "'+ msg+ '"!!'
    result += 'id is ' + str(id)
    return HttpResponse(result)
"""

def index(request):
    return render(request, 'hello/index.html')

