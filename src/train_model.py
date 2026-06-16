from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR.parent / "data" / "processed" / "cardio_model_ready.csv"
MODEL_DIR = PROJECT_DIR / "models"
REPORT_DIR = PROJECT_DIR / "reports"

TARGET = "target_cvd"
SPLIT = "split_hint"
RANDOM_STATE = 42


def evaluate(model: Any, x: pd.DataFrame, y: pd.Series) -> dict[str, Any]:
    predictions = model.predict(x)
    probabilities = model.predict_proba(x)[:, 1]

    return {
        "auc_roc": round(float(roc_auc_score(y, probabilities)), 4),
        "f1": round(float(f1_score(y, predictions)), 4),
        "recall_sensitivity": round(float(recall_score(y, predictions)), 4),
        "precision": round(float(precision_score(y, predictions)), 4),
        "confusion_matrix": confusion_matrix(y, predictions).tolist(),
    }


def load_splits() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, list[str]]:
    df = pd.read_csv(DATA_PATH)
    feature_columns = [column for column in df.columns if column not in [TARGET, SPLIT]]

    train_df = df[df[SPLIT].eq("train")]
    validation_df = df[df[SPLIT].eq("validation")]
    test_df = df[df[SPLIT].eq("test")]

    return (
        train_df[feature_columns],
        train_df[TARGET],
        validation_df[feature_columns],
        validation_df[TARGET],
        test_df[feature_columns],
        test_df[TARGET],
        feature_columns,
    )


def build_models() -> dict[str, Any]:
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=1000,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "xgboost": XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }


def write_markdown_report(results: dict[str, Any], best_model_name: str) -> None:
    lines = [
        "# Model Metrics",
        "",
        f"Best model by validation AUC-ROC: `{best_model_name}`",
        "",
        "| Model | Split | AUC-ROC | F1 | Recall/Sensitivity | Precision | Confusion Matrix [[TN, FP], [FN, TP]] |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    for model_name, split_results in results.items():
        for split_name, metrics in split_results.items():
            lines.append(
                "| "
                f"{model_name} | {split_name} | {metrics['auc_roc']} | "
                f"{metrics['f1']} | {metrics['recall_sensitivity']} | "
                f"{metrics['precision']} | `{metrics['confusion_matrix']}` |"
            )

    (REPORT_DIR / "model_metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    MODEL_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    print(f"Loading data from {DATA_PATH}")
    x_train, y_train, x_validation, y_validation, x_test, y_test, feature_columns = load_splits()

    print(f"Training rows: {len(x_train):,}")
    print(f"Validation rows: {len(x_validation):,}")
    print(f"Test rows: {len(x_test):,}")
    print(f"Feature columns: {len(feature_columns):,}")

    results: dict[str, Any] = {}
    models = build_models()

    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")
        model.fit(x_train, y_train)

        print(f"Evaluating {model_name}...")
        results[model_name] = {
            "validation": evaluate(model, x_validation, y_validation),
            "test": evaluate(model, x_test, y_test),
        }

        joblib.dump(model, MODEL_DIR / f"{model_name}.pkl")

    best_model_name = max(
        results,
        key=lambda name: results[name]["validation"]["auc_roc"],
    )

    with (MODEL_DIR / "feature_columns.json").open("w", encoding="utf-8") as file:
        json.dump(feature_columns, file, indent=2)

    with (REPORT_DIR / "model_metrics.json").open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    write_markdown_report(results, best_model_name)

    print("\nDone.")
    print(f"Best model by validation AUC-ROC: {best_model_name}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
