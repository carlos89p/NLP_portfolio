import speech_recognition as sr
import os

# Texto a Voz (TTS) usando "say" en Mac
def local_text_to_speech(text):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_directory, "output_tts.aiff")
    
    # Usar el comando "say" para generar el audio
    os.system(f'say -o "{output_path}" "{text}"')
    
    print(f"Audio guardado como AIFF en: {output_path}")

# Voz a Texto (STT) desde WAV o AIFF
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
            audio_file = input("Introduce la ruta del archivo de audio (.wav o .aiff): ")
            if not os.path.isfile(audio_file):
                print("Archivo no encontrado.")
                continue

            if not (audio_file.lower().endswith('.wav') or audio_file.lower().endswith('.aiff')):
                print("Este programa solo puede transcribir archivos WAV o AIFF directamente.")
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
