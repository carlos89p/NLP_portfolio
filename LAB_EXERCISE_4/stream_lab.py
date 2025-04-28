import streamlit as st
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
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ----------------------------
# LOCAL Speech-To-Text (STT)
# ----------------------------
def local_speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now!")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "[Could not understand audio]"
    except sr.RequestError as e:
        return f"[Error with service: {e}]"

# ----------------------------
# EXTERNAL API Speech-To-Text
# ----------------------------
def external_speech_to_text(api_key, audio_file_path):
    headers = {'authorization': api_key}
    with open(audio_file_path, 'rb') as f:
        upload_response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers=headers,
            files={'file': f}
        )
    audio_url = upload_response.json()['upload_url']
    
    transcript_request = {"audio_url": audio_url}
    response = requests.post(
        'https://api.assemblyai.com/v2/transcript',
        json=transcript_request,
        headers=headers
    )
    transcript_id = response.json()['id']
    
    while True:
        polling = requests.get(
            f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
            headers=headers
        ).json()
        
        if polling['status'] == 'completed':
            return polling['text']
        elif polling['status'] == 'failed':
            return "[Failed transcription]"

# ----------------------------
# EXTERNAL API Text-To-Speech
# ----------------------------
def external_text_to_speech(api_key, text, voice_id="EXAVITQu4vr4xnSDxMaL"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        audio_content = response.content
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_audio_file.write(audio_content)
        temp_audio_file.close()
        return temp_audio_file.name
    else:
        return None

# ----------------------------
# Keyword Spotting
# ----------------------------
def keyword_spotting(text, keyword):
    return keyword.lower() in text.lower()

# ----------------------------
# RECORD short audio for external STT
# ----------------------------
def record_audio(duration_seconds, filename):
    chunk = 1024
    fmt = pyaudio.paInt16
    channels = 1
    rate = 16000
    p = pyaudio.PyAudio()

    stream = p.open(format=fmt,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    for _ in range(int(rate / chunk * duration_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(fmt))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# ----------------------------
# STREAMLIT APP
# ----------------------------
st.title("🎙️ Speech Processing App")
st.markdown("This app allows you to perform **Text-to-Speech**, **Speech-to-Text**, use **external APIs**, and detect **keywords**!")

# API keys
assemblyai_api_key = st.text_input("Enter your AssemblyAI API Key:", type="password")
elevenlabs_api_key = st.text_input("Enter your ElevenLabs API Key:", type="password")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Local TTS", "Local STT", "Keyword Spotting", "External STT", "External TTS"])

# --- Local TTS ---
with tab1:
    st.header("🔊 Local Text-to-Speech")
    tts_text = st.text_area("Text to speak:")
    if st.button("Speak Locally"):
        if tts_text.strip():
            local_text_to_speech(tts_text)
        else:
            st.warning("Please enter some text.")

# --- Local STT ---
with tab2:
    st.header("🎤 Local Speech-to-Text")
    if st.button("Start Listening Locally"):
        local_result = local_speech_to_text()
        st.success(f"You said: {local_result}")

# --- Keyword Spotting ---
with tab3:
    st.header("🔎 Keyword Spotting")
    user_text = st.text_area("Enter text to analyze:")
    keyword = st.text_input("Keyword to detect:")
    if st.button("Detect Keyword"):
        if user_text and keyword:
            found = keyword_spotting(user_text, keyword)
            if found:
                st.success(f"Keyword '{keyword}' detected!")
            else:
                st.error(f"Keyword '{keyword}' not found.")

# --- External STT ---
with tab4:
    st.header("🌎 External Speech-to-Text (AssemblyAI)")
    if assemblyai_api_key:
        if st.button("Record 5s Audio and Send to API"):
            temp_audio_path = "temp_audio.wav"
            record_audio(5, temp_audio_path)
            with st.spinner("Sending audio and waiting for transcription..."):
                transcription = external_speech_to_text(assemblyai_api_key, temp_audio_path)
                st.success(f"External transcription: {transcription}")
            os.remove(temp_audio_path)
    else:
        st.warning("Please enter your AssemblyAI API Key above.")

# --- External TTS ---
with tab5:
    st.header("🌎 External Text-to-Speech (ElevenLabs)")
    ext_tts_text = st.text_area("Text to convert to speech externally:")
    if elevenlabs_api_key:
        if st.button("Send Text to External TTS"):
            if ext_tts_text.strip():
                audio_path = external_text_to_speech(elevenlabs_api_key, ext_tts_text)
                if audio_path:
                    st.audio(audio_path)
                    os.remove(audio_path)
                else:
                    st.error("Error generating audio from external service.")
            else:
                st.warning("Please enter text.")
    else:
        st.warning("Please enter your ElevenLabs API Key above.")
