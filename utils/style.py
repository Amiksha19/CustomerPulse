import streamlit as st
from pathlib import Path


def load_css():

    current_file = Path(__file__).resolve()

    # Project root = folder containing utils/
    project_root = current_file.parent.parent

    css_path = project_root / "assets" / "css" / "style.css"

    if not css_path.exists():
        st.error(f"CSS file not found at: {css_path}")
        return

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    st.html(f"<style>{css}</style>")