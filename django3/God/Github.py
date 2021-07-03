
from github import Github
from urllib.request import urlopen, quote
import urllib
from bs4 import BeautifulSoup
import os


credit_key = ""
if credit_key=="":
    with open("/God/Keys/github.key") as f:
        credit_key = f.read()

def upload(repo, filename, context):
    g = Github(credit_key)
    repo = g.get_user().get_repo(repo)
    repo.create_file(filename, 'commitmessage', context) 


def load(repo,filename):
    url = "https://raw.githubusercontent.com/kawadasatoshi/" + quote(repo) +"/master/" + filename
    response = urlopen(url).read()
    output = response.decode('utf-8')
    return output


def seach_page_list(repo):
    url = "https://github.com/kawadasatoshi/" + repo 
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    file_list = []
    flag = False
    for a_tag in  bsObj.findAll("a"):
        text = a_tag.get_text()
        if "commitmessage" == text :
            continue
        if "Terms" == text or "Releases" in text:
            break
        if text=="Create aaaaa":
            continue
        if text=="README.md":
            flag = False
        if flag:
            file_list.append(text)
        
        if text=="aaaaa":
            flag = True
    return file_list

    #<a class="js-navigation-open link-gray-dark" title="2進数.json" href="/kawadasatoshi/six_dim_wikipedia/blob/main/2%E9%80%B2%E6%95%B0.json">2進数.json</a>


def has_already_created(repo, filename):
    g = Github(credit_key)
    repo = g.get_user().get_repo(repo)
    obj = []
    try:
        obj = repo.get_dir_contents(path=filename)
    except:
        return False
    
    if type(obj) != type(list()):
        return True
    else:
        return False



def get_page_list(path="",):
    #g = Github("kawadasatoshi", "Withyou0114")
    g = Github(credit_key)
    repo = g.get_user().get_repo('memo')
    
    dir_list = []
    def get_path(path=""):
        #ファイルが一つしかないとき                
        obj = repo.get_dir_contents(path=path)


        if type(obj) != type(list()):
            print(obj)
            #シングル
            dir_list.append( path )
            return
        else:
            dir_list.append( path + "/")
            print(obj)
            for d in obj:
                next_path = os.path.join( path , d.name)
                get_path(next_path)
        
    get_path( path)

    return dir_list




class MemoTreeGenerator():
    def __init__(self):
        #g = Github("kawadasatoshi", "Withyou0114")
        g = Github(credit_key)
        self.repo = g.get_user().get_repo('memo')
        self.log_tree = {}
        self.get_path(path="", tree = self.log_tree)

    def get_path(self, path="", tree = {}):
        #ファイルが一つしかないとき                
        obj = self.repo.get_dir_contents(path=path)

        if type(obj) != type(list()):
            #ファイル
            info = grep_page_info(path)
            tree.update(info)
            return
            
        else:
            #フォルダー

            for d in obj:
                tree.update({
                    d.name : {}
                })

            for d in obj:
                print(d)
                next_path = os.path.join( path , d.name)
                self.get_path(next_path, tree[d.name])



def grep_page_info(path):
    info = {}
    content = load("memo", path)
    bsObj = BeautifulSoup(content)
    title_obj = bsObj.title
    if title_obj is not None:
        info.update({
            "title" : title_obj.get_text()
        })

    img_obj = bsObj.img
    if img_obj is not None:
        info.update({
            "img" : img_obj["src"]
        })


    return info





if __name__ == "__main__":
    result = seach_page_list("twitter_network")
    print(len(result))
