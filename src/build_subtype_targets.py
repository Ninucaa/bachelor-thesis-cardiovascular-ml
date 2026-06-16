from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
RAW_FEATURES_PATH = ROOT_DIR / "cardio_training_features.csv"
DIAGNOSES_PATH = ROOT_DIR / "diagnoses_icd.csv.gz"
DIAGNOSIS_DICT_PATH = ROOT_DIR / "d_icd_diagnoses.csv"
OUTPUT_PATH = ROOT_DIR / "data" / "processed" / "cardio_subtype_targets.csv"
REPORT_PATH = PROJECT_DIR / "reports" / "subtype_targets.md"


SUBTYPES = {
    "target_myocardial_infarction": {
        "label": "Myocardial infarction",
        "icd9_prefixes": ("410",),
        "icd10_prefixes": ("I21", "I22"),
    },
    "target_heart_failure": {
        "label": "Heart failure",
        "icd9_prefixes": ("428",),
        "icd10_prefixes": ("I50",),
    },
    "target_stroke": {
        "label": "Stroke / cerebrovascular disease",
        "icd9_prefixes": ("430", "431", "432", "433", "434", "436"),
        "icd10_prefixes": ("I60", "I61", "I62", "I63", "I64"),
    },
    "target_arrhythmia": {
        "label": "Cardiac arrhythmia",
        "icd9_prefixes": ("426", "427"),
        "icd10_prefixes": ("I44", "I45", "I47", "I48", "I49"),
    },
    "target_hypertension": {
        "label": "Hypertensive disease",
        "icd9_prefixes": ("401", "402", "403", "404", "405"),
        "icd10_prefixes": ("I10", "I11", "I12", "I13", "I15", "I16"),
    },
    "target_coronary_artery_disease": {
        "label": "Coronary artery / ischemic heart disease",
        "icd9_prefixes": ("411", "412", "413", "414"),
        "icd10_prefixes": ("I20", "I23", "I24", "I25"),
    },
}


def normalize_icd(code: object) -> str:
    return str(code).upper().replace(".", "").strip()


def has_prefix(code: str, prefixes: tuple[str, ...]) -> bool:
    return any(code.startswith(prefix) for prefix in prefixes)


def assign_subtypes(diagnoses: pd.DataFrame) -> pd.DataFrame:
    diagnoses = diagnoses[["hadm_id", "icd_code", "icd_version"]].copy()
    diagnoses["icd_code"] = diagnoses["icd_code"].map(normalize_icd)

    for target, config in SUBTYPES.items():
        icd9_mask = diagnoses["icd_version"].eq(9) & diagnoses["icd_code"].map(
            lambda code: has_prefix(code, config["icd9_prefixes"])
        )
        icd10_mask = diagnoses["icd_version"].eq(10) & diagnoses["icd_code"].map(
            lambda code: has_prefix(code, config["icd10_prefixes"])
        )
        diagnoses[target] = (icd9_mask | icd10_mask).astype("int8")

    targets = (
        diagnoses.groupby("hadm_id")[list(SUBTYPES)]
        .max()
        .reset_index()
    )
    return targets


def write_report(output: pd.DataFrame) -> None:
    lines = [
        "# Disease-Specific Target Report",
        "",
        f"Rows: {len(output):,}",
        "",
        "| Target | Label | Positive rows | Positive rate |",
        "|---|---|---:|---:|",
    ]

    for target, config in SUBTYPES.items():
        positives = int(output[target].sum())
        rate = positives / len(output) * 100
        lines.append(
            f"| `{target}` | {config['label']} | {positives:,} | {rate:.2f}% |"
        )

    lines.extend(
        [
            "",
            "## ICD Mapping",
            "",
            "| Target | ICD-9 prefixes | ICD-10 prefixes |",
            "|---|---|---|",
        ]
    )
    for target, config in SUBTYPES.items():
        lines.append(
            f"| `{target}` | `{', '.join(config['icd9_prefixes'])}` | "
            f"`{', '.join(config['icd10_prefixes'])}` |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "These targets are diagnosis-code based labels. They are more specific than the original `target_cvd`, but they still represent retrospective coded hospital diagnoses, not real-time confirmed clinical diagnoses.",
        ]
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    features = pd.read_csv(
        RAW_FEATURES_PATH,
        usecols=["subject_id", "hadm_id", "target_cvd", "split_hint"],
    )
    diagnoses = pd.read_csv(
        DIAGNOSES_PATH,
        dtype={"icd_code": "string", "icd_version": "int16", "hadm_id": "int64"},
        usecols=["hadm_id", "icd_code", "icd_version"],
    )

    targets = assign_subtypes(diagnoses)
    output = features.merge(targets, on="hadm_id", how="left")
    for target in SUBTYPES:
        output[target] = output[target].fillna(0).astype("int8")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_PATH, index=False)
    write_report(output)

    print(f"Wrote {OUTPUT_PATH}")
    print(f"Wrote {REPORT_PATH}")
    print(output[list(SUBTYPES)].sum().to_string())


if __name__ == "__main__":
    main()
