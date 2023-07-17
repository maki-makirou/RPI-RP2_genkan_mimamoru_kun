# RPI-RP2_genkan_mimamoru_kun
It is a device using Raspberry Pi Pico W that aggregates the detection results of the human sensor and reports it on LINE.

「玄関みまもるくん」（Raspberry Pi Pico W を使用した玄関の出入り監視装置）





人感センサーの反応回数を記録し、1日1回、1時間単位で集計してLINE通知してくれます。
その他に以下の機能があります。

・1日1回指定時間でのNTPサーバを使った時間合わせ
・指定時間内、初感知時のリアルタイムLINE通知（平日のみ。人感センサーが連続3秒反応があった時）
・毎時計測値のpico内ログ記録（急に電源が落ちても過去1日の計測値を確認出来る）

microPythonのコードを公開します。

main.pyの以下の設定を忘れずに行ってください。

# 自宅Wi-FiのSSIDとパスワードを入力
# LINE tokenを入力

main.py と同じ場所に以下の参考サイトにある tiny_line.py を置いてください。


【参考サイト】
sozorablog | Raspberry Piで電子工作をはじめよう
https://sozorablog.com/raspberry-pi-pico-w-review/

全面的に参考にさせていただいております。感謝。
