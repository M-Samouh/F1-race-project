from __future__ import annotations

import numpy as np
import pandas as pd


def compute_speed_per_lap(lap_data: pd.DataFrame) -> pd.DataFrame:
    """Estimate average speed per lap when the input contains enough columns."""
    df = lap_data.copy()

    driver_col = "driver" if "driver" in df.columns else "Driver"
    lap_col = "lap_number" if "lap_number" in df.columns else "LapNumber"

    if {"distance_km", "lap_time_seconds"}.issubset(df.columns):
        df["avg_speed_kmh"] = np.where(df["lap_time_seconds"] > 0, df["distance_km"] / (df["lap_time_seconds"] / 3600.0), np.nan)
    elif {"distance_m", "lap_time_ms"}.issubset(df.columns):
        df["avg_speed_kmh"] = np.where(df["lap_time_ms"] > 0, (df["distance_m"] / 1000.0) / (df["lap_time_ms"] / 3_600_000.0), np.nan)
    elif "speed" in df.columns:
        return (
            df.groupby([driver_col, lap_col], dropna=False)["speed"]
            .mean()
            .reset_index(name="avg_speed_kmh")
        )
    else:
        return pd.DataFrame(columns=[driver_col, lap_col, "avg_speed_kmh"])

    return df[[driver_col, lap_col, "avg_speed_kmh"]]


def summarize_driver_performance(lap_data: pd.DataFrame) -> pd.DataFrame:
    """Produce high-level driver metrics for ranking and dashboard views."""
    df = lap_data.copy()
    driver_col = "driver" if "driver" in df.columns else "Driver"

    if "lap_time_seconds" not in df.columns and "lap_time_ms" in df.columns:
        df["lap_time_seconds"] = df["lap_time_ms"] / 1000.0

    aggregations = {}
    if "lap_time_seconds" in df.columns:
        aggregations.update(
            mean_lap_time_seconds=("lap_time_seconds", "mean"),
            best_lap_time_seconds=("lap_time_seconds", "min"),
            lap_time_std_seconds=("lap_time_seconds", "std"),
        )
    if "position" in df.columns:
        aggregations["mean_position"] = ("position", "mean")
    if "speed" in df.columns:
        aggregations["mean_speed"] = ("speed", "mean")
    if "rpm" in df.columns:
        aggregations["mean_rpm"] = ("rpm", "mean")

    if not aggregations:
        return pd.DataFrame({driver_col: sorted(df[driver_col].dropna().astype(str).unique())})

    summary = df.groupby(driver_col, dropna=False).agg(**aggregations).reset_index()
    if "lap_time_std_seconds" in summary.columns:
        summary["consistency_score"] = 1 / (1 + summary["lap_time_std_seconds"].fillna(0))
    return summary.sort_values(summary.columns[1], ascending=True, na_position="last")
