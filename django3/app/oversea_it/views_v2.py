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
from .creator import selector, editor

REPO = "oversea_v2_it"
REPO_META = "meta"

global_params = {
    "site_name": "エラー解決！",
    "site_description" : "本サイトはあなたのエラーメッセージを解決に導きます。",
    "page_list" : [],
    "candidate_keyword_list" : [],
    "keyword_list" : set()
}
def rebuild_question_list():
    question_id_list = Github.seach_page_list_v2(REPO)
    page_info_list = []
    for question_id in question_id_list:
        raw_json = Github.load(REPO, question_id)
        try:
            page_info = json.loads(raw_json)[0]
            page_info_list.append(page_info)
        except:
            pass
    global_params["page_list"] = page_info_list
rebuild_question_list()


def rebuild_candidate_keyword_list():
    raw_json = Github.load(REPO_META, "oversea_it/candidate_keyword_list.json")
    global_params["candidate_keyword_list"] = json.loads(raw_json)
rebuild_candidate_keyword_list()


def page(request, page_id):
    params = global_params.copy()
    ## 2st. find page
    params.update({
        "tweet_list": get_questions(page_id + ".json")
    })
    params.update(params["tweet_list"][0])
    return render(request, "oversea_it/techblog_ver2/page/mkpage.html", params)

def search(request, keyword):
    params = global_params.copy()
    params.update(selector(keyword))
    return render(request,"oversea_it/techblog_ver2/page/category.html", params)

def sitemap(request):
    page_list = []
    for question_id in Github.seach_page_list_v2(REPO):
        question_id = question_id.replace(".json", "") 
        url = f"https://oversea-it.short-tips.info/{question_id}"
        page_list.append(url)
    page_list.append("https://oversea-it.short-tips.info/index.html")
    page_list.append("https://oversea-it.short-tips.info/questions/")
    page_list.append("https://oversea-it.short-tips.info/help.html")
    page_list.append("https://oversea-it.short-tips.info/post.html")
    dt_now = datetime.datetime.now()
    params = {}
    params.update({
        "page_list" : page_list,
        "last_mod"  :f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    })
    return render(request, "question/sitemap.xml", params)



def page_list(request):
    if request.GET.get("editor"):
        params = editor(request)
        rebuild_question_list()
    if request.GET.get("reload"):
        rebuild_question_list()
    params = global_params.copy()
    return render(request, f"oversea_it/techblog_ver2/page/index.html", params)











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
    Github.upload(REPO, max_question_id, json_info)
    return page_info

def get_questions(question_id):
    page_info = Github.load(REPO, question_id)
    return json.loads(page_info)



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


# IncompleteRead(128834 bytes read)

"""

   url = "https://github.com/kawadasatoshi/" + repo 
    if folder is None:
        url = "https://github.com/kawadasatoshi/" + repo 
    else:
        url = f"https://github.com/kawadasatoshi/{repo}/tree/main/{folder}"
    time.sleep(1)
    html = urlopen(url)
    bsObj = BeautifulSoup(html) …
    file_list = []
    flag = False
    for row in bsObj.findAll("div", attrs={"role": "rowheader"}):
        for a_tag in row.findAll( "a",attrs={"data-pjax": "#repo-content-pjax-container"}):
            if a_tag.has_key('title'):
                file_list.append(a_tag.get_text())

"""