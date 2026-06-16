from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import pandas as pd

from diagnosis_targets import EXPANDED_DIAGNOSIS_TARGETS


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent
OUTPUT_PATH = ROOT_DIR / "data" / "processed" / "cardio_time_aware_model_ready.csv"
REPORT_PATH = PROJECT_DIR / "reports" / "time_aware_dataset_report.md"
FEATURES_REPORT_PATH = PROJECT_DIR / "reports" / "time_aware_feature_summary.json"

OBSERVATION_HOURS = 24
RANDOM_STATE = 42

LAB_ITEMIDS = {
    50903: "lab_chol_ratio_mean",
    50904: "lab_hdl_mean",
    50905: "lab_ldl_calc_mean",
    50906: "lab_ldl_measured_mean",
    50907: "lab_chol_total_mean",
    51000: "lab_triglycerides_mean",
    51003: "lab_troponin_t_mean",
    50963: "lab_ntprobnp_mean",
    50912: "lab_creatinine_mean",
    52546: "lab_creatinine_mean",
    50931: "lab_glucose_mean",
    52569: "lab_glucose_mean",
    51222: "lab_hemoglobin_mean",
    51265: "lab_platelets_mean",
}

CHART_ITEMIDS = {
    220045: "icu_heart_rate_mean",
    220179: "icu_sbp_mean",
    220180: "icu_dbp_mean",
    220210: "icu_resp_rate_mean",
    220277: "icu_spo2_mean",
    223762: "icu_temperature_c_mean",
    223761: "icu_temperature_f_mean",
    226512: "icu_weight_kg_mean",
    226707: "icu_height_in_mean",
    226730: "icu_height_cm_mean",
}

LAB_FEATURES = sorted(set(LAB_ITEMIDS.values()))
CHART_FEATURES = sorted(set(CHART_ITEMIDS.values()))

SUBTYPE_PREFIXES = EXPANDED_DIAGNOSIS_TARGETS

HISTORY_PREFIXES = {
    "history_diabetes": {
        "icd9": ("250",),
        "icd10": ("E08", "E09", "E10", "E11", "E13"),
    },
    "history_chronic_kidney_disease": {
        "icd9": ("585",),
        "icd10": ("N18",),
    },
    "history_obesity": {
        "icd9": ("2780", "V85"),
        "icd10": ("E66", "Z68"),
    },
    "history_tobacco_or_nicotine": {
        "icd9": ("3051", "V1582", "98984"),
        "icd10": ("F17", "Z720", "Z87891", "T652"),
    },
}

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
    "ed_triage_heart_rate_mean": (20, 250),
    "ed_triage_resp_rate_mean": (4, 80),
    "ed_triage_spo2_mean": (50, 100),
    "ed_triage_sbp_mean": (40, 300),
    "ed_triage_dbp_mean": (20, 200),
    "ed_triage_acuity_mean": (1, 5),
    "triage_pain_mean": (0, 10),
    "icu_heart_rate_mean": (20, 250),
    "icu_sbp_mean": (40, 300),
    "icu_dbp_mean": (20, 200),
    "icu_resp_rate_mean": (4, 80),
    "icu_spo2_mean": (50, 100),
    "icu_temperature_c_mean": (30, 45),
    "icu_temperature_f_mean": (80, 110),
    "omr_bmi_mean": (10, 90),
    "omr_weight_lbs_mean": (50, 800),
    "omr_height_inches_mean": (36, 96),
    "omr_sbp_mean": (40, 300),
    "omr_dbp_mean": (20, 200),
}


class RunningStats:
    def __init__(self) -> None:
        self.sum = defaultdict(float)
        self.count = defaultdict(int)

    def add(self, key: int, value: float) -> None:
        if pd.isna(value):
            return
        self.sum[key] += float(value)
        self.count[key] += 1

    def to_frame(self, name: str) -> pd.DataFrame:
        rows = [
            {"hadm_id": key, name: self.sum[key] / self.count[key], f"{name}_count": self.count[key]}
            for key in self.count
        ]
        return pd.DataFrame(rows)


def split_for_subject(subject_id: int) -> str:
    digest = hashlib.md5(f"{subject_id}-{RANDOM_STATE}".encode()).hexdigest()
    bucket = int(digest[:8], 16) % 100
    if bucket < 70:
        return "train"
    if bucket < 90:
        return "validation"
    return "test"


