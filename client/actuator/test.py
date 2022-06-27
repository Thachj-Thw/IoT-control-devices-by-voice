from machine import Pin
from time import sleep


D5 = Pin(14, Pin.OUT)
D6 = Pin(12, Pin.OUT)
D7 = Pin(13, Pin.OUT)

D5.value(1)
D6.value(1)
D7.value(1)
sleep(10)
D5.value(0)
D6.value(0)
D7.value(0)