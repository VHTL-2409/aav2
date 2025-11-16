# app/pages/analysis.py
"""Main analysis page (RISKCAST v5.5 Enterprise)."""
import streamlit as st
import pandas as pd
from io import BytesIO
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ui.components import render_header, render_sidebar
from ui.charts import ChartFactory
from ui.templates import RESULT_CARD, EXPLANATION_BOX, TOP3_CARD, RISK_CARD
from ui.export import ReportGenerator
from core.mcdm import MultiPackageAnalyzer
from core.models import AnalysisParams
from utils.fuzzy import build_fuzzy_table, fuzzy_chart_premium, most_uncertain_criterion
from config.constants import ICC_PACKAGES, PRIORITY_PROFILES
import numpy as np


def display_profile_explanation(priority_profile: str) -> None:
    """Show selected priority profile and its criteria weights."""
    weights = PRIORITY_PROFILES[priority_profile]
    items_html = "".join([
        f'<li><b>{crit}</b>: {weight:.0%}</li>'
        for crit, weight in weights.items()
    ])
    
    st.markdown(EXPLANATION_BOX.format(
        title=f"🎯 Tiêu chí đánh giá: {priority_profile}",
        items=items_html,
        note="<p style='font-size:0.85rem; color:#888;'><i>Trọng số phản ánh ưu tiên của bạn trong quyết định chọn gói bảo hiểm.</i></p>"
    ), unsafe_allow_html=True)


def display_top_recommendations(result, params) -> None:
    """Display top-3 recommendations with gold-pulse animations."""
    st.subheader("🏆 Top 3 Gợi Ý Hàng Đầu")
    
    top3_df = result.results.head(3)
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    
    for idx, (col, (_, row)) in enumerate(zip(cols, top3_df.iterrows())):
        with col:
            card_class = "top3-card top3-card-1" if idx == 0 else "top3-card"
            title_class = "top3-title gold-pulse" if idx == 0 else "top3-title"
            
            html = TOP3_CARD.format(
                card_class=card_class,
                title_class=title_class,
                medal=medals[idx],
                rank=idx + 1,
                company=row.get('company', 'Unknown'),
                icc=row.get('icc_package', 'N/A'),
                category=row.get('category', 'N/A'),
                cost=row.get('estimated_cost', 0),
                score=row.get('score', 0),
                confidence=row.get('confidence', 0),
                risk_mean=row.get('C6: Rủi ro khí hậu', 0.0),
                risk_std=row.get('C6_std', 0.0)
            )
            st.markdown(html, unsafe_allow_html=True)


