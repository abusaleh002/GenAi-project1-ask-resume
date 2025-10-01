import os
import httpx
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_secret(name: str, default: str = "") -> str:
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, default)

def make_groq() -> Groq:
    key = get_secret("GROQ_API_KEY", "")
    if not key:
        st.warning("Missing GROQ_API_KEY. Add it in Settings → Secrets (cloud) or .env/.streamlit/secrets.toml (local).")
        st.stop()
    return Groq(api_key=key, http_client=httpx.Client())
