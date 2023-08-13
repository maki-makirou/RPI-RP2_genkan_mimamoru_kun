# 「玄関みまもるくん」 RPI-RP2_genkan_mimamoru_kun
It is a device using Raspberry Pi Pico W that aggregates the detection results of the human sensor and reports it on LINE.


## 機能
**「玄関みまもるくん」（Raspberry Pi Pico W を使用した玄関の出入り監視装置）**

<img src="https://github.com/maki-makirou/RPI-RP2_genkan_mimamoru_kun/blob/main/IMG_5380.JPG" width="320px">　　<img src="https://github.com/maki-makirou/RPI-RP2_genkan_mimamoru_kun/blob/main/IMG_5493.JPG" width="320px">

人感センサーの反応回数（測定間隔1秒）を記録し、1日1回、1時間単位で集計してLINE通知してくれます。
その他に以下の機能があります。

- 1日1回指定時間でのNTPサーバを使った時間合わせ
- 指定時間内、初感知時のリアルタイムLINE通知（人感センサーが連続3秒反応があった時。曜日指定可能。初期設定：月～金のみ）
- 毎時計測値のpico内ログ記録（急に電源が落ちても過去1日の計測値を確認出来る）


## 使用部品
- Raspberry Pi Pico W
- 人感センサー(HC-SR501)
- USB ACアダプタ
- USBケーブル (2.0タイプAオス-マイクロBケーブル) 
- 取付ケース（例としてティッシュペーパーの箱😅　取付方法は写真を参考に自由に作成してください。）

## 人感センサーの設定
ジャンパはH側とし待ち時間なしとする。
ジャンパに近い方が感度調整（3〜7m）なのでドライバで反時計回りに最大にし3mとする。
ジャンパから遠い方が時間遅延調整（5〜200秒）なので反時計回りに最大にして5秒とする。

<img src="https://github.com/maki-makirou/RPI-RP2_genkan_mimamoru_kun/blob/main/IMG_5570.JPG" width="320px">

**接続は、電源+を VBUS に、電源-を GND に、信号を GP16 にしてください。**


## 使い方
main.py と同じ場所に以下の参考サイトにある tiny_line.py を置いてください（参考サイト参照）。
また、main.py の以下を忘れずに書き換えてください。

- 「自宅Wi-FiのSSIDとパスワードを入力」
- 「LINE tokenを入力」

初期設定は以下の通りです。
　
- NTP時刻合わせ時間 3時29分
- レポート送信時間 8時10分
- 帰宅時間通知開始および終了時間 12時から21時まで

LINE token の取得方法については以下の参考サイトをご覧ください。

**無事に繋がると Raspberry Pi Pico W の LED が3回点滅**します。その他の場合は再度ACアダプタを抜き差しして電源を入れなおしてください。


## 注意点
- センサーの設置位置はなるべく低くしてください。誤検出が少なくいい結果が得られます。


## 参考サイト
- sozorablog | Raspberry Piで電子工作をはじめよう
https://sozorablog.com/raspberry-pi-pico-w-review/

本コードは、そぞらさんのサイト（sozorablog）を全面的に参考にさせていただいております。
コード掲載のご許可もいただきました。ありがとうございます。
