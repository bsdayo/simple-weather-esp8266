# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import ujson

# 读取配置文件
with open('config.json') as cfg_file:
    cfg_data = ujson.load(cfg_file)
WIFI_SSID = cfg_data['wifiSSID']
WIFI_PASSWORD = cfg_data['wifiPassword']

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
        print('Network Config:', wlan.ifconfig())

do_connect()
webrepl.start()
gc.collect()
