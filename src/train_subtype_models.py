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


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
FEATURES_PATH = ROOT_DIR / "data" / "processed" / "cardio_model_ready.csv"
TARGETS_PATH = ROOT_DIR / "data" / "processed" / "cardio_subtype_targets.csv"
MODEL_DIR = PROJECT_DIR / "models" / "subtypes"
REPORT_PATH = PROJECT_DIR / "reports" / "subtype_model_metrics.json"
REPORT_MD_PATH = PROJECT_DIR / "reports" / "subtype_model_metrics.md"

SPLIT = "split_hint"
TARGET_CVD = "target_cvd"
RANDOM_STATE = 42

SUBTYPE_TARGETS = {
    "target_myocardial_infarction": "Myocardial infarction",
    "target_heart_failure": "Heart failure",
    "target_stroke": "Stroke / cerebrovascular disease",
    "target_arrhythmia": "Cardiac arrhythmia",
    "target_hypertension": "Hypertensive disease",
    "target_coronary_artery_disease": "Coronary artery / ischemic heart disease",
}


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


def train_one(
    target: str,
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_validation: pd.DataFrame,
    y_validation: pd.Series,
    x_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[XGBClassifier, dict[str, Any]]:
    negatives = int((y_train == 0).sum())
    positives = int((y_train == 1).sum())
    scale_pos_weight = negatives / positives if positives else 1.0

    model = XGBClassifier(
        n_estimators=220,
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
    model.fit(x_train, y_train)

    return model, {
        "label": SUBTYPE_TARGETS[target],
        "train_positive_rows": positives,
        "train_negative_rows": negatives,
        "scale_pos_weight": round(float(scale_pos_weight), 4),
        "validation": evaluate(model, x_validation, y_validation),
        "test": evaluate(model, x_test, y_test),
    }


def write_markdown(results: dict[str, Any]) -> None:
    lines = [
        "# Subtype Model Metrics",
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
    features_df = pd.read_csv(FEATURES_PATH)
    targets_df = pd.read_csv(TARGETS_PATH, usecols=list(SUBTYPE_TARGETS))

    if len(features_df) != len(targets_df):
        raise ValueError("Feature and target row counts do not match.")

    feature_columns = [
        column for column in features_df.columns if column not in [SPLIT, TARGET_CVD]
    ]

    train_mask = features_df[SPLIT].eq("train")
    validation_mask = features_df[SPLIT].eq("validation")
    test_mask = features_df[SPLIT].eq("test")

    x_train = features_df.loc[train_mask, feature_columns]
    x_validation = features_df.loc[validation_mask, feature_columns]
    x_test = features_df.loc[test_mask, feature_columns]

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    results: dict[str, Any] = {}

    for target in SUBTYPE_TARGETS:
        print(f"Training {target}...")
        model, metrics = train_one(
            target=target,
            x_train=x_train,
            y_train=targets_df.loc[train_mask, target],
            x_validation=x_validation,
            y_validation=targets_df.loc[validation_mask, target],
            x_test=x_test,
            y_test=targets_df.loc[test_mask, target],
        )
        results[target] = metrics
        joblib.dump(model, MODEL_DIR / f"{target}.pkl")

    REPORT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_markdown(results)

    print(f"Wrote models to {MODEL_DIR}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {REPORT_MD_PATH}")


if __name__ == "__main__":
    main()
