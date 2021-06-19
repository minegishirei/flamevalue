from django.shortcuts import render

# Create your views here.
def index(request):
    params = {
        "title" : "反省書自動作成ツール🙇‍♂️",
        "favicon" : "/static/チャット.png"
    }
    return render(request,"apologagent/index.html",params)

def page(request, htmlname):
    return render(request, f"apologagent/page/{htmlname}")

