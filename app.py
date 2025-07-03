import streamlit as st
from audio import record_audio, transcribe_audio
from prompt import build_prompt
from llm import run_llm, print_sources

# Page configuration
st.set_page_config(page_title="Neonatal Triage", page_icon="👶", layout="wide")

# Sidebar content
with st.sidebar:
    st.header("🔧 Configuration")
    st.info("🎙️ Max recording time: **30 seconds**")
    st.markdown("""
    - Click **'Record Audio'** to begin.
    - Click **'Transcribe & Analyze'** after speaking.
    """)

# Main Title
st.title("👶 AI Neonatal Assistant - Voice-to-Triage")

# Record audio section
if st.button("🎙️ Record Audio"):
    record_audio("patient_voice.mp3")
    st.success("✅ Audio Recorded: `patient_voice.mp3`")

# Transcribe and analyze
if st.button("🧠 Transcribe & Analyze"):
    with st.spinner("Transcribing audio..."):
        transcript, lang = transcribe_audio("patient_voice.mp3")
        st.session_state.transcript = transcript
        st.session_state.lang = lang

    st.subheader("📝 Transcription")
    st.info(f"Language Detected: **{lang}**")
    st.write(transcript)

    prompt = build_prompt(transcript)

    with st.spinner("Running medical triage..."):
        result = run_llm(prompt)

    # Show AI Response
    st.subheader("🧠 AI Triage Response")
    st.write(result["result"])

    # Show sources
    # st.subheader("📄 Source Documents Used")
    print_sources(result["source_documents"])

# Disclaimer
st.markdown("""
---
⚠️ **Disclaimer:**
- The suggestions and home remedies provided are for informational purposes only and should not be considered as medical advice.
- Always consult a qualified healthcare provider before starting any new treatment or remedy.
- The system is not responsible for any adverse effects caused by the use of suggested remedies.
""")
