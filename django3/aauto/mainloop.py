import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime


repo = "engineer_rank"

def main():
    tag_list = Github.seach_page_list(repo)

    for htmlname in tag_lis[:1]:
        Github.delete_page(repo, htmlname)
        """
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list('"'+ htmlname+ '"' + " lang:ja min_faves:100", amount=50)
        
        git_json = {}
        git_json.update({
            "tweet_list" : tweet_list
        })

        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.upload(repo, htmlname, text)
        """
    
main()