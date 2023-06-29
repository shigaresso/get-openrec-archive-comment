import re

from convert_time import convert_time


def create_next_time(last_comment_time):
    """まだ保存していないコメントの先頭の時間を作成する

    Args:
        last_comment_time: 最後に保存したコメントの投稿時間
    Return:
        コメントの投稿時間
    """

    # 新しい時間を作成するのに不要な部分は取り除く
    extract = last_comment_time.replace("+09:00", "")
    # 文字列から連続した数字部分を文字列の配列として取り出す
    time_array = re.findall(r"\d+", extract)

    [year, month, day, hour, minute, second] = convert_time(time_array)
    return f"{year}-{month}-{day}T{hour}:{minute}:{second}"
