import streamlit as st
import speech_recognition as sr
import pyttsx3
import tempfile
import os

# Local Text-to-Speech
def local_text_to_speech(text):
    engine = pyttsx3.init()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
        path = fp.name
    engine.save_to_file(text, path)
    engine.runAndWait()
    return path

# Local Speech-to-Text (supports wav, mp3, flac, etc.)
def local_speech_to_text(uploaded_file):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio.flush()
        temp_audio_path = temp_audio.name
    try:
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        os.remove(temp_audio_path)
        return text
    except Exception as e:
        os.remove(temp_audio_path)
        return f"Error: {e}"

# Keyword Spotting
def keyword_spotting(text, keyword):
    return keyword.lower() in text.lower()

# Streamlit Interface
st.title("Local Speech Processing App (Improved)")

tab1, tab2, tab3 = st.tabs(["Local Text-to-Speech", "Local Speech-to-Text", "Keyword Spotting"])

with tab1:
    st.header("Local Text-to-Speech")
    text_input = st.text_area("Enter text to convert to speech:")
    if st.button("Convert to Speech"):
        if text_input.strip():
            audio_path = local_text_to_speech(text_input)
            st.audio(audio_path, format="audio/wav")
            os.remove(audio_path)
        else:
            st.warning("Please enter some text.")

with tab2:
    st.header("Local Speech-to-Text")
    uploaded_audio = st.file_uploader("Upload an audio file (WAV, MP3, FLAC, OGG)", type=["wav", "mp3", "flac", "ogg", "m4a"])
    if uploaded_audio and st.button("Transcribe Audio"):
        result = local_speech_to_text(uploaded_audio)
        st.success(f"Recognized Text: {result}")

with tab3:
    st.header("Keyword Spotting")
    input_text = st.text_area("Enter text to analyze:")
    keyword = st.text_input("Keyword to detect:")
    if st.button("Detect Keyword"):
        if input_text.strip() and keyword.strip():
            found = keyword_spotting(input_text, keyword)
            if found:
                st.success(f"Keyword '{keyword}' found!")
            else:
                st.error(f"Keyword '{keyword}' not found.")
        else:
            st.warning("Please enter both text and keyword.")