def normalize_icd(code: object) -> str:
    return str(code).upper().replace(".", "").strip()


def matches_prefix(code: str, version: int, prefixes: dict[str, tuple[str, ...]]) -> bool:
    key = "icd9" if version == 9 else "icd10"
    return code.startswith(prefixes.get(key, ()))


def prefix_mask(codes: pd.Series, versions: pd.Series, prefixes: dict[str, tuple[str, ...]]) -> pd.Series:
    mask = pd.Series(False, index=codes.index)
    if prefixes.get("icd9"):
        mask = mask | (versions.eq(9) & codes.str.startswith(prefixes["icd9"], na=False))
    if prefixes.get("icd10"):
        mask = mask | (versions.eq(10) & codes.str.startswith(prefixes["icd10"], na=False))
    if prefixes.get("exclude_icd9"):
        mask = mask & ~(versions.eq(9) & codes.str.startswith(prefixes["exclude_icd9"], na=False))
    if prefixes.get("exclude_icd10"):
        mask = mask & ~(versions.eq(10) & codes.str.startswith(prefixes["exclude_icd10"], na=False))
    return mask


def build_targets_and_history(admissions: pd.DataFrame, diagnoses_path: Path) -> pd.DataFrame:
    diagnoses = pd.read_csv(diagnoses_path, compression="infer")
    diagnoses["icd_code"] = diagnoses["icd_code"].map(normalize_icd)
    diagnoses = diagnoses.merge(
        admissions[["subject_id", "hadm_id", "admittime"]],
        on=["subject_id", "hadm_id"],
        how="inner",
    )

    target_rows = admissions[["subject_id", "hadm_id", "admittime"]].drop_duplicates().copy()
    for target, prefixes in SUBTYPE_PREFIXES.items():
        mask = prefix_mask(diagnoses["icd_code"], diagnoses["icd_version"], prefixes)
        positive = diagnoses.loc[mask, ["hadm_id"]].drop_duplicates()
        target_rows[target] = target_rows["hadm_id"].isin(set(positive["hadm_id"])).astype("int8")
    target_rows["target_cvd"] = target_rows[list(SUBTYPE_PREFIXES)].max(axis=1).astype("int8")

    admission_flags = admissions[["subject_id", "hadm_id", "admittime"]].drop_duplicates().copy()
    for history_name, prefixes in HISTORY_PREFIXES.items():
        mask = prefix_mask(diagnoses["icd_code"], diagnoses["icd_version"], prefixes)
        positive = diagnoses.loc[mask, ["hadm_id"]].drop_duplicates()
        admission_flags[history_name] = admission_flags["hadm_id"].isin(set(positive["hadm_id"])).astype("int8")

    admission_flags = admission_flags.sort_values(["subject_id", "admittime", "hadm_id"])
    history = admission_flags[["subject_id", "hadm_id"]].copy()
    for history_name in HISTORY_PREFIXES:
        prior = (
            admission_flags.groupby("subject_id")[history_name]
            .cumsum()
            .groupby(admission_flags["subject_id"])
            .shift(fill_value=0)
            .clip(upper=1)
            .astype("int8")
        )
        history[history_name] = prior.to_numpy()

    return target_rows.merge(history, on=["subject_id", "hadm_id"], how="left").drop(columns=["admittime"])


def add_demographics(admissions: pd.DataFrame, patients_path: Path) -> pd.DataFrame:
    patients = pd.read_csv(patients_path, compression="infer")
    df = admissions.merge(patients, on="subject_id", how="left")
    df["admit_year"] = df["admittime"].dt.year
    df["age"] = df["anchor_age"] + (df["admit_year"] - df["anchor_year"])
    df["age"] = df["age"].clip(18, 91)
    df["gender_male"] = df["gender"].eq("M").astype("int8")
    df["hospital_expire_flag"] = df["hospital_expire_flag"].fillna(0).astype("int8")
    df["split_hint"] = df["subject_id"].map(split_for_subject)
    return df[["subject_id", "hadm_id", "split_hint", "age", "gender_male", "hospital_expire_flag"]]


