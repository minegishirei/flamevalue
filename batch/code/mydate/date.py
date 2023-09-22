import datetime

def get_next_target_date(date, target_week):
    week = ['月','火','水','木','金','土','日']

    # 曜日を数値型で取得
    weekday = date.weekday()
    # dateから指定した曜日までの加算日数を計算
    add_days = 7 - weekday + week.index(target_week)
    # dateに加算
    next_target_date = date + datetime.timedelta(days = add_days)

    return next_target_date