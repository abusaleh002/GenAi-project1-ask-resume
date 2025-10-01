# GenAI Tools — Resume Q&A + JD ↔ Resume Match
Live Demo:
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://genai-tools-abu-saleh.streamlit.app/)

Upload a resume PDF and ask questions with page citations.  
Or paste a job description and your resume to see a match score and missing keywords.

## Features
- PDF → Q&A with grounded answers (MiniLM + FAISS + Groq Llama-3.1)
- JD ↔ Resume match with missing keywords
- Runs locally or on Streamlit Cloud

## Quickstart
```bash
# install
pip install -r requirements.txt

# set your key (pick one)
# 1) in .streamlit/secrets.toml:
#    GROQ_API_KEY = "sk_xxx"
# 2) or env var:
#    export GROQ_API_KEY="sk_xxx"   # macOS/Linux
#    setx GROQ_API_KEY "sk_xxx"     # Windows

# run
streamlit run app.py
