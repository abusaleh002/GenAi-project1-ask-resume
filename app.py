# app.py — Home / Landing page
import streamlit as st
from lib.ui import inject_css

# Page config
st.set_page_config(page_title="GenAI Tools", page_icon="🛠️", layout="wide")

# Keep the Home sidebar clean (page list will still show)
with st.sidebar:
    st.empty()

# Inject external CSS (relative to repo root)
inject_css("assets/landing.css")

# ----- Hero -----
st.markdown(
    """
    <div class="hero">
      <div class="title">
        <span class="emoji">🛠️</span>
        <h1>GenAI Tools</h1>
      </div>
      <div class="tagline">A small suite of AI utilities built with Streamlit + Groq.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Small spacer
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ----- Cards -----
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💬 Resume Q&A")
    st.markdown(
        "Upload a PDF and ask questions. Answers are grounded in the doc, "
        "with page citations."
    )
    st.page_link("pages/01_Resume_QA.py", label="Open Resume Q&A", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔎 JD ↔ Resume Match")
    st.markdown(
        "Paste a job description and your resume text. "
        "Get a match score and missing keywords."
    )
    st.page_link("pages/02_JD_Resume_Match.py", label="Open JD → Resume Match", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("Tip: Add more tools by creating new files in the `pages/` folder.")
