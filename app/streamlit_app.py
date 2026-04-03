from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from f1_race_project.analytics import summarize_driver_performance
from f1_race_project.data import discover_csv_files
from f1_race_project.features import build_lap_features
from f1_race_project.visualization import create_driver_comparison_figure, create_lap_pace_figure

st.set_page_config(page_title="F1 Performance Dashboard", layout="wide")
st.title("F1 Race Performance Dashboard")
st.caption("Telemetry-inspired exploration of lap and driver performance")

base_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
user_dir = st.sidebar.text_input("Dataset directory", str(base_dir))

try:
    csv_files = discover_csv_files(user_dir)
except FileNotFoundError:
    csv_files = []

if not csv_files:
    st.warning("No CSV files found. Download the dataset first or point to the extracted data folder.")
    st.stop()

selected_file = st.sidebar.selectbox("Lap table", csv_files, format_func=lambda path: path.name)
row_limit = st.sidebar.slider("Rows to load", min_value=100, max_value=50000, value=5000, step=100)

lap_data = pd.read_csv(selected_file, nrows=row_limit)
lap_data = build_lap_features(lap_data)
summary = summarize_driver_performance(lap_data)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_driver_comparison_figure(summary), use_container_width=True)
with col2:
    st.plotly_chart(create_lap_pace_figure(lap_data), use_container_width=True)

st.subheader("Driver summary")
st.dataframe(summary, use_container_width=True)

st.subheader("Raw sample")
st.dataframe(lap_data.head(100), use_container_width=True)
