from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from xgboost import XGBClassifier

from build_clinical_group_thresholds import best_threshold
from train_clinical_group_models import evaluate, write_markdown
from diagnosis_targets import CLINICAL_GROUP_TARGETS, add_clinical_group_targets


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
MODEL_DIR = PROJECT_DIR / "models" / "time_aware"
FEATURES_PATH = MODEL_DIR / "feature_columns.json"
REPORT_PATH = PROJECT_DIR / "reports" / "clinical_group_model_metrics.json"
TUNING_REPORT_PATH = PROJECT_DIR / "reports" / "clinical_group_tuning_report.json"
TUNING_REPORT_MD_PATH = PROJECT_DIR / "reports" / "clinical_group_tuning_report.md"

SPLIT = "split_hint"
RANDOM_STATE = 42

PARAMETER_SETS = [
    {
        "name": "baseline_balanced",
        "n_estimators": 260,
        "max_depth": 4,
        "learning_rate": 0.05,
        "min_child_weight": 1,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
        "reg_lambda": 1.0,
        "gamma": 0.0,
        "scale_pos_weight_multiplier": 1.0,
    },
    {
        "name": "regularized_precision",
        "n_estimators": 360,
        "max_depth": 3,
        "learning_rate": 0.04,
        "min_child_weight": 8,
        "subsample": 0.90,
        "colsample_bytree": 0.90,
        "reg_lambda": 3.0,
        "gamma": 0.5,
        "scale_pos_weight_multiplier": 0.75,
    },
    {
        "name": "recall_balanced",
        "n_estimators": 320,
        "max_depth": 4,
        "learning_rate": 0.04,
        "min_child_weight": 3,
        "subsample": 0.90,
        "colsample_bytree": 0.80,
        "reg_lambda": 1.5,
        "gamma": 0.0,
        "scale_pos_weight_multiplier": 1.20,
    },
    {
        "name": "deeper_regularized",
        "n_estimators": 300,
        "max_depth": 5,
        "learning_rate": 0.035,
        "min_child_weight": 6,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
        "reg_lambda": 2.5,
        "gamma": 0.2,
        "scale_pos_weight_multiplier": 0.90,
    },
]

TUNING_TARGETS = set(CLINICAL_GROUP_TARGETS)


def build_model(y_train: pd.Series, params: dict[str, Any]) -> XGBClassifier:
    negatives = int((y_train == 0).sum())
    positives = int((y_train == 1).sum())
    base_weight = negatives / positives if positives else 1.0
    scale_pos_weight = base_weight * params["scale_pos_weight_multiplier"]

    return XGBClassifier(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        learning_rate=params["learning_rate"],
        min_child_weight=params["min_child_weight"],
        subsample=params["subsample"],
        colsample_bytree=params["colsample_bytree"],
        reg_lambda=params["reg_lambda"],
        gamma=params["gamma"],
        objective="binary:logistic",
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        tree_method="hist",
    )


def selection_metrics(y_true: pd.Series, probabilities) -> dict[str, Any]:
    default_predictions = (probabilities >= 0.5).astype("int8")
    supportive = best_threshold(y_true, probabilities, 0.80)
    high_precision = best_threshold(y_true, probabilities, 0.90)
    return {
        "auc_roc": round(float(roc_auc_score(y_true, probabilities)), 4),
        "average_precision": round(float(average_precision_score(y_true, probabilities)), 4),
        "f1_at_0_5": round(float(f1_score(y_true, default_predictions, zero_division=0)), 4),
        "recall_at_0_5": round(float(recall_score(y_true, default_predictions, zero_division=0)), 4),
        "precision_at_0_5": round(float(precision_score(y_true, default_predictions, zero_division=0)), 4),
        "supportive": supportive,
        "high_precision": high_precision,
    }


def score(metrics: dict[str, Any]) -> float:
    supportive = metrics["supportive"]
    high_precision = metrics["high_precision"]
    return (
        metrics["average_precision"]
        + 0.30 * supportive["f1"]
        + 0.15 * high_precision["f1"]
        + 0.05 * metrics["auc_roc"]
    )


