import RPi.GPIO as GPIO
import os
import time
from datetime import datetime

MPG123 = "/usr/bin/mpg123"

# GPIO設定
ALARM_STOP_BTN = 17
MUSIC_BTN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(ALARM_STOP_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MUSIC_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


ALARM_SOUND = "sounds/hituzi.mp3"
MUSIC_SOUND = "sounds/music.mp3"

alarm_playing = False
alarm_done_today = False

current_date = datetime.now().strftime("%Y-%m-%d")
last_date = current_date


def get_alarm_time():
    try:
        with open("alarm.txt") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    
def start_alarm():
    print("アラーム開始")
    os.system(f"{MPG123} -q {ALARM_SOUND} &")
    return True

try:
    while True:
        alarm_time = get_alarm_time()
        now = datetime.now().strftime("%H:%M")

        today = datetime.now().strftime("%Y-%m-%d")
        if today != last_date:
            alarm_done_today = False
            last_date = today

        if alarm_time and now == alarm_time and not alarm_playing and not alarm_done_today:
            alarm_playing = start_alarm()

        if GPIO.input(ALARM_STOP_BTN) == GPIO.LOW and alarm_playing:
            print("アラーム停止")
            os.system("pkill mpg123")
            alarm_playing = False
            alarm_done_today = True
            time.sleep(1)

        if GPIO.input(MUSIC_BTN) == GPIO.LOW:
            print("音楽再生")
            os.system("pkill mpg123")
            alarm_playing = False
            os.system(f"{MPG123} {MUSIC_SOUND} &")
            time.sleep(1)

        time.sleep(0.2)



except KeyboardInterrupt:
    GPIO.cleanup()
    os.system("pkill mpg123")
    print("終了しました")
