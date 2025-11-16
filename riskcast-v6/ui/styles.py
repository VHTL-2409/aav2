# ui/styles.py
import streamlit as st
import os


def app_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="RISKCAST v5.5 — Enterprise Tooltip Edition",
        page_icon="🛡️",
        layout="wide"
    )


def apply_css():
    """Apply inline CSS (fallback if enterprise.css not found)."""
    st.markdown("""
    <style>
    .stApp { background: #0e1613 !important; color: #e9fff4 !important; }
    .block-container { padding-top: 1.2rem !important; max-width: 1500px !important; }
    /* Hide Streamlit pages navigation */
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebar"] nav { display: none !important; }
    section[data-testid="stSidebar"] > div > div:first-child { display: none !important; }
    button[kind="secondary"] { display: none !important; }
    .rc-header { padding: 1.2rem 1.6rem; border-radius: 18px; background: linear-gradient(135deg, rgba(18,44,36,0.9), rgba(5,15,12,0.98)); 
        border: 1px solid rgba(0,255,153,0.22); box-shadow: 0 10px 26px rgba(0,0,0,0.55); margin-bottom: 1.8rem; display: flex; 
        justify-content: space-between; align-items: center; gap: 1.4rem; }
    .rc-logo { width: 78px; height: 78px; border-radius: 18px; 
        background: radial-gradient(circle at 40% 35%, #ffffff 0%, #d7fff4 14%, #7affd4 32%, #00e6a7 55%, #003826 100%); 
        display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.75rem; color: #001c12; 
        border: 3px solid #c4ffea; box-shadow: 0 0 22px rgba(0,255,153,0.65); }
    .rc-title { font-size: 1.55rem; font-weight: 900; letter-spacing: 0.03em; 
        background: linear-gradient(90deg, #eafff8, #beffdd, #d2fff0); -webkit-background-clip: text; color: transparent; }
    .rc-subtitle { margin-top: 2px; font-size: 0.93rem; opacity: 0.92; color: #c4ffea; font-weight: 500; }
    .rc-badge { background: linear-gradient(120deg, #00e676, #00bfa5); padding: 0.55rem 1.1rem; border-radius: 999px; 
        color: #00140c; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.02em; box-shadow: 0 0 14px rgba(0,255,153,0.55); }
    .result-box { background: radial-gradient(circle at top left,#00ff99,#00bfa5); color: #00130d !important; 
        padding: 1.6rem 2rem; border-radius: 18px; font-weight: 800; box-shadow: 0 0 22px rgba(0, 255, 153, 0.7), 0 18px 40px rgba(0, 0, 0, 0.9); 
        border: 2px solid #b9f6ca; margin-top: 0.6rem; }
    .explanation-box { background: rgba(5,25,20,0.95); border-left: 4px solid #00e676; padding: 1.1rem 1.4rem; 
        border-radius: 12px; margin-top: 0.7rem; box-shadow: 0 0 16px rgba(0,0,0,0.7); }
    .tooltip-icon { display: inline-flex; align-items: center; justify-content: center; margin-left: 6px; 
        background: rgba(0,255,153,0.15); color: #a5ffdc; border-radius: 50%; width: 18px; height: 18px; 
        text-align: center; font-size: 12px; cursor: help; border: 1px solid rgba(0,255,153,0.4); font-weight: 700; 
        box-shadow: 0 0 8px rgba(0,255,153,0.25); position: relative; }
    .top3-card { position: relative; background: radial-gradient(circle at top left, rgba(0,255,153,0.12), rgba(0,0,0,0.78)); 
        border: 1px solid rgba(0,255,153,0.45); padding: 18px 18px; border-radius: 18px; box-shadow: 0 0 18px rgba(0,255,153,0.18); 
        margin-bottom: 18px; text-align: center; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); 
        transition: all 0.18s ease-out; }
    .top1-card { background: radial-gradient(circle at top left, rgba(255,215,0,0.18), rgba(0,0,0,0.88)); 
        border: 1px solid rgba(255,215,0,0.7); box-shadow: 0 0 26px rgba(255,215,0,0.45); animation: gold-pulse 2.4s ease-in-out infinite alternate; }
    @keyframes gold-pulse { 0% { box-shadow: 0 0 10px rgba(255,215,0,0.35); border-color: rgba(255,215,0,0.6); } 
        100% { box-shadow: 0 0 26px rgba(255,215,0,0.8); border-color: rgba(255,255,255,0.9); } }
    .stButton > button { background: linear-gradient(120deg, #00ff99, #00e676, #00bfa5) !important; color: #00140d !important; 
        font-weight: 800 !important; border-radius: 999px !important; border: none !important; padding: 0.6rem 1.7rem !important; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.7), 0 0 14px rgba(0,255,153,0.55) !important; }
    </style>
    """, unsafe_allow_html=True)


def apply_enterprise_css():
    """Apply enterprise CSS (try to load from file, fallback to inline)."""
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "enterprise.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback to inline CSS
        apply_css()