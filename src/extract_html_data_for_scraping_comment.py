import requests
from bs4 import BeautifulSoup
import re


def extract_html_data_for_scraping_comment(archived_url):
    """配信アーカイブページからアーカイブコメントを保存するために必要な情報を抜き出す

    Args:
        archived_url: 配信アーカイブの URL

    Returns:
        start_time: 配信開始時間
        movie_id: 配信枠の ID
    """
    # 配信アーカイブのページ取得
    response = requests.get(archived_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 配信開始時刻を取得
    start_time = soup.select("#google-markup > div > meta:nth-child(4)")

    # アーカイブの movie id の取得
    return {"start_time": start_time[0].get("content"), "movie_id": re.findall("\w+$", archived_url)[0]}
