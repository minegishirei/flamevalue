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
        "title" : "反省書自動作成ツール🙇‍♂️",
        "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
        "favicon" : "/static/チャット.png",
        "img": "http://apologagent.short-tips.info/static/thumbnail.png",
        "repo":repo,
        "htmlname" : htmlname,
    }
    if Github.has_already_created(repo, htmlname):
        pass
    else:
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list(htmlname)
        text= json.dumps(tweet_list, ensure_ascii=False, indent=4)
        Github.upload("twitter_json", htmlname, text)
    return render(request,"fanstatic/dashboard/charts.html",params)

