import time
from unittest import result
from venv import create
import requests
import json
import sys
import csv

# 利用する URL "https://public.openrec.tv/external/api/v5/movies/d1rn4jl998v/chats?from_created_at=2022-03-27T09:17:47.000Z&is_including_system_message=false"


def main():
    create_csv()
    # python3 main.py 2022-03-27T09:17:47 と実行すること前提で作られている
    live_start_time = sys.argv[1]
    save_comment_page(live_start_time)


# コメントを保存する一連の流れ 再起関数にする
def save_comment_page(start_time):
    # 次のコメントページも取得しやすいように URL は次の 3 つを組み合わせる
    server_url = ["https://public.openrec.tv/external/api/v5/movies/d1rn4jl998v/chats?from_created_at=", ".000Z&is_including_system_message=false"]
    connect_url = f"{server_url[0]}{start_time}{server_url[-1]}"
    # コメントページの取得
    response = requests.get(connect_url)
    # JSON 文字列を Python のオブジェクトとして使えるようにする
    comment_json = json.loads(response.text)

    # ここでコメントを CSV 形式で保存する処理
    # write_csv(comment_json)

    # コメント数が 100 じゃなければ配信が終わっている
    if len(comment_json) < 100:
        return

    # 次の URL に必要なページ最後のコメント時間
    last_comment_time = comment_json[-1]["posted_at"] # 2022-03-27T18:18:05+09:00 が取得される
    # TODO 時間を URL ように変換する方法が必要
    # start_time = next_url
    converted_url = create_next_time(last_comment_time)

    # 次に保存するコメントページの URL
    next_connect_url = f"{server_url[0]}{converted_url}{server_url[-1]}"

    # 1 秒待たせる
    # time.sleep(1)
    # 次のコメントを取得する
    # save_comment_page(start_time)

def create_csv():
    with open("./sample.csv", "w", encoding='utf-8') as f:
        csv.writer(f).writerow(["getTime", "message"])

# コメントを CSV ファイルに書き込み
def write_csv(comment_json):
    with open("./sample.csv", "a", encoding='utf-8') as f:
        for json in comment_json:
            csv.writer(f).writerow([{json["posted_at"]}, json["message"]])

def create_next_time(last_comment_time):
    result = ""
    return result

# 2022-03-27T18:18:05+09:00 という値から 2022-03-27T09:18:05.000Z という値に加工したい
# .000Z は別に含めておくので 2022-03-27T09:18:05 に出来れば OK


# 取得したデータを保存する
# with open('savefile.txt', 'w') as f:
#     f.write(response.text)



main()