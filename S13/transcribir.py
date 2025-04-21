import os
from pytube import YouTube
import S13.transcribir as transcribir

def descargar_audio_youtube(link, filename='audio.mp3'):
    try:
        yt = YouTube(link)
        print(f"Descargando: {yt.title}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename=filename)
        print(f"Audio descargado como {filename}")
        return filename
    except Exception as e:
        print(f"Error al descargar audio: {e}")
        return None

def transcribir_audio(ruta_audio):
    print("Cargando modelo Whisper...")
    model = transcribir.load_model("base")  # Puedes cambiar a 'small', 'medium', 'large' según prefieras
    print("Transcribiendo audio...")
    resultado = model.transcribe(ruta_audio)
    return resultado['text']

def main():
    link = input("Introduce el enlace de YouTube: ")
    audio_file = "audio.mp3"

    ruta = descargar_audio_youtube(link, filename=audio_file)
    if ruta:
        texto = transcribir_audio(ruta)
        print("\n📝 Transcripción:")
        print(texto)

        with open("transcripcion.txt", "w", encoding="utf-8") as f:
            f.write(texto)
        print("\n✅ Transcripción guardada en 'transcripcion.txt'.")

        # Eliminar el archivo de audio
        os.remove(audio_file)
        print(f"🧹 Archivo temporal '{audio_file}' eliminado.")

if __name__ == "__main__":
    main()
