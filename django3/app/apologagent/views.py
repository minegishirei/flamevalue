from django.shortcuts import render

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
        "title" : "反省書自動作成ツール🙇‍♂️",
        "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
        "favicon" : "/static/チャット.png"
    }
    return render(request, f"apologagent/page/{htmlname}")

