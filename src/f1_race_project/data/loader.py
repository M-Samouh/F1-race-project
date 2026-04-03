from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def discover_csv_files(data_dir: str | Path) -> list[Path]:
    """Return all CSV files found recursively in a dataset directory."""
    root = Path(data_dir)
    if not root.exists():
        raise FileNotFoundError(f"Dataset directory not found: {root}")
    return sorted(root.rglob("*.csv"))


def load_dataset_tables(data_dir: str | Path, sample_rows: int | None = None) -> Dict[str, pd.DataFrame]:
    """Load each CSV file into a dictionary keyed by file stem."""
    tables: Dict[str, pd.DataFrame] = {}
    for csv_file in discover_csv_files(data_dir):
        key = csv_file.stem
        tables[key] = pd.read_csv(csv_file, nrows=sample_rows)
    return tables


def profile_table(df: pd.DataFrame) -> dict:
    """Build a lightweight profile of a dataframe for quick inspection."""
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "dtypes": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "missing_values": df.isna().sum().to_dict(),
    }
