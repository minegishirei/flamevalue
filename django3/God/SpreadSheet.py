import gspread
import json

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 


def main(sheetname):
    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/God/key.json', scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '1I7hd3uJTAyBG9fwildgI6UPhUh1eIqu9Ai67VBIjyws'

    print(gc.open_by_key(SPREADSHEET_KEY))

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(sheetname)

    taglist = []
    for i, cell in enumerate(worksheet.range("A1:H1")):
        taglist.append(cell.value)
    
    infolist = []
    row = {}
    for i, cell in enumerate(worksheet.range("A2:H100")):
        column = (i+1)%8
        tag = taglist[column-1]
        row.update({
            tag : cell.value
        })
        if column == 0:
            if row["title"] == "":
                break
            infolist.append(row)
            row = {}
        
    return infolist

from collections import deque

def registar(row ):
    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/God/spreadsheet-test-96941483f853のコピー.json', scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '1I7hd3uJTAyBG9fwildgI6UPhUh1eIqu9Ai67VBIjyws'
    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet("stock")


    queue = deque(row)
    ds= worksheet.range("A1:C100")
    for i, cell in enumerate(ds):
        column = (i+1)%6-1
        if cell.value != "":
            continue

        if len(queue) == 0 :
            break
        else:
            cell.value = queue.popleft()
            print(cell.value)
    worksheet.update_cells(ds)