def symptom_flags(text: pd.Series) -> pd.DataFrame:
    lower = text.fillna("").astype("string").str.lower()
    return pd.DataFrame(
        {
            "symptom_chest_pain": lower.str.contains(r"chest pain|\bcp\b|chest pressure", regex=True).astype("int8"),
            "symptom_shortness_of_breath": lower.str.contains(
                r"shortness of breath|\bsob\b|dyspnea|difficulty breathing|trouble breathing",
                regex=True,
            ).astype("int8"),
            "symptom_palpitations": lower.str.contains(r"palpitation", regex=True).astype("int8"),
            "symptom_syncope": lower.str.contains(r"syncope|near syncope|faint|passed out", regex=True).astype("int8"),
            "symptom_dizziness": lower.str.contains(r"dizzy|dizziness|lightheaded|light headed", regex=True).astype("int8"),
            "symptom_edema": lower.str.contains(r"edema|swelling|leg swelling|lower extremity swelling", regex=True).astype("int8"),
        }
    )


def build_ed_features(edstays_path: Path, triage_path: Path) -> pd.DataFrame:
    edstays = pd.read_csv(edstays_path, compression="infer")
    triage = pd.read_csv(triage_path, compression="infer")
    df = edstays[["subject_id", "hadm_id", "stay_id", "arrival_transport"]].merge(
        triage, on=["subject_id", "stay_id"], how="left"
    )
    flags = symptom_flags(df["chiefcomplaint"])
    for column in flags:
        df[column] = flags[column]
    df["ed_arrived_by_ambulance"] = df.get("arrival_transport", "").astype(str).str.contains("AMBULANCE", case=False, na=False).astype("int8")
    df["triage_pain_mean"] = pd.to_numeric(df["pain"], errors="coerce")
    rename = {
        "temperature": "ed_triage_temperature_f_mean",
        "heartrate": "ed_triage_heart_rate_mean",
        "resprate": "ed_triage_resp_rate_mean",
        "o2sat": "ed_triage_spo2_mean",
        "sbp": "ed_triage_sbp_mean",
        "dbp": "ed_triage_dbp_mean",
        "acuity": "ed_triage_acuity_mean",
    }
    df = df.rename(columns=rename)
    agg = {
        "ed_triage_temperature_f_mean": "mean",
        "ed_triage_heart_rate_mean": "mean",
        "ed_triage_resp_rate_mean": "mean",
        "ed_triage_spo2_mean": "mean",
        "ed_triage_sbp_mean": "mean",
        "ed_triage_dbp_mean": "mean",
        "ed_triage_acuity_mean": "mean",
        "triage_pain_mean": "mean",
        "ed_arrived_by_ambulance": "max",
        "symptom_chest_pain": "max",
        "symptom_shortness_of_breath": "max",
        "symptom_palpitations": "max",
        "symptom_syncope": "max",
        "symptom_dizziness": "max",
        "symptom_edema": "max",
    }
    return df.groupby("hadm_id", as_index=False).agg(agg)


def build_omr_features(admissions: pd.DataFrame, omr_path: Path) -> pd.DataFrame:
    omr = pd.read_csv(omr_path, compression="infer")
    omr["chartdate"] = pd.to_datetime(omr["chartdate"], errors="coerce")
    omr["result_value"] = omr["result_value"].astype("string").str.strip()
    df = admissions[["subject_id", "hadm_id", "admittime"]].merge(omr, on="subject_id", how="left")
    df = df[df["chartdate"].notna() & (df["chartdate"] <= df["admittime"])]
    mapping = {
        "BMI (kg/m2)": "omr_bmi_mean",
        "BMI": "omr_bmi_mean",
        "Weight (Lbs)": "omr_weight_lbs_mean",
        "Weight": "omr_weight_lbs_mean",
        "Height (Inches)": "omr_height_inches_mean",
        "Height": "omr_height_inches_mean",
    }
    simple = df[df["result_name"].isin(mapping)].copy()
    simple["feature"] = simple["result_name"].map(mapping)
    simple["value"] = pd.to_numeric(simple["result_value"], errors="coerce")
    simple = simple.sort_values("chartdate").drop_duplicates(["hadm_id", "feature"], keep="last")
    simple_wide = simple.pivot(index="hadm_id", columns="feature", values="value").reset_index()

    bp = df[df["result_name"].str.contains("Blood Pressure", na=False)].copy()
    extracted = bp["result_value"].str.extract(r"^\s*(?P<sbp>\d{2,3})\s*/\s*(?P<dbp>\d{2,3})")
    bp["omr_sbp_mean"] = pd.to_numeric(extracted["sbp"], errors="coerce")
    bp["omr_dbp_mean"] = pd.to_numeric(extracted["dbp"], errors="coerce")
    bp = bp.sort_values("chartdate").drop_duplicates("hadm_id", keep="last")
    bp = bp[["hadm_id", "omr_sbp_mean", "omr_dbp_mean"]]

    return simple_wide.merge(bp, on="hadm_id", how="outer")


