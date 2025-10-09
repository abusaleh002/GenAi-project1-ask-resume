# pages/02_JD_Resume_Match.py
import io
import os
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Try DOCX support (optional but recommended)
try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except Exception:
    DOCX_AVAILABLE = False

from lib.core import make_groq

st.set_page_config(page_title="JD ↔ Resume Match", page_icon="🔎", layout="wide")
st.title("🔎 JD ↔ Resume Match")

st.write("Paste a job description, upload your resume file (PDF/DOCX/TXT), and get a match score with missing keywords.")

# ---------------- Helpers ----------------
def extract_text_from_pdf(uploaded_file) -> str:
    data = uploaded_file.read()
    reader = PdfReader(io.BytesIO(data))
    texts = []
    for i, page in enumerate(reader.pages):
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        if t.strip():
            texts.append(t)
    return "\n\n".join(texts).strip()

def extract_text_from_docx(uploaded_file) -> str:
    if not DOCX_AVAILABLE:
        raise RuntimeError("python-docx not installed. Add `python-docx==1.1.2` to requirements.txt.")
    doc = DocxDocument(uploaded_file)
    return "\n".join(p.text for p in doc.paragraphs).strip()

def extract_text_from_txt(uploaded_file) -> str:
    raw = uploaded_file.read()
    try:
        return raw.decode("utf-8").strip()
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="ignore").strip()

def clean_for_prompt(text: str, max_chars: int = 12000) -> str:
    text = " ".join(text.split())  # collapse whitespace
    return text[:max_chars]

# ---------------- UI ----------------
with st.container(border=True):
    st.subheader("Job Description")
    jd = st.text_area("Paste the JD here…", height=220, placeholder="Paste the job description text")

with st.container(border=True):
    st.subheader("Resume")
    resume_file = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    model = st.text_input("Model", value="llama-3.1-8b-instant")
    chunking = st.checkbox("Light chunking for long resumes", True)
    st.caption("Chunking can help long PDFs read better.")

# ---------------- Prepare inputs ----------------
resume_text = ""
if resume_file is not None:
    try:
        if resume_file.type == "application/pdf" or resume_file.name.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        elif resume_file.name.lower().endswith(".docx"):
            resume_text = extract_text_from_docx(resume_file)
        else:
            resume_text = extract_text_from_txt(resume_file)
    except Exception as e:
        st.error(f"Could not read resume: {e}")

if resume_text:
    st.success(f"Resume loaded ({len(resume_text):,} chars).")
    st.toggle("Show extracted resume text", value=False, key="show_resume")
    if st.session_state.show_resume:
        st.text_area("Extracted Resume (read-only)", value=resume_text[:5000], height=220)
else:
    st.info("Upload your resume to continue.")

# Optional light chunking (helps large resumes)
if chunking and resume_text:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_text(resume_text)
    resume_for_prompt = "\n\n".join(chunks[:8])  # cap a few chunks for token safety
else:
    resume_for_prompt = resume_text

# ---------------- Run match ----------------
col1, col2 = st.columns([1,1])
with col1:
    run = st.button("Evaluate", type="primary", use_container_width=True)
with col2:
    clear = st.button("Clear", use_container_width=True)

if clear:
    st.experimental_rerun()

if run:
    if not jd.strip():
        st.warning("Please paste the Job Description.")
    elif not resume_for_prompt:
        st.warning("Please upload a readable resume file.")
    else:
        client = make_groq()
        # Keep JD/resume to safe size for prompt
        jd_clean = clean_for_prompt(jd, 12000)
        resume_clean = clean_for_prompt(resume_for_prompt, 12000)

        prompt = f"""
You are a job-match evaluator. Compare the candidate resume to the Job Description.

Return JSON with fields:
- match_percent (0-100)
- top_skills_matched (list of 5)
- missing_keywords (list of up to 10)
- brief_feedback (1-2 sentences)

Job Description:
{jd_clean}

Resume:
{resume_clean}
"""

        with st.spinner("Scoring…"):
            res = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
        text = res.choices[0].message.content

        st.subheader("Result")
        st.write(text)

        m1, m2 = st.columns(2)
        m1.metric("JD length (chars)", f"{len(jd_clean):,}")
        m2.metric("Resume length (chars)", f"{len(resume_clean):,}")

# Footer (optional)
from datetime import datetime
st.caption(f"© {datetime.now().year} • Created by **Abu Saleh**")
