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