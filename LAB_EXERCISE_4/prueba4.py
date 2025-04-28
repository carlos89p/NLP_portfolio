import speech_recognition as sr
import pyttsx3
import tempfile
import os
from pydub import AudioSegment
from pydub.utils import which

# Solución para encontrar ffmpeg y ffprobe
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# Función Local de Texto a Voz (genera mp3)
def local_text_to_speech(text):
    engine = pyttsx3.init()
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    temp_wav_path = os.path.join(script_directory, "temp_output.wav")
    final_mp3_path = os.path.join(script_directory, "output_tts.mp3")

    engine.save_to_file(text, temp_wav_path)
    engine.runAndWait()

    # Convertir WAV a MP3
    sound = AudioSegment.from_wav(temp_wav_path)
    sound.export(final_mp3_path, format="mp3")

    # Eliminar el wav temporal
    os.remove(temp_wav_path)

    print(f"Audio guardado como MP3 en: {final_mp3_path}")

# Función Local de Voz a Texto
def local_speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "No se pudo entender el audio."
    except sr.RequestError as e:
        return f"Error de servicio: {e}"

# Función de detección de palabra clave
def keyword_spotting(text, keyword):
    return keyword.lower() in text.lower()

# Menú Principal
def main():
    while True:
        print("\n--- Menú ---")
        print("1. Convertir texto a voz (TTS)")
        print("2. Transcribir audio a texto (STT)")
        print("3. Detectar palabra clave en texto")
        print("4. Salir")

        choice = input("\nSelecciona una opción: ")

        if choice == '1':
            text = input("Introduce el texto a convertir en voz: ")
            if text.strip():
                local_text_to_speech(text)
            else:
                print("No se ha introducido texto válido.")

        elif choice == '2':
            audio_file = input("Introduce la ruta del archivo de audio (.wav, .mp3, .ogg): ")
            if not os.path.isfile(audio_file):
                print("Archivo no encontrado.")
                continue

            # Convertir el archivo a wav si es necesario
            if not audio_file.lower().endswith('.wav'):
                print("Convirtiendo el archivo a WAV...")
                sound = AudioSegment.from_file(audio_file)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav:
                    sound.export(temp_wav.name, format="wav")
                    audio_file = temp_wav.name

            transcription = local_speech_to_text(audio_file)
            print(f"Texto reconocido: {transcription}")

            if audio_file.startswith(tempfile.gettempdir()):
                os.remove(audio_file)

        elif choice == '3':
            text = input("Introduce el texto: ")
            keyword = input("Introduce la palabra clave a buscar: ")
            if keyword_spotting(text, keyword):
                print(f"¡Palabra clave '{keyword}' encontrada!")
            else:
                print(f"Palabra clave '{keyword}' no encontrada.")

        elif choice == '4':
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()
