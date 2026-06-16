from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ID_COLUMNS = ["subject_id", "hadm_id"]
TARGET_COLUMN = "target_cvd"
SPLIT_COLUMN = "split_hint"

DROP_ALWAYS = [
    # Entirely empty in the current assembled dataset.
    "lab_troponin_i_mean",
    # Constant zero in the current assembled dataset, so it carries no signal.
    "lab_troponin_i_count",
]

ECG_COLUMNS = [
    "ecg_rr_interval",
    "ecg_p_onset",
    "ecg_p_end",
    "ecg_qrs_onset",
    "ecg_qrs_end",
    "ecg_t_end",
    "ecg_p_axis",
    "ecg_qrs_axis",
    "ecg_t_axis",
]

OMR_FEATURE_COLUMNS = [
    "omr_bmi_mean",
    "omr_weight_lbs_mean",
    "omr_height_inches_mean",
    "omr_sbp_mean",
    "omr_dbp_mean",
]

DIAGNOSIS_HISTORY_COLUMNS = [
    "history_diabetes",
    "history_chronic_kidney_disease",
    "history_obesity",
    "history_tobacco_or_nicotine",
]

TRIAGE_SYMPTOM_COLUMNS = [
    "triage_pain_mean",
    "symptom_chest_pain",
    "symptom_shortness_of_breath",
    "symptom_palpitations",
    "symptom_syncope",
    "symptom_dizziness",
    "symptom_edema",
]

INTERACTION_COLUMNS = [
    "interaction_age_omr_sbp",
    "interaction_bmi_omr_sbp",
    "interaction_glucose_bmi",
    "interaction_ntprobnp_age",
    "interaction_troponin_ecg_available",
]

# Conservative physiologic ranges. Values outside these bounds are treated as
# extraction artifacts or charting errors and imputed later from training data.
VALID_RANGES = {
    "age": (18, 110),
    "lab_chol_ratio_mean": (0.5, 20),
    "lab_hdl_mean": (1, 200),
    "lab_ldl_calc_mean": (1, 400),
    "lab_ldl_measured_mean": (1, 400),
    "lab_chol_total_mean": (20, 500),
    "lab_triglycerides_mean": (1, 2000),
    "lab_troponin_t_mean": (0, 100),
    "lab_ntprobnp_mean": (0, 100000),
    "lab_creatinine_mean": (0.1, 30),
    "lab_glucose_mean": (20, 1000),
    "lab_hemoglobin_mean": (1, 25),
    "lab_platelets_mean": (1, 1500),
    "ed_triage_temperature_f_mean": (80, 110),
    "ed_temperature_f_mean": (80, 110),
    "ed_temperature_f_min": (80, 110),
    "ed_temperature_f_max": (80, 110),
    "ed_triage_heart_rate_mean": (20, 250),
    "ed_heart_rate_mean": (20, 250),
    "ed_heart_rate_min": (20, 250),
    "ed_heart_rate_max": (20, 250),
    "icu_heart_rate_mean": (20, 250),
    "icu_heart_rate_min": (20, 250),
    "icu_heart_rate_max": (20, 250),
    "ed_triage_resp_rate_mean": (4, 80),
    "ed_resp_rate_mean": (4, 80),
    "icu_resp_rate_mean": (4, 80),
    "ed_triage_spo2_mean": (50, 100),
    "ed_spo2_mean": (50, 100),
    "icu_spo2_mean": (50, 100),
    "ed_triage_sbp_mean": (40, 300),
    "ed_sbp_mean": (40, 300),
    "ed_sbp_min": (40, 300),
    "ed_sbp_max": (40, 300),
    "icu_sbp_mean": (40, 300),
    "icu_sbp_min": (40, 300),
    "icu_sbp_max": (40, 300),
    "ed_triage_dbp_mean": (20, 200),
    "ed_dbp_mean": (20, 200),
    "icu_dbp_mean": (20, 200),
    "icu_dbp_min": (20, 200),
    "icu_dbp_max": (20, 200),
    "icu_temperature_c_mean": (30, 45),
    "ed_triage_acuity_mean": (1, 5),
    "ecg_rr_interval": (200, 3000),
    "ecg_p_onset": (0, 2000),
    "ecg_p_end": (0, 2000),
    "ecg_qrs_onset": (0, 2000),
    "ecg_qrs_end": (0, 2000),
    "ecg_t_end": (0, 3000),
    "ecg_p_axis": (-180, 180),
    "ecg_qrs_axis": (-180, 180),
    "ecg_t_axis": (-180, 180),
    "omr_bmi_mean": (10, 90),
    "omr_weight_lbs_mean": (50, 800),
    "omr_height_inches_mean": (36, 96),
    "omr_sbp_mean": (40, 300),
    "omr_dbp_mean": (20, 200),
    "triage_pain_mean": (0, 10),
}


