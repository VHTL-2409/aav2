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
    page_title="RISKCAST v6 — Enterprise Neon Premium",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 Import CSS + page config
from ui.styles import app_config, apply_enterprise_css, load_neon_premium_styles

# 📊 Page: Analysis
from app.pages.analysis import show_analysis


def main():
    # Global config
    app_config()

    # Load CSS themes
    apply_enterprise_css()          # Giao diện hiện tại
    load_neon_premium_styles()      # ⬅ THÊM CSS NEON PREMIUM V6

    # Render main page
    show_analysis()


if __name__ == "__main__":
    main()
