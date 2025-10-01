# lib/ui.py
from pathlib import Path
import streamlit as st

def inject_css(relative_to_root: str) -> None:
    """Inject a CSS file located relative to the project root."""
    root = Path(__file__).resolve().parents[1]      # project root
    css_path = root / relative_to_root
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>",
                unsafe_allow_html=True)
