import warnings
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
from io import BytesIO
import os

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*torch.classes.*")
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
import warnings
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
from io import BytesIO
import os
import warnings


warnings.filterwarnings("ignore", category=UserWarning, message=".*torch.classes.*")
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
AudioSegment.converter = which("ffmpeg")

# Lazy import whisper so we can wrap it safely
WHISPER_MODEL = "large"

def record_audio(filename):
    try:
        r = sr.Recognizer()
        r.pause_threshold = 2.0  # 2 seconds silence = stop
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=20, phrase_time_limit=30)
            with BytesIO() as buffer:
                buffer.write(audio.get_wav_data())
                buffer.seek(0)
                AudioSegment.from_wav(buffer).export(filename, format="mp3")
    except Exception as e:
        print(f"[⚠️ Recording Error] {e}")

def transcribe_audio(filepath):
    try:
        import whisper  # defer import to allow exception handling
        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(filepath)
        return result["text"], result["language"]
    except RuntimeError as e:
        if "torch" in str(e) or "__path__._path" in str(e):
            print(f"[⚠️ Torch Runtime Error Handled] {e}")
            return "[Error] Torch runtime issue occurred", "unknown"
        else:
            raise
    except Exception as e:
        print(f"[⚠️ Transcription Error] {e}")
        return "[Error] Transcription failed", "unknown"

# Setup ffmpeg
AudioSegment.converter = which("ffmpeg")

# Whisper model name
WHISPER_MODEL = "large"

def transcribe_audio(filepath):
    try:
        import whisper  # deferred import
        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(filepath)
        return result["text"], result["language"]
    except RuntimeError as e:
        if "torch" in str(e) or "__path__._path" in str(e):
            print(f"[⚠️ Torch Runtime Error Handled] {e}")
            return "[Error] Torch runtime issue occurred", "unknown"
        else:
            raise
    except Exception as e:
        print(f"[⚠️ Transcription Error] {e}")
        return "[Error] Transcription failed", "unknown"
