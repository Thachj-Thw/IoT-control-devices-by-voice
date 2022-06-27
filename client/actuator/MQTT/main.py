from modules import Client, Button
from modules.tools import AutoSetup
from machine import Pin


device = Pin(14, Pin.OUT)
device.value(1)
button = Button(Pin(5, Pin.IN), device)

client = Client(ID, SERVER, PORT)
AutoSetup(client, {"device": device})
client.run(button.update)
