import streamlit as st

def load_global_styles():
    st.markdown("""
    <style>

    /* =========================================================
       NEON PREMIUM v6 — Top Recommendation Card
       Designed by Kai for Bùi Xuân Hoàng
       ========================================================= */

    .neon-card {
        padding: 28px 30px;
        border-radius: 22px;
        background: rgba(0, 15, 12, 0.90);
        border: 2px solid rgba(0, 255, 170, 0.45);

        box-shadow:
            0 0 12px rgba(0, 255, 170, 0.35),
            0 0 30px rgba(0, 255, 170, 0.20),
            inset 0 0 12px rgba(0, 255, 170, 0.15);

        backdrop-filter: blur(6px);
        transition: all 0.25s ease-in-out;
    }

    .neon-card:hover {
        transform: translateY(-3px);
        box-shadow:
            0 0 16px rgba(0, 255, 170, 0.55),
            0 0 40px rgba(0, 255, 200, 0.28),
            inset 0 0 16px rgba(0, 255, 170, 0.22);
    }

    .neon-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #C9FFE8;
        margin-bottom: 18px;
        letter-spacing: 0.5px;
    }

    .neon-company {
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(90deg, #A5FFDC, #65FFC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .neon-info {
        font-size: 1.1rem;
        color: #C2FFE4;
        margin-bottom: 8px;
    }

    .neon-info b {
        color: #FFFFFF;
    }

    .icc-desc {
        margin-top: 14px;
        padding-top: 12px;
        font-size: 0.95rem;
        color: #E8FFF5;
        border-top: 1px solid rgba(0,255,170,0.25);
    }

    </style>
    """, unsafe_allow_html=True)
