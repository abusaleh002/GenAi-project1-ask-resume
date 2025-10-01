# Project 1 — Upload and Ask about Your Resume (PDF) Chatbot

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge.svg)](https://genai-project1-ask-resume-rbyksdwddtvtaw4wshmsvb.streamlit.app)

Local sentence-transformer embeddings + **Groq Llama-3.1** for grounded answers.  
**Live demo:** https://genai-project1-ask-resume-rbyksdwddtvtaw4wshmsvb.streamlit.app

> **Privacy:** demo is for non-sensitive PDFs. Scanned PDFs without text extraction may not work (no OCR).


## Requirements
- **Python 3.11** (pinned on Cloud via `runtime.txt`)
- A Groq API key (free): https://console.groq.com/keys

---

## Quickstart (local)

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt


# .streamlit/secrets.toml
GROQ_API_KEY = "sk_XXXXXXXXXXXXXXXXXXXXXXXX"

# .env
GROQ_API_KEY=sk_XXXXXXXXXXXXXXXXXXXXXXXX


Run
streamlit run app.py

Open http://localhost:8501, upload a PDF, and ask a question.

Privacy: this demo is for non-sensitive PDFs. Don’t upload confidential documents.


Features

PDF text extraction (pypdf)

Chunking with LangChain RecursiveCharacterTextSplitter

Embeddings: sentence-transformers/all-MiniLM-L6-v2 (CPU)

Vector store: FAISS by default (Chroma fallback supported)

RAG prompt with page citations

Small per-session rate limit (public demo)

Streamlit UI with chat history

Configuration (sidebar)

Model: llama-3.1-8b-instant (try llama-3.1-70b for quality)

Retriever top-k: raise to 6–8 if answers miss context

Temperature: 0.0–0.3 for factual answers


Project structure
.
├─ app.py
├─ requirements.txt
├─ runtime.txt          # python-3.11.9 for Streamlit Cloud
├─ .env.template
└─ .gitignore


<details> <summary><b>Deploy (Streamlit Cloud)</b></summary>

Repo: abusaleh002/GenAi-project1-ask-resume

Branch: main

Main file: app.py

Python: 3.11 (runtime.txt)

Secrets (Settings → Secrets)


GROQ_API_KEY = "sk_XXXXXXXXXXXXXXXXXXXXXXXX"
</details> <details> <summary><b>Troubleshooting</b></summary>

Requirements error on Cloud → keep Python 3.11 and the pinned versions in requirements.txt.

FAISS build issue → replace FAISS with Chroma:

requirements.txt: chromadb==0.5.11

app.py: from langchain_community.vectorstores import Chroma and use Chroma.from_documents(...).

Secret not found → add GROQ_API_KEY in Secrets or .env.

Scanned PDFs → current version doesn’t do OCR; text extraction may fail.

</details>

## Tech stack
Streamlit • LangChain • sentence-transformers • FAISS/Chroma • **Groq (Llama-3.1)**

## License
MIT — see [LICENSE](./LICENSE).








