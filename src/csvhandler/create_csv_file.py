import csv


def create_csv_file(movie_id):
    """配信コメントを保存するための CSV ファイルを作成する

    Args:
        movie_id: 配信アーカイブとなった動画の ID
    """
    with open(f"./{movie_id}.csv", "w", encoding='utf-8') as f:
        csv.writer(f).writerow(["getTime", "id", "message"])