def load_omr_features(omr_csv: Path) -> pd.DataFrame:
    omr = pd.read_csv(
        omr_csv,
        usecols=["subject_id", "result_name", "result_value"],
        compression="infer",
    )
    omr["result_value"] = omr["result_value"].astype("string").str.strip()

    simple_feature_map = {
        "BMI (kg/m2)": "omr_bmi_mean",
        "BMI": "omr_bmi_mean",
        "Weight (Lbs)": "omr_weight_lbs_mean",
        "Weight": "omr_weight_lbs_mean",
        "Height (Inches)": "omr_height_inches_mean",
        "Height": "omr_height_inches_mean",
    }

    simple = omr[omr["result_name"].isin(simple_feature_map)].copy()
    simple["feature"] = simple["result_name"].map(simple_feature_map)
    simple["value"] = pd.to_numeric(simple["result_value"], errors="coerce")

    blood_pressure = omr[omr["result_name"].str.contains("Blood Pressure", na=False)].copy()
    extracted = blood_pressure["result_value"].str.extract(
        r"^\s*(?P<sbp>\d{2,3})\s*/\s*(?P<dbp>\d{2,3})"
    )
    blood_pressure["omr_sbp_mean"] = pd.to_numeric(extracted["sbp"], errors="coerce")
    blood_pressure["omr_dbp_mean"] = pd.to_numeric(extracted["dbp"], errors="coerce")

    simple_agg = simple.pivot_table(
        index="subject_id",
        columns="feature",
        values="value",
        aggfunc="median",
    )
    bp_agg = blood_pressure.groupby("subject_id")[["omr_sbp_mean", "omr_dbp_mean"]].median()

    features = simple_agg.join(bp_agg, how="outer").reset_index()
    for column in OMR_FEATURE_COLUMNS:
        if column not in features.columns:
            features[column] = pd.NA
    return features[["subject_id"] + OMR_FEATURE_COLUMNS]


def load_diagnosis_history_features(diagnoses_csv: Path) -> pd.DataFrame:
    diagnoses = pd.read_csv(
        diagnoses_csv,
        usecols=["subject_id", "icd_code", "icd_version"],
        compression="infer",
    )
    diagnoses["icd_code"] = (
        diagnoses["icd_code"].astype("string").str.upper().str.replace(".", "", regex=False)
    )

    is_icd9 = diagnoses["icd_version"].eq(9)
    is_icd10 = diagnoses["icd_version"].eq(10)
    code = diagnoses["icd_code"]

    diagnoses["history_diabetes"] = (
        (is_icd9 & code.str.startswith("250", na=False))
        | (is_icd10 & code.str.match(r"^E0[89]|^E1[013]", na=False))
    ).astype("int8")
    diagnoses["history_chronic_kidney_disease"] = (
        (is_icd9 & code.str.startswith("585", na=False))
        | (is_icd10 & code.str.startswith("N18", na=False))
    ).astype("int8")
    diagnoses["history_obesity"] = (
        (is_icd9 & (code.str.startswith("2780", na=False) | code.str.startswith("V85", na=False)))
        | (is_icd10 & (code.str.startswith("E66", na=False) | code.str.startswith("Z68", na=False)))
    ).astype("int8")
    diagnoses["history_tobacco_or_nicotine"] = (
        (
            is_icd9
            & (
                code.str.startswith("3051", na=False)
                | code.str.startswith("V1582", na=False)
                | code.str.startswith("98984", na=False)
            )
        )
        | (
            is_icd10
            & (
                code.str.startswith("F17", na=False)
                | code.str.startswith("Z720", na=False)
                | code.str.startswith("Z87891", na=False)
                | code.str.startswith("T652", na=False)
            )
        )
    ).astype("int8")

    return diagnoses.groupby("subject_id", as_index=False)[DIAGNOSIS_HISTORY_COLUMNS].max()


