import time
import requests
import json
import sys

from create_next_time import create_next_time
from create_scraping_url import create_scraping_url
from display_execution_time import display_execution_time
from extract_html_data_for_scraping_comment import extract_html_data_for_scraping_comment
from csvhandler.create_csv_file import create_csv_file
from csvhandler.write_comment_to_csv_file import write_comment_to_csv_file


# アーカイブの URL を受け取る (python3 main.py https://www.openrec.tv/live/d1rn4jl998v のようにしてプログラムを起動させる)
def main():
    archieve_url = sys.argv[1]
    need_parameter = extract_html_data_for_scraping_comment(archieve_url)
    create_csv_file(need_parameter["movie_id"])
    live_start_time = create_next_time(need_parameter["start_time"])

    # コメント取得開始時間
    program_start_time = time.time()
    # 最初の接続時はコメントがないので第三引数には空配列を渡す
    save_comment_page(live_start_time, need_parameter["movie_id"], [])

    display_execution_time(program_start_time)


# コメントを保存する一連の流れ 再帰関数にする
def save_comment_page(start_time, movie_id, current_time_past_added_jsons):
    # ユーザーエージェントを追記していないと弾かれる可能性がある
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    headers = {"user-agent": user_agent}
    # コメントページの取得
    response = requests.get(create_scraping_url(start_time, movie_id), headers=headers)
    # JSON 文字列を Python のオブジェクトとして使えるようにする
    comment_jsons = json.loads(response.text)

    # 保存する必要がある差分コメント
    unique_comments = save_unique_comments(comment_jsons, current_time_past_added_jsons)

    # ここでコメントを CSV 形式で保存する処理
    write_comment_to_csv_file(movie_id, unique_comments)

    # 次に保存するコメントページの URL の一部が戻り値
    next_time = create_next_time(comment_jsons[-1]["posted_at"])
    print(f"次に保存されるコメントの時間は {next_time}")

    # 今回のページの最初のコメント時間と、次回のページの最初のコメント時間が同じ場合は配信が終了しているとみなす
    if (next_time == start_time):
        return

    # 既に追加したコメント 次のページで一度追加したコメントを 2 回保存しないために用いる
    already_added_comments = saved_comments(comment_jsons)
    # 1 秒待たせる
    time.sleep(1)
    # 次のコメントを取得する
    save_comment_page(next_time, movie_id, already_added_comments)





# 差分のコメント配列を作成する
def save_unique_comments(comment_jsons, past_added_jsons):
    # 前回のコメントと今回のコメントで被っていないコメントのみを抽出する
    unique_comments = []
    for comment_json in comment_jsons:
        # 前回の配列と比較して入ってないものがあれば配列に追加
        if comment_json not in past_added_jsons:
            unique_comments.append(comment_json)
    return unique_comments










# 既に CSV ファイルに入っているコメントの配列を作成する
def saved_comments(comment_jsons):
    added_comments = []
    for comment_json in comment_jsons:
        if comment_json["posted_at"] == comment_jsons[-1]["posted_at"]:
            added_comments.append(comment_json)
    return added_comments




main()
