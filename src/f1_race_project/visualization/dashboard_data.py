from __future__ import annotations

import pandas as pd
import plotly.express as px


def create_driver_comparison_figure(summary: pd.DataFrame):
    if summary.empty:
        return px.bar(title="No driver summary data available")

    y_column = "mean_lap_time_seconds" if "mean_lap_time_seconds" in summary.columns else summary.columns[1]
    x_column = summary.columns[0]
    return px.bar(summary, x=x_column, y=y_column, title="Driver performance comparison")


def create_lap_pace_figure(lap_data: pd.DataFrame):
    if lap_data.empty:
        return px.line(title="No lap data available")

    lap_col = "lap_number" if "lap_number" in lap_data.columns else "LapNumber"
    driver_col = "driver" if "driver" in lap_data.columns else "Driver"
    y_column = "lap_time_seconds" if "lap_time_seconds" in lap_data.columns else lap_data.columns[-1]
    return px.line(lap_data, x=lap_col, y=y_column, color=driver_col, title="Lap pace evolution")
