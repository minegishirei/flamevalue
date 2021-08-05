from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Yahoo
import MyJson
# Create your views here.


all_category = {
    "mental"    : "https://chiebukuro.yahoo.co.jp/category/2078297858/question/list?page={}",
    "media"     : "https://chiebukuro.yahoo.co.jp/category/2080401283/question/list?page={}",
    "device"    : "https://chiebukuro.yahoo.co.jp/category/2080401469/question/list?page={}",
    "programming": "https://chiebukuro.yahoo.co.jp/category/2078297616/question/list?page={}"
}


####################
class AddContentManager():
    def __init__(self):
        """
        ユーザーに後悔するページを登録するjsonファイル
        """
        self.myJson = MyJson.MyLocalJson("/app/question/addContent.json")
        
    def addContent(self, category, yahoo_id):
        yahooQuestionPage = Yahoo.YahooQuestionPage("https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q" + yahoo_id)
        content = yahooQuestionPage.collect()
        #get data
        new_dict = {
            "yahoo_id"  : yahoo_id,
            "content"   : content
        }
        #add to json_file
        before_dict = self.myJson.read()
        before_dict[category]["page_list"].append(new_dict)
        self.myJson.write(before_dict)
        
    def loadContent(self, category, yahoo_id):
        return_json = self.myJson.read()
        for page_dict in return_json[category]["page_list"]:
            if page_dict["yahoo_id"] == yahoo_id:
                return page_dict
    
    def loadCategory(self, category):
        return self.myJson.read()[category]
####################



addContentManager = AddContentManager()

global_params = {
"site_name": "こんな質問を見つけた",
"all_category" : all_category
}


def index(request):
    global global_params
    params = global_params.copy()
    return render(request,"question/index.html",params)


def category_list(request, category):
    global global_params
    params = global_params.copy()
    if request.GET.get("edit"):
        page_info_list = Yahoo.main(all_category[category])
        params.update({
            "category" : category,
            "page_info_list" : page_info_list
        })
        return render(request,"question/category_list_edit.html",params)
    else:
        category_dict = addContentManager.loadCategory(category)
        params.update({
            "category" : category,
            "page_info_list" : category_dict["page_list"]
        })
        return render(request,"question/category_list.html",params)
    


def page(request, category, yahoo_id):
    global global_params
    if request.GET.get("add"):
        addContentManager.addContent(category, yahoo_id)
    page_dict = addContentManager.loadContent(category, yahoo_id)
    params = global_params.copy()
    params.update({
        "page_dict" : page_dict
    })
    return render(request,"question/page.html",params)








