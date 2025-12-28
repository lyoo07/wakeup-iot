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
alarm_process = None

def get_alarm_time():
    with open("alarm.txt", "r") as f:
        return f.read().strip()

try:
    while True:
        alarm_time = get_alarm_time()
        now = datetime.now().strftime("%H:%M")

        if now == ALARM_TIME and not alarm_playing:
            print("アラーム開始")
            alarm_process = os.system(f"{MPG123} -q {ALARM_SOUND} &")
            alarm_playing = True

        if GPIO.input(ALARM_STOP_BTN) == GPIO.LOW and alarm_playing:
            print("アラーム停止")
            os.system("pkill mpg123")
            alarm_playing = False
            time.sleep(1)

        if GPIO.input(MUSIC_BTN) == GPIO.LOW:
            print("音楽再生")
            os.system("pkill mpg123")
            os.system(f"{MPG123} {MUSIC_SOUND} &")
            time.sleep(1)

        time.sleep(0.2)



except KeyboardInterrupt:
    GPIO.cleanup()
    os.system("pkill mpg123")
    print("終了しました")
