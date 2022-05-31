import network
import gc
import time
import esp


esp.osdebug(None)
gc.collect()

# station = network.WLAN(network.AP_IF)
# station.active(True)
# station.config(essid="Server", password="12345678")
ssid = "Covid19"
password = "Manh184200"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep_ms(100)

IP = station.ifconfig()[0]
print(IP)
