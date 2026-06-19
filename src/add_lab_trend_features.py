from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from build_time_aware_dataset import LAB_ITEMIDS, OBSERVATION_HOURS


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
ADMISSIONS_PATH = ROOT_DIR / "admissions.csv.gz"
LABEVENTS_PATH = ROOT_DIR / "labevents.csv.gz"
REPORT_PATH = PROJECT_DIR / "reports" / "lab_trend_features.md"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    admissions = pd.read_csv(ADMISSIONS_PATH, compression="infer", usecols=["hadm_id", "admittime"])
    admissions = admissions[admissions["hadm_id"].isin(set(df["hadm_id"]))].copy()
    admissions["hadm_id"] = admissions["hadm_id"].astype("int64")
    admissions["admittime"] = pd.to_datetime(admissions["admittime"], errors="coerce")
    admissions["window_end"] = admissions["admittime"] + pd.Timedelta(hours=OBSERVATION_HOURS)

    rows = []
    usecols = ["hadm_id", "itemid", "charttime", "valuenum"]
    for chunk in pd.read_csv(LABEVENTS_PATH, usecols=usecols, chunksize=1_000_000, compression="infer"):
        chunk = chunk[chunk["hadm_id"].notna()]
        chunk["hadm_id"] = chunk["hadm_id"].astype("int64")
        chunk = chunk[chunk["itemid"].isin(LAB_ITEMIDS)]
        if chunk.empty:
            continue
        chunk["charttime"] = pd.to_datetime(chunk["charttime"], errors="coerce")
        chunk["valuenum"] = pd.to_numeric(chunk["valuenum"], errors="coerce")
        chunk = chunk.merge(admissions, on="hadm_id", how="inner")
        chunk = chunk[
            chunk["charttime"].notna()
            & chunk["valuenum"].notna()
            & chunk["charttime"].between(chunk["admittime"], chunk["window_end"], inclusive="both")
        ]
        if chunk.empty:
            continue
        chunk["feature"] = chunk["itemid"].map(LAB_ITEMIDS)
        rows.append(chunk[["hadm_id", "feature", "charttime", "valuenum"]])

    if not rows:
        print("No lab trend rows found.")
        return

    labs = pd.concat(rows, ignore_index=True)
    labs = labs.sort_values(["hadm_id", "feature", "charttime"])
    grouped = labs.groupby(["hadm_id", "feature"])["valuenum"]
    trends = grouped.agg(["first", "last", "min", "max", "count"]).reset_index()
    trends["delta"] = trends["last"] - trends["first"]

    wide_frames = []
    for metric in ["first", "last", "min", "max", "delta"]:
        pivot = trends.pivot(index="hadm_id", columns="feature", values=metric)
        pivot.columns = [f"{column}_{metric}" for column in pivot.columns]
        wide_frames.append(pivot)
    trend_wide = pd.concat(wide_frames, axis=1).reset_index()

    new_columns = [column for column in trend_wide.columns if column != "hadm_id"]
    existing = [column for column in new_columns if column in df.columns]
    if existing:
        df = df.drop(columns=existing)
    df = df.merge(trend_wide, on="hadm_id", how="left")

    train_mask = df["split_hint"].eq("train")
    added_indicators = []
    for column in new_columns:
        indicator = f"{column}_missing"
        if indicator in df.columns:
            df = df.drop(columns=[indicator])
        df[indicator] = df[column].isna().astype("int8")
        added_indicators.append(indicator)
        median = df.loc[train_mask, column].median()
        if pd.isna(median):
            median = 0.0
        df[column] = df[column].fillna(float(median))

    df.to_csv(DATA_PATH, index=False)

    lines = [
        "# Lab Trend Features",
        "",
        f"Dataset: `{DATA_PATH}`",
        f"Source: `{LABEVENTS_PATH}`",
        f"Observation window: first {OBSERVATION_HOURS} hours after admission.",
        "",
        f"Added trend feature columns: {len(new_columns)}",
        f"Added missing indicator columns: {len(added_indicators)}",
        "",
        "Trend metrics: first, last, min, max, delta.",
        "",
        "## Columns",
        *[f"- `{column}`" for column in new_columns],
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    feature_summary_path = PROJECT_DIR / "reports" / "time_aware_feature_summary.json"
    if feature_summary_path.exists():
        summary = json.loads(feature_summary_path.read_text(encoding="utf-8"))
        summary["rows"] = int(len(df))
        summary["columns"] = list(df.columns)
        summary["lab_trend_feature_count"] = len(new_columns)
        summary["lab_trend_missing_indicator_count"] = len(added_indicators)
        feature_summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote {DATA_PATH}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Added {len(new_columns)} lab trend columns and {len(added_indicators)} missing indicators.")


if __name__ == "__main__":
    main()