def load_triage_symptom_features(triage_csv: Path) -> pd.DataFrame:
    triage = pd.read_csv(
        triage_csv,
        usecols=["subject_id", "pain", "chiefcomplaint"],
        compression="infer",
    )
    text = triage["chiefcomplaint"].fillna("").astype("string").str.lower()

    triage["triage_pain_mean"] = pd.to_numeric(triage["pain"], errors="coerce")
    triage["symptom_chest_pain"] = text.str.contains(
        r"chest pain|\bcp\b|chest pressure", regex=True
    ).astype("int8")
    triage["symptom_shortness_of_breath"] = text.str.contains(
        r"shortness of breath|\bsob\b|dyspnea|difficulty breathing|trouble breathing",
        regex=True,
    ).astype("int8")
    triage["symptom_palpitations"] = text.str.contains(
        r"palpitation|palpitations", regex=True
    ).astype("int8")
    triage["symptom_syncope"] = text.str.contains(
        r"syncope|near syncope|faint|passed out", regex=True
    ).astype("int8")
    triage["symptom_dizziness"] = text.str.contains(
        r"dizzy|dizziness|lightheaded|light headed", regex=True
    ).astype("int8")
    triage["symptom_edema"] = text.str.contains(
        r"edema|swelling|leg swelling|lower extremity swelling", regex=True
    ).astype("int8")

    return triage.groupby("subject_id", as_index=False).agg(
        {
            "triage_pain_mean": "median",
            "symptom_chest_pain": "max",
            "symptom_shortness_of_breath": "max",
            "symptom_palpitations": "max",
            "symptom_syncope": "max",
            "symptom_dizziness": "max",
            "symptom_edema": "max",
        }
    )


def add_interaction_features(df: pd.DataFrame) -> list[str]:
    if {"age", "omr_sbp_mean"}.issubset(df.columns):
        df["interaction_age_omr_sbp"] = df["age"] * df["omr_sbp_mean"]
    if {"omr_bmi_mean", "omr_sbp_mean"}.issubset(df.columns):
        df["interaction_bmi_omr_sbp"] = df["omr_bmi_mean"] * df["omr_sbp_mean"]
    if {"lab_glucose_mean", "omr_bmi_mean"}.issubset(df.columns):
        df["interaction_glucose_bmi"] = df["lab_glucose_mean"] * df["omr_bmi_mean"]
    if {"lab_ntprobnp_mean", "age"}.issubset(df.columns):
        df["interaction_ntprobnp_age"] = df["lab_ntprobnp_mean"] * df["age"]
    if {"lab_troponin_t_mean", "ecg_available"}.issubset(df.columns):
        df["interaction_troponin_ecg_available"] = (
            df["lab_troponin_t_mean"] * df["ecg_available"]
        )
    return [column for column in INTERACTION_COLUMNS if column in df.columns]


def replace_out_of_range(df: pd.DataFrame) -> dict[str, int]:
    replaced: dict[str, int] = {}
    for column, (lower, upper) in VALID_RANGES.items():
        if column not in df.columns:
            continue
        mask = df[column].notna() & ~df[column].between(lower, upper)
        count = int(mask.sum())
        if count:
            df.loc[mask, column] = pd.NA
        replaced[column] = count
    return replaced


def clean_ecg_sentinels(df: pd.DataFrame) -> dict[str, int]:
    replaced: dict[str, int] = {}
    for column in ECG_COLUMNS:
        if column not in df.columns:
            continue
        mask = df[column].notna() & (df[column].abs() >= 9999)
        count = int(mask.sum())
        if count:
            df.loc[mask, column] = pd.NA
        replaced[column] = count
    return replaced


def add_missing_indicators(df: pd.DataFrame, feature_columns: list[str]) -> list[str]:
    indicator_columns: list[str] = []
    for column in feature_columns:
        if df[column].isna().any():
            indicator = f"{column}_missing"
            df[indicator] = df[column].isna().astype("int8")
            indicator_columns.append(indicator)
    return indicator_columns


