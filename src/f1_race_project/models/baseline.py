from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


@dataclass
class BaselineRacePredictor:
    feature_columns: list[str]
    target_column: str
    random_state: int = 42

    def build_pipeline(self) -> Pipeline:
        return Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("model", RandomForestClassifier(n_estimators=200, random_state=self.random_state)),
            ]
        )


def train_and_evaluate_classifier(data: pd.DataFrame, feature_columns: list[str], target_column: str) -> dict:
    """Train a baseline classifier and return evaluation artifacts."""
    model = BaselineRacePredictor(feature_columns=feature_columns, target_column=target_column)
    clean = data.dropna(subset=[target_column]).copy()

    if clean.empty:
        raise ValueError("Target column contains no usable rows for training.")

    X = clean[feature_columns]
    y = clean[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=model.random_state,
        stratify=y if y.nunique() > 1 else None,
    )

    pipeline = model.build_pipeline()
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    return {
        "pipeline": pipeline,
        "accuracy": accuracy_score(y_test, predictions),
        "report": classification_report(y_test, predictions, output_dict=True),
        "test_size": int(len(X_test)),
    }
