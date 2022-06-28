import machine
import esp
import gc
from ubinascii import hexlify
import network
import time


class Wifi:
    def __init__(self, ssid, pwd):
        self._ssid = ssid
        self._pwd = pwd
        self._station = network.WLAN(network.STA_IF)

    def connect(self, timeout_ms: float = 60000):
        self._station.active(True)
        self._station.connect(self._ssid, self._pwd)

        start = time.ticks_ms()
        led = machine.Pin(2, machine.Pin.OUT)
        while not self._station.isconnected():
            led.value(int(not led.value()))
            time.sleep(.1)
            if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
                return False
        return True

    def ifconfig(self):
        return self._station.ifconfig()


esp.osdebug(None)
gc.collect()

SSID = "laohac"
PASSWORD = "cocaicut"
SERVER = "192.168.137.27"
PORT = 1883
ID = hexlify(machine.unique_id())

TOPIC = b"device"

wifi = Wifi(SSID, PASSWORD)
if wifi.connect():
    print("connected successfully", *wifi.ifconfig())
    led = machine.Pin(2, machine.Pin.OUT)
    led.value(0)
    time.sleep(3)
    led.value(1)
else:
    print("connection timeout")
    machine.reset()
