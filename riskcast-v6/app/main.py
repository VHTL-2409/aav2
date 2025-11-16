# app/main.py
import streamlit as st
import sys
import os

# Add project root to path for imports and set working directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set working directory to project root for data file loading
os.chdir(project_root)

# Hide Streamlit navigation pages
st.set_page_config(
    page_title="RISKCAST v5.5",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from ui.styles import app_config, apply_enterprise_css
from app.pages.analysis import show_analysis

def main():
    app_config()
    apply_enterprise_css()
    show_analysis()

if __name__ == "__main__":
    main()