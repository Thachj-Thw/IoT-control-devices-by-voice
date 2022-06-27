from modules import Client
from modules.tools import AutoSetup
from machine import Pin


pins = {"D5": 14, "D6": 12, "D7": 13, "D1": 5, "D2": 4}

led = Pin(pins["D7"], Pin.OUT)
led.value(0)
fan = Pin(pins["D6"], Pin.OUT)
fan.value(0)
led2 = Pin(pins["D5"], Pin.OUT)
led2.value(0)

client = Client(ID, SERVER, PORT)
AutoSetup(client, {
    "LivingRoom/led": led,
    "LivingRoom/fan": fan,
    "LivingRoom/led2": led2,
})
client.run()
