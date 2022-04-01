import re
import time
import requests
import json
import sys
import csv
from bs4 import BeautifulSoup

# アーカイブの URL を受け取る (python3 main.py https://www.openrec.tv/live/d1rn4jl998v のようにしてプログラムを起動させる)
def main():

    archieve_url = sys.argv[1]
    need_parameter = get_need_parameter(archieve_url)
    create_csv(need_parameter["movie_id"])
    start_time = create_next_time(need_parameter["start_time"])
    save_comment_page(start_time, need_parameter["movie_id"])
    print("コメント取得を終了しました")


def create_csv(movie_id):
    with open(f"./{movie_id}.csv", "w", encoding='utf-8') as f:
        csv.writer(f).writerow(["getTime", "id", "message"])


# アーカイブに接続し、必要な情報を取ってくる
def get_need_parameter(archive_url):
    # 配信アーカイブのページ取得
    response = requests.get(archive_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 配信開始時刻を取得
    start_time = soup.select("#google-markup > div > meta:nth-child(4)")

    # 現時点では配信継続時間が不要そうなのでコメントアウトした 必要になった場合は
    # , "live_duration_time": live_duration_time[0].get("content") を戻り値の引数に入れる
    # 配信継続時間を取得
    # live_duration_time = soup.select("#google-markup > div > meta:nth-child(5)")
    # , "live_duration_time": live_duration_time[0].get("content")

    # アーカイブの movie id の取得
    return {"start_time": start_time[0].get("content"), "movie_id": re.findall("\w+$", archive_url)[0]}


# コメントを保存する一連の流れ 再帰関数にする
def save_comment_page(start_time, movie_id):
    # 次のコメントページも取得しやすいように URL は次の 3 つを組み合わせる
    server_url = [f"https://public.openrec.tv/external/api/v5/movies/{movie_id}/chats?from_created_at=", ".000Z&is_including_system_message=false"]
    connect_url = f"{server_url[0]}{start_time}{server_url[-1]}"
    # コメントページの取得
    response = requests.get(connect_url)
    # JSON 文字列を Python のオブジェクトとして使えるようにする
    comment_json = json.loads(response.text)

    # ここでコメントを CSV 形式で保存する処理
    write_csv(movie_id, comment_json)

    # 次に保存するコメントページの URL の一部が戻り値
    next_time = create_next_time(comment_json[-1]["posted_at"])
    print(next_time)

    # 今回のページの最初のコメント時間と、次回のページの最初のコメント時間が同じ場合は配信が終了しているとみなす
    if (next_time == start_time):
        return

    # 1 秒待たせる
    time.sleep(1)
    # 次のコメントを取得する
    save_comment_page(next_time, movie_id)


# コメントを CSV ファイルに書き込み
def write_csv(movie_id, comment_json):
    with open(f"./{movie_id}.csv", "a", encoding='utf-8') as f:
        for json in comment_json:
            csv.writer(f).writerow([json["posted_at"], json["id"], json["message"]])


def create_next_time(last_comment_time):
    # 新しい時間を作成するのに不要な部分は取り除く
    extract = last_comment_time.replace("+09:00", "")
    # 文字列から連続した数字部分を文字列の配列として取り出す
    time_array = re.findall(r"\d+", extract)

    [year, month, day, hour, minute, second] = convert_time(time_array)
    return f"{year}-{month}-{day}T{hour}:{minute}:{second}"


# 受け取った時間から 9 引く必要があるのでこの関数が必要
def convert_time(time_array):
    [year, month, day, hour, minute, second] = time_array
    # 時間が 2桁 なら素直に 9 引ける
    if (hour[0] != "0"):
        hour = f"{int(hour) - 9}"
        # 引いた数値が 1 桁だった時に 0 を加える必要がある
        if (len(hour) == 1):
            hour = f"0{hour}"
        return [year, month, day, hour, minute, second]
    # 上の if で時間が ２桁 は除いてるので 09 だったら
    elif (hour == "09"):
        hour = "00"
        return [year, month, day, hour, minute, second]
    # 時間が 9 で引けない 1桁 であれば
    else:
        hour = f"{24 + int(hour[1]) - 9}"
        # 1日前になるので日付をずらす
        day = f"{day[0]}{int(day[1])-1}"
        return [year, month, day, hour, minute, second]


main()