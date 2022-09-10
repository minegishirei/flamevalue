import requests
from bs4 import BeautifulSoup
 
# User-Agent
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
 
def get_html(url, params=None, headers=None):
 
    try:
        # データ取得
        resp = requests.get(url, params=params, headers=headers)
        resp.encoding = 'shift_jis'  # 文字コード
        #print(resp.text)
        # 要素の抽出
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup
    except Exception as e:
        return None
     
def get_text_by_class(soup, class_name):
     
    text = soup.find(class_=class_name).text
    text = text.strip()  
     
    return text
 
def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None
 
# 募集概要マスター
def get_master_offer():
     
    d = {}
    d["job"] = "仕事内容"
    d["skill"] = "求めている人材"
    d["location"] = "勤務地"
    d["salary"] = "給与"
    d["work_time"] = "勤務時間"
    d["holiday"] = "休日・休暇"
    d["benefits"] = "待遇・福利厚生"
 
    return d
 
 
# 会社概要マスター
def get_master_company_info():
     
    d = {}
    d["company_name"] = "社名"
    d["date"] = "設立"
    d["representative"] = "代表者"
    d["capital"] = "資本金"
    d["sales"] = "売上高"
    d["employees"] = "従業員数"
    d["office"] = "事業所"
    d["industry"] = "業種"
    d["business"] = "事業内容"
 
    return d
 
if __name__ == '__main__':
     
    # 結果
    result = {}
     
    # 募集概要
    d_offer = get_master_offer()
 
    # 会社概要
    d_heading = get_master_company_info()
 
    # データ取得
    url = "https://next.rikunabi.com/company/cmi3631612001/nx2_rq0019322789/"
    params = {}
    headers = {"User-Agent": user_agent}
    soup = get_html(url, params, headers)
     
    if soup != None:
         
        # タイトル
        title = get_text_by_class(soup, "rn3-companyOfferHeader__heading")
        result["title"] = title
         
        # タイトル
        period = get_text_by_class(soup, "rn3-companyOfferHeader__period")
        result["period"] = period
         
        # 募集概要
        elems_offer_info = soup.find_all(class_="rn3-companyOfferRecruitment__info")
        for elem_offer_info in elems_offer_info:
            heading = get_text_by_class(elem_offer_info, "rn3-companyOfferRecruitment__heading")
            text = get_text_by_class(elem_offer_info, "rn3-companyOfferRecruitment__text")
             
            key = get_key_from_value(d_offer, heading)
             
            if key:
                result[key] = text
             
        # 会社概要
        elems_company_info = soup.find_all(class_="rn3-companyOfferCompany__info")
        for elem_company_info in elems_company_info:
            heading = get_text_by_class(elem_company_info, "rn3-companyOfferCompany__heading")
            text = get_text_by_class(elem_company_info, "rn3-companyOfferCompany__text")
             
            key = get_key_from_value(d_heading, heading)
            result[key] = text
             
    else:
        print("エラー")
     
    print(result)
