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



class ActionFactory():
    def __init__(self):
        super().__init__()
    
    def getAction(self, char, target):
        if char == "u":
            return UpdateAction(target)
        elif char=="d":
            return DeleteAction(target)

                
                
actionFactory = ActionFactory()
def page(request, htmlname):
    session = request.session
    params = {
        "title" : "反省書エディター🙇‍♂️",
        "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
        "favicon" : "/static/チャット.png"
    }
    value = getSessionValue(request, "deleteAll")
    if len(value) > 1 and ("transition" in session):
        del session["transition"]

    #新規作成
    if 'transition' not in session:
        transition = [{
                "process":"1",
                "name": "input1",
                "title": "結論",
                "supp":"あなたは何をやらかしました？",
                "preface":"この度は",
                "example":"定例会議に15分以上も遅刻してしまい",
                "afterword":"、申し訳ございませんでした。",
                "next":"./oko.html#slide=3"
            },{
                "process":"2",
                "name": "input2",
                "title": "原因",
                "supp":"何がよくなかったでしょう？",
                "preface":"直接の原因は",
                "example":"昨日タイマーを設定し忘れたこと",
                "afterword":"が原因です。",
                "next":"./oko.html#slide=4"
            }
        ]
        request.session["transition"] = transition
    
    transition = request.session["transition"]
    pageContentList = []
    for component in transition:
        for action in [ UpdateAction(component), DeleteAction(component)]:
            value = getSessionValue(request, component["name"] + "-" + action.char)
            component = action.run(value)
        pageContentList.append(component)
    request.session["transition"] = transition

    buildSentense = BuildSentense(transition)
    params.update({
        "pageContentList":pageContentList,
        "sentense" : buildSentense.build()
    })
    return render(request, f"apologagent/page/{htmlname}",params)




import random
class BuildSentense():
    def __init__(self, transition):
        super().__init__()
        self.transition = transition
        self.sentense = ""
    
    def build(self):
        self.sentense = ""
        for component in self.transition:
            for keytype in ["preface", "value", "afterword"]:
                if keytype in component:
                    self.sentense += component[keytype]
            self.sentense += "\n"
        self.sentense +=   self.decoration()
        return self.sentense 
    
    def decoration(self):
        choiceList = ["""このようなことが２度と起こらないよう、再発防止に努めます。
誠に申し訳ございませんでした。""",
        "二度と同じミスを犯さぬよう細心の注意を払う所存です。本当に申し訳ございませんでした。"]
        choice = random.choice(choiceList)
        return choice


class Action():
    def __init__(self, infodict):
        self.infodict = infodict
        super().__init__()
    def check(self, value):
        if len(value) > 1:
            return True
        return False
    def run(self):
        pass

class DeleteAction(Action):
    def __init__(self, infodict):
        super().__init__(infodict)
        self.char = "d"
    def run(self, value):
        if self.check(value):
            del self.infodict["value"]
        return self.infodict


class UpdateAction(Action):
    def __init__(self, infodict):
        super().__init__(infodict)
        self.char = "u"
    def run(self, value):
        if self.check(value):
            self.infodict["value"] = value
        return self.infodict







def getSessionValue(request, key):
    ans = request.POST.get(key)
    if ans is None:
        return ""
    return ans


def saveSessionValue(request, key, value):
    request.session[key] = value