from __future__ import annotations

from pathlib import Path

import pandas as pd

from diagnosis_targets import EXPANDED_DIAGNOSIS_TARGETS
from build_time_aware_dataset import normalize_icd, prefix_mask


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
DIAGNOSES_PATH = ROOT_DIR / "diagnoses_icd.csv.gz"
REPORT_PATH = PROJECT_DIR / "reports" / "synced_diagnosis_targets.md"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    diagnoses = pd.read_csv(DIAGNOSES_PATH, compression="infer", usecols=["hadm_id", "icd_code", "icd_version"])
    diagnoses = diagnoses[diagnoses["hadm_id"].isin(set(df["hadm_id"]))].copy()
    diagnoses["icd_code"] = diagnoses["icd_code"].map(normalize_icd)

    lines = [
        "# Synced Diagnosis Targets",
        "",
        f"Dataset: `{DATA_PATH}`",
        f"Diagnoses source: `{DIAGNOSES_PATH}`",
        "",
        "| Target | Label | Positive rows | Positive rate |",
        "|---|---|---:|---:|",
    ]

    for target, config in EXPANDED_DIAGNOSIS_TARGETS.items():
        target_mask = prefix_mask(diagnoses["icd_code"], diagnoses["icd_version"], config)
        positive_hadm_ids = set(diagnoses.loc[target_mask, "hadm_id"].drop_duplicates())
        df[target] = df["hadm_id"].isin(positive_hadm_ids).astype("int8")
        lines.append(
            f"| `{target}` | {config['label_ge']} | {int(df[target].sum())} | {float(df[target].mean()):.4f} |"
        )

    target_columns = list(EXPANDED_DIAGNOSIS_TARGETS)
    df["target_cvd"] = df[target_columns].max(axis=1).astype("int8")
    lines.append("")
    lines.append(f"`target_cvd` positive rows after sync: {int(df['target_cvd'].sum())}")
    lines.append(f"`target_cvd` positive rate after sync: {float(df['target_cvd'].mean()):.4f}")

    df.to_csv(DATA_PATH, index=False)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {DATA_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
