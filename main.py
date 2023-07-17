import utime
import urequests as requests
import network
import socket
from tiny_line import tiny_line
import ntptime
from machine import Pin #import Pin library

### 初期設定
# NTP時刻合わせ時間
ntp_h = 3
ntp_m = 29

# レポート送信時間
repo_h = 8
repo_m = 10

# 帰宅時間通知開始および終了時間
start_h = 12
stop_h = 21

pir = Pin(16, Pin.IN,Pin.PULL_DOWN)  # set GP16 as digital input pin for PIR motion sensor

# 自宅Wi-FiのSSIDとパスワードを入力
ssid = 'YOUR NETWORK SSID'
password = 'YOUR NETWORK PASSWORD'

# LINE tokenを入力
access_token = 'YOUR LINE Notify token'

# 初期化
tl = tiny_line(access_token, debug=True)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
#    print('waiting for connection...')
    utime.sleep(1)
    
# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        utime.sleep(0.2)
        led.off()
        utime.sleep(0.2)
        
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth        

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

status = wlan.ifconfig()


def ntp_set():
    timZone = 9
    ntptime.host = "ntp.nict.jp"
    ntptime.settime()
    t0 = machine.RTC().datetime()
    hour = t0[4] + timZone
    day = t0[2]

    # 24時を超えた場合、時間を-24する
    if hour >= 24:
        hour -= 24
        day += 1
        
    global LINE_Message
    LINE_Message = "{0}/{1:02d}/{2:02d} {3:02d}:{4:02d}:{5:02d}".format(t0[0], t0[1], day, hour, t0[5], t0[6]) +" スタート"
    utime.sleep(1)


def ntp_set_line():
    ntp_set()
    tl.notify(LINE_Message)    

def report():
    global LINE_Message
    LINE_Message = "{0}/{1:02d}/{2:02d} {3:02d}:{4:02d}".format(now_yy, now_mm, now_d, now_h, now_m) +" 時点" \
                     + " 0時: " + str(on_count[0]) + ", " + str(off_count[0]) + ", " \
                     + " 1時: " + str(on_count[1]) + ", " + str(off_count[1]) + ", " \
                     + " 2時: " + str(on_count[2]) + ", " + str(off_count[2]) + ", " \
                     + " 3時: " + str(on_count[3]) + ", " + str(off_count[3]) + ", " \
                     + " 4時: " + str(on_count[4]) + ", " + str(off_count[4]) + ", " \
                     + " 5時: " + str(on_count[5]) + ", " + str(off_count[5]) + ", " \
                     + " 6時: " + str(on_count[6]) + ", " + str(off_count[6]) + ", " \
                     + " 7時: " + str(on_count[7]) + ", " + str(off_count[7]) + ", " \
                     + " 8時: " + str(on_count[8]) + ", " + str(off_count[8]) + ", " \
                     + " 9時: " + str(on_count[9]) + ", " + str(off_count[9]) + ", " \
                     + "10時: " + str(on_count[10]) + ", " + str(off_count[10]) + ", " \
                     + "11時: " + str(on_count[11]) + ", " + str(off_count[11]) + ", " \
                     + "12時: " + str(on_count[12]) + ", " + str(off_count[12]) + ", " \
                     + "13時: " + str(on_count[13]) + ", " + str(off_count[13]) + ", " \
                     + "14時: " + str(on_count[14]) + ", " + str(off_count[14]) + ", " \
                     + "15時: " + str(on_count[15]) + ", " + str(off_count[15]) + ", " \
                     + "16時: " + str(on_count[16]) + ", " + str(off_count[16]) + ", " \
                     + "17時: " + str(on_count[17]) + ", " + str(off_count[17]) + ", " \
                     + "18時: " + str(on_count[18]) + ", " + str(off_count[18]) + ", " \
                     + "19時: " + str(on_count[19]) + ", " + str(off_count[19]) + ", " \
                     + "20時: " + str(on_count[20]) + ", " + str(off_count[20]) + ", " \
                     + "21時: " + str(on_count[21]) + ", " + str(off_count[21]) + ", " \
                     + "22時: " + str(on_count[22]) + ", " + str(off_count[22]) + ", " \
                     + "23時: " + str(on_count[23]) + ", " + str(off_count[23]) + "\n" \
                     + "-------------- \n" \
                     + "7:00−7:10: " + str(rin_count[0]) + "\n" \
                     + "7:10−7:20: " + str(rin_count[1]) + "\n" \
                     + "7:20−7:30: " + str(rin_count[2]) + "\n" \
                     + "7:30−7:40: " + str(rin_count[3]) + "\n" \
                     + "7:40−7:50: " + str(rin_count[4]) + "\n" \
                     + "7:50−8:00: " + str(rin_count[5]) + "\n" \
                     + "8:00−8:10: " + str(rin_count[6])


