# -*- coding: utf-8 -*-
from modules import speak, DeviceMain


SERVER = "192.168.0.108"
PORT = 1883


def turn_on(resp):
    if resp == "SUCCESS":
        speak("đèn đã bật")
    elif resp == "IS TURN ON":
        speak("đèn vẫn đang bật")

def turn_off(resp):
    if resp == "SUCCESS":
        speak("đèn đã tắt")
    elif resp == "IS TURN OFF":
        speak("đèn không được bật")

def check(resp):
    if resp == "ON":
        speak("đèn đang bật")
    elif resp == "OFF":
        speak("đèn đang tắt")


data = {
    "bật đèn": {
        "topic": "device",
        "payload": "TURN ON",
        "callback": turn_on
    },
    "tắt đèn": {
        "topic": "device",
        "payload": "TURN OFF",
        "callback": turn_off
    },
    "kiểm tra trạng thái đèn": {
        "topic": "divece",
        "payload": "CHECK",
        "callback": check
    }
}



main = DeviceMain(SERVER, PORT, data)
speak("sẵn sàng")
main.run()
