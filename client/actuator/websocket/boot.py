from machine import Pin
import network
import gc
import time
import esp


esp.osdebug(None)
gc.collect()

ssid = "Covid19"
password = "Manh184200"

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep_ms(100)

print('Connection successful')
IP = station.ifconfig()[0]
print(IP)

D5 = Pin(14, Pin.OUT)
D5.value(1)
D6 = Pin(12, Pin.OUT)
D6.value(1)
D7 = Pin(13, Pin.OUT)
D7.value(1)
D1 = Pin(5, Pin.IN)
D2 = Pin(4, Pin.IN)
