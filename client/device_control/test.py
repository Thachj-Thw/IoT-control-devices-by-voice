import speech_recognition as sr
import requests


recognizer = sr.Recognizer()
with sr.Microphone() as source:
    while True:
        recognizer.adjust_for_ambient_noise(source)
        sound = recognizer.listen(source, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(sound, language="vi-VN")
        except Exception as e:
            text = "..." + str(e)
        print(text)
        if text == "...":
            try:
                requests.get("https://www.google.com/", timeout=3)
                print("have internet")
            except Exception:
                print("no internet connection")
