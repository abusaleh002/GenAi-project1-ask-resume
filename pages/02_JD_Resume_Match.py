# pages/02_JD_Resume_Match.py
import streamlit as st
from lib.core import make_groq
from datetime import datetime


st.set_page_config(page_title="JD ↔ Resume Match", page_icon="🔎", layout="wide")
st.title("🔎 JD ↔ Resume Match")

st.write("Paste a job description and your resume text. Get a quick match score and missing keywords suggestions.")

with st.container(border=True):
    jd = st.text_area("Job Description", height=220, placeholder="Paste the JD here…")
with st.container(border=True):
    resume = st.text_area("Your Resume (text)", height=220, placeholder="Paste your resume text…")

col1, col2 = st.columns([1,1])
with col1:
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
with col2:
    model = st.text_input("Model", value="llama-3.1-8b-instant")

if st.button("Evaluate", type="primary", use_container_width=True):
    if not jd.strip() or not resume.strip():
        st.warning("Please paste both the JD and your resume text."); st.stop()

    client = make_groq()
    prompt = f"""
You are a job-match evaluator. Compare the candidate resume to the Job Description.

Return JSON with fields:
- match_percent (0-100)
- top_skills_matched (list of 5)
- missing_keywords (list of up to 10)
- brief_feedback (1-2 sentences)

JD:
{jd}

Resume:
{resume}
"""
    with st.spinner("Scoring…"):
        res = client.chat.completions.create(
            model=model, temperature=temperature,
            messages=[{"role":"user","content":prompt}],
        )
    st.subheader("Result")
    st.write(res.choices[0].message.content)

st.caption(f"© {datetime.now().year} • Created by **Abu Saleh**")