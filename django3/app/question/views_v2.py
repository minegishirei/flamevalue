from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Yahoo
import MyJson
import NatureLang
import datetime
import Github
import UniqueAPI


global_params = {
    "site_name": "エラー解決！",
    "site_description" : "本サイトはあなたのエラーメッセージを解決に導きます。"
}


# double page app

# first page: QA page
## Search Bar ( simple like google )
## 広告
## Main Content
### *Error Message
### Code
### Supplement
## Main Content2 (if exsists)
### Answer Code
### Supplement

# second page: Build QA page
### *Error Message
### Code
### Supplement


def html_page(request, html_name):
    params = {}
    params.update({
        "title" : global_params["site_name"],
        "description" : global_params["site_description"]
    })
    return render(request, f"question_v2/{html_name}", params)


def main(request, page_id):
    params = {}
    error_message_param = {}
    if "create_new_page" in request.POST:
        ## 1st. create new page
        new_error_message_param = post_questions(request)
        return redirect( "./" + str(new_error_message_param["question_id"]))
    else:
        ## 2st. find page
        new_error_message_param = get_questions(page_id)
        error_message_param = {
            "title" : new_error_message_param["error_message"][:50],
            "description" : new_error_message_param["error_message"],
            "error_message" : new_error_message_param["error_message"],
            "code" : new_error_message_param["code"],
            "supplement" : new_error_message_param["supplement"]
        }
    answer_code_param = None
    if "answer_new_page" in request.POST:
        ## 1st. create answer page
        new_answer_code_param = post_answers(request, page_id)
        return redirect( "./" + str(new_answer_code_param["question_id"]))
    else:
        try:
            answer_code_param = get_answers(page_id)
        except:
            pass
    ## 2nd. build params from page info
    params.update({
            "title" : error_message_param["title"],
            "error_message_param" : error_message_param,
            "answer_code_param" : answer_code_param
        })
    return render(request, f"question_v2/blog_details.html", params)




def sitemap(request):
    page_list = []
    for question_id in Github.seach_page_list_v2(REPO_QUESTIONS):
        url = f"http://question.short-tips.info/questions/{question_id}"
        page_list.append(url)
    dt_now = datetime.datetime.now()
    params = {}
    params.update({
        "page_list" : page_list,
        "last_mod"  :f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    })
    return render(request, "question/sitemap.xml", params)




REPO_QUESTIONS = "questions"
def post_questions(request):
    max_question_id = str(UniqueAPI.get_unique_id()["value"])
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
        "supplement" : supplement,
        "question_id" : max_question_id
    }
    json_info = json.dumps(page_info, ensure_ascii=False, indent=4)
    Github.upload(REPO_QUESTIONS, max_question_id, json_info)
    return page_info

def get_questions(question_id):
    page_info = Github.load(REPO_QUESTIONS, question_id)
    return json.loads(page_info)


REPO_ANSWERS = "answers"
def post_answers(request, question_id):
    answer_id = question_id + "/" +str(UniqueAPI.get_unique_id()["value"])
    title = ""
    code = ""
    supplement = ""
    if "title" in request.POST:
        title = request.POST.get("title")
    if "code" in request.POST:
        code = request.POST["code"]
    if "supplement" in request.POST:
        supplement = request.POST["supplement"]
    page_info = {
        "title" : title,
        "code" : code,
        "supplement" : supplement,
        "answer_id" : answer_id,
        "question_id" : question_id
    }
    json_info = json.dumps(page_info, ensure_ascii=False, indent=4)
    Github.upload(REPO_ANSWERS, answer_id, json_info)
    return page_info

def get_answers(question_id):
    answer_id_list = Github.seach_page_list_v2(REPO_ANSWERS, question_id)
    page_info_list = []
    for answer_id in answer_id_list:
        page_info = Github.load(REPO_ANSWERS, question_id + "/" +answer_id)
        page_info_list.append(json.loads(page_info))
    return page_info_list

# HTTP Error 404: Not Found 
# Beautiful Soup urlopen python


