import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import tempfile
from audio import transcribe_audio
from prompt import build_prompt
from llm import run_llm, print_sources

# Streamlit config
st.set_page_config(page_title="Neonatal Triage", page_icon="👶", layout="wide")
st.title("👶 AI Neonatal Assistant - Voice-to-Triage")

st.sidebar.header("🔧 Configuration")
st.sidebar.info("🎙️ Record up to ~30 seconds. Click stop to process.")

# Create a temporary WAV file
audio_buffer = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

# Audio Processor
class AudioProcessor:
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame)
        return frame

    def get_audio_bytes(self):
        return b''.join(f.planes[0].to_bytes() for f in self.frames)

# Start the mic
ctx = webrtc_streamer(
    key="audio",
    mode=WebRtcMode.SENDONLY,
    in_audio=True,
    client_settings=ClientSettings(media_stream_constraints={"audio": True, "video": False}),
    audio_processor_factory=AudioProcessor,
)

if ctx and ctx.audio_processor and st.button("🛑 Stop & Transcribe"):
    with st.spinner("Processing audio..."):
        audio_bytes = ctx.audio_processor.get_audio_bytes()
        with open(audio_buffer.name, "wb") as f:
            f.write(audio_bytes)
        transcript, lang = transcribe_audio(audio_buffer.name)

    st.subheader("📝 Transcription")
    st.info(f"Language Detected: **{lang}**")
    st.write(transcript)

    prompt = build_prompt(transcript)

    with st.spinner("Running medical triage..."):
        result = run_llm(prompt)

    st.subheader("🧠 AI Triage Response")
    st.write(result["result"])
    print_sources(result["source_documents"])
