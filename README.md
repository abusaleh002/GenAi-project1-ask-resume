# Project 1 — Upload and Ask about Your Resume (PDF) Chatbot

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge.svg)](https://genai-project1-ask-resume-rbyksdwddtvtaw4wshmsvb.streamlit.app)

Upload a PDF (resume or paper) and ask grounded questions about it. Local sentence-transformer embeddings + Groq Llama-3.1.

## Quickstart
```bash
git clone https://github.com/abusaleh002/GenAi-project1-ask-resume.git
cd GenAi-project1-ask-resume
python -m venv .venv && . .venv/Scripts/activate   # Windows
# or: python3 -m venv .venv && source .venv/bin/activate  # macOS/Linux
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py

Configure the key

Set GROQ_API_KEY with one of:

.streamlit/secrets.toml:
GROQ_API_KEY = "sk_...your key..."


.env:
GROQ_API_KEY=sk_...your key...

Tech
Streamlit • LangChain • sentence-transformers • FAISS/Chroma • Groq (Llama-3.1)


## If you want a “richer” README without clutter
Use collapsible details for extras:

```markdown
<details>
<summary>Deployment (Streamlit Cloud)</summary>

- Repo: `abusaleh002/GenAi-project1-ask-resume`
- Branch: `main`
- Main file: `app.py`
- Python: 3.11 (`runtime.txt`)
- Secrets:


GROQ_API_KEY = "sk_...your key..."

</details>

<details>
<summary>Troubleshooting</summary>

- If FAISS fails on Cloud, switch to `chromadb==0.5.11` and use Chroma vector store.
- If secrets error, add `GROQ_API_KEY` in Settings → Secrets or `.env`.
</details>


## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.