def impute_from_train_medians(
    df: pd.DataFrame, feature_columns: list[str]
) -> dict[str, float]:
    train_mask = df[SPLIT_COLUMN].eq("train")
    medians = df.loc[train_mask, feature_columns].median(numeric_only=True)
    fill_values: dict[str, float] = {}

    for column in feature_columns:
        value = medians.get(column)
        if pd.isna(value):
            value = 0.0
        fill_values[column] = float(value)
        df[column] = df[column].fillna(value)

    return fill_values


def build_report(
    raw_df: pd.DataFrame,
    clean_df: pd.DataFrame,
    dropped_columns: list[str],
    out_of_range_counts: dict[str, int],
    ecg_sentinel_counts: dict[str, int],
    indicator_columns: list[str],
    output_csv: Path,
    omr_features: pd.DataFrame | None,
    diagnosis_features: pd.DataFrame | None,
    triage_features: pd.DataFrame | None,
    interaction_columns: list[str],
) -> str:
    target_counts = raw_df[TARGET_COLUMN].value_counts().sort_index()
    split_counts = raw_df[SPLIT_COLUMN].value_counts()

    lines = [
        "# Cardio Dataset Preprocessing Report",
        "",
        f"Input shape: {raw_df.shape[0]:,} rows x {raw_df.shape[1]:,} columns",
        f"Output shape: {clean_df.shape[0]:,} rows x {clean_df.shape[1]:,} columns",
        f"Output file: `{output_csv}`",
        "",
        "## Target Distribution",
    ]
    for label, count in target_counts.items():
        pct = count / len(raw_df) * 100
        lines.append(f"- `{label}`: {count:,} rows ({pct:.2f}%)")

    lines.extend(["", "## Split Distribution"])
    for label, count in split_counts.items():
        pct = count / len(raw_df) * 100
        lines.append(f"- `{label}`: {count:,} rows ({pct:.2f}%)")

    lines.extend(["", "## Dropped Columns"])
    for column in dropped_columns:
        lines.append(f"- `{column}`")

    if omr_features is not None:
        lines.extend(["", "## OMR Features Added"])
        for column in OMR_FEATURE_COLUMNS:
            available = int(omr_features[column].notna().sum())
            pct = available / len(raw_df) * 100
            lines.append(f"- `{column}`: available in {available:,} rows ({pct:.2f}%) before imputation")

    if diagnosis_features is not None:
        lines.extend(["", "## ICD History Features Added"])
        for column in DIAGNOSIS_HISTORY_COLUMNS:
            positive = int(diagnosis_features[column].sum())
            pct = positive / len(raw_df) * 100
            lines.append(f"- `{column}`: positive in {positive:,} rows ({pct:.2f}%)")

    if triage_features is not None:
        lines.extend(["", "## Triage Symptom Features Added"])
        for column in TRIAGE_SYMPTOM_COLUMNS:
            if column == "triage_pain_mean":
                available = int(triage_features[column].notna().sum())
                pct = available / len(raw_df) * 100
                lines.append(f"- `{column}`: available in {available:,} rows ({pct:.2f}%) before imputation")
            else:
                positive = int(triage_features[column].sum())
                pct = positive / len(raw_df) * 100
                lines.append(f"- `{column}`: positive in {positive:,} rows ({pct:.2f}%)")

    if interaction_columns:
        lines.extend(["", "## Interaction Features Added"])
        for column in interaction_columns:
            lines.append(f"- `{column}`")

    lines.extend(["", "## Out-of-Range Values Replaced With Missing"])
    for column, count in sorted(out_of_range_counts.items()):
        if count:
            lines.append(f"- `{column}`: {count:,}")

    lines.extend(["", "## ECG Sentinel Values Replaced With Missing"])
    for column, count in sorted(ecg_sentinel_counts.items()):
        if count:
            lines.append(f"- `{column}`: {count:,}")

    lines.extend(
        [
            "",
            "## Missingness Handling",
            f"- Added {len(indicator_columns):,} missing-value indicator columns.",
            "- Numeric missing values were imputed with medians calculated from the training split only.",
            "- `ecg_available` missing values were converted to `0` before imputation.",
            "- OMR BMI, weight, height, and outpatient blood pressure were aggregated by patient using medians.",
            "- ICD history and triage symptom features were aggregated by patient because the added files do not provide a direct `hadm_id` link for every row.",
            "",
            "## Modeling Notes",
            "- Do not use `subject_id`, `hadm_id`, or `split_hint` as model features.",
            "- Keep the existing train/validation/test split because it has no patient overlap.",
            "- Use `target_cvd` as the label.",
        ]
    )
    return "\n".join(lines) + "\n"