def aggregate_events(
    events_path: Path,
    admissions: pd.DataFrame,
    item_map: dict[int, str],
    value_column: str = "valuenum",
    chunksize: int = 1_000_000,
) -> pd.DataFrame:
    window = admissions[["hadm_id", "admittime"]].copy()
    window["window_end"] = window["admittime"] + pd.Timedelta(hours=OBSERVATION_HOURS)
    stats = {feature: RunningStats() for feature in set(item_map.values())}

    usecols = ["hadm_id", "itemid", "charttime", value_column]
    for chunk in pd.read_csv(events_path, usecols=usecols, chunksize=chunksize, compression="infer"):
        chunk = chunk[chunk["hadm_id"].notna()]
        chunk["hadm_id"] = chunk["hadm_id"].astype("int64")
        chunk = chunk[chunk["itemid"].isin(item_map)]
        if chunk.empty:
            continue
        chunk["charttime"] = pd.to_datetime(chunk["charttime"], errors="coerce")
        chunk[value_column] = pd.to_numeric(chunk[value_column], errors="coerce")
        chunk = chunk.merge(window, on="hadm_id", how="inner")
        chunk = chunk[
            chunk["charttime"].notna()
            & chunk["charttime"].between(chunk["admittime"], chunk["window_end"], inclusive="both")
        ]
        if chunk.empty:
            continue
        chunk["feature"] = chunk["itemid"].map(item_map)
        for feature, group in chunk.groupby("feature"):
            for hadm_id, value in zip(group["hadm_id"], group[value_column]):
                stats[feature].add(int(hadm_id), value)

    frames = [stat.to_frame(feature) for feature, stat in stats.items() if stat.count]
    if not frames:
        return pd.DataFrame({"hadm_id": []})
    out = frames[0]
    for frame in frames[1:]:
        out = out.merge(frame, on="hadm_id", how="outer")
    return out


def clean_ranges(df: pd.DataFrame) -> dict[str, int]:
    counts = {}
    for column, (low, high) in VALID_RANGES.items():
        if column not in df.columns:
            continue
        mask = df[column].notna() & ~df[column].between(low, high)
        counts[column] = int(mask.sum())
        df.loc[mask, column] = pd.NA
    return counts


def add_interactions(df: pd.DataFrame) -> None:
    if {"age", "omr_sbp_mean"}.issubset(df.columns):
        df["interaction_age_omr_sbp"] = df["age"] * df["omr_sbp_mean"]
    if {"omr_bmi_mean", "omr_sbp_mean"}.issubset(df.columns):
        df["interaction_bmi_omr_sbp"] = df["omr_bmi_mean"] * df["omr_sbp_mean"]
    if {"lab_glucose_mean", "omr_bmi_mean"}.issubset(df.columns):
        df["interaction_glucose_bmi"] = df["lab_glucose_mean"] * df["omr_bmi_mean"]
    if {"lab_ntprobnp_mean", "age"}.issubset(df.columns):
        df["interaction_ntprobnp_age"] = df["lab_ntprobnp_mean"] * df["age"]


def add_missing_and_impute(df: pd.DataFrame, feature_columns: list[str]) -> list[str]:
    indicator_columns = []
    for column in feature_columns:
        if df[column].isna().any():
            indicator = f"{column}_missing"
            df[indicator] = df[column].isna().astype("int8")
            indicator_columns.append(indicator)
    train_mask = df["split_hint"].eq("train")
    medians = df.loc[train_mask, feature_columns].median(numeric_only=True)
    for column in feature_columns:
        value = medians.get(column)
        if pd.isna(value):
            value = 0
        df[column] = df[column].fillna(float(value))
    return indicator_columns


def check_patient_split_overlap(df: pd.DataFrame) -> dict[str, int]:
    split_subjects = {
        split: set(group["subject_id"])
        for split, group in df.groupby("split_hint")
    }
    return {
        "train_validation_overlap": len(split_subjects.get("train", set()) & split_subjects.get("validation", set())),
        "train_test_overlap": len(split_subjects.get("train", set()) & split_subjects.get("test", set())),
        "validation_test_overlap": len(split_subjects.get("validation", set()) & split_subjects.get("test", set())),
    }


