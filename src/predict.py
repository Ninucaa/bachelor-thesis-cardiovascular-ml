from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_DIR.parent / "data" / "processed" / "cardio_model_ready.csv"
MODEL_PATH = PROJECT_DIR / "models" / "xgboost.pkl"
FEATURES_PATH = PROJECT_DIR / "models" / "feature_columns.json"
TARGET = "target_cvd"
SPLIT = "split_hint"


def load_model_and_features() -> tuple[Any, list[str]]:
    model = joblib.load(MODEL_PATH)
    features = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))
    return model, features


def risk_level(probability: float) -> str:
    if probability >= 0.75:
        return "high"
    if probability >= 0.40:
        return "medium"
    return "low"


def load_patient_from_csv(
    csv_path: Path, row_index: int, split_filter: str | None, features: list[str]
) -> tuple[pd.DataFrame, dict[str, Any]]:
    df = pd.read_csv(csv_path)
    if split_filter:
        if SPLIT not in df.columns:
            raise ValueError(f"Cannot use split filter because `{SPLIT}` is not in the CSV.")
        df = df[df[SPLIT].eq(split_filter)]

    if row_index < 0 or row_index >= len(df):
        raise IndexError(f"row_index must be between 0 and {len(df) - 1}")

    row = df.iloc[[row_index]].copy()
    metadata = {
        "row_index": row_index,
        "original_csv_index": int(row.index[0]),
        "split": row[SPLIT].iloc[0] if SPLIT in row.columns else None,
        "actual_target": int(row[TARGET].iloc[0]) if TARGET in row.columns else None,
    }
    return row[features], metadata


def load_patient_from_json(json_path: Path, features: list[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    missing = [feature for feature in features if feature not in payload]
    if missing:
        raise ValueError(
            "Input JSON is missing model-ready feature columns. "
            f"First missing columns: {missing[:10]}"
        )
    return pd.DataFrame([{feature: payload[feature] for feature in features}]), {
        "source": str(json_path)
    }


def explain_prediction(model: Any, patient: pd.DataFrame, top_n: int) -> list[dict[str, Any]]:
    try:
        import shap
    except ImportError:
        return []

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(patient)

    if isinstance(shap_values, list):
        values = shap_values[1][0]
    else:
        values = shap_values[0]

    rows = []
    for feature, value, contribution in zip(patient.columns, patient.iloc[0], values):
        rows.append(
            {
                "feature": feature,
                "value": float(value),
                "shap_value": float(contribution),
                "direction": "increases_risk" if contribution > 0 else "decreases_risk",
            }
        )

    rows.sort(key=lambda item: abs(item["shap_value"]), reverse=True)
    return rows[:top_n]


def predict(patient: pd.DataFrame, metadata: dict[str, Any], top_n: int) -> dict[str, Any]:
    model, _features = load_model_and_features()
    probability = float(model.predict_proba(patient)[:, 1][0])
    predicted_class = int(probability >= 0.5)

    return {
        "metadata": metadata,
        "risk_probability": round(probability, 4),
        "predicted_class": predicted_class,
        "risk_level": risk_level(probability),
        "top_factors": explain_prediction(model, patient, top_n),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one CVD risk prediction.")
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Model-ready CSV to read a row from.",
    )
    input_group.add_argument(
        "--json",
        type=Path,
        help="JSON file containing all model-ready feature columns.",
    )
    parser.add_argument("--row-index", type=int, default=0, help="Zero-based row index for --csv.")
    parser.add_argument(
        "--split-filter",
        choices=["train", "validation", "test"],
        default="test",
        help="Use only this split when selecting a CSV row. Use no filter by passing an empty value.",
    )
    parser.add_argument("--top-n", type=int, default=8, help="Number of SHAP factors to show.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _model, features = load_model_and_features()

    if args.json:
        patient, metadata = load_patient_from_json(args.json, features)
    else:
        split_filter = args.split_filter or None
        patient, metadata = load_patient_from_csv(args.csv, args.row_index, split_filter, features)

    result = predict(patient, metadata, args.top_n)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
