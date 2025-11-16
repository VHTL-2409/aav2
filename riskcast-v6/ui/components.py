# ui/components.py
import streamlit as st
from core.models import AnalysisParams
from config.constants import PRIORITY_PROFILES
from .templates import TOOLTIP_ICON

def render_header():
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 0;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 78px; height: 78px; background: radial-gradient(circle at 40% 35%, #ffffff 0%, #d7fff4 14%, #7affd4 32%, #00e6a7 55%, #003826 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; color: #00130d; font-size: 1.4rem;">
                RC
            </div>
            <div>
                <div style="font-size: 1.55rem; font-weight: 900; background: linear-gradient(90deg, #eafff8, #beffdd, #d2fff0); -webkit-background-clip: text; color: transparent;">
                    RISKCAST v6.0 — MULTI-PACKAGE
                </div>
                <div style="color: #a5ffdc; font-size: 0.95rem;">15 phương án · Profile-based · Hybrid ESG Engine</div>
            </div>
        </div>
        <div style="background: linear-gradient(120deg, #00e676, #00bfa5); padding: 0.55rem 1.1rem; border-radius: 999px; font-weight: 800; color: #00130d;">
            Smart ESG Risk & Insurance
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar() -> AnalysisParams:
    with st.sidebar:
        st.header("Thông tin lô hàng")
        cargo_value = st.number_input("Giá trị (USD)", 1000, value=39_000, step=1_000)
        route = st.selectbox("Tuyến", ["VN - EU", "VN - US", "VN - Singapore", "VN - China", "Domestic"])
        month = st.selectbox("Tháng", list(range(1, 13)), index=8)
        priority_profile = st.selectbox("Mục tiêu", list(PRIORITY_PROFILES.keys()))

        st.markdown("---")
        st.header("Cấu hình")
        col1, col2 = st.columns(2)
        with col1:
            use_fuzzy = st.checkbox("Fuzzy AHP", True)
            use_arima = st.checkbox("ARIMA", True)
        with col2:
            use_mc = st.checkbox("Monte Carlo", True)
            use_var = st.checkbox("VaR/CVaR", True)

        mc_runs = st.slider("MC Runs", 500, 5000, 2000, 500)
        fuzzy_uncertainty = st.slider("Fuzzy (%)", 0, 50, 15) if use_fuzzy else 15

        return AnalysisParams(
            cargo_value=cargo_value, good_type="", route=route, method="Sea",
            month=month, priority_profile=priority_profile, use_fuzzy=use_fuzzy, use_arima=use_arima,
            use_mc=use_mc, use_var=use_var, mc_runs=mc_runs, fuzzy_uncertainty=fuzzy_uncertainty
        )

def render_tooltip(text: str, tip: str):
    return f"{text} {TOOLTIP_ICON.format(tip=tip)}"