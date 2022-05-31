from moduls import Client, Button
from machine import Pin


pins = {
    "D5": 14,
    "D6": 12,
    "D7": 13,
    "D1": 5,
    "D2": 4
}


device = Pin(14, Pin.OUT)
device.value(1)
button = Button(Pin(5, Pin.IN), device)


def on_turn_on(pin):
    value = pin.value()
    if value == 1:
        pin.value(0)
        return b"SUCCESS"
    return b"IS TURN ON"

def on_turn_off(pin):
    value = pin.value()
    if value == 0:
        pin.value(1)
        return b"SUCCESS"
    return b"IS TURN OFF"

def on_check(pin):
    if pin.value() == 0:
        return b"ON"
    return b"OFF"


methods = {
    "TURN ON": on_turn_on,
    "TURN OFF": on_turn_off,
    "CHECK": on_check
}


def on_message(topic: bytes, message: bytes, *args, **kwargs):
    if topic == b"device":
        msg = methods[message.decode("utf-8")](device)
        device.publish("response", msg)
    device.publish("response", b"FAILED")


client = Client(ID, SERVER, PORT)
client.on_message(on_message)
client.subscribe(TOPIC)


client.run(button.update)
