import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Quant Pair Analytics",
    layout="wide"
)

# Title
st.title("Market Pair Analytics – Prototype Dashboard")
st.caption("Offline quant analytics prototype | Focus on analytics flow and visualization")

# Sidebar controls
st.sidebar.header("Controls")
window = st.sidebar.slider("Rolling Window", 5, 50, 20)
show_spread = st.sidebar.checkbox("Show Spread", True)
show_zscore = st.sidebar.checkbox("Show Z-Score", True)

# Load data
df = pd.read_csv("data.csv")

# Basic assumption: two price columns
price_cols = df.columns[1:3]

# Calculations
df["spread"] = df[price_cols[0]] - df[price_cols[1]]
df["zscore"] = (df["spread"] - df["spread"].rolling(window).mean()) / df["spread"].rolling(window).std()

df["rolling_mean"] = df["spread"].rolling(window).mean()
df["rolling_std"] = df["spread"].rolling(window).std()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Trends")
    st.line_chart(df[price_cols])

with col2:
    if show_spread:
        st.subheader("Spread & Rolling Mean")
        st.line_chart(df[["spread", "rolling_mean"]])

if show_zscore:
    st.subheader("Z-Score")
    st.line_chart(df["zscore"])

# Summary stats
st.subheader("Summary Statistics")

stats = {
    "Metric": ["Mean Spread", "Std Spread", "Max Z-Score", "Min Z-Score"],
    "Value": [
        round(df["spread"].mean(), 4),
        round(df["spread"].std(), 4),
        round(df["zscore"].max(), 4),
        round(df["zscore"].min(), 4)
    ]
}

st.table(pd.DataFrame(stats))

st.caption("Note: This is a simplified prototype designed for demonstrating analytics structure and dashboard interactivity.")
