import csv


def write_comment_to_csv_file(movie_id, comment_jsons):
    """コメントを csv ファイルに書き込む

    Args:
        movie_id: 保存する CSV ファイル名
        comment_jsons: オブジェクト形式のコメント配列
    """
    with open(f"./{movie_id}.csv", "a", encoding='utf-8') as f:
        for comment in comment_jsons:
            csv.writer(f).writerow([comment["posted_at"], comment["id"], comment["message"]])
