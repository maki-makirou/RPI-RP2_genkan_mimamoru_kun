# 「玄関みまもるくん」 RPI-RP2_genkan_mimamoru_kun
It is a device using Raspberry Pi Pico W that aggregates the detection results of the human sensor and reports it on LINE.

## 機能
「玄関みまもるくん」（Raspberry Pi Pico W を使用した玄関の出入り監視装置）

人感センサーの反応回数（測定間隔1秒）を記録し、1日1回、1時間単位で集計してLINE通知してくれます。
その他に以下の機能があります。

- 1日1回指定時間でのNTPサーバを使った時間合わせ
- 指定時間内、初感知時のリアルタイムLINE通知（平日のみ。人感センサーが連続3秒反応があった時）
- 毎時計測値のpico内ログ記録（急に電源が落ちても過去1日の計測値を確認出来る）


## 使用部品
- Raspberry Pi Pico W
- 人感センサー(HC-SR501)

## 使い方
main.py と同じ場所に以下の参考サイトにある tiny_line.py を置いてください。
main.pyの以下を忘れずに書き換えてください。

「自宅Wi-FiのSSIDとパスワードを入力」
「LINE tokenを入力」

初期設定は以下の通りです。

- NTP時刻合わせ時間 3時29分
- レポート送信時間 8時10分
- 帰宅時間通知開始および終了時間 12時から21時まで

LINE tokenの取得方法については以下をご覧ください。

## 参考サイト
- sozorablog | Raspberry Piで電子工作をはじめよう
https://sozorablog.com/raspberry-pi-pico-w-review/

本コードは、そぞらさんのサイト（sozorablog）を全面的に参考にさせていただいております。
コード掲載のご許可もいただきました。ありがとうございます。

## 注意点
- センサーの設置位置はなるべく低くしてください。誤検出が少なくいい結果が得られます。
