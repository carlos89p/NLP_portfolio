import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
import tempfile
import os

# Local Text-To-Speech (TTS)
def local_text_to_speech(text):
    engine = pyttsx3.init()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
        temp_audio_path = fp.name
    engine.save_to_file(text, temp_audio_path)
    engine.runAndWait()
    return temp_audio_path

# Local Speech-To-Text (STT) from uploaded audio
def local_speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Service error: {e}"

# External API Speech-To-Text using Wit.ai
def external_speech_to_text(api_key, audio_file):
    url = "https://api.wit.ai/speech?v=20210928"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "audio/wav"
    }
    response = requests.post(url, headers=headers, data=audio_file.read())
    if response.status_code == 200:
        return response.json().get("text", "No text found")
    else:
        return f"Error: {response.text}"

# External API Text-To-Speech using VoiceRSS
def external_text_to_speech(api_key, text):
    url = "https://api.voicerss.org/"
    params = {
        "key": api_key,
        "hl": "en-us",
        "src": text,
        "c": "MP3",
        "f": "44khz_16bit_stereo"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
            temp_audio_file.write(response.content)
            return temp_audio_file.name
    else:
        return None

# Simple Voice Gender Estimation based on volume
def estimate_voice_gender(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    energy = audio.frame_data.count(b'\xff') / len(audio.frame_data)
    return "Male" if energy > 0.12 else "Female"

# Interface
st.title("Speech Processing App")
st.markdown("Includes Local and External Speech Tasks.")

# API Keys
wit_ai_api_key = "IAB3MQAE2G6AYVY3GSP3LEFYOZGGYQIP"
voicerss_api_key = "b1d12b89fef54c92a77805cbd5f6ff62"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Local TTS", "Local STT", "Voice Gender Detection", "External STT", "External TTS"])

with tab1:
    st.header("Local Text-to-Speech")
    tts_text = st.text_area("Enter text:")
    if st.button("Speak Locally"):
        if tts_text:
            audio_path = local_text_to_speech(tts_text)
            st.audio(audio_path, format="audio/wav")
            os.remove(audio_path)
        else:
            st.warning("Please enter some text.")

with tab2:
    st.header("Local Speech-to-Text")
    uploaded_audio = st.file_uploader("Upload WAV", type=["wav"], key="local_audio")
    if uploaded_audio and st.button("Transcribe Locally"):
        transcription = local_speech_to_text(uploaded_audio)
        st.success(f"Recognized: {transcription}")

with tab3:
    st.header("Voice Gender Detection (Simple)")
    gender_audio = st.file_uploader("Upload WAV", type=["wav"], key="gender_audio")
    if gender_audio and st.button("Estimate Voice Gender"):
        gender = estimate_voice_gender(gender_audio)
        st.info(f"Estimated Gender: {gender}")

with tab4:
    st.header("External Speech-to-Text (Wit.ai)")
    uploaded_audio_ext = st.file_uploader("Upload WAV for External STT", type=["wav"], key="external_audio")
    if uploaded_audio_ext and st.button("Transcribe with External API"):
        transcription = external_speech_to_text(wit_ai_api_key, uploaded_audio_ext)
        st.success(f"External transcription: {transcription}")

with tab5:
    st.header("External Text-to-Speech (VoiceRSS)")
    ext_tts_text = st.text_area("Enter text for External TTS:")
    if st.button("Generate External Speech"):
        if ext_tts_text:
            audio_path = external_text_to_speech(voicerss_api_key, ext_tts_text)
            if audio_path:
                st.audio(audio_path)
                os.remove(audio_path)
            else:
                st.error("Error generating external audio.")
        else:
            st.warning("Please enter text.")
