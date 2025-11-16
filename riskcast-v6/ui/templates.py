# ui/templates.py
# HTML templates for result cards, tooltips, and UI components (RISKCAST v5.5)

RESULT_CARD = """
<div class="result-box">
    🏆 <b>GỢI Ý TỐT NHẤT CHO MỤC TIÊU: {priority}</b><br><br>
    <span style="font-size:1.6rem;">{company} - {icc}</span><br><br>
    💰 Chi phí: <b>${cost:,.0f}</b> ({rate:.2%} giá trị hàng)<br>
    📊 Điểm TOPSIS: <b>{score:.3f}</b> | 🎯 Độ tin cậy: <b>{confidence:.2f}</b><br>
    📦 Loại gợi ý: <b>{category}</b><br>
    📜 Gói ICC: <b>{desc}</b>
</div>
"""

TOOLTIP_ICON = '<span class="tooltip-icon" data-tip="{tip}">i</span>'

EXPLANATION_BOX = """
<div class="explanation-box">
    <h4>{title}</h4>
    <ul>{items}</ul>
    {note}
</div>
"""

TOP3_CARD = """
<div class="{card_class}">
    <div class="{title_class}">{medal} #{rank}: {company}</div>
    <div class="top3-sub">
        <span class="badge-icc">{icc}</span>
        <div class="pill-badge">{category}</div>
    </div>
    <div class="top3-sub" style="color:#7CFFA1; font-size:0.98rem;">
        💰 Chi phí: <b>${cost:,.0f}</b>
    </div>
    <div class="top3-sub">
        📊 Điểm TOPSIS: <b>{score:.3f}</b>
    </div>
    <div class="top3-sub">
        🎯 Tin cậy mô hình: <b>{confidence:.2f}</b>
    </div>
    <div class="top3-sub">
        🌪 Rủi ro khí hậu (mean ± std): <b>{risk_mean:.2%} ± {risk_std:.2%}</b>
    </div>
</div>
"""

RISK_CARD = """
<div class="explanation-box">
    <h4>⚠️ Đánh giá rủi ro tài chính (VaR / CVaR) {tooltip}</h4>
    <ul>
        <li><b>VaR 95%:</b> ${var:,.0f} ({var_pct:.1f}% giá trị hàng).</li>
        <li><b>CVaR 95%:</b> ${cvar:,.0f} – tổn thất trung bình trong vùng tail.</li>
        <li><b>Nhận định:</b> {assessment}</li>
    </ul>
</div>
"""