def write_report(df: pd.DataFrame, out_of_range_counts: dict[str, int], indicator_columns: list[str], output_path: Path) -> None:
    target_counts = df["target_cvd"].value_counts().sort_index()
    split_counts = df["split_hint"].value_counts()
    overlaps = check_patient_split_overlap(df)
    lines = [
        "# Time-Aware Cardio Dataset Report",
        "",
        f"Output file: `{output_path}`",
        f"Shape: {df.shape[0]:,} rows x {df.shape[1]:,} columns",
        f"Observation window: first {OBSERVATION_HOURS} hours after `admittime`.",
        "",
        "## Target Distribution",
    ]
    for label, count in target_counts.items():
        lines.append(f"- `{label}`: {count:,} ({count / len(df) * 100:.2f}%)")
    lines.extend(["", "## Split Distribution"])
    for split, count in split_counts.items():
        lines.append(f"- `{split}`: {count:,} ({count / len(df) * 100:.2f}%)")
    lines.extend(["", "## Patient Split Overlap"])
    for name, count in overlaps.items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "## Missing Handling", f"- Added {len(indicator_columns):,} missing indicators."])
    lines.extend(["", "## Out-of-Range Values Replaced"])
    for column, count in sorted(out_of_range_counts.items()):
        if count:
            lines.append(f"- `{column}`: {count:,}")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    feature_summary = {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "target_positive_rate": float(df["target_cvd"].mean()),
        "missing_indicator_count": len(indicator_columns),
        "patient_split_overlap": overlaps,
    }
    FEATURES_REPORT_PATH.write_text(json.dumps(feature_summary, indent=2), encoding="utf-8")


def build_dataset(root: Path, output_path: Path) -> None:
    admissions = pd.read_csv(root / "admissions.csv.gz", compression="infer")
    admissions["admittime"] = pd.to_datetime(admissions["admittime"], errors="coerce")
    admissions["dischtime"] = pd.to_datetime(admissions["dischtime"], errors="coerce")
    admissions = admissions[admissions["hadm_id"].notna() & admissions["admittime"].notna()].copy()
    admissions["hadm_id"] = admissions["hadm_id"].astype("int64")

    print("Building demographics...")
    df = add_demographics(admissions, root / "patients.csv.gz")

    print("Building targets and prior history...")
    targets = build_targets_and_history(admissions, root / "diagnoses_icd.csv.gz")
    df = df.merge(targets, on=["subject_id", "hadm_id"], how="inner")

    print("Building ED features...")
    df = df.merge(build_ed_features(root / "edstays.csv.gz", root / "triage.csv.gz"), on="hadm_id", how="left")

    print("Building OMR features...")
    df = df.merge(build_omr_features(admissions, root / "omr.csv.gz"), on="hadm_id", how="left")

    print("Aggregating labevents...")
    df = df.merge(aggregate_events(root / "labevents.csv.gz", admissions, LAB_ITEMIDS), on="hadm_id", how="left")

    print("Aggregating chartevents...")
    df = df.merge(aggregate_events(root / "chartevents.csv.gz", admissions, CHART_ITEMIDS), on="hadm_id", how="left")

    if "icu_temperature_f_mean" in df.columns:
        celsius = (df["icu_temperature_f_mean"] - 32) * 5 / 9
        df["icu_temperature_c_mean"] = df["icu_temperature_c_mean"].fillna(celsius)
        df = df.drop(columns=["icu_temperature_f_mean"])

    add_interactions(df)
    out_of_range_counts = clean_ranges(df)

    target_columns = ["target_cvd", *SUBTYPE_PREFIXES.keys()]
    id_columns = ["subject_id", "hadm_id"]
    feature_columns = [
        column
        for column in df.columns
        if column not in id_columns + ["split_hint"] + target_columns
    ]
    indicator_columns = add_missing_and_impute(df, feature_columns)

    output_columns = ["subject_id", "hadm_id", "split_hint", *target_columns, *feature_columns, *indicator_columns]
    output_df = df[output_columns].copy()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False)
    write_report(output_df, out_of_range_counts, indicator_columns, output_path)
    print(f"Wrote {output_path}")
    print(f"Wrote {REPORT_PATH}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build time-aware MIMIC-IV CVD dataset.")
    parser.add_argument("--root", type=Path, default=PROJECT_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build_dataset(args.root, args.output)