def display_full_results_table(result) -> None:
    """Display full 15-option ranking table."""
    st.subheader("📋 Bảng Xếp Hạng Đầy Đủ (15 Phương Án)")
    
    display_df = result.results[['rank', 'company', 'icc_package', 'category', 'estimated_cost', 'score', 'confidence']].copy()
    display_df.columns = ['Rank', 'Company', 'ICC Package', 'Category', 'Cost', 'TOPSIS Score', 'Confidence']
    
    # Format columns
    display_df['Cost'] = display_df['Cost'].apply(lambda x: f"${x:,.0f}")
    display_df['TOPSIS Score'] = display_df['TOPSIS Score'].apply(lambda x: f"{x:.4f}")
    display_df['Confidence'] = display_df['Confidence'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(display_df, use_container_width=True)


def display_risk_metrics(result) -> None:
    """Display VaR/CVaR risk metrics with interpretation."""
    st.subheader("⚠️ Phân Tích Rủi Ro Tài Chính")
    
    var_value = result.var if hasattr(result, 'var') else 0
    cvar_value = result.cvar if hasattr(result, 'cvar') else 0
    cargo_val = 100000  # Placeholder: should come from params
    
    var_pct = (var_value / cargo_val * 100) if cargo_val > 0 else 0
    
    # Assessment logic
    if var_pct < 2:
        assessment = "✅ Rủi ro thấp – an toàn cho lô hàng nhỏ đến vừa."
    elif var_pct < 5:
        assessment = "⚠️ Rủi ro trung bình – cần cân nhắc kỳ vọng giá trị hàng."
    else:
        assessment = "🔴 Rủi ro cao – xem xét bảo hiểm cao hơn hoặc phân chia lô."
    
    html = RISK_CARD.format(
        tooltip="<span class='tooltip-icon' data-tip='Rủi ro ở mức tin cậy 95%'>i</span>",
        var=var_value,
        var_pct=var_pct,
        cvar=cvar_value,
        assessment=assessment
    )
    st.markdown(html, unsafe_allow_html=True)


def display_analysis_charts(result, params) -> None:
    """Display 8 Plotly charts for comprehensive analysis."""
    st.subheader("📊 Phân Tích Chi Tiết & Biểu Đồ")
    
    chart_factory = ChartFactory()
    
    # Chart 1: Weights pie chart
    st.markdown("**Trọng số tiêu chí**")
    try:
        weights_fig = chart_factory.create_weights_pie(result.weights)
        st.plotly_chart(weights_fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Không thể hiển thị biểu đồ trọng số: {e}")
    
    # Chart 2: Cost-Benefit scatter
    st.markdown("**Bản đồ Chi phí - Điểm TOPSIS**")
    try:
        cost_benefit_fig = chart_factory.create_cost_benefit_scatter(result.results)
        st.plotly_chart(cost_benefit_fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Không thể hiển thị biểu đồ chi phí: {e}")
    
    # Chart 3: Top recommendations bar
    st.markdown("**Top 5 Phương Án Được Chọn**")
    try:
        bar_fig = chart_factory.create_top_recommendations_bar(result.results)
        st.plotly_chart(bar_fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Không thể hiển thị biểu đồ top 5: {e}")
    
    # Chart 4: Forecast (if available)
    st.markdown("**Dự Báo Rủi Ro (ARIMA Trend)**")
    if hasattr(result, 'forecast') and result.forecast is not None:
        try:
            forecast_fig = chart_factory.create_forecast_chart(
                result.historical, 
                result.forecast,
                route=params.route,
                selected_month=params.month
            )
            st.plotly_chart(forecast_fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Không thể hiển thị dự báo: {e}")
    else:
        st.info("Dự báo ARIMA không khả dụng (cần statsmodels)")
    
    # Chart 5: Category comparison
    st.markdown("**So Sánh Theo Loại Công Ty**")
    try:
        category_fig = chart_factory.create_category_comparison(result.results)
        st.plotly_chart(category_fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Không thể hiển thị so sánh loại: {e}")
    
    # Chart 6: Fuzzy heatmap (if enabled)
    if params.use_fuzzy:
        st.markdown("**Mức Độ Không Chắc Chắn (Fuzzy AHP)**")
        try:
            fuzzy_fig = chart_factory.create_fuzzy_heatmap(result.results)
            st.plotly_chart(fuzzy_fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Không thể hiển thị Fuzzy heatmap: {e}")
    
    # Chart 7: Sensitivity spider
    st.markdown("**Phân Tích Độ Nhạy (Spider)**")
    try:
        spider_fig = chart_factory.create_sensitivity_spider(result.results)
        st.plotly_chart(spider_fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Không thể hiển thị biểu đồ độ nhạy: {e}")
    
    # Chart 8: Confidence radar
    st.markdown("**Radar Độ Tin Cậy Mô Hình**")
    try:
        radar_fig = chart_factory.create_confidence_radar(result.results)
        st.plotly_chart(radar_fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Không thể hiển thị radar: {e}")


def display_fuzzy_analysis(result, params) -> None:
    """Display detailed Fuzzy AHP analysis if enabled."""
    if not params.use_fuzzy:
        return
    
    st.subheader("🌀 Phân Tích Fuzzy AHP - Đo Lường Không Chắc Chắn")
    
    try:
        # Build fuzzy table
        fuzzy_table = build_fuzzy_table(result.weights, params.fuzzy_uncertainty)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Hàm Kỳ Vọng Mờ (Fuzzy Membership Functions)**")
            st.dataframe(fuzzy_table, use_container_width=True)
        
        with col2:
            uncertain_crit, _ = most_uncertain_criterion(result.weights, params.fuzzy_uncertainty)
            st.markdown(f"**Tiêu chí Bất định Nhất:** {uncertain_crit}")
            st.info(f"Khoảng mờ lớn nhất → Cần thu thập thêm dữ liệu cho {uncertain_crit}")
        
        # Fuzzy visualization
        st.markdown("**Biểu Đồ Hàm Kỳ Vọng (Fuzzy Membership)**")
        fuzzy_chart = fuzzy_chart_premium(fuzzy_table)
        st.plotly_chart(fuzzy_chart, use_container_width=True)
    except Exception as e:
        st.warning(f"Lỗi khi hiển thị Fuzzy analysis: {e}")


def display_export_section(result, params) -> None:
    """Display export options (PDF, Excel)."""
    st.divider()
    st.subheader("📥 Xuất Báo Cáo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Xuất PDF"):
            try:
                report_gen = ReportGenerator()
                pdf_bytes = report_gen.generate_pdf(result, params)
                st.download_button(
                    label="⬇️ Tải Báo Cáo PDF",
                    data=pdf_bytes,
                    file_name="RISKCAST_Report.pdf",
                    mime="application/pdf"
                )
                st.success("✅ PDF đã được tạo thành công!")
            except Exception as e:
                st.error(f"❌ Lỗi tạo PDF: {e}")
    
    with col2:
        if st.button("📊 Xuất Excel"):
            try:
                report_gen = ReportGenerator()
                excel_bytes = report_gen.generate_excel(result, params)
                st.download_button(
                    label="⬇️ Tải Báo Cáo Excel",
                    data=excel_bytes,
                    file_name="RISKCAST_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ Excel đã được tạo thành công!")
            except Exception as e:
                st.error(f"❌ Lỗi tạo Excel: {e}")
    
    with col3:
        if st.button("🔄 Phân Tích Lại"):
            st.session_state.clear()
            st.rerun()


def show_analysis():
    """Main analysis page flow (RISKCAST v5.5)."""
    render_header()
    
    # Render sidebar for input parameters
    params = render_sidebar()
    
    # Analyze button
    if st.button("▶️ PHÂN TÍCH 15 PHƯƠNG ÁN", key="analyze_btn", use_container_width=True):
        with st.spinner("⏳ Đang phân tích..."):
            analyzer = MultiPackageAnalyzer()
            result = analyzer.run_analysis(params)
        
        # Store in session state
        st.session_state.last_result = result
        st.session_state.last_params = params
    
    # Display results if available
    if "last_result" in st.session_state:
        result = st.session_state.last_result
        params = st.session_state.last_params
        
        # 1. Show profile explanation
        display_profile_explanation(params.priority_profile)
        
        # 2. Top recommendation card
        st.markdown("---")
        st.markdown("### 🎯 Gợi Ý Chính")
        top_row = result.results.iloc[0]
        cargo_value = params.cargo_value if hasattr(params, 'cargo_value') else 100000
        result_html = RESULT_CARD.format(
            priority=params.priority_profile,
            company=top_row.get('company', 'Unknown'),
            icc=top_row.get('icc_package', 'N/A'),
            cost=top_row.get('estimated_cost', 0),
            rate=(top_row.get('estimated_cost', 0) / cargo_value if cargo_value > 0 else 0),
            score=top_row.get('score', 0),
            confidence=top_row.get('confidence', 0),
            category=top_row.get('category', 'N/A'),
            desc=ICC_PACKAGES.get(top_row.get('icc_package', 'ICC A'), {}).get('description', 'Gói ICC')
        )
        st.markdown(result_html, unsafe_allow_html=True)
        
        # 3. Top 3 recommendations
        st.markdown("---")
        display_top_recommendations(result, params)
        
        # 4. Full results table
        st.markdown("---")
        display_full_results_table(result)
        
        # 5. Risk metrics
        st.markdown("---")
        display_risk_metrics(result)
        
        # 6. Analysis charts
        st.markdown("---")
        display_analysis_charts(result, params)
        
        # 7. Fuzzy analysis (if enabled)
        if params.use_fuzzy:
            st.markdown("---")
            display_fuzzy_analysis(result, params)
        
        # 8. Export options
        display_export_section(result, params)