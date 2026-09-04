import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Configuration
st.set_page_config(page_title="Stat-Arb Engine", layout="wide")
st.title("Statistical Arbitrage & Cointegration Engine")
st.markdown("Automated pairs trading backtester using the Engle-Granger two-step method.")

@st.cache_data
def load_data():
    return pd.read_csv('data/backtest_results.csv', index_col='Date', parse_dates=True)

try:
    df = load_data()
    
    # Calculate top-level KPIs
    total_return = df['Cumulative_Return'].iloc[-1]
    active_days = (df['Strategy_Return'] != 0).sum()
    win_rate = (df['Strategy_Return'] > 0).sum() / active_days * 100 if active_days > 0 else 0
    
    # Render Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Strategy Profit (Spread Units)", f"{total_return:.4f}")
    col2.metric("Profitable Trading Days (%)", f"{win_rate:.1f}%")
    col3.metric("Live Portfolio", "github.com/Ma2323/stat-arb-engine")
    
    st.markdown("---")
    
    # Construct dual-axis Plotly charts
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        subplot_titles=("Z-Score Divergence & Mean Reversion Signals", 
                                        "Cumulative Strategy Equity Curve"),
                        vertical_spacing=0.1)

    # 1. Z-Score Chart
    fig.add_trace(go.Scatter(x=df.index, y=df['Z_Score'], name='Z-Score', line=dict(color='#1f77b4')), row=1, col=1)
    fig.add_hline(y=2.0, line_dash="dash", line_color="red", row=1, col=1, annotation_text="Short Spread Entry")
    fig.add_hline(y=-2.0, line_dash="dash", line_color="green", row=1, col=1, annotation_text="Long Spread Entry")
    fig.add_hline(y=0, line_color="black", row=1, col=1, annotation_text="Mean Reversion (Exit)")

    # 2. Equity Curve Chart
    fig.add_trace(go.Scatter(x=df.index, y=df['Cumulative_Return'], name='Cumulative Return', 
                             line=dict(color='#9467bd'), fill='tozeroy'), row=2, col=1)

    fig.update_layout(height=700, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("Data matrix not found. Please run the backtester script first.")