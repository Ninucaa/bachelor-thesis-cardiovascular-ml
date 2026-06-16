from __future__ import annotations

from pathlib import Path

import pandas as pd

from diagnosis_targets import EXPANDED_DIAGNOSIS_TARGETS


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
DIAGNOSES_PATH = ROOT_DIR / "diagnoses_icd.csv.gz"
REPORT_PATH = PROJECT_DIR / "reports" / "expanded_diagnosis_targets.md"


def normalize_icd(code: object) -> str:
    return str(code).upper().replace(".", "").strip()


def prefix_mask(codes: pd.Series, versions: pd.Series, config: dict[str, object]) -> pd.Series:
    mask = pd.Series(False, index=codes.index)
    icd9 = tuple(config.get("icd9", ()))
    icd10 = tuple(config.get("icd10", ()))
    if icd9:
        mask = mask | (versions.eq(9) & codes.str.startswith(icd9, na=False))
    if icd10:
        mask = mask | (versions.eq(10) & codes.str.startswith(icd10, na=False))
    exclude_icd9 = tuple(config.get("exclude_icd9", ()))
    exclude_icd10 = tuple(config.get("exclude_icd10", ()))
    if exclude_icd9:
        mask = mask & ~(versions.eq(9) & codes.str.startswith(exclude_icd9, na=False))
    if exclude_icd10:
        mask = mask & ~(versions.eq(10) & codes.str.startswith(exclude_icd10, na=False))
    return mask


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    diagnoses = pd.read_csv(
        DIAGNOSES_PATH,
        compression="infer",
        usecols=["hadm_id", "icd_code", "icd_version"],
        dtype={"hadm_id": "int64", "icd_code": "string", "icd_version": "int16"},
    )
    diagnoses["icd_code"] = diagnoses["icd_code"].map(normalize_icd)

    target_columns = []
    report_rows = []
    for target, config in EXPANDED_DIAGNOSIS_TARGETS.items():
        mask = prefix_mask(diagnoses["icd_code"], diagnoses["icd_version"], config)
        positive_hadm_ids = set(diagnoses.loc[mask, "hadm_id"].dropna().astype("int64"))
        df[target] = df["hadm_id"].isin(positive_hadm_ids).astype("int8")
        target_columns.append(target)
        positives = int(df[target].sum())
        report_rows.append(
            {
                "target": target,
                "label_ge": config["label_ge"],
                "label_en": config["label_en"],
                "icd9": ", ".join(config.get("icd9", ())) or "-",
                "icd10": ", ".join(config.get("icd10", ())) or "-",
                "positive_rows": positives,
                "positive_rate": positives / len(df),
            }
        )

    df["target_cvd"] = df[target_columns].max(axis=1).astype("int8")
    df.to_csv(DATA_PATH, index=False)

    lines = [
        "# Expanded Diagnosis Targets",
        "",
        f"Dataset: `{DATA_PATH}`",
        f"Rows: `{len(df):,}`",
        "",
        "| Target | Georgian label | English label | ICD-9 prefixes | ICD-10 prefixes | Positive rows | Positive rate |",
        "|---|---|---|---|---|---:|---:|",
    ]
    for row in sorted(report_rows, key=lambda item: item["positive_rows"], reverse=True):
        lines.append(
            f"| `{row['target']}` | {row['label_ge']} | {row['label_en']} | "
            f"`{row['icd9']}` | `{row['icd10']}` | {row['positive_rows']:,} | {row['positive_rate']:.2%} |"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated {DATA_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()

