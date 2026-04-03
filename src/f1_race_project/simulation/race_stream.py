from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import pandas as pd


@dataclass(slots=True)
class RaceEvent:
    timestamp: int
    driver: str
    lap_number: int
    event_type: str
    payload: dict


class RaceStreamSimulator:
    """Emit lap-level events from a dataframe in pseudo real time order."""

    def __init__(self, lap_data: pd.DataFrame, timestamp_column: str | None = None) -> None:
        self.lap_data = lap_data.copy()
        self.timestamp_column = timestamp_column or self._infer_timestamp_column()

    def _infer_timestamp_column(self) -> str:
        candidates = ["timestamp", "lap_start_time_ms", "session_time_ms", "date"]
        for candidate in candidates:
            if candidate in self.lap_data.columns:
                return candidate
        self.lap_data = self.lap_data.reset_index().rename(columns={"index": "event_order"})
        return "event_order"

    def stream(self) -> Iterator[RaceEvent]:
        ordered = self.lap_data.sort_values(self.timestamp_column)
        for _, row in ordered.iterrows():
            driver = str(row.get("driver", row.get("Driver", "unknown")))
            lap_number = int(row.get("lap_number", row.get("LapNumber", 0)))
            event_type = "lap_completed"
            payload = row.to_dict()
            yield RaceEvent(
                timestamp=int(row[self.timestamp_column]) if pd.notna(row[self.timestamp_column]) else 0,
                driver=driver,
                lap_number=lap_number,
                event_type=event_type,
                payload=payload,
            )
