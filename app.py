import os
import io
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS  # or Chroma if you switched
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq

load_dotenv()

def get_secret(name: str, default: str = "") -> str:
    # Works with Streamlit Cloud secrets and local env/.env
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, default)

st.set_page_config(page_title="Upload Your Resume & Ask about your Resume (PDF) Chatbot", page_icon="💬")
st.title("💬 Ask Your Resume (PDF) Chatbot — Free Stack")
st.caption("Local embeddings (sentence-transformers) + Groq Llama-3.1 (free). No OpenAI needed.")

with st.sidebar:
    st.header("Settings")

    # 👉 If a server-side secret exists, use it and hide the input.
    key_from_secret = get_secret("GROQ_API_KEY", "")
    if key_from_secret:
        groq_key = key_from_secret
        st.caption("Using server-side key (demo mode).")
    else:
        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Create one at https://console.groq.com/keys (free tier)."
        )

    model = st.text_input(
        "Model name",
        value="llama-3.1-8b-instant",
        help="Examples: llama-3.1-8b-instant, llama-3.1-8b, llama-3.1-70b"
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1)
    k = st.slider("Retriever top-k", 1, 8, 4, 1)
    embed_model = st.text_input(
        "Embedding model",
        value="sentence-transformers/all-MiniLM-L6-v2",
        help="Runs locally on CPU."
    )

if not groq_key:
    st.warning("Enter your Groq API key in the sidebar to begin.", icon="🔑")
    st.stop()

uploaded = st.file_uploader("Upload a PDF (resume, paper, etc.)", type=["pdf"])

@st.cache_resource(show_spinner=False)
def build_index(pdf_bytes: bytes, embed_model_name: str, k: int):
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

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = []
    for pageno, text in pages:
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata={"page": pageno}))

    embeddings = HuggingFaceEmbeddings(
        model_name=embed_model_name,
        model_kwargs={"device": "cpu"}
    )

    vs = FAISS.from_documents(docs, embeddings)  # or Chroma.from_documents(...)
    return vs.as_retriever(search_kwargs={"k": k})

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

if uploaded:
    try:
        retriever = build_index(uploaded.read(), embed_model_name=embed_model, k=k)
        st.success("Index built. Ask questions below.")

        if "history" not in st.session_state:
            st.session_state.history = []

        user_q = st.text_input("Your question", placeholder="e.g., What are my top 3 strengths in this resume?")
        ask = st.button("Ask")

        if ask and user_q.strip():
            with st.spinner("Thinking..."):
                client = Groq(api_key=groq_key)
                answer, sources = answer_with_rag(client, retriever, user_q, model, temperature)

            st.markdown(f"**Answer:** {answer}")
            with st.expander("Sources"):
                for i, doc in enumerate(sources, 1):
                    page = doc.metadata.get("page", "?")
                    snippet = doc.page_content[:400].replace("\n", " ")
                    st.markdown(f"**{i}. Page {page}:** {snippet}...")

            st.session_state.history.append({"q": user_q, "a": answer})

        if st.session_state.history:
            st.divider()
            st.subheader("Chat History")
            for turn in st.session_state.history[::-1]:
                st.markdown(f"**You:** {turn['q']}")
                st.markdown(f"**Bot:** {turn['a']}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Upload a PDF to begin. Tip: try your resume first!")
