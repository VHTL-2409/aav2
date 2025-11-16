# ui/charts.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict


class ChartFactory:
    @staticmethod
    def _apply_theme(fig: go.Figure, title: str) -> go.Figure:
        fig.update_layout(
            template="plotly_dark",
            title=dict(text=f"<b>{title}</b>", font=dict(size=22, color="#e6fff7"), x=0.5),
            font=dict(size=15, color="#e6fff7"),
            plot_bgcolor="#001016",
            paper_bgcolor="#000c11",
            margin=dict(l=70, r=40, t=80, b=70),
            legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="#00e676", borderwidth=1)
        )
        fig.update_xaxes(showgrid=True, gridcolor="#00332b", tickfont=dict(size=14, color="#e6fff7"))
        fig.update_yaxes(showgrid=True, gridcolor="#00332b", tickfont=dict(size=14, color="#e6fff7"))
        return fig

    @staticmethod
    def create_weights_pie(weights: pd.Series, title: str = "Trọng số tiêu chí") -> go.Figure:
        colors = ['#00e676', '#69f0ae', '#b9f6ca', '#00bfa5', '#1de9b6', '#64ffda']
        labels_full = list(weights.index)
        labels_short = [c.split(':')[0] for c in labels_full]

        fig = go.Figure(data=[go.Pie(
            labels=labels_full,
            values=weights.values,
            text=labels_short,
            textinfo='text+percent',
            textposition='inside',
            hole=0.18,
            marker=dict(colors=colors, line=dict(color='#00130d', width=2)),
            pull=[0.04] * len(weights),
            hovertemplate="<b>%{label}</b><br>Tỉ trọng: %{percent}<extra></extra>"
        )])

        fig.update_layout(
            title=dict(text=f"<b>{title}</b>", font=dict(size=20, color="#a5ffdc"), x=0.5, y=0.98),
            showlegend=True,
            legend=dict(title="<b>Các tiêu chí</b>", font=dict(size=13, color="#e6fff7")),
            paper_bgcolor="#001016",
            plot_bgcolor="#001016",
            margin=dict(l=0, r=0, t=80, b=0),
            height=480
        )
        return fig

    @staticmethod
    def create_cost_benefit_scatter(results: pd.DataFrame) -> go.Figure:
        color_map = {"ICC A": "#ff6b6b", "ICC B": "#ffd93d", "ICC C": "#6bcf7f"}
        fig = go.Figure()

        for icc in ["ICC C", "ICC B", "ICC A"]:
            df_icc = results[results["icc_package"] == icc]
            fig.add_trace(go.Scatter(
                x=df_icc["estimated_cost"],
                y=df_icc["score"],
                mode="markers+text",
                name=icc,
                text=df_icc["company"],
                textposition="top center",
                marker=dict(size=15, color=color_map[icc], line=dict(width=2, color="#000")),
                hovertemplate="<b>%{text}</b><br>Gói: " + icc + "<br>Chi phí: $%{x:,.0f}<br>Điểm: %{y:.3f}<extra></extra>"
            ))

        fig.update_xaxes(title="<b>Chi phí ước tính ($)</b>")
        fig.update_yaxes(title="<b>Điểm TOPSIS</b>", range=[0, 1])
        fig = ChartFactory._apply_theme(fig, "Chi phí vs Chất lượng (Cost-Benefit Analysis)")
        fig.update_layout(height=480)
        return fig

    @staticmethod
    def create_top_recommendations_bar(results: pd.DataFrame) -> go.Figure:
        df = results.head(5).copy()
        df["label"] = df["company"] + " - " + df["icc_package"]

        fig = go.Figure(data=[go.Bar(
            x=df["score"],
            y=df["label"],
            orientation="h",
            text=[f"{v:.3f}" for v in df["score"]],
            textposition="outside",
            marker=dict(
                color=df["score"],
                colorscale=[[0, '#69f0ae'], [0.5, '#00e676'], [1, '#00c853']],
                line=dict(color='#00130d', width=1)
            ),
            hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<br>Chi phí: $%{customdata:,.0f}<extra></extra>",
            customdata=df["estimated_cost"]
        )])

        fig.update_xaxes(title="<b>Điểm TOPSIS</b>", range=[0, 1])
        fig.update_yaxes(title="<b>Phương án</b>")
        fig = ChartFactory._apply_theme(fig, "Top 5 Phương án Tốt nhất")
        fig.update_layout(height=440)
        return fig

    @staticmethod
    def create_forecast_chart(
        historical: np.ndarray,
        forecast: np.ndarray,
        route: str = "VN - EU",
        selected_month: int = 9
    ) -> go.Figure:
        hist_len = len(historical)
        months_hist = list(range(1, hist_len + 1))
        next_month = selected_month % 12 + 1
        months_fc = [next_month]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months_hist, y=historical,
            mode="lines+markers", name="Lịch sử",
            line=dict(color="#00e676", width=3), marker=dict(size=9),
            hovertemplate="Tháng %{x}<br>Rủi ro: %{y:.1%}<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=months_fc, y=forecast,
            mode="lines+markers", name="Dự báo",
            line=dict(color="#ffeb3b", width=3, dash="dash"),
            marker=dict(size=11, symbol="diamond"),
            hovertemplate="Tháng %{x}<br>Dự báo: %{y:.1%}<extra></extra>"
        ))

        fig = ChartFactory._apply_theme(fig, f"Dự báo rủi ro khí hậu — {route}")
        fig.update_xaxes(title="<b>Tháng</b>", tickmode="linear", tick0=1, dtick=1, range=[1, 12], tickvals=list(range(1, 13)))
        max_val = max(float(historical.max()), float(forecast.max()))
        fig.update_yaxes(title="<b>Mức rủi ro (0–1)</b>", range=[0, max(1.0, max_val * 1.15)], tickformat=".0%")
        fig.update_layout(height=450)
        return fig

    @staticmethod
    def create_fuzzy_heatmap(results: pd.DataFrame) -> go.Figure:
        """Create heatmap for fuzzy uncertainty from results DataFrame."""
        if len(results) == 0:
            return go.Figure().add_annotation(text="Không có dữ liệu")
        
        # Extract fuzzy columns if they exist, otherwise use score variance as proxy
        fuzzy_cols = [col for col in results.columns if 'fuzzy' in col.lower()]
        if fuzzy_cols:
            fuzzy_data = results[fuzzy_cols].head(10).values
            labels = fuzzy_cols
        else:
            # Use first 10 options, score as single metric
            fuzzy_data = results["score"].head(10).values.reshape(-1, 1)
            labels = ["Điểm TOPSIS"]
        
        option_labels = results["company"].head(10).values + " - " + results["icc_package"].head(10).values
        
        fig = go.Figure(data=go.Heatmap(
            z=fuzzy_data,
            x=labels,
            y=option_labels,
            colorscale='Greens',
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.3f}<extra></extra>"
        ))
        fig = ChartFactory._apply_theme(fig, "Mức dao động Fuzzy")
        fig.update_layout(height=400)
        return fig

    @staticmethod
    def create_sensitivity_spider(results: pd.DataFrame) -> go.Figure:
        """Create spider/radar chart for sensitivity analysis."""
        top_5 = results.head(5)
        fig = go.Figure()
        categories = ['Giá', 'Chất lượng', 'Rủi ro', 'Dịch vụ', 'Uy tín']
        for _, row in top_5.iterrows():
            values = [
                float(1.0 - row.get("C1: Tỷ lệ phí", 0.5)),  # inverse cost
                float(row.get("C2: Thời gian xử lý", 0.5)),
                float(1.0 - row.get("C6: Rủi ro khí hậu", 0.5)),  # inverse risk
                float(row.get("C4: Hỗ trợ ICC", 0.5)),
                float(row.get("C5: Chăm sóc KH", 0.5))
            ]
            fig.add_trace(go.Scatterpolar(r=values, theta=categories, name=f"{row['company']} - {row['icc_package']}"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, height=500)
        fig = ChartFactory._apply_theme(fig, "Phân tích độ nhạy")
        return fig

    @staticmethod
    def create_confidence_radar(results: pd.DataFrame) -> go.Figure:
        """Create confidence/reliability radar chart."""
        top_5 = results.head(5)
        fig = go.Figure()
        for _, row in top_5.iterrows():
            confidence = float(row.get("confidence", 0.5))
            fig.add_trace(go.Bar(y=[confidence], name=f"{row['company']} - {row['icc_package']}"))
        fig.update_layout(title="<b>Độ tin cậy dự báo</b>", yaxis_range=[0, 1], height=400)
        fig = ChartFactory._apply_theme(fig, "Độ tin cậy")
        return fig

    @staticmethod
    def create_category_comparison(results: pd.DataFrame) -> go.Figure:
        """Create category comparison chart with dual axes."""
        categories = ["Tiết kiệm", "Cân bằng", "An toàn"]
        avg_scores = []
        avg_costs = []

        for cat in categories:
            df_cat = results[results["category"] == cat]
            avg_scores.append(df_cat["score"].mean() if len(df_cat) > 0 else 0)
            avg_costs.append(df_cat["estimated_cost"].mean() if len(df_cat) > 0 else 0)

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Điểm trung bình", x=categories, y=avg_scores, marker=dict(color='#00e676'), yaxis="y"))
        fig.add_trace(go.Scatter(name="Chi phí trung bình", x=categories, y=avg_costs, mode="lines+markers",
                                 marker=dict(size=10, color='#ffeb3b'), line=dict(width=3, color='#ffeb3b'), yaxis="y2"))

        fig.update_layout(
            title=dict(text="<b>So sánh 3 loại phương án</b>", font=dict(size=22, color="#e6fff7"), x=0.5),
            yaxis=dict(title=dict(text="<b>Điểm TOPSIS</b>", font=dict(color="#00e676")), range=[0, 1]),
            yaxis2=dict(title=dict(text="<b>Chi phí ($)</b>", font=dict(color="#ffeb3b")), overlaying="y", side="right"),
            paper_bgcolor="#000c11", plot_bgcolor="#001016", font=dict(color="#e6fff7"),
            legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="#00e676", borderwidth=1),
            margin=dict(l=60, r=60, t=80, b=60), height=480
        )
        return fig