def write_tuning_markdown(tuning: dict[str, Any]) -> None:
    lines = [
        "# Clinical Group Tuning Report",
        "",
        "Model selection score = average precision + 0.30 * supportive F1 + 0.15 * high-precision F1 + 0.05 * AUC.",
        "",
        "| Target | Selected config | Validation AUC | Validation AP | Supportive F1 | High Precision F1 | Score |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for target, result in tuning.items():
        metrics = result["selected_validation_metrics"]
        lines.append(
            f"| `{target}` | {result['selected_config']['name']} | {metrics['auc_roc']} | "
            f"{metrics['average_precision']} | {metrics['supportive']['f1']} | "
            f"{metrics['high_precision']['f1']} | {result['selection_score']:.4f} |"
        )
    TUNING_REPORT_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading data from {DATA_PATH}")
    df = add_clinical_group_targets(pd.read_csv(DATA_PATH))
    feature_columns = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))

    train_mask = df[SPLIT].eq("train")
    validation_mask = df[SPLIT].eq("validation")
    test_mask = df[SPLIT].eq("test")

    x_train = df.loc[train_mask, feature_columns]
    x_validation = df.loc[validation_mask, feature_columns]
    x_test = df.loc[test_mask, feature_columns]

    results: dict[str, Any] = {}
    if REPORT_PATH.exists():
        results.update(json.loads(REPORT_PATH.read_text(encoding="utf-8")))
    tuning_report: dict[str, Any] = {}
    if TUNING_REPORT_PATH.exists():
        tuning_report.update(json.loads(TUNING_REPORT_PATH.read_text(encoding="utf-8")))

    for target, config in CLINICAL_GROUP_TARGETS.items():
        if target not in TUNING_TARGETS:
            continue
        print(f"\nTuning {target}...")
        y_train = df.loc[train_mask, target]
        y_validation = df.loc[validation_mask, target]

        best: tuple[float, dict[str, Any], XGBClassifier, dict[str, Any]] | None = None
        candidates = []
        for params in PARAMETER_SETS:
            print(f"  trying {params['name']}...")
            model = build_model(y_train, params)
            model.fit(x_train, y_train)
            probabilities = model.predict_proba(x_validation)[:, 1]
            metrics = selection_metrics(y_validation, probabilities)
            candidate_score = score(metrics)
            candidates.append(
                {
                    "config": params,
                    "validation_metrics": metrics,
                    "selection_score": round(candidate_score, 6),
                }
            )
            if best is None or candidate_score > best[0]:
                best = (candidate_score, params, model, metrics)

        assert best is not None
        best_score, best_params, best_model, best_metrics = best
        print(f"  selected {best_params['name']} score={best_score:.4f}")

        results[target] = {
            "label": config["label_ge"],
            "members": list(config["members"]),
            "selected_config": best_params,
            "train_positive_rows": int((y_train == 1).sum()),
            "train_negative_rows": int((y_train == 0).sum()),
            "validation": evaluate(best_model, x_validation, df.loc[validation_mask, target]),
            "test": evaluate(best_model, x_test, df.loc[test_mask, target]),
        }
        tuning_report[target] = {
            "label": config["label_ge"],
            "selected_config": best_params,
            "selected_validation_metrics": best_metrics,
            "selection_score": round(best_score, 6),
            "candidates": candidates,
        }
        joblib.dump(best_model, MODEL_DIR / f"{target}.pkl")
        REPORT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        TUNING_REPORT_PATH.write_text(json.dumps(tuning_report, indent=2, ensure_ascii=False), encoding="utf-8")
        write_markdown(results)
        write_tuning_markdown(tuning_report)

    print(f"\nWrote tuned group models to {MODEL_DIR}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {TUNING_REPORT_PATH}")
    print(f"Wrote {TUNING_REPORT_MD_PATH}")


if __name__ == "__main__":
    main()
