from django.shortcuts import render, redirect
import json
import sys

if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
import markdown
import GoogleTrans

from .mock import test_list
FEATUHER = {
    'access_token' : '968269222525587456-nTufoFnhYpNIY1sLQwB9WYGiDlAIEMM',
    'access_secret' : 'rhoqnAXt3VHz9dnNv8DlyDUd9V1fijfw2Of091UkjVUTV',
    'consumer_key' : 'nAllJpqiUKtnUG4aHrk2G6T9v',
    'consumer_secret' : 'QAY2CnNGt2onuun6QckyYniZeh753q6X4dEXw9mS3pjTecPk9Y'
}

REPO = "oversea_v2_it"

def selector(request):
    #myTwitterAction = Twitter.MyTwitterAction(FEATUHER)
    #tweet_list = myTwitterAction.search_tweet_list("1026294188634042368", 100)

    params = {
        "tweet_list" : tweet_list
    }


def editor(request):
    since = request.GET["since"]
    until = request.GET["until"]
    user  = request.GET["user"]
    tweet_id = request.GET["tweet_id"]
    q = f"to:{user} until:{until} since:{since} min_faves:20"
    #to:d_feldman until:2018-08-08 since:2018-08-06 
    FEATUHER = {
        'access_token' : '968269222525587456-nTufoFnhYpNIY1sLQwB9WYGiDlAIEMM',
        'access_secret' : 'rhoqnAXt3VHz9dnNv8DlyDUd9V1fijfw2Of091UkjVUTV',
        'consumer_key' : 'nAllJpqiUKtnUG4aHrk2G6T9v',
        'consumer_secret' : 'QAY2CnNGt2onuun6QckyYniZeh753q6X4dEXw9mS3pjTecPk9Y'
    }
    print(q)
    myTwitterAction = Twitter.MyTwitterAction(FEATUHER)
    tweet_list = myTwitterAction.search_tweet_list(q, 100)
    #tweet_list = test_list
    tweetListParser = TweetListParser(tweet_list)
    tweetListParser.diet()
    tweetListParser.add_column("title", "")
    tweetListParser.add_column("supplement", "")
    tweetListParser.sort("favorite_count")
    tweetListParser.cutoff(50)
    tweetListParser.lang_trans()

    #tweetListParser.filter("id", tweet_id)
    new_tweet_list = tweetListParser.get()
    json_info = json.dumps(new_tweet_list, ensure_ascii=False, indent=4)
    Github.upload(REPO,  tweet_id+".json", json_info)

    print(new_tweet_list)
    params = {
        "tweet_list" : tweet_list
    }
    return params


class TweetListParser():
    def __init__(self, tweet_list):
        self.tweet_list = tweet_list
        self.trans_tweet_list = tweet_list
    
    def diet(self):
        #filter_method = ""
        #if filter = "":
        #    filter_method = self.cut
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            new_tweet_list.append(self.cut(tweet))
        self.trans_tweet_list = new_tweet_list
        return self.trans_tweet_list
    
    def cut(self, tweet):
        new_tags = ["id", "text", "retweet_count", "favorite_count", "in_reply_to_status_id"]
        new_tweet = {}
        for tag in new_tags:
            new_tweet[tag] = tweet[tag]
        twitterUserParser = TwitterUserParser(tweet["user"])
        new_tweet["user"] = twitterUserParser.cut()
        return new_tweet
    
    def add_column(self, tag, init):
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            tweet[tag] = init
            new_tweet_list.append(tweet)
        self.trans_tweet_list = new_tweet_list
        return self.trans_tweet_list
    
    def filter(self, tag, value):
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            print(tweet["id"])
            print(value)
            if( str(tweet[tag]) == str(value) ):
                new_tweet_list.append(tweet)
        self.trans_tweet_list = new_tweet_list
        return new_tweet_list
    
    def sort(self, tag):
        self.trans_tweet_list = sorted(self.trans_tweet_list, key=lambda x: x[tag])
        return self.trans_tweet_list
    
    def cutoff(self, num):
        new_tweet_list = []
        for i, tweet in enumerate(self.trans_tweet_list):
            new_tweet_list.append(tweet)
            if i>= num:
                break
        self.trans_tweet_list = new_tweet_list
        return new_tweet_list
    
    def lang_trans(self):
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            tweet["ja_text"] = GoogleTrans.en_to_ja(tweet["text"])
            print(tweet["ja_text"])
            new_tweet_list.append(tweet)
        self.trans_tweet_list = new_tweet_list
    
    def get(self):
        return self.trans_tweet_list
    

class TwitterUserParser():
    def __init__(self, user_info):
        self.user_info = user_info
        self.trans_user = {}
    
    def cut(self):
        new_tags = [
            "id", 
            "name", 
            "screen_name", 
            "location", 
            "description", 
            "profile_background_image_url", 
            "profile_image_url",
            "followers_count", 
            "friends_count"
        ]
        for tag in new_tags:
            self.trans_user[tag] = self.user_info[tag]
        return self.trans_user



def main():
    class Request():
        def __init__(self):
            self.GET = {
                "since" : "2022-05-23",
                "until" : "2022-05-24",
                "user"  : "denicmarko",
                "tweet_id"    : "1528678833561509897"
            }
    request = Request()
    params = editor(request)

if __name__ == "__main__":
    main()

