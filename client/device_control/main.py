# -*- coding: utf-8 -*-
from modules import speak, DeviceMain


SERVER = "192.168.137.27"
PORT = 1883

def multi_speak(resp, data):
    if resp in data:
        speak(data[resp])

data = {
    "bật đèn": {
        "topic": "device",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn, đã bật",
            "IS TURN ON": "đèn, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt đèn": {
        "topic": "device",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn, đã tắt",
            "IS TURN OFF": "đèn, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra trạng thái đèn": {
        "topic": "divece",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "đèn, đang bật",
            "OFF": "đèn, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "bật đèn phòng khách": {
        "topic": "LivingRoom/led2",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn phòng khách, đã bật",
            "IS TURN ON": "đèn phòng khách, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt đèn phòng khách": {
        "topic": "LivingRoom/led2",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn phòng khách, đã tắt",
            "IS TURN OFF": "đèn phòng khách, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra đèn phòng khách": {
        "topic": "LivingRoom/led2",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "đèn phòng khách, đang bật",
            "OFF": "đèn phòng khách, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "bật quạt phòng khách": {
        "topic": "LivingRoom/fan",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "quạt phòng khách, đã bật",
            "IS TURN ON": "quạt phòng khách, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt quạt phòng khách": {
        "topic": "LivingRoom/fan",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "quạt phòng khách, đã tắt",
            "IS TURN OFF": "quạt phòng khách, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra quạt phòng khách": {
        "topic": "LivingRoom/fan",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "quạt phòng khách, đang bật",
            "OFF": "quạt phòng khách, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "bật đèn nhà bếp": {
        "topic": "LivingRoom/led",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn nhà bếp, đã bật",
            "IS TURN ON": "đèn nhà bếp, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt đèn nhà bếp": {
        "topic": "LivingRoom/led",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn nhà bếp, đã tắt",
            "IS TURN OFF": "đèn nhà bếp, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra đèn nhà bếp": {
        "topic": "LivingRoom/led",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "đèn nhà bếp, đang bật",
            "OFF": "đèn nhà bếp, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "bật đèn phòng ngủ 1": {
        "topic": "BedRoom1/led",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn phòng ngủ một, đã bật",
            "IS TURN ON": "đèn phòng ngủ hai, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt đèn phòng ngủ 1": {
        "topic": "BedRoom1/led",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn phòng ngủ một, đã tắt",
            "IS TURN OFF": "đèn phòng ngủ một, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra đèn phòng ngủ 1": {
        "topic": "BedRoom1/led",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "đèn phòng ngủ một, đang bật",
            "OFF": "đèn phòng ngủ một, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "bật quạt phòng ngủ 1": {
        "topic": "BedRoom1/fan",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "quạt phòng ngủ một, đã bật",
            "IS TURN ON": "quạt phòng ngủ một, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt quạt phòng ngủ 1": {
        "topic": "BedRoom1/fan",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "quạt phòng ngủ một, đã tắt",
            "IS TURN OFF": "quạt phòng ngủ một, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra quạt phòng ngủ 1": {
        "topic": "BedRoom1/fan",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "quạt phòng ngủ một, đang bật",
            "OFF": "quạt phòng ngủ một, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "bật đèn phòng ngủ 2": {
        "topic": "BedRoom2/led",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn phòng ngủ hai, đã bật",
            "IS TURN ON": "đèn phòng ngủ hai, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt đèn phòng ngủ 2": {
        "topic": "BedRoom2/led",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "đèn phòng ngủ hai, đã tắt",
            "IS TURN OFF": "đèn phòng ngủ hai, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra đèn phòng ngủ 2": {
        "topic": "BedRoom2/led",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "đèn phòng ngủ hai, đang bật",
            "OFF": "đèn phòng ngủ hai, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "bật quạt phòng ngủ 2": {
        "topic": "BedRoom2/fan",
        "payload": "ON",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "quạt phòng ngủ hai, đã bật",
            "IS TURN ON": "quạt phòng ngủ hai, đang bật",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "tắt quạt phòng ngủ 2": {
        "topic": "BedRoom2/fan",
        "payload": "OFF",
        "callback": lambda resp: multi_speak(resp, {
            "SUCCESS": "quạt phòng ngủ hai, đã tắt",
            "IS TURN OFF": "quạt phòng ngủ hai, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    },
    "kiểm tra quạt phòng ngủ 2": {
        "topic": "BedRoom2/fan",
        "payload": "CHECK",
        "callback": lambda resp: multi_speak(resp, {
            "ON": "quạt phòng ngủ hai, đang bật",
            "OFF": "quạt phòng ngủ hai, đang tắt",
            "ERROR": "thiết bị không phản hồi"
            })
    }
}


try:
    main = DeviceMain(SERVER, PORT, data)
    speak("sẵn sàng")
    main.run()
except Exception:
    speak("máy chủ xảy ra lỗi")
