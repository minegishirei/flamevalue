from django.shortcuts import render

# Create your views here.
def index(request):
    params = {
        "title" : "反省書自動作成ツール"
    }
    return render(request,"apologagent/index.html")

def page(request, htmlname):
    return render(request, f"apologagent/page/{htmlname}")

