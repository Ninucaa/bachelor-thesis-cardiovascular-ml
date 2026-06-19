from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

from diagnosis_targets import EXPANDED_DIAGNOSIS_TARGETS


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
MODEL_DIR = PROJECT_DIR / "models" / "time_aware"
FEATURES_PATH = MODEL_DIR / "feature_columns.json"
OUTPUT_PATH = MODEL_DIR / "diagnosis_thresholds.json"
REPORT_PATH = PROJECT_DIR / "reports" / "diagnosis_thresholds.md"

SPLIT = "split_hint"
TARGETS = {
    target: config["label_ge"]
    for target, config in EXPANDED_DIAGNOSIS_TARGETS.items()
}
MIN_SUBTYPE_PRECISION = 0.30


def metrics_at(y_true: pd.Series, probabilities: np.ndarray, threshold: float) -> dict[str, Any]:
    predictions = (probabilities >= threshold).astype("int8")
    return {
        "threshold": round(float(threshold), 4),
        "f1": round(float(f1_score(y_true, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, predictions, zero_division=0)), 4),
        "precision": round(float(precision_score(y_true, predictions, zero_division=0)), 4),
        "predicted_positive": int(predictions.sum()),
        "confusion_matrix": confusion_matrix(y_true, predictions).tolist(),
    }


def best_threshold(y_true: pd.Series, probabilities: np.ndarray) -> dict[str, Any]:
    candidates = np.unique(np.quantile(probabilities, np.linspace(0.02, 0.995, 220)))
    candidates = np.unique(np.concatenate([candidates, np.linspace(0.05, 0.995, 190)]))
    evaluated = [metrics_at(y_true, probabilities, threshold) for threshold in candidates]
    precision_eligible = [
        item
        for item in evaluated
        if item["precision"] >= MIN_SUBTYPE_PRECISION and item["predicted_positive"] >= 10
    ]
    if precision_eligible:
        best = max(
            precision_eligible,
            key=lambda item: (item["f1"], item["recall"], item["precision"]),
        )
        best["selection_rule"] = f"max_f1_with_precision_at_least_{MIN_SUBTYPE_PRECISION:.2f}"
        return best
    best = max(
        evaluated,
        key=lambda item: (item["precision"], item["f1"], item["recall"]),
    )
    best["selection_rule"] = f"fallback_max_precision_below_{MIN_SUBTYPE_PRECISION:.2f}"
    return best


def confidence_level(probability: float, threshold: float) -> str:
    if probability >= max(0.75, threshold * 1.5):
        return "high"
    if probability >= threshold:
        return "diagnostic_signal"
    if probability >= threshold * 0.75:
        return "borderline"
    return "low"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    feature_columns = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))

    validation = df[df[SPLIT].eq("validation")]
    test = df[df[SPLIT].eq("test")]
    x_validation = validation[feature_columns]
    x_test = test[feature_columns]

    thresholds: dict[str, Any] = {}
    lines = [
        "# Diagnosis Thresholds",
        "",
        (
            "Thresholds were selected on the validation split using a precision-oriented rule: "
            f"maximize F1 among thresholds with validation precision >= {MIN_SUBTYPE_PRECISION:.2f}. "
            "If a subtype cannot reach that precision with enough positive predictions, the fallback is maximum precision."
        ),
        "",
        "| Target | Label | Threshold | Rule | Validation F1 | Validation Recall | Validation Precision | Test F1 | Test Recall | Test Precision |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]

    for target, label in TARGETS.items():
        model = joblib.load(MODEL_DIR / f"{target}.pkl")
        validation_probabilities = model.predict_proba(x_validation)[:, 1]
        test_probabilities = model.predict_proba(x_test)[:, 1]
        validation_metrics = best_threshold(validation[target], validation_probabilities)
        test_metrics = metrics_at(test[target], test_probabilities, validation_metrics["threshold"])

        thresholds[target] = {
            "label": label,
            "threshold": validation_metrics["threshold"],
            "selection_rule": validation_metrics.get("selection_rule"),
            "min_precision_target": MIN_SUBTYPE_PRECISION,
            "validation": validation_metrics,
            "test": test_metrics,
            "confidence_rule": {
                "high": "probability >= max(0.75, threshold * 1.5)",
                "diagnostic_signal": "probability >= threshold",
                "borderline": "probability >= threshold * 0.75",
                "low": "probability < threshold * 0.75",
            },
        }
        lines.append(
            f"| `{target}` | {label} | {validation_metrics['threshold']} | {validation_metrics.get('selection_rule', '')} | "
            f"{validation_metrics['f1']} | {validation_metrics['recall']} | {validation_metrics['precision']} | "
            f"{test_metrics['f1']} | {test_metrics['recall']} | {test_metrics['precision']} |"
        )

    OUTPUT_PATH.write_text(json.dumps(thresholds, indent=2, ensure_ascii=False), encoding="utf-8")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
