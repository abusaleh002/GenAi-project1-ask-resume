# Project 1 — Upload and Ask about Your Resume (PDF) Chatbot

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge.svg)](https://genai-project1-ask-resume-rbyksdwddtvtaw4wshmsvb.streamlit.app)

Upload a PDF (resume, paper, etc.) and ask questions about it.  
The app builds a local embedding index and uses **Groq’s Llama‑3.1** to answer with page‑level citations.

**Live demo:** https://genai-project1-ask-resume-rbyksdwddtvtaw4wshmsvb.streamlit.app  
**Repo:** https://github.com/abusaleh002/GenAi-project1-ask-resume

> Privacy: use non‑sensitive PDFs. Scanned PDFs without text may need OCR (not included yet).

---

## Features
- PDF upload (up to Streamlit’s default 200 MB limit)
- Automatic chunking + embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- Vector search with **FAISS** (or **Chroma** as a fallback)
- Grounded answers with page citations using **Groq Llama‑3.1**
- Works locally and on **Streamlit Cloud**
- Supports server‑side secret so visitors don’t need to paste a key (demo mode)

## Tech
- Streamlit, LangChain, sentence‑transformers, FAISS (or Chroma), Groq (Llama‑3.1)

## How it works (short)
1. Extracts text from PDF pages (`pypdf`).
2. Splits into chunks and embeds with MiniLM.
3. Stores vectors in FAISS, retrieves top‑k chunks per question.
4. Sends a grounded prompt to Groq’s Llama‑3.1 and renders the answer + sources.

---

## Quickstart (local)

> **Python 3.11** recommended (Cloud is pinned via `runtime.txt`).

### macOS / Linux
```bash
git clone https://github.com/abusaleh002/GenAi-project1-ask-resume.git
cd GenAi-project1-ask-resume

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
git clone https://github.com/abusaleh002/GenAi-project1-ask-resume.git
cd GenAi-project1-ask-resume

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Configure the API key (pick one)

**A) `.streamlit/secrets.toml` (recommended)**
```toml
GROQ_API_KEY = "sk_XXXXXXXXXXXXXXXXXXXXXXXX"
```

**B) `.env` file**
```
GROQ_API_KEY=sk_XXXXXXXXXXXXXXXXXXXXXXXX
```

**C) Environment variable**
- PowerShell: `setx GROQ_API_KEY "sk_XXXXXXXXXXXXXXXXXXXXXXXX"` (restart terminal)  
- Git Bash: `export GROQ_API_KEY="sk_XXXXXXXXXXXXXXXXXXXXXXXX"`

### Run
```bash
streamlit run app.py
```

---

## Deploy to Streamlit Cloud

1. Push this repo to GitHub (already done).
2. Go to https://share.streamlit.io → **New app**  
   - **Repo:** `abusaleh002/GenAi-project1-ask-resume`  
   - **Branch:** `main`  
   - **Main file path:** `app.py`
3. Set **Python version** to **3.11** (also keep `runtime.txt` with `python-3.11.9`).
4. Add **Settings → Secrets**:
   ```toml
   GROQ_API_KEY = "sk_XXXXXXXXXXXXXXXXXXXXXXXX"
   ```
5. Deploy. Share the app URL or customize the slug in **Settings → General → App URL**.

---

## Requirements (versions known to work on Cloud)

```txt
streamlit==1.38.0
pypdf==5.0.0
python-dotenv==1.0.1

langchain==0.2.15
langchain-community==0.2.13
langchain-text-splitters==0.2.2

sentence-transformers==2.2.2
huggingface-hub==0.24.6

faiss-cpu==1.8.0.post1
numpy<2

groq==0.12.0
openai==1.51.0
httpx==0.27.2
```

> If FAISS gives trouble on Cloud, swap to `chromadb==0.5.11` and replace FAISS with Chroma in code:
> ```python
> from langchain_community.vectorstores import Chroma
> vs = Chroma.from_documents(docs, embeddings, persist_directory=".chroma")
> return vs.as_retriever(search_kwargs={"k": k})
> ```

---

## Troubleshooting

- **“Error installing requirements”**  
  Ensure Python 3.11; use the versions above. If FAISS fails, switch to Chroma.

- **`streamlit.errors.StreamlitSecretNotFoundError`**  
  Use the safe helper in `app.py` or add the secret via **Settings → Secrets** or a local `.env`/`.streamlit/secrets.toml`.

- **`Client.__init__() got an unexpected keyword argument 'proxies'`**  
  Pin to `groq==0.12.0`, `openai==1.51.0`, and `httpx==0.27.2` (shown above).

- **“No extractable text found in the PDF”**  
  The PDF is likely scanned; OCR not included yet.

---

## Roadmap
- OCR for scanned PDFs
- Multiple PDFs per session
- Export chat history
- Rate limiting for public demo
- Multipage app (Project 2)

## License
MIT

---



Paste that over your current README and commit. The badge will render, commands will format properly, and the page will be easy to



















