import time
from . import umqttsimple
import machine


class Client:
    def __init__(self, _id, sv_host, sv_port):
        self._client = umqttsimple.MQTTClient(_id, sv_host, sv_port, keepalive=60)
        self._client.connect()

    def subscribe(self, *topic, qos=0):
        for t in topic:
            self._client.subscribe(t, qos)
            print("Subscribed topic", t)

    def publish(self, topic, msg, retain=False, qos=0):
        self._client.publish(topic, msg, retain, qos)

    def on_message(self, callback):
        self._client.set_callback(callback)

    def run(self, func=None):
        start = time.ticks_ms()
        if func:
            while True:
                try:
                    self._client.check_msg()
                    func()
                    now = time.ticks_ms()
                    if time.ticks_diff(now, start) > 30000:
                        start = now
                        self._client.ping()
                    time.sleep(.1)
                except OSError as e:
                    time.sleep(5)
                    machine.reset()
        else:
            while True:
                try:
                    self._client.check_msg()
                    now = time.ticks_ms()
                    if time.ticks_diff(now, start) > 30000:
                        start = now
                        self._client.ping()
                    time.sleep(.1)
                except OSError as e:
                    time.sleep(5)
                    machine.reset()


class Button:
    def __init__(self, btn, control):
        self._btn = btn
        self._old_state = 1
        self._control = control

    def update(self):
        if self._btn.value() == 0 and self._old_state == 1:
            value = self._control.value() ^ 0b1
            self._control.value(value)
        self._old_state = self._btn.value()
