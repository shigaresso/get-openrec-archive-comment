import math


def display_execution_time(start_time, end_time):
    """全コメントの取得に費やした時間を出力

    Args:
        start_time: コメント取得を開始した時間
        end_time: コメント取得が終了した時間
    """
    # コメント取得に経過した時間
    run_time = end_time - start_time

    # コメント取得に何分:何秒掛かったかへの変換
    minute = run_time // 60
    second = run_time % 60
    # 時間を 2 桁でない場合は 0 で埋め、文字列にする
    minute_string = str(math.floor(minute)).rjust(2, "0")
    second_string = str(math.floor(second)).rjust(2, "0")
    print(f"コメント取得に費やした時間: {minute_string}:{second_string}")
