from __future__ import annotations

import pandas as pd

from f1_race_project.analytics.performance import compute_speed_per_lap, summarize_driver_performance


def test_compute_speed_per_lap_from_distance_and_time() -> None:
    df = pd.DataFrame(
        {
            "driver": ["VER", "VER"],
            "lap_number": [1, 2],
            "distance_km": [5.0, 5.0],
            "lap_time_seconds": [100.0, 95.0],
        }
    )

    result = compute_speed_per_lap(df)

    assert "avg_speed_kmh" in result.columns
    assert result["avg_speed_kmh"].iloc[0] == 180.0


def test_summarize_driver_performance_creates_consistency_score() -> None:
    df = pd.DataFrame(
        {
            "driver": ["VER", "VER", "LEC"],
            "lap_time_ms": [100000, 101000, 102000],
            "speed": [210.0, 215.0, 208.0],
        }
    )

    result = summarize_driver_performance(df)

    assert "consistency_score" in result.columns
    assert set(result["driver"]) == {"VER", "LEC"}
