# Project 1 — Upload and Ask about Your Resume (PDF) Chatbot

[![Open in Streamlit]
https://static.streamlit.io/badges/streamlit_badge.svg)](https://genai-project1-ask-resume-rbyksdwddtvtaw4wshmsvb.streamlit.app

Local sentence-transformer embeddings + **Groq Llama-3.1** for grounded answers.  
**Live demo:** https://genai-project1-ask-resume-rbyksdwddtvtaw4wshmsvb.streamlit.app

> **Privacy:** demo is for non-sensitive PDFs. Scanned PDFs without text extraction may not work (no OCR).

## Requirements
- **Python 3.11** (pinned on Cloud via `runtime.txt`)
- A **Groq API key** (free): https://console.groq.com/keys

---

## Quickstart (local)

### macOS / Linux
```bash
git clone https://github.com/abusaleh002/GenAi-project1-ask-resume.git
cd GenAi-project1-ask-resume

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

Windows (PowerShell)
git clone https://github.com/abusaleh002/GenAi-project1-ask-resume.git
cd GenAi-project1-ask-resume

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

Configure the key (pick one)

A) .streamlit/secrets.toml (recommended)

GROQ_API_KEY = "sk_XXXXXXXXXXXXXXXXXXXXXXXX"


B) .env

GROQ_API_KEY=sk_XXXXXXXXXXXXXXXXXXXXXXXX


C) Environment variable

# Windows (persistent)
setx GROQ_API_KEY "sk_XXXXXXXXXXXXXXXXXXXXXXXX"

# macOS / Linux (current shell)
export GROQ_API_KEY="sk_XXXXXXXXXXXXXXXXXXXXXXXX"

Run
streamlit run app.py


Open http://localhost:8501
, upload a PDF, and ask a question.


Features

PDF text extraction (pypdf)

Chunking with LangChain RecursiveCharacterTextSplitter

Embeddings: sentence-transformers/all-MiniLM-L6-v2 (CPU)

Vector store: FAISS by default (Chroma fallback supported)

RAG prompt with page citations

Small per-session rate limit (public demo)

Streamlit UI with chat history


Tech stack
Streamlit • LangChain • sentence-transformers • FAISS/Chroma • Groq (Llama-3.1)

License
MIT — see LICENSE

Paste that over your current README and commit. The badge will render, commands will format properly, and the page will be easy to



















