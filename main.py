import RPi.GPIO as GPIO
import os
import time
from datetime import datetime

BUTTON_PIN = 17  # GPIO17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("起きましたボタン待機中...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
            os.system(f"fswebcam photos/{filename}")
            print(f"撮影しました: {filename}")
            time.sleep(1)  # 連打防止
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("終了しました")
