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
