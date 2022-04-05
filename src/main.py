import math
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
    live_start_time = create_next_time(need_parameter["start_time"])

    # コメント取得開始時間
    program_start_time = time.time()
    # 最初の接続時はコメントがないので第三引数には空配列を渡す
    save_comment_page(live_start_time, need_parameter["movie_id"], [])

    # コメント取得に経過した時間
    run_time = time.time() - program_start_time

    # コメント取得に何分:何秒掛かったか
    minute = run_time // 60
    second = run_time % 60
    # 時間を 2 桁でない場合は 0 で埋め、文字列にする
    minute_string = str(math.floor(minute)).rjust(2, "0")
    second_string = str(math.floor(second)).rjust(2, "0")
    print(f"コメント取得に費やした時間: {minute_string}:{second_string}")


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
def save_comment_page(start_time, movie_id, current_time_past_added_jsons):
    # ユーザーエージェントを追記していないと弾かれる可能性がある
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    headers = {"user-agent": user_agent} 
    # コメントページの取得
    response = requests.get(create_connect_url(start_time, movie_id), headers=headers)
    # JSON 文字列を Python のオブジェクトとして使えるようにする
    comment_jsons = json.loads(response.text)

    # 保存する必要がある差分コメント
    unique_comments = save_unique_comments(comment_jsons, current_time_past_added_jsons)

    # ここでコメントを CSV 形式で保存する処理
    write_csv(movie_id, unique_comments)

    # 次に保存するコメントページの URL の一部が戻り値
    next_time = create_next_time(comment_jsons[-1]["posted_at"])
    print(next_time)

    # 今回のページの最初のコメント時間と、次回のページの最初のコメント時間が同じ場合は配信が終了しているとみなす
    if (next_time == start_time):
        return

    # 既に追加したコメント 次のページで一度追加したコメントを 2 回保存しないために用いる
    already_added_comments = saved_comments(comment_jsons)
    # 1 秒待たせる
    time.sleep(1)
    # 次のコメントを取得する
    save_comment_page(next_time, movie_id, already_added_comments)


# 次に接続するページの URL を作成する
def create_connect_url(start_time, movie_id):
    server_url = [f"https://public.openrec.tv/external/api/v5/movies/{movie_id}/chats?from_created_at=", ".000Z&is_including_system_message=false"]
    return f"{server_url[0]}{start_time}{server_url[-1]}"


# 差分のコメント配列を作成する
def save_unique_comments(comment_jsons, past_added_jsons):
    # 前回のコメントと今回のコメントで被っていないコメントのみを抽出する
    unique_comments = []
    for comment_json in comment_jsons:
        # 前回の配列と比較して入ってないものがあれば配列に追加
        if comment_json not in past_added_jsons:
            unique_comments.append(comment_json)
    return unique_comments


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


# 既に CSV ファイルに入っているコメントの配列を作成する
def saved_comments(comment_jsons):
    added_comments = []
    for comment_json in comment_jsons:
        if comment_json["posted_at"] == comment_jsons[-1]["posted_at"]:
            added_comments.append(comment_json)
    return added_comments


main()