import streamlit as st
from audio import transcribe_audio  # Removed record_audio for compatibility with Streamlit Cloud
from prompt import build_prompt
from llm import run_llm, print_sources

# Page configuration
st.set_page_config(page_title="Neonatal Triage", page_icon="👶", layout="wide")

# Sidebar content
with st.sidebar:
    st.header("🔧 Configuration")
    st.info("🎙️ Max audio length: **30 seconds**")
    st.markdown("""
    - Upload baby's audio file.
    - Click **'Transcribe & Analyze'** to get triage.
    """)

# Main Title
st.title("👶 AI Neonatal Assistant - Voice-to-Triage")

# Upload audio file
uploaded_audio = st.file_uploader("📤 Upload baby's voice recording (MP3/WAV)", type=["mp3", "wav"])

# Store transcript in session_state
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "lang" not in st.session_state:
    st.session_state.lang = ""

# Transcribe and analyze
if st.button("🧠 Transcribe & Analyze") and uploaded_audio is not None:
    # Save audio locally
    with open("patient_voice.mp3", "wb") as f:
        f.write(uploaded_audio.read())

    with st.spinner("Transcribing audio..."):
        transcript, lang = transcribe_audio("patient_voice.mp3")
        st.session_state.transcript = transcript
        st.session_state.lang = lang

    st.subheader("📝 Transcription")
    st.info(f"Language Detected: **{lang}**")
    st.write(transcript)

    # Build triage prompt
    prompt = build_prompt(transcript)

    with st.spinner("Running medical triage..."):
        result = run_llm(prompt)

    # Show AI Response
    st.subheader("🧠 AI Triage Response")
    st.write(result["result"])

    # Print sources in terminal (if running locally)
    print_sources(result["source_documents"])

elif st.button("🧠 Transcribe & Analyze") and uploaded_audio is None:
    st.warning("⚠️ Please upload an audio file before analyzing.")

# Disclaimer
st.markdown("""
---
⚠️ **Disclaimer:**
- The suggestions and home remedies provided are for informational purposes only and should not be considered medical advice.
- Always consult a qualified healthcare provider before starting any new treatment or remedy.
- This system is not responsible for any adverse effects caused by the use of suggested remedies.
""")
