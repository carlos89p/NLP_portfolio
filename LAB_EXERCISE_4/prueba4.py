import speech_recognition as sr
import pyttsx3
import tempfile
import os

# Texto a Voz (TTS) en WAV
def local_text_to_speech(text):
    engine = pyttsx3.init()
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_directory, "output_tts.wav")
    
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()  # <-- MUY importante en Mac para guardar el archivo correctamente
    print(f"Audio guardado como WAV en: {output_path}")

# Voz a Texto (STT) desde WAV
def local_speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language="es-ES")
        return text
    except sr.UnknownValueError:
        return "No se pudo entender el audio."
    except sr.RequestError as e:
        return f"Error de servicio: {e}"

# Menú Principal
def main():
    while True:
        print("\n--- Menú ---")
        print("1. Convertir texto a voz (TTS)")
        print("2. Transcribir audio a texto (STT)")
        print("3. Salir")

        choice = input("\nSelecciona una opción: ")

        if choice == '1':
            text = input("Introduce el texto a convertir en voz: ")
            if text.strip():
                local_text_to_speech(text)
            else:
                print("No se ha introducido texto válido.")

        elif choice == '2':
            audio_file = input("Introduce la ruta del archivo de audio (.wav solamente): ")
            if not os.path.isfile(audio_file):
                print("Archivo no encontrado.")
                continue

            if not audio_file.lower().endswith('.wav'):
                print("Este programa solo puede transcribir archivos WAV directamente.")
                continue

            transcription = local_speech_to_text(audio_file)
            print(f"Texto reconocido: {transcription}")

        elif choice == '3':
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()
