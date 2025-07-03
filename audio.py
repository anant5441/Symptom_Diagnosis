import warnings
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
from io import BytesIO
import os

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*torch.classes.*")
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

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
