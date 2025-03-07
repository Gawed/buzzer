import RPi.GPIO as GPIO
import time

# 设置 GPIO 模式为 BCM
GPIO.setmode(GPIO.BCM)
# 设置 GPIO17 为输出模式
GPIO.setup(17, GPIO.OUT)

try:
    while True:
        # 蜂鸣器响
        GPIO.output(17, GPIO.HIGH)
        time.sleep(1)  # 持续 1 秒
        # 蜂鸣器停
        GPIO.output(17, GPIO.LOW)
        time.sleep(1)  # 持续 1 秒
except KeyboardInterrupt:
    pass
finally:
    # 清理 GPIO 设置
    GPIO.cleanup()
