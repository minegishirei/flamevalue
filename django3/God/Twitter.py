import json
from requests_oauthlib import OAuth1Session
import pprint
MAIN_KEYS = {
    'consumer_key':'kBAze00GyDfwYaz673itPtWHx',
    'consumer_secret':'gr5WuLP4mdCBedKyyva1PIYq7ylSU9Kicp3vC4fyAyjYyL3geD',
    'access_token':'968269222525587456-gYTZbY4ph179lrI8mZDPEWXnAubYIbr',
    'access_secret':'0BpC5rsM2VVGjteHJPm53nk8bzidGGMIAboWf5Dyk9P3J',
}


class MyTwitterException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyTwitterAction():
    def __init__(self):
        KEYS = MAIN_KEYS
        self.twitter = OAuth1Session(KEYS['consumer_key'],KEYS['consumer_secret'],KEYS['access_token'],KEYS['access_secret'])

    def search_tweet_list(self, q, amount):
        params = {
            "q" : q,
            #'q' : "仕事" + " since:20{}-{}-{}_00:00:00_JST min_faves:1000".format(year,month,day),  #検索文字列
            #'q' : "あけ since:2018-12-31_23:59:59_JST until:2019-01-01_00:00:00_JST",
            'count': amount
        }
        url = "https://api.twitter.com/1.1/search/tweets.json"
        req = self.twitter.get(url, params = params)
        if req.status_code == 200:
            tweet = json.loads(req.text)
            search_timeline = json.loads(req.text)
        else:
            import traceback
            raise MyTwitterException(traceback.print_exc())
        return search_timeline['statuses']
