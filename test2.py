import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# GPIO 设定
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# MQTT 设定
MQTT_BROKER = "192.168.1.205"  # 替换为你的 MQTT 服务器地址
MQTT_PORT = 1883  # MQTT 默认端口
TOPIC_BUZZER_ON = "buzzer/on"
TOPIC_BUZZER_FREQ = "buzzer/frequence"

# 默认状态
buzzer_on = False
buzzer_mode = 2  # 默认模式：1=3秒响3秒停, 2=1秒响1秒停, 3=一直响

def on_message(client, userdata, msg):
    global buzzer_on, buzzer_mode
    
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    
    if topic == TOPIC_BUZZER_ON:
        if payload.lower() == "on":
            buzzer_on = True
        elif payload.lower() == "off":
            buzzer_on = False
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # 立即关闭蜂鸣器
    
    elif topic == TOPIC_BUZZER_FREQ:
        if payload.isdigit():
            buzzer_mode = int(payload)
            if buzzer_mode < 1 or buzzer_mode > 3:
                buzzer_mode = 2  # 设定默认值

# 连接 MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe([(TOPIC_BUZZER_ON, 0), (TOPIC_BUZZER_FREQ, 0)])
client.loop_start()

try:
    while True:
        if buzzer_on:
            if buzzer_mode == 1:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(3)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                time.sleep(3)
            elif buzzer_mode == 2:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                time.sleep(1)
            elif buzzer_mode == 3:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(0.1)  # 避免阻塞 MQTT
        else:
            time.sleep(0.5)  # 休眠减少 CPU 占用
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()
