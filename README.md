# F1 Race Performance Project

A modular Python project for exploring Formula 1 race telemetry as if it were a live race feed.

## Goals
- Simulate race telemetry and lap events in pseudo real time.
- Build advanced visualizations to understand F1 performance dynamics.
- Compute performance metrics such as pace, consistency, lap speed, and delta trends.
- Train baseline machine learning models to estimate driver or team success.
- Study the impact of car setup proxies and driving style signals on outcomes.

## Audience
- F1 fans exploring race telemetry.
- Researchers in motorsport analytics.
- Developers building simulation, analytics, or visualization tools.

## Project Structure
- `data/raw/`: raw downloaded dataset files.
- `data/processed/`: engineered outputs and cached tables.
- `src/f1_race_project/data/`: ingestion, discovery, profiling, validation.
- `src/f1_race_project/simulation/`: pseudo real-time race event stream.
- `src/f1_race_project/features/`: feature engineering for laps and race context.
- `src/f1_race_project/analytics/`: statistics and performance metrics.
- `src/f1_race_project/models/`: baseline ML training and evaluation.
- `src/f1_race_project/visualization/`: reusable plotting helpers.
- `app/`: interactive dashboard entry points.
- `scripts/`: operational scripts for bootstrap and pipeline execution.
- `tests/`: lightweight regression tests.

## Quick Start
1. Create a Python 3.11+ virtual environment.
2. Install the project:
   - `pip install -e .`
3. Download the dataset:
   - `python scripts/testing_data.py`
4. Run the example pipeline:
   - `python scripts/run_pipeline.py --data-dir data/raw`
5. Start the dashboard:
   - `streamlit run app/streamlit_app.py`

## Initial Modules
- **Dataset loader**: finds CSV files, loads tables, profiles schemas.
- **Race simulator**: emits lap-level events ordered like a live feed.
- **Analytics layer**: driver pace, consistency, speed per lap, ranking snapshots.
- **Feature engineering**: transforms lap-level data into ML-ready features.
- **Baseline model**: trains a simple classifier on engineered data.
- **Visualization layer**: Plotly figures for driver comparisons and lap pace.

## Next Recommended Steps
- Add schema-specific adapters once the dataset column names are confirmed.
- Expand the simulator to sector-level and telemetry-level events.
- Introduce DuckDB for fast table exploration and joins.
- Add experiment tracking and stronger evaluation reports.