def preprocess(
    input_csv: Path,
    output_csv: Path,
    report_path: Path,
    omr_csv: Path | None,
    diagnoses_csv: Path | None,
    triage_csv: Path | None,
) -> None:
    df = pd.read_csv(input_csv)
    raw_df = df.copy()
    row_omr_features = None
    row_diagnosis_features = None
    row_triage_features = None

    if omr_csv and omr_csv.exists():
        patient_omr_features = load_omr_features(omr_csv)
        df = df.merge(patient_omr_features, on="subject_id", how="left")
        row_omr_features = df[OMR_FEATURE_COLUMNS].copy()

    if diagnoses_csv and diagnoses_csv.exists():
        patient_diagnosis_features = load_diagnosis_history_features(diagnoses_csv)
        df = df.merge(patient_diagnosis_features, on="subject_id", how="left")
        for column in DIAGNOSIS_HISTORY_COLUMNS:
            df[column] = df[column].fillna(0).astype("int8")
        row_diagnosis_features = df[DIAGNOSIS_HISTORY_COLUMNS].copy()

    if triage_csv and triage_csv.exists():
        patient_triage_features = load_triage_symptom_features(triage_csv)
        df = df.merge(patient_triage_features, on="subject_id", how="left")
        for column in TRIAGE_SYMPTOM_COLUMNS:
            if column != "triage_pain_mean":
                df[column] = df[column].fillna(0).astype("int8")
        row_triage_features = df[TRIAGE_SYMPTOM_COLUMNS].copy()

    if "ecg_available" in df.columns:
        df["ecg_available"] = df["ecg_available"].fillna(0).astype("int8")

    dropped_columns = [column for column in DROP_ALWAYS if column in df.columns]
    df = df.drop(columns=dropped_columns)

    out_of_range_counts = replace_out_of_range(df)
    ecg_sentinel_counts = clean_ecg_sentinels(df)

    feature_columns = [
        column
        for column in df.columns
        if column not in ID_COLUMNS + [TARGET_COLUMN, SPLIT_COLUMN]
    ]

    indicator_columns = add_missing_indicators(df, feature_columns)
    impute_from_train_medians(df, feature_columns)
    interaction_columns = add_interaction_features(df)
    feature_columns.extend(interaction_columns)

    output_columns = [SPLIT_COLUMN, TARGET_COLUMN] + feature_columns + indicator_columns
    clean_df = df[output_columns]

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output_csv, index=False)
    report_path.write_text(
        build_report(
            raw_df=raw_df,
            clean_df=clean_df,
            dropped_columns=dropped_columns,
            out_of_range_counts=out_of_range_counts,
            ecg_sentinel_counts=ecg_sentinel_counts,
            indicator_columns=indicator_columns,
            output_csv=output_csv,
            omr_features=row_omr_features,
            diagnosis_features=row_diagnosis_features,
            triage_features=row_triage_features,
            interaction_columns=interaction_columns,
        ),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean the assembled CVD dataset.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("../cardio_training_features.csv"),
        help="Path to the assembled input CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/cardio_model_ready.csv"),
        help="Path for the model-ready output CSV.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/preprocessing_report.md"),
        help="Path for the preprocessing report.",
    )
    parser.add_argument(
        "--omr",
        type=Path,
        default=Path("../omr.csv.gz"),
        help="Optional MIMIC-IV OMR CSV with BMI, weight, height, and blood pressure.",
    )
    parser.add_argument(
        "--diagnoses",
        type=Path,
        default=Path("../diagnoses_icd.csv.gz"),
        help="Optional MIMIC-IV diagnoses ICD CSV for comorbidity history features.",
    )
    parser.add_argument(
        "--triage",
        type=Path,
        default=Path("../triage.csv.gz"),
        help="Optional MIMIC-IV ED triage CSV for symptom features.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    preprocess(args.input, args.output, args.report, args.omr, args.diagnoses, args.triage)
