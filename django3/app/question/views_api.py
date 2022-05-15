from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Yahoo
import MyJson
import NatureLang
import datetime
import Github
from django.views.decorators.csrf import csrf_exempt

REPO_QUESTIONS = "questions"

def get_questions(request, question_id):
    page_info = Github.load(REPO_QUESTIONS, question_id)
    response = HttpResponse(json.dumps(page_info, ensure_ascii=False, indent=4), content_type='application/json; charset=UTF-8')
    return response

post_count = 10

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

