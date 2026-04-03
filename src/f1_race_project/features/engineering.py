from __future__ import annotations

import pandas as pd


def build_lap_features(lap_data: pd.DataFrame) -> pd.DataFrame:
    """Create a first set of robust lap-level features from common racing columns."""
    df = lap_data.copy()

    if "lap_time_ms" in df.columns:
        df["lap_time_seconds"] = df["lap_time_ms"] / 1000.0
    elif "LapTimeSeconds" not in df.columns and "lap_time" in df.columns:
        df["lap_time_seconds"] = df["lap_time"]

    if "speed" in df.columns:
        df["speed_delta"] = df.groupby(df.get("driver", pd.Series(index=df.index))).speed.diff().fillna(0)

    if "rpm" in df.columns:
        df["rpm_normalized"] = df["rpm"] / df["rpm"].max()

    if "brake" in df.columns:
        df["heavy_braking"] = (df["brake"] > df["brake"].median()).astype(int)

    return df
