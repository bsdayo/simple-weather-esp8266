# -*- coding:utf-8 -*-

import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import ujson
import urequests as ur

# 硬件
i2c = I2C(sda=Pin(4), scl=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)

# 读取配置文件
with open('config.json') as cfg_file:
    cfg_data = ujson.load(cfg_file)

# 宏定义
API_KEY = cfg_data['apiKey']
DEFAULT_CITY = cfg_data['defaultCity']
BASE_URL = cfg_data['baseUrl']
LOCAL_IP = network.WLAN(network.STA_IF).ifconfig()[0]

def draw_frame():
    oled.fill(0)
    oled.hline(0, 10, 128, 1)
    oled.hline(0, 11, 128, 1)
    oled.hline(0, 52, 128, 1)
    oled.hline(0, 53, 128, 1)
    oled.show()

def get_weather_info(city):
    paras = 'location={}&key={}&language=en'.format(city, API_KEY)
    data = ujson.loads(ur.get(BASE_URL+paras).text)
    return data['results'][0]

def draw_info(data):
    for day in data['daily']:
        oled.fill(0)
        draw_frame()
        oled.text(data['location']['name'], 32, 56)
        oled.text('Date: ' + day['date'], 0, 0)
        oled.text('D:{}'.format(day['text_day']), 0, 14)
        oled.text('N:{}'.format(day['text_night']), 0, 23)
        oled.text('Temp: {}-{}`C'.format(day['low'], day['high']), 0, 32)
        oled.text('Humi: {}%'.format(day['humidity']), 0, 41)
        oled.show()
        time.sleep(5)

if __name__ == '__main__':
    count = 0
    data = get_weather_info(DEFAULT_CITY)
    while True:
        count += 1
        if count > 20:
            data = get_weather_info(DEFAULT_CITY)
            count = 0
        draw_info(data)
        
