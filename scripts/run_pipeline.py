from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from f1_race_project.analytics import compute_speed_per_lap, summarize_driver_performance
from f1_race_project.data import discover_csv_files
from f1_race_project.features import build_lap_features


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a lightweight F1 data preview pipeline.")
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"), help="Directory containing raw CSV files.")
    parser.add_argument("--rows", type=int, default=10000, help="Number of rows to load from the selected CSV file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_files = discover_csv_files(args.data_dir)
    if not csv_files:
        raise FileNotFoundError(f"No CSV files were found in {args.data_dir}. Download the dataset first.")

    lap_data = pd.read_csv(csv_files[0], nrows=args.rows)
    feature_data = build_lap_features(lap_data)
    speed = compute_speed_per_lap(feature_data)
    summary = summarize_driver_performance(feature_data)

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    speed.to_csv(output_dir / "speed_per_lap_preview.csv", index=False)
    summary.to_csv(output_dir / "driver_summary_preview.csv", index=False)

    manifest = {
        "source_file": csv_files[0].name,
        "rows_loaded": int(len(lap_data)),
        "speed_preview_rows": int(len(speed)),
        "summary_rows": int(len(summary)),
    }
    (output_dir / "pipeline_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Pipeline preview completed.")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
