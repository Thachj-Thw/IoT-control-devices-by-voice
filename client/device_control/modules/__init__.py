# -*- coding: utf-8 -*-
import paho.mqtt.client as MQTTClient
import requests
import os
import time
import speech_recognition as sr


path = os.path.dirname(__file__)



class DeviceMain:
    def __init__(self, server, port, cmd_data):
        self._client = Client("assistant", server, port)
        self._client.on_message(self._on_message)
        self._client.connect()
        self._client.subscribe("response")
        self._cmd_data = cmd_data
        self._cmd = ""
        self._speech2text = Speech2Text()

    def _on_message(self, client, user_data, message):
        if message.topic == "response":
            if self._cmd in self._cmd_data:
                self._cmd_data[self._cmd]["callback"](message.payload.decode("utf-8"))

    def run(self):
        try:
            with self._speech2text.microphone as source:
                while True:
                    self._speech2text.wait_wake_word(("alo", ), source)
                    speak("có")
                    cmd = ""
                    count = 0
                    while not cmd:
                        cmd = self._speech2text.get(source)
                        time.sleep(.1)
                        count += 1
                        if count == 50:
                            speak("bạn còn đó không")
                        if count == 150:
                            speak("gọi tôi khi bạn cần")
                            break
                    print("cmd", cmd)
                    self._cmd = cmd
                    if self._cmd in self._cmd_data:
                        speak("đang " + self._cmd)
                        self._client.publish(self._cmd_data[self._cmd]["topic"], self._cmd_data[self._cmd]["payload"])
                        if not self._client.wait_response():
                            speak("thiết bị, không, phản hồi")
                    elif cmd:
                        speak("xin lỗi, tôi không hiểu")
        except Exception:
            os.system("sudo reboot now")



class Client:
    def __init__(self, cid, sv_host, sv_port=1883, username="", password=""):
        self._connected = False
        self._host = sv_host
        self._port = sv_port
        self._username = username
        self._password = password
        self._client = MQTTClient.Client(cid)
        if self._username and self._password:
            self._client.username_pw_set(self._username, self._password)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_msg
        self._got_resp = False
        self._callback = None

    def connect(self, **kwargs):
        self._client.connect(self._host, self._port, **kwargs)
        self._client.loop_start()
        while not self._connected:
            time.sleep(.1)

    def _on_connect(self, client, user_data, flags, rc):
        if not rc:
            print("client is connected")
            self._connected = True
        else:
            print("connection failed")

    def is_connected(self):
        return self._connected

    def subscribe(self, topic, **kwargs):
        if self._connected:
            self._client.subscribe(topic, **kwargs)
        else:
            print("client is not connected to server")

    def publish(self, topic, payload, qos=0, **kwargs):
        if self._connected:
            self._got_msg = False
            self._client.publish(topic, payload, qos, **kwargs)
        else:
            print("Client is not connected to server")

    def on_message(self, func):
        self._callback = func

    def _on_msg(self, *args, **kwargs):
        self._got_msg = True
        if self._callback:
            self._callback(*args, **kwargs)

    def disconnect(self):
        self._client.loop_stop()

    def wait_response(self, timeout=3):
        start = time.perf_counter()
        while not self._got_msg:
            time.sleep(.1)
            if time.perf_counter() - start > timeout:
                return False
        return True


class Speech2Text:
    def __init__(self):
        self._recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def wait_wake_word(self, words, source, language="vi-VN"):
        while True:
            audio = self._recognizer.listen(source, phrase_time_limit=1)
            try:
                text = self._recognizer.recognize_google(audio, language=language).lower()
            except Exception:
                text = ""
            print("wake", text)
            print(text in words, words)
            if text in words:
                return True
            else:
                if is_internet_disconnected():
                    speak("Thông báo, mất mạng")
                    counter = 0
                    while is_internet_disconnected():
                        time.sleep(1)
                        counter = (counter + 1) % 300
                        if counter == 299:
                            speak("không có mạng, tôi không thể, làm việc")

    def get(self, source, language="vi-VN"):
        audio = None
        while not audio:
            try:
                audio = self._recognizer.listen(source, timeout=1, phrase_time_limit=5)
            except Exception:
                audio = None
                continue
        try:
            text = self._recognizer.recognize_google(audio, language=language).lower()
        except Exception:
            text = ""
        return text


def is_internet_disconnected(timeout=1):
    try:
        requests.get("https://www.google.com/", timeout=timeout)
    except (requests.ConnectionError, requests.Timeout):
        return True
    return False


def speak(text):
    os.system("espeak-ng \"%s\" -v vi -s 140 -a 60" % text)
