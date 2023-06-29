# 次に接続するページの URL を作成する
def create_scraping_url(start_time, movie_id):
    server_url = [f"https://public.openrec.tv/external/api/v5/movies/{movie_id}/chats?from_created_at=", ".000Z&is_including_system_message=false"]
    return f"{server_url[0]}{start_time}{server_url[-1]}"
