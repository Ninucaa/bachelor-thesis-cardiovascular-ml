from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from xgboost import XGBClassifier

from diagnosis_targets import EXPANDED_DIAGNOSIS_TARGETS


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
MODEL_DIR = PROJECT_DIR / "models" / "time_aware"
REPORT_PATH = PROJECT_DIR / "reports" / "time_aware_model_metrics.json"
REPORT_MD_PATH = PROJECT_DIR / "reports" / "time_aware_model_metrics.md"

SPLIT = "split_hint"
RANDOM_STATE = 42

TARGETS = {
    "target_cvd": "Any cardiovascular diagnosis",
    **{
        target: config["label_en"]
        for target, config in EXPANDED_DIAGNOSIS_TARGETS.items()
    },
}

EXCLUDED_FEATURE_COLUMNS = {"subject_id", "hadm_id", "hospital_expire_flag"}


def evaluate(model: Any, x: pd.DataFrame, y: pd.Series) -> dict[str, Any]:
    probabilities = model.predict_proba(x)[:, 1]
    predictions = (probabilities >= 0.5).astype("int8")

    return {
        "auc_roc": round(float(roc_auc_score(y, probabilities)), 4),
        "average_precision": round(float(average_precision_score(y, probabilities)), 4),
        "f1": round(float(f1_score(y, predictions, zero_division=0)), 4),
        "recall_sensitivity": round(float(recall_score(y, predictions, zero_division=0)), 4),
        "precision": round(float(precision_score(y, predictions, zero_division=0)), 4),
        "positive_rate": round(float(y.mean()), 4),
        "confusion_matrix": confusion_matrix(y, predictions).tolist(),
    }


def build_model(y_train: pd.Series) -> XGBClassifier:
    negatives = int((y_train == 0).sum())
    positives = int((y_train == 1).sum())
    scale_pos_weight = negatives / positives if positives else 1.0

    return XGBClassifier(
        n_estimators=260,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="binary:logistic",
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


def write_markdown(results: dict[str, Any]) -> None:
    lines = [
        "# Time-Aware Model Metrics",
        "",
        f"Training data: `{DATA_PATH}`",
        "",
        "| Target | Label | Split | AUC-ROC | Avg Precision | F1 | Recall | Precision | Positive Rate |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for target, result in results.items():
        for split_name in ["validation", "test"]:
            metrics = result[split_name]
            lines.append(
                f"| `{target}` | {result['label']} | {split_name} | "
                f"{metrics['auc_roc']} | {metrics['average_precision']} | "
                f"{metrics['f1']} | {metrics['recall_sensitivity']} | "
                f"{metrics['precision']} | {metrics['positive_rate']} |"
            )

    REPORT_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading data from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    target_columns = set(TARGETS)
    feature_columns = [
        column
        for column in df.columns
        if column not in EXCLUDED_FEATURE_COLUMNS
        and column != SPLIT
        and column not in target_columns
        and not column.startswith("target_")
    ]

    train_mask = df[SPLIT].eq("train")
    validation_mask = df[SPLIT].eq("validation")
    test_mask = df[SPLIT].eq("test")

    x_train = df.loc[train_mask, feature_columns]
    x_validation = df.loc[validation_mask, feature_columns]
    x_test = df.loc[test_mask, feature_columns]

    print(f"Training rows: {len(x_train):,}")
    print(f"Validation rows: {len(x_validation):,}")
    print(f"Test rows: {len(x_test):,}")
    print(f"Feature columns: {len(feature_columns):,}")

    results: dict[str, Any] = {}
    for target, label in TARGETS.items():
        print(f"\nTraining {target}...")
        y_train = df.loc[train_mask, target]
        model = build_model(y_train)
        model.fit(x_train, y_train)

        results[target] = {
            "label": label,
            "train_positive_rows": int((y_train == 1).sum()),
            "train_negative_rows": int((y_train == 0).sum()),
            "validation": evaluate(model, x_validation, df.loc[validation_mask, target]),
            "test": evaluate(model, x_test, df.loc[test_mask, target]),
        }
        joblib.dump(model, MODEL_DIR / f"{target}.pkl")

    with (MODEL_DIR / "feature_columns.json").open("w", encoding="utf-8") as file:
        json.dump(feature_columns, file, indent=2)
    REPORT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_markdown(results)

    print(f"\nWrote models to {MODEL_DIR}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {REPORT_MD_PATH}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
