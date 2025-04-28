import speech_recognition as sr
import pyttsx3
import requests
import wave
import pyaudio
import tempfile
import os

# ----------------------------
# LOCAL Text-To-Speech (TTS)
# ----------------------------
def local_text_to_speech(text):
    print("[Local TTS] Speaking...")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# ----------------------------
# LOCAL Speech-To-Text (STT)
# ----------------------------
def local_speech_to_text():
    print("[Local STT] Listening...")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"[Local STT] Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("[Local STT] Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"[Local STT] Error with service; {e}")
        return ""
