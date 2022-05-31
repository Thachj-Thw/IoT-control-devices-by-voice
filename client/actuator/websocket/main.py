from client import AsyncClient
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import time


client = AsyncClient(server="192.168.100.9", port=8123)
client_topic = "LIVING ROOM"


async def callback(topic, message):
    print(topic, message)
    msg = "SUCCESS"
    if message == "CHECK LED":
        msg = "OFF" if D5.value() else "ON"
    elif message == "LED ON":
        if D5.value():
            D5.value(0)
        else:
            msg = "LED IS TURN ON"
    elif message == "LED OFF":
        if D5.value():
            msg = "LED IS TURN OFF"
        else:
            D5.value(1)
    elif message == "FAN ON":
        if D6.value():
            D6.value(0)
        else:
            msg = "FAN IS TURN ON"
    elif message == "FAN OFF":
        if D6.value():
            msg = "FAN IS TURN OFF"
        else:
            D6.value(1)
    elif message == "CHECK FAN":
        msg = "OFF" if D6.value() else "ON"
    elif message == "LED2 ON":
        if D7.value():
            D7.value(0)
        else:
            msg = "LED2 IS TURN ON"
    elif message == "LED2 OFF":
        if D7.value():
            msg = "LED2 IS TURN OFF"
        else:
            D7.value(1)
    elif message == "CHECK LED2":
        msg = "OFF" if D7.value() else "ON"
    else:
        msg = "FAILED"
    await client.publish(topic, msg, get_resp=False)


async def main():
    suc = await client.subscribe(client_topic)
    if not suc:
        return
    client.set_callback(callback)
    while True:
        await client.check_msg()
        if D1.value() == 0 and b_d1 == 1:
            value = D5.value() ^ 0b1
            D5.value(value)
        b_d1 = D1.value()
        if D2.value() == 0 and b_d2 == 1:
            value = D6.value() ^ 0b1
            D6.value(value)
        b_d2 = D2.value()
        time.sleep_ms(100)

asyncio.run(main())
