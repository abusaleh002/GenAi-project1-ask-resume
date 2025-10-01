import os, io, httpx
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq
from lib.core import get_secret

load_dotenv()
st.set_page_config(page_title="Resume Q&A", page_icon="💬", layout="wide")

st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem; max-width: 1100px;}
      .hero {padding: 1.25rem 1.5rem; border-radius: 16px;
        background: linear-gradient(135deg, rgba(98,106,254,.10), rgba(125,211,252,.10));
        border: 1px solid rgba(120,120,120,.15); margin-bottom: 1rem;}
      .hero h1 {margin:0 0 .25rem 0; font-size: 2rem;}
      .chip {display:inline-block; padding:.25rem .6rem; border-radius:999px;
             border:1px solid rgba(120,120,120,.25); margin-right:.35rem; font-size:.80rem;}
      .stButton>button {border-radius:10px; font-weight:600;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>💬 Resume Q&A</h1>
      <div>Local embeddings (sentence-transformers) + Groq Llama-3.1. No OpenAI needed.</div>
      <div style="margin-top:.5rem;">
        <span class="chip">Model: llama-3.1</span>
        <span class="chip">Embeddings: MiniLM</span>
        <span class="chip">Backend: FAISS</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Settings")
    key_from_secret = get_secret("GROQ_API_KEY", "")
    if key_from_secret:
        groq_key = key_from_secret
        st.caption("Using server-side key (demo mode).")
    else:
        groq_key = st.text_input("Groq API Key", type="password", help="https://console.groq.com/keys")
    model = st.text_input("Model name", value="llama-3.1-8b-instant")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1)
    k = st.slider("Retriever top-k", 1, 8, 4, 1)
    embed_model = st.text_input("Embedding model", value="sentence-transformers/all-MiniLM-L6-v2")
    st.caption("Vector backend: FAISS")

if not groq_key:
    st.warning("Enter your Groq API key to begin.", icon="🔑")
    st.stop()

with st.container(border=True):
    st.subheader("Upload a PDF (resume, paper, etc.)", divider=False)
    uploaded = st.file_uploader(" ", type=["pdf"], label_visibility="collapsed")

@st.cache_resource(show_spinner=False)
def build_index(pdf_bytes: bytes, embed_model_name: str, k: int):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for i, page in enumerate(reader.pages):
        try: text = page.extract_text() or ""
        except Exception: text = ""
        if text.strip(): pages.append((i + 1, text))
    if not pages:
        raise ValueError("No extractable text found in the PDF (is it scanned?).")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = []
    for pageno, text in pages:
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata={"page": pageno}))

    embeddings = HuggingFaceEmbeddings(model_name=embed_model_name, model_kwargs={"device": "cpu"})
    vs = FAISS.from_documents(docs, embeddings)
    return vs.as_retriever(search_kwargs={"k": k}), {"pages": len(pages), "chunks": len(docs)}

def answer_with_rag(groq_client: Groq, retriever, question: str, model: str, temperature: float):
    docs = retriever.get_relevant_documents(question)
    sources_text = "\n\n".join([f"[Page {d.metadata.get('page', '?')}] {d.page_content}" for d in docs])
    system = "You answer strictly using the provided context. If not in context, say you couldn't find it."
    user = f"Context from the PDF:\n\n{sources_text}\n\nQuestion: {question}\n\nAnswer concisely. Cite pages."
    chat = groq_client.chat.completions.create(
        model=model, temperature=temperature,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return chat.choices[0].message.content, docs

if uploaded:
    try:
        retriever, stats = build_index(uploaded.read(), embed_model_name=embed_model, k=k)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pages", stats["pages"]); c2.metric("Chunks", stats["chunks"])
        c3.metric("Top-k", k); c4.metric("Embedding", "MiniLM-L6-v2")

        if "chat" not in st.session_state: st.session_state.chat = []
        for turn in st.session_state.chat:
            with st.chat_message(turn["role"]): st.write(turn["text"])

        user_q = st.chat_input("Ask about your PDF…")
        if user_q:
            st.chat_message("user").write(user_q)
            with st.spinner("Thinking…"):
                client = Groq(api_key=groq_key, http_client=httpx.Client())
                answer, sources = answer_with_rag(client, retriever, user_q, model, temperature)
            with st.chat_message("assistant"):
                st.write(answer)
                with st.expander("Sources"):
                    for i, doc in enumerate(sources, 1):
                        page = doc.metadata.get("page", "?")
                        snippet = doc.page_content[:400].replace("\n", " ")
                        st.markdown(f"**{i}. Page {page}:** {snippet}…")
            st.session_state.chat += [{"role": "user", "text": user_q}, {"role": "assistant", "text": answer}]
    except Exception as e:
        st.error(f"Error: {e}")
else:
    with st.container(border=True):
        st.info("Upload a PDF to begin. Tip: try your resume first!")
