from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

from diagnosis_targets import CLINICAL_GROUP_TARGETS, add_clinical_group_targets


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
MODEL_DIR = PROJECT_DIR / "models" / "time_aware"
FEATURES_PATH = MODEL_DIR / "feature_columns.json"
OUTPUT_PATH = MODEL_DIR / "clinical_group_thresholds.json"
REPORT_PATH = PROJECT_DIR / "reports" / "clinical_group_thresholds.md"

SPLIT = "split_hint"
SUPPORTIVE_PRECISION = 0.80
HIGH_PRECISION = 0.72


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


def best_threshold(y_true: pd.Series, probabilities: np.ndarray, min_precision: float) -> dict[str, Any]:
    y = y_true.to_numpy(dtype="int8")
    order = probabilities.argsort()[::-1]
    sorted_probabilities = probabilities[order]
    sorted_y = y[order]
    true_positives = sorted_y.cumsum()
    predicted_positive = pd.Series(range(1, len(sorted_y) + 1)).to_numpy()
    total_positive = int(sorted_y.sum())
    precision_values = true_positives / predicted_positive
    recall_values = true_positives / total_positive if total_positive else true_positives * 0
    f1_values = 2 * precision_values * recall_values / (precision_values + recall_values + 1e-12)

    evaluated = []
    last_probability = None
    for index, threshold in enumerate(sorted_probabilities):
        if last_probability == threshold:
            continue
        last_probability = threshold
        evaluated.append(
            {
                "threshold": round(float(threshold), 4),
                "f1": round(float(f1_values[index]), 4),
                "recall": round(float(recall_values[index]), 4),
                "precision": round(float(precision_values[index]), 4),
                "predicted_positive": int(predicted_positive[index]),
            }
        )

    precision_eligible = [item for item in evaluated if item["precision"] >= min_precision and item["predicted_positive"] >= 10]
    if precision_eligible:
        best_candidate = max(precision_eligible, key=lambda item: (item["f1"], item["recall"], item["precision"]))
        best = metrics_at(y_true, probabilities, best_candidate["threshold"])
        best["selection_rule"] = f"max_f1_with_precision_at_least_{min_precision:.2f}"
        return best
    best_candidate = max(evaluated, key=lambda item: (item["precision"], item["f1"], item["recall"]))
    best = metrics_at(y_true, probabilities, best_candidate["threshold"])
    best["selection_rule"] = f"fallback_max_precision_below_{min_precision:.2f}"
    return best


def main() -> None:
    df = add_clinical_group_targets(pd.read_csv(DATA_PATH))
    feature_columns = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))

    validation = df[df[SPLIT].eq("validation")]
    test = df[df[SPLIT].eq("test")]
    x_validation = validation[feature_columns]
    x_test = test[feature_columns]

    thresholds: dict[str, Any] = {}
    lines = [
        "# Clinical Group Thresholds",
        "",
        (
            "Two threshold tiers were selected on the validation split. The supportive tier targets "
            f"precision >= {SUPPORTIVE_PRECISION:.2f}. The high-precision tier targets "
            f"precision >= {HIGH_PRECISION:.2f}. In the frontend this tier is used as a balanced main "
            "diagnostic direction: precision remains constrained, while recall is allowed to improve. "
            "Supportive thresholds are kept as secondary signals."
        ),
        "",
        "| Target | Label | Tier | Threshold | Rule | Validation F1 | Validation Recall | Validation Precision | Test F1 | Test Recall | Test Precision |",
        "|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]

    for target, config in CLINICAL_GROUP_TARGETS.items():
        label = config["label_ge"]
        model = joblib.load(MODEL_DIR / f"{target}.pkl")
        validation_probabilities = model.predict_proba(x_validation)[:, 1]
        test_probabilities = model.predict_proba(x_test)[:, 1]
        supportive_validation = best_threshold(validation[target], validation_probabilities, SUPPORTIVE_PRECISION)
        supportive_test = metrics_at(test[target], test_probabilities, supportive_validation["threshold"])
        high_validation = best_threshold(validation[target], validation_probabilities, HIGH_PRECISION)
        high_test = metrics_at(test[target], test_probabilities, high_validation["threshold"])

        thresholds[target] = {
            "label": label,
            "members": list(config["members"]),
            "threshold": supportive_validation["threshold"],
            "selection_rule": supportive_validation.get("selection_rule"),
            "min_precision_target": SUPPORTIVE_PRECISION,
            "validation": supportive_validation,
            "test": supportive_test,
            "supportive": {
                "threshold": supportive_validation["threshold"],
                "selection_rule": supportive_validation.get("selection_rule"),
                "min_precision_target": SUPPORTIVE_PRECISION,
                "validation": supportive_validation,
                "test": supportive_test,
            },
            "high_precision": {
                "threshold": high_validation["threshold"],
                "selection_rule": high_validation.get("selection_rule"),
                "min_precision_target": HIGH_PRECISION,
                "validation": high_validation,
                "test": high_test,
            },
            "confidence_rule": {
                "high": "probability >= max(0.75, threshold * 1.5)",
                "diagnostic_signal": "probability >= threshold",
                "borderline": "probability >= threshold * 0.75",
                "low": "probability < threshold * 0.75",
            },
        }
        lines.append(
            f"| `{target}` | {label} | supportive | {supportive_validation['threshold']} | {supportive_validation.get('selection_rule', '')} | "
            f"{supportive_validation['f1']} | {supportive_validation['recall']} | {supportive_validation['precision']} | "
            f"{supportive_test['f1']} | {supportive_test['recall']} | {supportive_test['precision']} |"
        )
        lines.append(
            f"| `{target}` | {label} | high_precision | {high_validation['threshold']} | {high_validation.get('selection_rule', '')} | "
            f"{high_validation['f1']} | {high_validation['recall']} | {high_validation['precision']} | "
            f"{high_test['f1']} | {high_test['recall']} | {high_test['precision']} |"
        )

    OUTPUT_PATH.write_text(json.dumps(thresholds, indent=2, ensure_ascii=False), encoding="utf-8")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
