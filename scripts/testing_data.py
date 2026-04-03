from __future__ import annotations

import shutil
from pathlib import Path

import kagglehub


def main() -> None:
    downloaded_path = Path(kagglehub.dataset_download("alexjr2001/formula-1-dataset-race-data-and-telemetry"))
    destination = Path(__file__).resolve().parents[1] / "data" / "raw"
    destination.mkdir(parents=True, exist_ok=True)

    for item in downloaded_path.iterdir():
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)

    print(f"Dataset downloaded to cache: {downloaded_path}")
    print(f"Dataset copied to project folder: {destination}")


if __name__ == "__main__":
    main()
