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

# ----------------------------
# EXTERNAL API Speech-To-Text
# (Using AssemblyAI or a similar free API)
# ----------------------------
def external_speech_to_text(api_key, audio_file_path):
    print("[External STT] Sending audio to external API...")
    headers = {'authorization': api_key}
    
    # Upload audio file
    with open(audio_file_path, 'rb') as f:
        upload_response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers=headers,
            files={'file': f}
        )
    audio_url = upload_response.json()['upload_url']
    
    # Request transcription
    transcript_request = {
        "audio_url": audio_url
    }
    response = requests.post(
        'https://api.assemblyai.com/v2/transcript',
        json=transcript_request,
        headers=headers
    )
    transcript_id = response.json()['id']
    
    # Poll for completion
    while True:
        polling = requests.get(
            f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
            headers=headers
        ).json()
        
        if polling['status'] == 'completed':
            print(f"[External STT] Transcription: {polling['text']}")
            return polling['text']
        elif polling['status'] == 'failed':
            print("[External STT] Failed to transcribe.")
            return ""
        

# ----------------------------
# EXTERNAL API Text-To-Speech
# (Using ElevenLabs API for TTS)
# ----------------------------
def external_text_to_speech(api_key, text, voice_id="EXAVITQu4vr4xnSDxMaL"):
    print("[External TTS] Requesting speech from external API...")
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
        print(f"[External TTS] Playing received speech...")
        os.system(f"start {temp_audio_file.name}" if os.name == 'nt' else f"afplay {temp_audio_file.name}")
    else:
        print("[External TTS] Error:", response.text)