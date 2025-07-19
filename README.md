# AI Neonatal Assistant - Voice-to-Triage

A  Clinical assistant for neonatal triage, leveraging voice input and large language models (LLMs) to provide structured, evidence-informed medical triage and home care advice for newborns based on caregiver descriptions.

## Features
- **Voice-to-Triage:** Record caregiver voice, transcribe using Whisper, and analyze symptoms with an LLM.
- **Structured Medical Output:** Extracts symptoms, urgency, recommended specialty, home remedies, supportive care, and more.
- **Evidence-Based:** Uses standard neonatal protocols and references for recommendations.
- **Source Transparency:** Shows source documents used for LLM responses.


## 🌐 Multilingual Support
- The app uses OpenAI Whisper for speech-to-text, which supports transcription in many languages and automatically detects the spoken language.
- The detected language is displayed after transcription.
- **Note:** The AI triage and prompt are optimized for English. For best results, provide input in English. Other languages may work for transcription, but the LLM's understanding and response quality may vary depending on its multilingual capabilities.

## How It Works
1. **Record Audio:** Click 'Record Audio' and describe the baby's symptoms.
2. **Transcribe & Analyze:** The app transcribes the audio and analyzes the text using a prompt designed for neonatal triage.
3. **AI Response:** The LLM provides a structured triage response, including urgency, home care, and next steps.
4. **Disclaimer:** All advice is informational and not a substitute for professional medical care.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd Symptom_Diagnosis
```

### 2. Install Dependencies
Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the project root with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Prepare Data
- Place relevant medical PDFs in the `data/` directory for vector search.
- The app will automatically create or load a Chroma vector store from these documents.

### 5. Run the App
```bash
streamlit run app.py
```

## File Structure
- `app.py` — Streamlit UI and main workflow
- `audio.py` — Audio recording and transcription (Whisper)
- `prompt.py` — Prompt template for LLM
- `llm.py` — LLM and vector store logic (LangChain, Chroma, Groq)
- `requirements.txt` — Python dependencies
- `data/` — Medical reference PDFs
- `chroma_db/` — Vector store (auto-generated)

## Dependencies
- streamlit
- pydub
- SpeechRecognition
- openai-whisper
- python-dotenv
- torch
- transformers
- sentence-transformers
- langchain & langchain-community
- chromadb
- PyPDF2
- langchain-huggingface
- protobuf==3.20.3
- langchain-groq

## Disclaimer
> **The suggestions and home remedies provided are for informational purposes only and should not be considered as medical advice. Always consult a qualified healthcare provider before starting any new treatment or remedy. The system is not responsible for any adverse effects caused by the use of suggested remedies.**

---

## 🤝 Suggestions Welcome
This project is open for suggestions, improvements, and contributions! Feel free to open an issue or submit a pull request if you have ideas to make it better.

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