def report_line():
    report()
    tl.notify(LINE_Message)
    utime.sleep(1)


def detected_line():
    global LINE_Message
    LINE_Message = "{0}/{1:02d}/{2:02d} {3:02d}:{4:02d}".format(now_yy, now_mm, now_d, now_h, now_m) + "感知しました！！"
    tl.notify(LINE_Message)
    utime.sleep(1)
    

def save_log():
    report()
    with open('log.txt', 'w') as f:
        print(LINE_Message, file=f)


ntp_set_line()

with open('log.txt', 'w') as f:
    print("", file=f)

timZone = 9
t = machine.RTC().datetime()
hour = t[4] + timZone
if hour >= 24:
    hour -= 24
pre_h = hour
pre_m = t[5]
pre_s = t[6]

utime.sleep(5)

on_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
off_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
rin_count = [0,0,0,0,0,0,0]    # 7:00-,7:10-,7:20-,7:30-,7:40-,7:50-,8:00-

send_flag = 1
seq_flag = 0
seq1 = 0
seq2 = 0
seq3 = 0
while True:
    t = machine.RTC().datetime()
    hour = t[4] + timZone
    day = t[2]
    week = t[3]
    if hour >= 24:
        hour -= 24
        day += 1
        week += 1
        if week == 7:
            week == 0
    now_yy = t[0]
    now_mm = t[1]
    now_d = day
    now_h = hour
    now_w = week
    now_m = t[5]
    now_s = t[6]
    if now_h == pre_h and now_m == pre_m and now_s == pre_s:
        pass
    else:
        if now_h == stop_h and now_m == 0 and now_s == 0:    # reset send_flag
            send_flag = 1
        if pir.value():    #when PIR detects motion 
            on_count[hour] += 1
            seq3 = seq2
            seq2 = seq1
            seq1 = 1
            if seq1 == 1 and seq2 == 1 and seq3 == 1: 
                seq_flag = 1
            if now_h == 7 and now_m >= 0 and now_m <= 9:
                rin_count[0] += 1
            elif now_h == 7 and now_m >= 10 and now_m <= 19:
                rin_count[1] += 1            
            elif now_h == 7 and now_m >= 20 and now_m <= 29:
                rin_count[2] += 1
            elif now_h == 7 and now_m >= 30 and now_m <= 39:
                rin_count[3] += 1
            elif now_h == 7 and now_m >= 40 and now_m <= 49:
                rin_count[4] += 1
            elif now_h == 7 and now_m >= 50 and now_m <= 59:
                rin_count[5] += 1            
            elif now_h == 8 and now_m >= 0 and now_m <= 9:
                rin_count[6] += 1
            # now_w <= 4: 月曜から金曜まで動作。　now_w <= 5: 月曜から土曜まで動作。　now_w <= 6: 月曜から日曜まで動作。
            elif now_h >= start_h and now_h <= (stop_h - 1) and send_flag == 1 and now_w >= 0 and now_w <= 4 and seq_flag == 1:
                detected_line()
                send_flag = 0
                seq_flag = 0
                seq1 = 0
                seq2 = 0
                seq3 = 0
        else:
            off_count[hour] += 1
            seq3 = seq2
            seq2 = seq1
            seq1 = 0
        print(t[6],seq1,seq2,seq3)

        if now_m == 1 and now_s == 0:
            save_log()

        if now_h == ntp_h and now_m == ntp_m and now_s == 0:
            ntp_set()

        if now_h == repo_h and now_m == repo_m and now_s == 0:
            report_line()
            on_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            off_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            rin_count = [0,0,0,0,0,0,0] 

        pre_h = now_h
        pre_m = now_m
        pre_s = now_s

    utime.sleep(0.6)

