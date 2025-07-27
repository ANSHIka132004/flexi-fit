import speech_recognition as sr
from pydub import AudioSegment
import io
import os

# ✅ Absolute paths
ffmpeg_path = r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
ffprobe_path = r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe"

# ✅ Set ffmpeg + ffprobe manually
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

# Optional: Add to PATH just in case
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

def transcribe_audio(django_file):
    recognizer = sr.Recognizer()

    # Convert uploaded file to wav using pydub
    audio = AudioSegment.from_file(django_file)
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
