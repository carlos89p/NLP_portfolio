import subprocess
import whisper
import sys

def transcribe_youtube_audio(url):
    print("Extrayendo audio en streaming con yt_dlp...")

    # Comando para obtener solo el audio y mandarlo a stdout
    command = [
        'yt-dlp',
        '-f', 'bestaudio',
        '-o', '-',  # salida a stdout
        '--quiet',
        '--no-warnings',
        url
    ]

    # ffmpeg convierte el stream de audio a wav en tiempo real
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', 'pipe:0',         # entrada desde stdin (yt_dlp)
        '-f', 'wav',            # formato de salida
        '-acodec', 'pcm_s16le', # códec sin compresión
        '-ar', '16000',         # frecuencia de muestreo
        '-ac', '1',             # canal mono
        'pipe:1'                # salida a stdout (para whisper)
    ]

    # conectar yt_dlp y ffmpeg
    try:
        yt_dlp_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=yt_dlp_proc.stdout, stdout=subprocess.PIPE)

        model = whisper.load_model("base")  # puedes cambiar a tiny, small, etc.
        print("Transcribiendo audio...")

        # transcribe el audio directamente desde el output de ffmpeg
        result = model.transcribe(ffmpeg_proc.stdout)
        print("\n📝 Transcripción:\n")
        print(result["text"])

    except Exception as e:
        print(f"Error durante la transcripción: {e}")

if __name__ == "__main__":
    url = input("Introduce el enlace de YouTube: ").strip()
    transcribe_youtube_audio(url)
