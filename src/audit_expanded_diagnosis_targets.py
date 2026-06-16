from __future__ import annotations

from pathlib import Path

import pandas as pd

from diagnosis_targets import EXPANDED_DIAGNOSIS_TARGETS


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
DIAGNOSES_PATH = ROOT_DIR / "diagnoses_icd.csv.gz"
REPORT_PATH = PROJECT_DIR / "reports" / "expanded_diagnosis_target_audit.md"


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
    diagnoses = pd.read_csv(
        DIAGNOSES_PATH,
        compression="infer",
        usecols=["hadm_id", "icd_code", "icd_version"],
        dtype={"hadm_id": "int64", "icd_code": "string", "icd_version": "int16"},
    )
    diagnoses["icd_code"] = diagnoses["icd_code"].map(normalize_icd)
    total_admissions = diagnoses["hadm_id"].nunique()

    rows = []
    for target, config in EXPANDED_DIAGNOSIS_TARGETS.items():
        mask = prefix_mask(diagnoses["icd_code"], diagnoses["icd_version"], config)
        positive_admissions = diagnoses.loc[mask, "hadm_id"].nunique()
        rows.append(
            {
                "target": target,
                "label_ge": config["label_ge"],
                "label_en": config["label_en"],
                "icd9": ", ".join(config.get("icd9", ())) or "-",
                "icd10": ", ".join(config.get("icd10", ())) or "-",
                "positive_admissions": positive_admissions,
                "positive_rate": positive_admissions / total_admissions,
                "recommended": positive_admissions >= 1000,
            }
        )

    audit = pd.DataFrame(rows).sort_values("positive_admissions", ascending=False)
    lines = [
        "# Expanded Diagnosis Target Audit",
        "",
        f"Source: `{DIAGNOSES_PATH}`",
        f"Admissions with diagnoses: `{total_admissions:,}`",
        "",
        "Recommendation rule: keep targets with at least 1,000 positive admissions for the next model iteration.",
        "",
        "| Target | Georgian label | English label | ICD-9 prefixes | ICD-10 prefixes | Positive admissions | Positive rate | Recommended |",
        "|---|---|---|---|---|---:|---:|---|",
    ]
    for row in audit.to_dict("records"):
        lines.append(
            f"| `{row['target']}` | {row['label_ge']} | {row['label_en']} | "
            f"`{row['icd9']}` | `{row['icd10']}` | "
            f"{row['positive_admissions']:,} | {row['positive_rate']:.2%} | "
            f"{'yes' if row['recommended'] else 'no'} |"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(audit.to_string(index=False))
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
