from django.shortcuts import render
from .sentense_class import InputText, Choice

# Create your views here.
def index(request):
    params = {
        "title" : "反省書自動作成ツール🙇‍♂️",
        "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
        "favicon" : "/static/チャット.png"
    }
    return render(request,"apologagent/index.html",params)

def page(request, htmlname):
    params = {
        "title" : "反省書エディター🙇‍♂️",
        "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
        "favicon" : "/static/チャット.png"
    }

    transition = [
        InputText({
            "name": "input1",
           "title": "結論",
           "preface":"この度は",
           "example":"定例会議に15分以上も遅刻してしまい",
           "afterword":"、申し訳ございませんでした。",
           "next":"./oko.html#slide=3"
        }),
        InputText({
            "name": "input2",
           "title": "原因",
           "preface":"直接の原因は",
           "example":"昨日タイマーを設定し忘れたこと",
           "afterword":"が原因です。",
           "next":"./oko.html#slide=4"
        })
    ]
    pageContentList = []
    for component in transition:
        value = getSessionValue(request, component.info["name"])
        saveSessionValue(request, component.info["name"], value)
        component.setValue(value)
        pageContentList.append(component.info)
    params.update({
        "pageContentList":pageContentList
    })
    return render(request, f"apologagent/page/{htmlname}",params)


def getSessionValue(request, key):
    ans = request.session.get(key)
    if ans is None:
        return ""
    return ans


def saveSessionValue(request, key, value):
    request.session[key] = value