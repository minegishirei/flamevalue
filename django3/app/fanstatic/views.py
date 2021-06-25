from django.shortcuts import render
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github

repo = "twitter_json"
# Create your views here.
def page(request, htmlname):
    params = {
        "title" : htmlname + " - ファン統計",
        "description" : "アニメ、オタク、サブカルを惹きつけるものは何か。データから推察するためのウェブサイトです。",
        "favicon" : "/static/チャット.png",
        "img": "http://apologagent.short-tips.info/static/thumbnail.png",
        "repo":repo,
        "htmlname" : htmlname,
    }
    if Github.has_already_created(repo, htmlname):
        pass
    else:
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list(htmlname, amount=50)
        text= json.dumps(tweet_list, ensure_ascii=False, indent=4)
        Github.upload("twitter_json", htmlname, text)
    return render(request,"fanstatic/dashboard/charts.html",params)

