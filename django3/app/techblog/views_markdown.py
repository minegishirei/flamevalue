# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Sitemap
import Statichub
import datetime
import markdown


repo = "markdown_store"

def markdown_check(request):
    params = {}
    return render(request,f"blog/techblog_ver2/page/markdown_check.html",params)

@csrf_exempt
def edit(request):
    if request.POST.get("edit"):
        text = request.POST.get("edit")
        htmlname = str(datetime.datetime.now()) + ".md"
        Github.upload(repo, htmlname, text)
    page_info = {
        "success" : 200
    }
    response = JsonResponse(page_info)
    response['Access-Control-Allow-Origin'] = '*'
    response['Accept'] = '*/*'
    return response


@csrf_exempt
def post_questions(request):
    global post_count
    post_count += 4
    error_message = ""
    code = ""
    supplement = ""
    if "error_message" in request.POST:
        error_message = request.POST.get("error_message")
    if "code" in request.POST:
        code = request.POST["code"]
    if "supplement" in request.POST:
        supplement = request.POST["supplement"]
    
    page_info = {
        "error_message" : error_message,
        "code" : code,
        "supplement" : supplement
    }
    question_json_info = json.dumps(page_info, ensure_ascii=False, indent=4)
    Github.upload(REPO_QUESTIONS, str(post_count), str(page_info))
    response = JsonResponse(page_info)
    response['Access-Control-Allow-Origin'] = '*'
    response['Accept'] = '*/*'
    return response


