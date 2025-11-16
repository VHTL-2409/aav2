import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def apply_fuzzy(weights: pd.Series, uncertainty_pct: float) -> pd.Series:
    factor = uncertainty_pct / 100.0
    w = weights.values
    low = np.maximum(w * (1 - factor), 1e-9)
    high = np.minimum(w * (1 + factor), 0.9999)
    defuzzified = (low + w + high) / 3.0
    normalized = defuzzified / defuzzified.sum()
    return pd.Series(normalized, index=weights.index)

def build_fuzzy_table(weights: pd.Series, fuzzy_pct: float) -> pd.DataFrame:
    rows = []
    factor = fuzzy_pct / 100.0
    for crit in weights.index:
        w = float(weights[crit])
        low = max(w * (1 - factor), 0.0)
        high = min(w * (1 + factor), 1.0)
        centroid = (low + w + high) / 3.0
        rows.append([crit, round(low, 4), round(w, 4), round(high, 4), round(centroid, 4)])
    return pd.DataFrame(rows, columns=["Tiêu chí", "Low", "Mid", "High", "Centroid"])

def most_uncertain_criterion(weights: pd.Series, fuzzy_pct: float):
    factor = fuzzy_pct / 100.0
    diff_map = {}
    for crit in weights.index:
        w = float(weights[crit])
        low = w * (1 - factor)
        high = w * (1 + factor)
        diff_map[crit] = float(high - low)
    most_unc = max(diff_map, key=diff_map.get)
    return most_unc, diff_map

def fuzzy_heatmap_premium(diff_map):
    values = list(diff_map.values())
    labels = list(diff_map.keys())
    fig = px.imshow([values], x=labels, y=[""], color_continuous_scale="Greens")
    fig.update_layout(title="<b>Heatmap mức dao động Fuzzy</b>", paper_bgcolor="#001a12", plot_bgcolor="#001a12")
    return fig

def fuzzy_chart_premium(fuzzy_table: pd.DataFrame) -> go.Figure:
    """Create fuzzy membership visualization from fuzzy table."""
    fig = go.Figure()
    
    criteria = fuzzy_table["Tiêu chí"].values
    low_vals = fuzzy_table["Low"].values
    mid_vals = fuzzy_table["Mid"].values
    high_vals = fuzzy_table["High"].values
    
    # Add traces for low, mid, high
    fig.add_trace(go.Bar(
        y=criteria, x=low_vals, name="Low", orientation="h",
        marker=dict(color="#1de9b6"), opacity=0.6
    ))
    fig.add_trace(go.Bar(
        y=criteria, x=mid_vals, name="Mid (Weight)", orientation="h",
        marker=dict(color="#00e676")
    ))
    fig.add_trace(go.Bar(
        y=criteria, x=high_vals, name="High", orientation="h",
        marker=dict(color="#69f0ae"), opacity=0.6
    ))
    
    fig.update_layout(
        barmode="overlay",
        title="<b>Hàm Kỳ Vọng Mờ (Fuzzy Membership Functions)</b>",
        xaxis_title="<b>Trọng số</b>",
        yaxis_title="<b>Tiêu chí</b>",
        template="plotly_dark",
        paper_bgcolor="#000c11",
        plot_bgcolor="#001016",
        font=dict(color="#e6fff7", size=12),
        height=400
    )
    return fig