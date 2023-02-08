# アプリケーションの利用方法

プログラム言語は Python3 を利用している。  
GitHub から本プロジェクトをダウンロードする。  
プロジェクトのルート上のターミナルで

```sh
pip install -r requirements.txt
```

で依存関係のインストールを行う。

```sh
cd src
python3 main.py コメントを保存したいアーカイブの URL
```

を実行する。

## TODO 改善が必要な点

（優先順位）

1. 作成する URL が日またぎになる場合の処理は作成しているが、月またぎや年またぎ（閏年の場合も考慮）になる配信の場合、サーバーにうまく接続できないのでその改善も必要。
2. CSV として保存するコメント取得時間を毎分辺りのグラフに利用できるように加工して保存するようにも改善が必要。
3. 全コメントの取得に掛かった時間をターミナルへ表示するようにしたい。

## 利用ライブラリ

requests、bs4（BeautifulSoup）

## チャットのサーバーに接続するには何が必要か？

- アーカイブの URL  
  ここから抜き出せるものは複数ある

1. アーカイブの movie ID  
   チャットを保存するために接続する URL の生成に必要。
2. 配信の開始時間  
   何分からコメントを取得すれば良いかがわかる。
3. 配信の終了時間
   いつスクレイピングを止めれば良いかがわかる。

これらは requests と BeautifulSoup を利用して、アーカイブ画面の HTML から抜き出す。

## 分析には何が必要か？

- **コメントが流れた時間**「"posted_at" プロパティ」  
  コメントが流れた時間は、 一定時間に流れたコメントの数を分析するために必要となる。

- **コメント内容**「"message" プロパティ」  
  コメント内容は、『草』などの盛り上がりを表すコメントが一定時間にどれだけ流れたかを知りたい場合に必要となる。

- **ユーザー名**「"id" プロパティ」  
  ユーザー名は、次のコメントページへ移動する際に、同じコメントを保存してしまう。  
  その重複を避けるには、"posted_at" と "id" の 2 つが同じ場合はコメントを保存しない処理をする必要がある。

## 次のコメント保存ページへの移動方法

次のコメントページへの移動は、コメントページ内の末尾の **"posted_at"** のプロパティを加工して URL を作成することになる。

ただし、取得した値が 2022-03-27T18:17:57+09:00 の場合  
T 以降から 9 時間引いた値を用いて 2022-03-27T09:17:57Z とする。  
9 時を越えるまでのマイナスになる時間（要するに 0 時から 9 時までの間は +24 した値から 9 引くことになる）  
"posted_at":"2022-03-28T00:42:04+09:00" の場合、2022-03-27T15:42:04.000Z となる。  
T09 を越えるまではずっと 2022−03−27 と変更した URL が必要であることに注意。

## 苦戦した点

次のページの URL 作成時、時間を −9 するが、引いた結果が一桁だった時、に 01 のように変更することを忘れていた。  
次のページの URL の一部を引数として関数に渡すのに、URL すべてを渡してエラーが出ていることに気付かなかった。  
エラーが出ている箇所は **converted_url = create_next_time（comment_json[-1]["posted_at"]）** だったり **csv.writer（f）.writerow（[json["posted_at"], json["id"], json["message"]]）** だが、正しくない URL にアクセスしていたので、存在しない配列を取得しようとしてエラーが出ていたと思われる。  
1 ページにコメントが最大 100 個なのだが、100 個じゃなければ配信が終了していると定義していた。  
すると 99 個しか取得できていないが配信が続いている場合がある。

どう対処する？  
配信に投稿されたコメントの末尾は、アクセスした URL と次のページの URL の時間がイコールになったら最後のコメントだと考える。  
ただし、1 秒間で 100 コメント流れる場合は成立しない。  
なので、時間がイコールになると 1 秒足した URL を渡すことにする。  
配列が空なら配信の最後のコメントまで取得した事になると考える。

1 つ前のコメントと現在のコメントの URL の時間を比較することになる。  
現在のコメントがひとつ前のコメントにあった場合削除する。  
現在のループでは、

- ひとつ前のページの現在時間の URL 時間コメント
- 現在のページの次のページ時間の URL 時間コメント
- 現在のコメントと 1 つ前の現在の URL 時間コメントの差分  
  の 3 つの変数を所持していたい。  
  最後の 1 つはその部分を csv に書き込めば良いので、変数として保持する必要はない？
