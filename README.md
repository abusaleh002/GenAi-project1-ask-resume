# Project 1 — Ask My Resume (PDF) Chatbot

A lightweight Streamlit app that lets you upload a PDF (e.g., your resume or a paper),
builds a vector index on the fly, and answers questions grounded in that PDF using
Retrieval-Augmented Generation (RAG).

## Quickstart

1) **Clone / unzip** this folder.
2) **Install Python 3.10+** and create a virtual environment.
3) `pip install -r requirements.txt`
4) Put your OpenAI key in a `.env` file (copy `.env.template` → `.env` and fill it).
5) Run: `streamlit run app.py`
6) In the app: upload your PDF and start asking questions.

## Notes
- Default model: `gpt-4o-mini` via OpenAI.
- Index is built only from the PDF you upload each session. Nothing is stored on disk.
- For best results, use clear questions like:
  - "Summarize my experience in 3 bullets."
  - "What are my top skills mentioned?"
  - "What metrics do I highlight in project X?"

## Optional: Switch models
You can change the model name in the sidebar. Ensure your API access supports that model.

## Troubleshooting
- If you see import errors, run `pip install -r requirements.txt` again.
- If FAISS fails to install on Apple Silicon, try: `pip install faiss-cpu==1.8.0.post1 --no-cache-dir`
- If OpenAI auth fails, confirm your `.env` has a valid key and you restarted Streamlit.

## License
MIT
