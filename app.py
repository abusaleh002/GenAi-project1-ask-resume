import os
import io
import httpx
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS  # swap to Chroma if you prefer
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq

# ---------- boot ----------
load_dotenv()
st.set_page_config(
    page_title="Ask My Resume (PDF) Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- tiny helper ----------
def get_secret(name: str, default: str = "") -> str:
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, default)

# ---------- light CSS polish ----------
st.markdown(
    """
    <style>
      /* overall width tweak */
      .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px;}
      /* header */
      .app-hero {
        padding: 1.25rem 1.5rem; border-radius: 16px;
        background: linear-gradient(135deg, rgba(98,106,254,.10), rgba(125,211,252,.10));
        border: 1px solid rgba(120, 120, 120, .15);
        margin-bottom: 1rem;
      }
      .app-hero h1 {margin: 0 0 .25rem 0; font-size: 2rem;}
      .sub {color: rgba(0,0,0,.6); font-size: .95rem;}
      /* chips */
      .chip {
        display:inline-block; padding:.25rem .6rem; border-radius:999px;
        border:1px solid rgba(120,120,120,.25); margin-right:.35rem;
        font-size:.80rem; color:rgba(0,0,0,.7); background: rgba(255,255,255,.6);
      }
      /* buttons */
      .stButton>button, .stDownloadButton>button {
        border-radius: 10px !important; padding:.5rem 1rem !important; font-weight:600;
      }
      /* expander */
      details>summary {font-weight:600;}
      /* hide default footer */
      footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- sidebar (settings) ----------
with st.sidebar:
    st.header("Settings")
    key_from_secret = get_secret("GROQ_API_KEY", "")
    if key_from_secret:
        groq_key = key_from_secret
        st.caption("Using server-side key (demo mode).")
    else:
        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Create one at https://console.groq.com/keys (free tier).",
        )

    model = st.text_input(
        "Model name",
        value="llama-3.1-8b-instant",
        help="Examples: llama-3.1-8b-instant, llama-3.1-8b, llama-3.1-70b",
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1)
    k = st.slider("Retriever top-k", 1, 8, 4, 1)
    embed_model = st.text_input(
        "Embedding model",
        value="sentence-transformers/all-MiniLM-L6-v2",
        help="Runs locally on CPU.",
    )
    st.caption("Vector backend: FAISS")

if not groq_key:
    st.warning("Enter your Groq API key to begin.", icon="🔑")
    st.stop()

# ---------- header ----------
st.markdown(
    """
    <div class="app-hero">
      <h1>💬 Ask My Resume (PDF) Chatbot — Free Stack</h1>
      <div class="sub">
        Local embeddings (sentence-transformers) + Groq Llama-3.1. No OpenAI needed.
      </div>
      <div style="margin-top:.5rem;">
        <span class="chip">Model: llama-3.1</span>
        <span class="chip">Embeddings: MiniLM</span>
        <span class="chip">Backend: FAISS</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- file card ----------
with st.container(border=True):
    st.subheader("Upload a PDF (resume, paper, etc.)", divider=False)
    uploaded = st.file_uploader(" ", type=["pdf"], label_visibility="collapsed")

# ---------- index builder ----------
@st.cache_resource(show_spinner=False)
def build_index(pdf_bytes: bytes, embed_model_name: str, k: int):
    # 1) Extract text
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            pages.append((i + 1, text))
    if not pages:
        raise ValueError("No extractable text found in the PDF (is it scanned?).")

    # 2) Chunk
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = []
    for pageno, text in pages:
        chunks = splitter.split_text(text)
        for ch in chunks:
            docs.append(Document(page_content=ch, metadata={"page": pageno}))

    # 3) Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=embed_model_name,
        model_kwargs={"device": "cpu"}  # set "cuda" if running with GPU
    )

    # 4) Vector store + retriever
    vs = FAISS.from_documents(docs, embeddings)
    retriever = vs.as_retriever(search_kwargs={"k": k})

    stats = {"pages": len(pages), "chunks": len(docs)}
    return retriever, stats

def answer_with_rag(groq_client: Groq, retriever, question: str, model: str, temperature: float):
    docs = retriever.get_relevant_documents(question)
    sources_text = "\n\n".join(
        [f"[Page {d.metadata.get('page', '?')}] {d.page_content}" for d in docs]
    )

    system = (
        "You are a helpful assistant that answers strictly using the provided context. "
        "If the answer is not in the context, say: 'I couldn't find that in the PDF.'"
    )
    user = (
        f"Context from the PDF:\n\n{sources_text}\n\n"
        f"Question: {question}\n\n"
        "Answer concisely. Cite page numbers in parentheses when possible."
    )

    chat = groq_client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return chat.choices[0].message.content, docs

# ---------- main flow ----------
if uploaded:
    try:
        with st.spinner("Building index…"):
            retriever, stats = build_index(uploaded.read(), embed_model_name=embed_model, k=k)

        # pretty metrics row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pages", stats["pages"])
        c2.metric("Chunks", stats["chunks"])
        c3.metric("Top-k", k)
        c4.metric("Embedding", "MiniLM-L6-v2")

        # init chat state
        if "chat" not in st.session_state:
            st.session_state.chat = []   # list of {"role": "user"/"assistant", "text": str, "sources": list}

        # render history
        for turn in st.session_state.chat:
            with st.chat_message(turn["role"]):
                st.write(turn["text"])
                if turn.get("sources"):
                    with st.expander("Sources"):
                        for i, doc in enumerate(turn["sources"], 1):
                            page = doc.metadata.get("page", "?")
                            snippet = doc.page_content[:400].replace("\n", " ")
                            st.markdown(f"**{i}. Page {page}:** {snippet}…")

        # chat input at the bottom
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

            st.session_state.chat.append({"role": "user", "text": user_q})
            st.session_state.chat.append({"role": "assistant", "text": answer, "sources": sources})

    except Exception as e:
        st.error(f"Error: {e}")
else:
    with st.container(border=True):
        st.info("Upload a PDF to begin. Tip: try your resume first!")
