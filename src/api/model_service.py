from __future__ import annotations

import json
from functools import cached_property
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.diagnosis_targets import EXPANDED_CLINICAL_CHECKS, EXPANDED_DIAGNOSIS_TARGETS


PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_DIR.parent / "data" / "processed" / "cardio_time_aware_model_ready.csv"
MODEL_DIR = PROJECT_DIR / "models" / "time_aware"
MODEL_PATH = MODEL_DIR / "target_cvd.pkl"
FEATURES_PATH = MODEL_DIR / "feature_columns.json"
SUBTYPE_MODEL_DIR = MODEL_DIR
DIAGNOSIS_THRESHOLDS_PATH = MODEL_DIR / "diagnosis_thresholds.json"
TARGET_NAME = "target_cvd"
DISPLAY_TARGET_NAME = "გულ-სისხლძარღვთა სავარაუდო დიაგნოსტიკური მიმართულება"
TARGET_DESCRIPTION = (
    "მოდელი პაციენტის ადრეულ კლინიკურ მონაცემებზე დაყრდნობით პროგნოზირებს, "
    "რომელ ICD-კოდირებული გულ-სისხლძარღვთა დიაგნოზის ჯგუფთან არის პაციენტის "
    "პროფილი ყველაზე მეტად დაკავშირებული. შედეგი არის სავარაუდო დიაგნოსტიკური "
    "მიმართულება და საჭიროებს ექიმის დადასტურებას."
)
METHOD_NOTE = (
    "პროგნოზისთვის გამოყენებულია XGBoost, ხოლო ახსნისთვის SHAP. თითოეული subtype "
    "მოდელი გაწვრთნილია MIMIC-IV-ში დაფიქსირებულ რეალურ ICD დიაგნოზებზე. სისტემა "
    "სწავლობს სტატისტიკურ კავშირებს და არ ცვლის ექიმის საბოლოო დიაგნოზს."
)
SUBTYPE_NOTE = (
    "ქვემოთ ნაჩვენებია სავარაუდო გულ-სისხლძარღვთა დიაგნოზის ჯგუფები. "
    "დიაგნოსტიკური სიგნალი ჩნდება მხოლოდ მაშინ, როცა მოდელის ალბათობა validation "
    "split-ზე დათვლილ threshold-ს აჭარბებს."
)

SUBTYPE_LABELS = {
    target: config["label_ge"]
    for target, config in EXPANDED_DIAGNOSIS_TARGETS.items()
}

CLINICAL_CHECKS = EXPANDED_CLINICAL_CHECKS

FEATURE_GROUPS = {
    "age": "დემოგრაფიული მონაცემები",
    "gender": "დემოგრაფიული მონაცემები",
    "history_": "დიაგნოზების ისტორიიდან მიღებული რისკ-ფაქტორები",
    "symptom_": "გადაუდებელი მიმართვის სიმპტომები",
    "triage_pain": "გადაუდებელი მიმართვის სიმპტომები",
    "interaction_": "კომბინირებული რისკ-სიგნალები",
    "omr_": "ამბულატორიული BMI, წონა, სიმაღლე და წნევა",
    "lab_": "ლაბორატორიული ანალიზები",
    "ed_triage": "გადაუდებელი განყოფილების triage მაჩვენებლები",
    "ed_": "გადაუდებელი განყოფილების vital ნიშნები",
    "icu_": "ინტენსიური თერაპიის vital ნიშნები",
}

FEATURE_LABELS = {
    "age": "ასაკი",
    "gender_male": "სქესი",
    "omr_bmi_mean": "BMI",
    "omr_weight_lbs_mean": "წონა",
    "omr_height_inches_mean": "სიმაღლე",
    "omr_sbp_mean": "ამბულატორიული სისტოლური წნევა",
    "omr_dbp_mean": "ამბულატორიული დიასტოლური წნევა",
    "history_diabetes": "დიაბეტის ისტორია",
    "history_chronic_kidney_disease": "თირკმლის ქრონიკული დაავადების ისტორია",
    "history_obesity": "სიმსუქნის ისტორია",
    "history_tobacco_or_nicotine": "თამბაქოს/ნიკოტინის ისტორია",
    "triage_pain_mean": "ტკივილის შეფასება გადაუდებელში",
    "symptom_chest_pain": "გულმკერდის ტკივილის ჩივილი",
    "symptom_shortness_of_breath": "ქოშინის/სუნთქვის გაძნელების ჩივილი",
    "symptom_palpitations": "გულის ფრიალის ჩივილი",
    "symptom_syncope": "გულის წასვლის/სინკოპეს ჩივილი",
    "symptom_dizziness": "თავბრუსხვევის ჩივილი",
    "symptom_edema": "შეშუპების ჩივილი",
    "interaction_age_omr_sbp": "ასაკისა და სისტოლური წნევის კომბინაცია",
    "interaction_bmi_omr_sbp": "BMI-ისა და სისტოლური წნევის კომბინაცია",
    "interaction_glucose_bmi": "გლუკოზისა და BMI-ის კომბინაცია",
    "interaction_ntprobnp_age": "NT-proBNP-ისა და ასაკის კომბინაცია",
    "lab_chol_ratio_mean": "ქოლესტერინის თანაფარდობა",
    "lab_hdl_mean": "HDL ქოლესტერინი",
    "lab_ldl_calc_mean": "LDL ქოლესტერინი",
    "lab_ldl_measured_mean": "გაზომილი LDL ქოლესტერინი",
    "lab_chol_total_mean": "საერთო ქოლესტერინი",
    "lab_triglycerides_mean": "ტრიგლიცერიდები",
    "lab_troponin_t_mean": "ტროპონინი T",
    "lab_ntprobnp_mean": "NT-proBNP",
    "lab_creatinine_mean": "კრეატინინი",
    "lab_glucose_mean": "გლუკოზა",
    "lab_hemoglobin_mean": "ჰემოგლობინი",
    "lab_platelets_mean": "თრომბოციტები",
    "lab_chol_ratio_mean_count": "ქოლესტერინის თანაფარდობის ჩანაწერების რაოდენობა",
    "lab_hdl_mean_count": "HDL ქოლესტერინის ჩანაწერების რაოდენობა",
    "lab_ldl_calc_mean_count": "LDL ქოლესტერინის ჩანაწერების რაოდენობა",
    "lab_ldl_measured_mean_count": "გაზომილი LDL ქოლესტერინის ჩანაწერების რაოდენობა",
    "lab_chol_total_mean_count": "საერთო ქოლესტერინის ჩანაწერების რაოდენობა",
    "lab_triglycerides_mean_count": "ტრიგლიცერიდების ჩანაწერების რაოდენობა",
    "lab_troponin_t_mean_count": "ტროპონინი T-ის ჩანაწერების რაოდენობა",
    "lab_ntprobnp_mean_count": "NT-proBNP-ის ჩანაწერების რაოდენობა",
    "lab_creatinine_mean_count": "კრეატინინის ჩანაწერების რაოდენობა",
    "lab_glucose_mean_count": "გლუკოზის ჩანაწერების რაოდენობა",
    "lab_hemoglobin_mean_count": "ჰემოგლობინის ჩანაწერების რაოდენობა",
    "lab_platelets_mean_count": "თრომბოციტების ჩანაწერების რაოდენობა",
    "ed_arrived_by_ambulance": "სასწრაფო დახმარებით მიყვანა",
    "ed_triage_temperature_f_mean": "triage ტემპერატურა",
    "ed_triage_resp_rate_mean": "triage სუნთქვის სიხშირე",
    "ed_triage_heart_rate_mean": "triage გულისცემა",
    "ed_triage_sbp_mean": "triage სისტოლური წნევა",
    "ed_triage_dbp_mean": "triage დიასტოლური წნევა",
    "ed_triage_spo2_mean": "triage SpO2",
    "ed_triage_acuity_mean": "triage სიმძიმე",
    "icu_temperature_c_mean": "ICU ტემპერატურა",
    "icu_heart_rate_mean": "ICU გულისცემა",
    "icu_sbp_mean": "ICU სისტოლური წნევა",
    "icu_dbp_mean": "ICU დიასტოლური წნევა",
    "icu_resp_rate_mean": "ICU სუნთქვის სიხშირე",
    "icu_spo2_mean": "ICU SpO2",
    "icu_weight_kg_mean": "ICU წონა",
    "icu_height_cm_mean": "ICU სიმაღლე",
    "icu_height_in_mean": "ICU სიმაღლე",
}

FEATURE_REFERENCE_RANGES = {
    "omr_bmi_mean": (18.5, 24.9, "kg/m2"),
    "omr_sbp_mean": (90, 120, "mmHg"),
    "omr_dbp_mean": (60, 80, "mmHg"),
    "ed_triage_heart_rate_mean": (60, 100, "bpm"),
    "ed_triage_resp_rate_mean": (12, 20, "breaths/min"),
    "ed_triage_spo2_mean": (95, 100, "%"),
    "ed_triage_sbp_mean": (90, 120, "mmHg"),
    "ed_triage_dbp_mean": (60, 80, "mmHg"),
    "lab_creatinine_mean": (0.6, 1.3, "mg/dL"),
    "lab_hemoglobin_mean": (12, 17.5, "g/dL"),
    "lab_glucose_mean": (70, 140, "mg/dL"),
    "lab_ntprobnp_mean": (0, 450, "pg/mL"),
    "lab_troponin_t_mean": (0, 0.01, "ng/mL"),
    "lab_chol_ratio_mean": (0, 5, ""),
    "lab_hdl_mean": (40, 1000, "mg/dL"),
    "lab_ldl_calc_mean": (0, 100, "mg/dL"),
    "lab_ldl_measured_mean": (0, 100, "mg/dL"),
    "lab_chol_total_mean": (0, 200, "mg/dL"),
    "lab_triglycerides_mean": (0, 150, "mg/dL"),
    "lab_platelets_mean": (150, 450, "K/uL"),
}

COUNTERFACTUAL_GROUPS = [
    {
        "factor_group": "წნევა და სასიცოცხლო ნიშნები",
        "current_profile": "პაციენტის წნევის, გულისცემისა და გადაუდებელი ნიშნების არსებული კომბინაცია",
        "reference_profile": "reference პროფილი: სისტოლური წნევა 120 mmHg, დიასტოლური 80 mmHg, გულისცემა 80 bpm",
        "values": {
            "omr_sbp_mean": 120,
            "omr_dbp_mean": 80,
            "ed_triage_sbp_mean": 120,
            "ed_triage_dbp_mean": 80,
            "ed_triage_heart_rate_mean": 80,
            "icu_sbp_mean": 120,
            "icu_dbp_mean": 80,
            "icu_heart_rate_mean": 80,
        },
    },
    {
        "factor_group": "მეტაბოლური პროფილი",
        "current_profile": "პაციენტის BMI, გლუკოზა, დიაბეტი და სიმსუქნის ისტორია ერთად",
        "reference_profile": "reference პროფილი: BMI 25, გლუკოზა 100 mg/dL, დიაბეტი/სიმსუქნე არ არის",
        "values": {
            "omr_bmi_mean": 25,
            "lab_glucose_mean": 100,
            "history_diabetes": 0,
            "history_obesity": 0,
        },
    },
    {
        "factor_group": "გულის ბიომარკერები",
        "current_profile": "პაციენტის NT-proBNP და Troponin T მაჩვენებლები",
        "reference_profile": "reference პროფილი: NT-proBNP 300, Troponin T 0.01",
        "values": {
            "lab_ntprobnp_mean": 300,
            "lab_troponin_t_mean": 0.01,
        },
    },
    {
        "factor_group": "გადაუდებელი სიმპტომები",
        "current_profile": "პაციენტის ჩივილები: ტკივილი, გულმკერდის ტკივილი, ქოშინი, გულის ფრიალი, სინკოპე, თავბრუსხვევა, შეშუპება",
        "reference_profile": "reference პროფილი: აღნიშნული სიმპტომები არ ფიქსირდება და ტკივილის ქულა 0-ია",
        "values": {
            "triage_pain_mean": 0,
            "symptom_chest_pain": 0,
            "symptom_shortness_of_breath": 0,
            "symptom_palpitations": 0,
            "symptom_syncope": 0,
            "symptom_dizziness": 0,
            "symptom_edema": 0,
        },
    },
    {
        "factor_group": "თირკმელი და სისხლის მაჩვენებლები",
        "current_profile": "პაციენტის კრეატინინი, ჰემოგლობინი და თირკმლის ქრონიკული დაავადების ისტორია",
        "reference_profile": "reference პროფილი: კრეატინინი 1.0, ჰემოგლობინი 13.0, თირკმლის ქრონიკული დაავადება არ არის",
        "values": {
            "lab_creatinine_mean": 1.0,
            "lab_hemoglobin_mean": 13.0,
            "history_chronic_kidney_disease": 0,
        },
    },
    {
        "factor_group": "ლიპიდური პროფილი",
        "current_profile": "პაციენტის საერთო ქოლესტერინი, LDL, HDL და ტრიგლიცერიდები",
        "reference_profile": "reference პროფილი: საერთო ქოლესტერინი 180, LDL 100, HDL 50, ტრიგლიცერიდები 150",
        "values": {
            "lab_chol_total_mean": 180,
            "lab_ldl_calc_mean": 100,
            "lab_hdl_mean": 50,
            "lab_triglycerides_mean": 150,
        },
    },
]


class FeatureValidationError(ValueError):
    def __init__(self, missing: list[str], extra: list[str]) -> None:
        self.missing = missing
        self.extra = extra
        super().__init__("Invalid feature payload.")


def risk_level(probability: float) -> str:
    if probability >= 0.75:
        return "high"
    if probability >= 0.40:
        return "medium"
    return "low"


def diagnosis_confidence(probability: float, threshold: float) -> str:
    high_threshold = min(0.95, threshold + 0.15)
    if probability >= high_threshold:
        return "high"
    if probability >= threshold:
        return "diagnostic_signal"
    if probability >= threshold * 0.75:
        return "borderline"
    return "low"


def diagnosis_status(confidence: str) -> str:
    if confidence == "high":
        return "ძლიერი სავარაუდო დიაგნოზის ჯგუფი"
    if confidence == "diagnostic_signal":
        return "სავარაუდო დიაგნოზის ჯგუფი"
    if confidence == "borderline":
        return "სუსტი/საზღვრული დამხმარე სიგნალი"
    return "დაბალი დიაგნოსტიკური მხარდაჭერა"


def is_available(row: dict[str, float], feature: str) -> bool:
    if feature not in row:
        return False
    if float(row.get(f"{feature}_missing", 0.0)) >= 0.5:
        return False
    value = row.get(feature)
    return value is not None and pd.notna(value)


def feature_value(row: dict[str, float], feature: str, default: float = 0.0) -> float:
    if not is_available(row, feature):
        return default
    return float(row[feature])


def flag(row: dict[str, float], feature: str) -> bool:
    return feature_value(row, feature) >= 0.5


def add_signal(signals: list[tuple[int, str]], condition: bool, score: int, text: str) -> None:
    if condition:
        signals.append((score, text))


def clinical_support_for_target(target: str, row: dict[str, float]) -> dict[str, Any]:
    troponin = feature_value(row, "lab_troponin_t_mean")
    ntprobnp = feature_value(row, "lab_ntprobnp_mean")
    creatinine = feature_value(row, "lab_creatinine_mean")
    sbp = max(feature_value(row, "omr_sbp_mean"), feature_value(row, "ed_triage_sbp_mean"))
    dbp = max(feature_value(row, "omr_dbp_mean"), feature_value(row, "ed_triage_dbp_mean"))
    heart_rate = feature_value(row, "ed_triage_heart_rate_mean")
    resp_rate = feature_value(row, "ed_triage_resp_rate_mean")
    spo2 = feature_value(row, "ed_triage_spo2_mean", 100.0)
    acuity = feature_value(row, "ed_triage_acuity_mean", 5.0)
    pain = feature_value(row, "triage_pain_mean")

    chest_pain = flag(row, "symptom_chest_pain")
    dyspnea = flag(row, "symptom_shortness_of_breath")
    palpitations = flag(row, "symptom_palpitations")
    syncope = flag(row, "symptom_syncope")
    dizziness = flag(row, "symptom_dizziness")
    edema = flag(row, "symptom_edema")
    diabetes = flag(row, "history_diabetes")
    kidney_history = flag(row, "history_chronic_kidney_disease")
    tobacco = flag(row, "history_tobacco_or_nicotine")
    ambulance = flag(row, "ed_arrived_by_ambulance")

    lipid_signal = any(
        [
            is_available(row, "lab_ldl_calc_mean") and feature_value(row, "lab_ldl_calc_mean") > 130,
            is_available(row, "lab_ldl_measured_mean") and feature_value(row, "lab_ldl_measured_mean") > 130,
            is_available(row, "lab_chol_total_mean") and feature_value(row, "lab_chol_total_mean") > 200,
            is_available(row, "lab_hdl_mean") and feature_value(row, "lab_hdl_mean") < 40,
            is_available(row, "lab_triglycerides_mean") and feature_value(row, "lab_triglycerides_mean") > 150,
        ]
    )

    signals: list[tuple[int, str]] = []

    if target in {"target_myocardial_infarction", "target_acute_ischemic_heart_disease"}:
        add_signal(signals, troponin > 0.01, 35, f"Troponin T მომატებულია ({format_numeric_value('lab_troponin_t_mean', troponin, 'ng/mL')})")
        add_signal(signals, chest_pain, 25, "მითითებულია გულმკერდის ტკივილი")
        add_signal(signals, pain >= 5, 10, f"ტკივილის შეფასება მაღალია ({round(pain, 1)} / 10)")
        add_signal(signals, dyspnea, 10, "თან ახლავს ქოშინი")
        add_signal(signals, diabetes or tobacco or lipid_signal, 10, "არსებობს კორონარული რისკ-ფაქტორები")
    elif target == "target_heart_failure":
        add_signal(signals, ntprobnp > 450, 35, f"NT-proBNP მომატებულია ({format_numeric_value('lab_ntprobnp_mean', ntprobnp, 'pg/mL')})")
        add_signal(signals, dyspnea, 25, "მითითებულია ქოშინი")
        add_signal(signals, edema, 20, "მითითებულია შეშუპება")
        add_signal(signals, spo2 < 95, 10, f"SpO2 დაბალია ({round(spo2)}%)")
        add_signal(signals, resp_rate > 20, 10, f"სუნთქვის სიხშირე მომატებულია ({round(resp_rate)} / min)")
    elif target in {"target_atrial_fibrillation_flutter", "target_paroxysmal_tachycardia", "target_other_arrhythmia"}:
        add_signal(signals, palpitations, 25, "მითითებულია გულის ფრიალი")
        add_signal(signals, heart_rate >= 110, 25, f"გულისცემა მაღალია ({round(heart_rate)} bpm)")
        add_signal(signals, syncope or dizziness, 20, "არის სინკოპე ან თავბრუსხვევა")
        add_signal(signals, dyspnea, 10, "თან ახლავს ქოშინი")
    elif target == "target_av_conduction_block":
        add_signal(signals, syncope or dizziness, 30, "არის სინკოპე ან თავბრუსხვევა")
        add_signal(signals, heart_rate and heart_rate <= 55, 25, f"გულისცემა დაბალია ({round(heart_rate)} bpm)")
        add_signal(signals, palpitations, 10, "მითითებულია გულის ფრიალი")
    elif target == "target_cardiac_arrest":
        add_signal(signals, acuity <= 2, 25, f"triage სიმძიმე მაღალია ({round(acuity)} / 5)")
        add_signal(signals, ambulance, 20, "პაციენტი სასწრაფოთი არის მოყვანილი")
        add_signal(signals, spo2 < 90, 20, f"SpO2 მკვეთრად დაბალია ({round(spo2)}%)")
        add_signal(signals, troponin > 0.01, 15, "Troponin T მომატებულია")
        add_signal(signals, heart_rate >= 130 or heart_rate <= 45, 10, "გულისცემის უკიდურესი მაჩვენებელია")
    elif target in {
        "target_primary_hypertension",
        "target_hypertensive_heart_disease",
        "target_hypertensive_kidney_disease",
        "target_hypertensive_heart_kidney_disease",
        "target_hypertensive_crisis",
    }:
        severe_pressure = sbp >= 180 or dbp >= 120
        high_pressure = sbp >= 140 or dbp >= 90
        add_signal(signals, severe_pressure, 35, f"წნევა ძალიან მაღალია ({round(sbp)}/{round(dbp)} mmHg)")
        add_signal(signals, high_pressure and not severe_pressure, 25, f"წნევა მომატებულია ({round(sbp)}/{round(dbp)} mmHg)")
        add_signal(signals, kidney_history or creatinine > 1.3, 20, "არსებობს თირკმლის დაზიანების/კრეატინინის სიგნალი")
        add_signal(signals, target in {"target_hypertensive_heart_disease", "target_hypertensive_heart_kidney_disease"} and (dyspnea or edema or ntprobnp > 450), 20, "არის გულის დატვირთვის ან უკმარისობის დამხმარე ნიშნები")
        add_signal(signals, target == "target_hypertensive_crisis" and (chest_pain or dyspnea or dizziness or troponin > 0.01), 25, "მაღალ წნევას ახლავს ორგანული დაზიანების შესაძლო ნიშნები")
    elif target in {"target_angina_pectoris", "target_chronic_ischemic_heart_disease"}:
        add_signal(signals, chest_pain, 30, "მითითებულია გულმკერდის ტკივილი")
        add_signal(signals, diabetes or tobacco or lipid_signal, 25, "არის კორონარული რისკ-ფაქტორები")
        add_signal(signals, pain >= 4, 10, f"ტკივილის შეფასება მომატებულია ({round(pain, 1)} / 10)")
        add_signal(signals, dyspnea, 10, "თან ახლავს ქოშინი")
        add_signal(signals, troponin <= 0.01 and is_available(row, "lab_troponin_t_mean"), 10, "Troponin T მწვავე ინფარქტის სასარგებლოდ არ არის მკვეთრად მომატებული")
    elif target in {
        "target_subarachnoid_hemorrhage",
        "target_intracerebral_hemorrhage",
        "target_ischemic_stroke",
        "target_other_cerebrovascular_disease",
    }:
        add_signal(signals, dizziness or syncope, 25, "არის ნევროლოგიურად საყურადღებო თავბრუსხვევა/სინკოპე")
        add_signal(signals, sbp >= 160 or dbp >= 100, 20, f"წნევა მაღალია ({round(sbp)}/{round(dbp)} mmHg)")
        add_signal(signals, palpitations, 15, "არის არითმიის შესაძლო სიმპტომი")
        add_signal(signals, diabetes or kidney_history, 10, "არსებობს სისხლძარღვოვანი რისკ-ფაქტორები")

    if not signals:
        add_signal(signals, True, 10, "სპეციფიკური კლინიკური დამადასტურებელი ნიშანი მკვეთრად არ ჩანს")

    signals.sort(key=lambda item: item[0], reverse=True)
    score = min(100, sum(score for score, _text in signals))
    if score >= 70:
        level = "strong"
    elif score >= 40:
        level = "partial"
    else:
        level = "weak"

    return {
        "score": score,
        "level": level,
        "reasons": [text for _score, text in signals[:4]],
    }


def subtype_precision(thresholds: dict[str, Any], target: str) -> float | None:
    value = thresholds.get(target, {}).get("test", {}).get("precision")
    if value is None:
        return None
    return float(value)


def reliability_note(precision: float | None) -> str:
    if precision is None:
        return "ამ subtype-ის test precision ხელმისაწვდომი არ არის; პასუხი აუცილებლად გადაამოწმეთ კლინიკურად."
    if precision >= 0.5:
        level = "შედარებით მაღალი"
    elif precision >= 0.3:
        level = "საშუალო"
    else:
        level = "დაბალი"
    return f"ამ subtype-ზე test precision არის {precision:.2f} ({level}); დადებითი პასუხი გამოიყენეთ როგორც გადასამოწმებელი სიგნალი."


def verification_priority(confidence: str, support_level: str, precision: float | None) -> str:
    if confidence in {"high", "diagnostic_signal"} and support_level == "strong" and (precision is None or precision >= 0.3):
        return "კლინიკურად გამყარებული სავარაუდო მიმართულება"
    if confidence in {"high", "diagnostic_signal"} and support_level in {"strong", "partial"}:
        return "სასწრაფოდ გადასამოწმებელი სიგნალი"
    if confidence in {"high", "diagnostic_signal"}:
        return "მოდელის სიგნალი სუსტი კლინიკური მხარდაჭერით"
    if confidence == "borderline":
        return "საზღვრული სიგნალი"
    return "დაბალი პრიორიტეტი"


def calibrated_diagnosis_status(confidence: str, support_level: str, precision: float | None) -> str:
    if confidence in {"high", "diagnostic_signal"} and support_level == "strong" and (precision is None or precision >= 0.3):
        return "კლინიკურად გამყარებული სავარაუდო დიაგნოზის ჯგუფი"
    if confidence in {"high", "diagnostic_signal"} and support_level in {"strong", "partial"}:
        return "სავარაუდო დიაგნოზის ჯგუფი - საჭიროებს დადასტურებას"
    if confidence in {"high", "diagnostic_signal"}:
        return "მოდელის სიგნალი - კლინიკური მხარდაჭერა სუსტია"
    return diagnosis_status(confidence)


def diagnosis_interpretation(
    display_name: str,
    probability: float,
    threshold: float,
    confidence: str,
    factors: list[dict[str, Any]],
    support: dict[str, Any] | None = None,
    precision: float | None = None,
) -> str:
    probability_text = f"{round(probability * 100, 1)}%"
    threshold_text = f"{round(threshold * 100, 1)}%"
    increasing = [factor for factor in factors if factor["shap_value"] > 0]
    increasing_text = join_phrases([factor_phrase(factor) for factor in increasing[:4]])
    support_text = ""
    if support:
        support_text = (
            f" კლინიკური დამხმარე ქულა არის {support['score']}% "
            f"({', '.join(support['reasons'][:2])})."
        )
    precision_text = f" subtype-ის test precision არის {precision:.2f}." if precision is not None else ""

    if confidence in {"high", "diagnostic_signal"}:
        return (
            f"{display_name}: სიგნალი threshold-ს აჭარბებს ({probability_text} / ზღვარი {threshold_text}). "
            f"მთავარი დამხმარე ნიშნებია: {increasing_text}.{support_text}{precision_text}"
        )
    if confidence == "borderline":
        return (
            f"{display_name}: სიგნალი ახლოსაა threshold-თან, მაგრამ საკმარისად არ აჭარბებს მას "
            f"({probability_text} / ზღვარი {threshold_text}). ეს არის სუსტი/საზღვრული დამხმარე სიგნალი. "
            f"დამხმარე ნიშნებია: {increasing_text}.{support_text}"
        )
    return (
        f"{display_name}: სიგნალი threshold-ზე დაბალია ({probability_text} / ზღვარი {threshold_text}); "
        "ამ მონაცემებით ამ დიაგნოზის მხარდაჭერა სუსტია."
    )


def risk_explanation(level: str) -> str:
    if level == "high":
        return (
            "მაღალი რისკი ნიშნავს, რომ მოდელმა პაციენტის მონაცემებში ძლიერი მსგავსება "
            "დაინახა იმ პაციენტებთან, რომლებსაც მონაცემთა ბაზაში გულ-სისხლძარღვთა "
            "დაავადების დადებითი კლასი ჰქონდათ. ასეთი შემთხვევა ექიმმა ყურადღებით უნდა განიხილოს."
        )
    if level == "medium":
        return (
            "საშუალო რისკი ნიშნავს, რომ მოდელმა გარკვეული გულ-სისხლძარღვთა რისკის "
            "სიგნალები დაინახა, თუმცა შედეგი მკვეთრად დაბალი ან მაღალი არ არის. "
            "შესაძლოა საჭირო იყოს დამატებითი კლინიკური შეფასება ან ანალიზები."
        )
    return (
        "დაბალი რისკი ნიშნავს, რომ არსებულ მონაცემებში მოდელმა შედარებით ნაკლები "
        "გულ-სისხლძარღვთა რისკის სიგნალი დაინახა. ეს დაავადებას სრულად არ გამორიცხავს."
    )


def feature_group(feature: str) -> str:
    for prefix, group in FEATURE_GROUPS.items():
        if feature.startswith(prefix):
            return group
    return "სხვა კლინიკური მახასიათებლები"


def feature_label(feature: str) -> str:
    if feature.endswith("_missing"):
        base_feature = feature.removesuffix("_missing")
        return f"{FEATURE_LABELS.get(base_feature, base_feature)} აკლდა"
    if feature.endswith("_count"):
        base_feature = feature.removesuffix("_count")
        return f"{FEATURE_LABELS.get(base_feature, base_feature)} - ჩანაწერების რაოდენობა"
    return FEATURE_LABELS.get(feature, feature)


def format_feature_value(feature: str, value: float) -> str:
    if feature == "gender_male":
        return "მამრობითი" if value >= 0.5 else "მდედრობითი"
    if feature.startswith("history_") or feature.startswith("symptom_"):
        return "დიახ" if value >= 0.5 else "არა"
    if feature.endswith("_missing"):
        return "აკლდა" if value >= 0.5 else "არსებობდა"
    if feature.endswith("_count"):
        return str(round(value, 1))
    return str(round(value, 2))


def format_numeric_value(feature: str, value: float, unit: str = "") -> str:
    if feature == "lab_troponin_t_mean":
        formatted = f"{value:.3f}"
    elif feature in {"lab_creatinine_mean", "lab_glucose_mean"}:
        formatted = f"{value:.2f}"
    elif abs(value) >= 100:
        formatted = str(round(value))
    else:
        formatted = str(round(value, 1))
    return f"{formatted} {unit}".strip()


def value_status(feature: str, value: float) -> str | None:
    reference = FEATURE_REFERENCE_RANGES.get(feature)
    if not reference:
        return None
    low, high, _unit = reference
    if value < low:
        return "დაბალი"
    if value > high:
        return "მაღალი"
    return "ნორმაში"


def clinical_factor_label(factor: dict[str, Any]) -> str:
    feature = factor["feature"]
    value = float(factor["value"])
    label = feature_label(feature)

    if feature == "age":
        return f"ასაკი: {round(value)} წელი"
    if feature == "gender_male":
        return f"სქესი: {format_feature_value(feature, value)}"
    if feature.startswith("history_") or feature.startswith("symptom_") or feature == "ed_arrived_by_ambulance":
        return label if value >= 0.5 else f"{label}: არა"
    if feature == "ed_triage_acuity_mean":
        return f"triage სიმძიმე: {round(value)} / 5"
    if feature == "triage_pain_mean":
        return f"ტკივილის შეფასება: {round(value, 1)} / 10"
    if feature in FEATURE_REFERENCE_RANGES:
        _low, _high, unit = FEATURE_REFERENCE_RANGES[feature]
        status = value_status(feature, value)
        formatted = format_numeric_value(feature, value, unit)
        if status == "ნორმაში":
            return f"{label}: {formatted} (ნორმაში)"
        return f"{status} {label}: {formatted}"
    if feature.startswith("interaction_"):
        return f"{label}: {format_numeric_value(feature, value)}"
    return f"{label}: {format_feature_value(feature, value)}"


def factor_phrase(factor: dict[str, Any]) -> str:
    return clinical_factor_label(factor)


def short_factor_label(factor: dict[str, Any]) -> str:
    if factor["feature"].endswith("_missing") and factor["value"] < 0.5:
        return f"{feature_label(factor['feature'].removesuffix('_missing'))} მითითებულია"
    return clinical_factor_label(factor)


def is_user_facing_positive_factor(factor: dict[str, Any]) -> bool:
    if factor["shap_value"] <= 0:
        return False
    if factor["feature"].endswith("_missing"):
        return False
    if factor["feature"].endswith("_count"):
        return False
    return True


def user_facing_factors(factors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [factor for factor in factors if not factor["feature"].endswith("_missing") and not factor["feature"].endswith("_count")]


def join_phrases(phrases: list[str]) -> str:
    if not phrases:
        return "მკვეთრი ფაქტორი არ გამოიკვეთა"
    if len(phrases) == 1:
        return phrases[0]
    return ", ".join(phrases[:-1]) + " და " + phrases[-1]


def analytical_summary(
    probability: float, level: str, factors: list[dict[str, Any]]
) -> str:
    increasing = [factor for factor in factors if factor["shap_value"] > 0]
    decreasing = [factor for factor in factors if factor["shap_value"] < 0]

    probability_text = f"{round(probability * 100, 1)}%"
    risk_text = {
        "high": "მაღალი",
        "medium": "საშუალო",
        "low": "დაბალი",
    }[level]

    increasing_text = join_phrases([factor_phrase(factor) for factor in increasing[:4]])
    decreasing_text = join_phrases([factor_phrase(factor) for factor in decreasing[:3]])

    return (
        f"ამ პაციენტის საერთო გულ-სისხლძარღვთა რისკი არის {probability_text}, "
        f"რაც შეფასებულია როგორც {risk_text} რისკი. რისკის ზრდისკენ ყველაზე მეტად "
        f"მიუთითებს: {increasing_text}. რისკის შემცირებისკენ ან დაბალ მსგავსებაზე "
        f"მიუთითებს: {decreasing_text}. ამ შედეგის კლინიკური შინაარსი ასეთია: "
        f"პაციენტის ასაკობრივი, ლაბორატორიული, წნევის, სიმპტომებისა და სასიცოცხლო ნიშნების "
        f"პროფილი მთლიანობაში ჰგავს იმ პაციენტების პროფილს, ვისთანაც მონაცემებში "
        f"გულ-სისხლძარღვთა დიაგნოზი დაფიქსირდა."
    )


def recompute_interactions(row: dict[str, float]) -> None:
    if {"age", "omr_sbp_mean", "interaction_age_omr_sbp"}.issubset(row):
        row["interaction_age_omr_sbp"] = row["age"] * row["omr_sbp_mean"]
    if {"omr_bmi_mean", "omr_sbp_mean", "interaction_bmi_omr_sbp"}.issubset(row):
        row["interaction_bmi_omr_sbp"] = row["omr_bmi_mean"] * row["omr_sbp_mean"]
    if {"lab_glucose_mean", "omr_bmi_mean", "interaction_glucose_bmi"}.issubset(row):
        row["interaction_glucose_bmi"] = row["lab_glucose_mean"] * row["omr_bmi_mean"]
    if {"lab_ntprobnp_mean", "age", "interaction_ntprobnp_age"}.issubset(row):
        row["interaction_ntprobnp_age"] = row["lab_ntprobnp_mean"] * row["age"]


def set_demo_value(row: dict[str, float], key: str, value: float, count: float = 1.0) -> None:
    if key not in row:
        return
    row[key] = float(value)
    missing_key = f"{key}_missing"
    count_key = f"{key}_count"
    count_missing_key = f"{count_key}_missing"
    if missing_key in row:
        row[missing_key] = 0.0
    if count_key in row:
        row[count_key] = float(count)
    if count_missing_key in row:
        row[count_missing_key] = 0.0


def set_demo_symptom(row: dict[str, float], key: str, present: bool) -> None:
    if key in row:
        row[key] = 1.0 if present else 0.0
    missing_key = f"{key}_missing"
    if missing_key in row:
        row[missing_key] = 0.0


class ModelService:
    @cached_property
    def model(self) -> Any:
        return joblib.load(MODEL_PATH)

    @cached_property
    def feature_columns(self) -> list[str]:
        return json.loads(FEATURES_PATH.read_text(encoding="utf-8"))

    @cached_property
    def explainer(self) -> Any:
        import shap

        return shap.TreeExplainer(self.model)

    @cached_property
    def subtype_models(self) -> dict[str, Any]:
        models: dict[str, Any] = {}
        for target in SUBTYPE_LABELS:
            path = SUBTYPE_MODEL_DIR / f"{target}.pkl"
            if path.exists():
                models[target] = joblib.load(path)
        return models

    @cached_property
    def diagnosis_thresholds(self) -> dict[str, Any]:
        if not DIAGNOSIS_THRESHOLDS_PATH.exists():
            return {}
        return json.loads(DIAGNOSIS_THRESHOLDS_PATH.read_text(encoding="utf-8"))

    @cached_property
    def subtype_explainers(self) -> dict[str, Any]:
        import shap

        return {
            target: shap.TreeExplainer(model)
            for target, model in self.subtype_models.items()
        }

    @cached_property
    def demo_base_row(self) -> tuple[pd.Series, dict[str, float]]:
        df = pd.read_csv(DATA_PATH)
        test_df = df[df["split_hint"].eq("test")]
        source_row = test_df.iloc[0]
        features = {
            column: float(source_row[column])
            for column in self.feature_columns
        }
        return source_row, features

    @cached_property
    def sample_patient(self) -> dict[str, Any]:
        return self.sample_patient_by_id("demo-1")

    def sample_patient_by_id(self, sample_id: str = "demo-1") -> dict[str, Any]:
        source_row, features = self.demo_base_row
        profiles: dict[str, dict[str, Any]] = {
            "demo-1": {
                "label": "სატესტო პაციენტი 1",
                "source": "კომპლექსური დემო პაციენტი: გულის უკმარისობის/ჰიპერტენზიული პროფილი",
                "values": {
                    "age": 76,
                    "gender_male": 0,
                    "history_diabetes": 1,
                    "history_chronic_kidney_disease": 1,
                    "history_obesity": 1,
                    "history_tobacco_or_nicotine": 1,
                    "omr_weight_lbs_mean": 194.0,
                    "omr_height_inches_mean": 64.6,
                    "omr_bmi_mean": 32.7,
                    "omr_sbp_mean": 164,
                    "omr_dbp_mean": 92,
                    "ed_triage_temperature_f_mean": 98.8,
                    "ed_triage_heart_rate_mean": 118,
                    "ed_triage_resp_rate_mean": 28,
                    "ed_triage_spo2_mean": 89,
                    "ed_triage_sbp_mean": 168,
                    "ed_triage_dbp_mean": 96,
                    "ed_triage_acuity_mean": 2,
                    "triage_pain_mean": 6,
                    "ed_arrived_by_ambulance": 1,
                    "lab_creatinine_mean": 1.82,
                    "lab_hemoglobin_mean": 10.9,
                    "lab_triglycerides_mean": 225,
                    "lab_chol_ratio_mean": 7.0,
                    "lab_hdl_mean": 34,
                    "lab_ntprobnp_mean": 9800,
                    "lab_ldl_measured_mean": 160,
                    "lab_platelets_mean": 310,
                    "lab_troponin_t_mean": 0.14,
                    "lab_glucose_mean": 186,
                    "lab_chol_total_mean": 238,
                    "lab_ldl_calc_mean": 158,
                },
                "symptoms": {
                    "symptom_chest_pain": True,
                    "symptom_shortness_of_breath": True,
                    "symptom_palpitations": True,
                    "symptom_syncope": False,
                    "symptom_dizziness": True,
                    "symptom_edema": True,
                },
                "symptom_text": (
                    "პაციენტი სასწრაფოთი მოყვანილია. აქვს ძლიერი ქოშინი დატვირთვისა და მოსვენებისას, "
                    "გულმკერდის მოჭერის ტიპის ტკივილი, გულის ფრიალი, თავბრუსხვევა და ქვედა კიდურების შეშუპება. "
                    "გულის წასვლა არ ჰქონია."
                ),
                "ecg_finding": "st_depression",
                "ecg_note": "ლატერალურ განხრებში აღინიშნება ST სეგმენტის დაწევა; აღწერილია არარეგულარული რიტმი და საჭიროა წინაგულთა ფიბრილაციის გამორიცხვა.",
            },
            "demo-2": {
                "label": "სატესტო პაციენტი 2",
                "source": "კომპლექსური დემო პაციენტი: მწვავე კორონარული სინდრომის/ინფარქტის მსგავსი პროფილი",
                "values": {
                    "age": 68,
                    "gender_male": 1,
                    "history_diabetes": 1,
                    "history_chronic_kidney_disease": 0,
                    "history_obesity": 0,
                    "history_tobacco_or_nicotine": 1,
                    "omr_weight_lbs_mean": 183.0,
                    "omr_height_inches_mean": 68.0,
                    "omr_bmi_mean": 27.8,
                    "omr_sbp_mean": 172,
                    "omr_dbp_mean": 98,
                    "ed_triage_temperature_f_mean": 98.4,
                    "ed_triage_heart_rate_mean": 106,
                    "ed_triage_resp_rate_mean": 24,
                    "ed_triage_spo2_mean": 94,
                    "ed_triage_sbp_mean": 184,
                    "ed_triage_dbp_mean": 102,
                    "ed_triage_acuity_mean": 2,
                    "triage_pain_mean": 9,
                    "ed_arrived_by_ambulance": 1,
                    "lab_creatinine_mean": 1.25,
                    "lab_hemoglobin_mean": 13.2,
                    "lab_triglycerides_mean": 260,
                    "lab_chol_ratio_mean": 6.2,
                    "lab_hdl_mean": 35,
                    "lab_ntprobnp_mean": 850,
                    "lab_ldl_measured_mean": 178,
                    "lab_platelets_mean": 285,
                    "lab_troponin_t_mean": 3.2,
                    "lab_glucose_mean": 174,
                    "lab_chol_total_mean": 256,
                    "lab_ldl_calc_mean": 176,
                },
                "symptoms": {
                    "symptom_chest_pain": True,
                    "symptom_shortness_of_breath": True,
                    "symptom_palpitations": False,
                    "symptom_syncope": False,
                    "symptom_dizziness": False,
                    "symptom_edema": False,
                },
                "symptom_text": "პაციენტს აქვს მწვავე, ძლიერი გულმკერდის ტკივილი, ქოშინი და ცივი ოფლიანობა. ტკივილი დაიწყო ბოლო საათებში.",
                "ecg_finding": "st_elevation",
                "ecg_note": "ქვედა განხრებში აღინიშნება ST სეგმენტის აწევა; სერიული Troponin T მკვეთრად მომატებულია.",
            },
            "demo-3": {
                "label": "სატესტო პაციენტი 3",
                "source": "კომპლექსური დემო პაციენტი: არითმიის/წინაგულთა ფიბრილაციის მსგავსი პროფილი",
                "values": {
                    "age": 72,
                    "gender_male": 1,
                    "history_diabetes": 0,
                    "history_chronic_kidney_disease": 0,
                    "history_obesity": 0,
                    "history_tobacco_or_nicotine": 1,
                    "omr_weight_lbs_mean": 176.0,
                    "omr_height_inches_mean": 69.0,
                    "omr_bmi_mean": 26.0,
                    "omr_sbp_mean": 140,
                    "omr_dbp_mean": 84,
                    "ed_triage_temperature_f_mean": 98.1,
                    "ed_triage_heart_rate_mean": 146,
                    "ed_triage_resp_rate_mean": 22,
                    "ed_triage_spo2_mean": 96,
                    "ed_triage_sbp_mean": 132,
                    "ed_triage_dbp_mean": 80,
                    "ed_triage_acuity_mean": 2,
                    "triage_pain_mean": 3,
                    "ed_arrived_by_ambulance": 1,
                    "lab_creatinine_mean": 1.05,
                    "lab_hemoglobin_mean": 13.8,
                    "lab_triglycerides_mean": 160,
                    "lab_chol_ratio_mean": 4.5,
                    "lab_hdl_mean": 44,
                    "lab_ntprobnp_mean": 1600,
                    "lab_ldl_measured_mean": 118,
                    "lab_platelets_mean": 245,
                    "lab_troponin_t_mean": 0.04,
                    "lab_glucose_mean": 112,
                    "lab_chol_total_mean": 198,
                    "lab_ldl_calc_mean": 122,
                },
                "symptoms": {
                    "symptom_chest_pain": False,
                    "symptom_shortness_of_breath": True,
                    "symptom_palpitations": True,
                    "symptom_syncope": True,
                    "symptom_dizziness": True,
                    "symptom_edema": False,
                },
                "symptom_text": "პაციენტს აქვს გულის ფრიალი, თავბრუსხვევა და მოკლე სინკოპე. გულმკერდის ტკივილს უარყოფს.",
                "ecg_finding": "atrial_fibrillation",
                "ecg_note": "აღწერილია არარეგულარულად არარეგულარული რიტმი, რაც წინაგულთა ფიბრილაციის სურათს შეესაბამება.",
            },
            "demo-4": {
                "label": "სატესტო პაციენტი 4",
                "source": "სატესტო პაციენტი: შედარებით დაბალი რისკის კონტრასტული პროფილი",
                "values": {
                    "age": 36,
                    "gender_male": 0,
                    "history_diabetes": 0,
                    "history_chronic_kidney_disease": 0,
                    "history_obesity": 0,
                    "history_tobacco_or_nicotine": 0,
                    "omr_weight_lbs_mean": 139.0,
                    "omr_height_inches_mean": 66.0,
                    "omr_bmi_mean": 22.4,
                    "omr_sbp_mean": 116,
                    "omr_dbp_mean": 74,
                    "ed_triage_temperature_f_mean": 98.2,
                    "ed_triage_heart_rate_mean": 72,
                    "ed_triage_resp_rate_mean": 16,
                    "ed_triage_spo2_mean": 99,
                    "ed_triage_sbp_mean": 118,
                    "ed_triage_dbp_mean": 76,
                    "ed_triage_acuity_mean": 4,
                    "triage_pain_mean": 0,
                    "ed_arrived_by_ambulance": 0,
                    "lab_creatinine_mean": 0.78,
                    "lab_hemoglobin_mean": 13.6,
                    "lab_triglycerides_mean": 105,
                    "lab_chol_ratio_mean": 3.1,
                    "lab_hdl_mean": 58,
                    "lab_ntprobnp_mean": 75,
                    "lab_ldl_measured_mean": 92,
                    "lab_platelets_mean": 250,
                    "lab_troponin_t_mean": 0.01,
                    "lab_glucose_mean": 91,
                    "lab_chol_total_mean": 174,
                    "lab_ldl_calc_mean": 96,
                },
                "symptoms": {
                    "symptom_chest_pain": False,
                    "symptom_shortness_of_breath": False,
                    "symptom_palpitations": False,
                    "symptom_syncope": False,
                    "symptom_dizziness": False,
                    "symptom_edema": False,
                },
                "symptom_text": "პაციენტი უარყოფს გულმკერდის ტკივილს, ქოშინს, გულის ფრიალს, თავბრუსხვევას და შეშუპებას.",
                "ecg_finding": "normal",
                "ecg_note": "სინუსური რიტმი; მწვავე იშემიური ცვლილებები აღწერილი არ არის.",
            },
            "demo-5": {
                "label": "სატესტო პაციენტი 5",
                "source": "კომპლექსური დემო პაციენტი: ჰიპერტენზიული გულის დაავადების მსგავსი პროფილი",
                "values": {
                    "age": 64,
                    "gender_male": 0,
                    "history_diabetes": 1,
                    "history_chronic_kidney_disease": 0,
                    "history_obesity": 1,
                    "history_tobacco_or_nicotine": 0,
                    "omr_weight_lbs_mean": 205.0,
                    "omr_height_inches_mean": 64.0,
                    "omr_bmi_mean": 35.2,
                    "omr_sbp_mean": 178,
                    "omr_dbp_mean": 104,
                    "ed_triage_temperature_f_mean": 98.6,
                    "ed_triage_heart_rate_mean": 96,
                    "ed_triage_resp_rate_mean": 21,
                    "ed_triage_spo2_mean": 95,
                    "ed_triage_sbp_mean": 186,
                    "ed_triage_dbp_mean": 108,
                    "ed_triage_acuity_mean": 3,
                    "triage_pain_mean": 2,
                    "ed_arrived_by_ambulance": 0,
                    "lab_creatinine_mean": 1.18,
                    "lab_hemoglobin_mean": 12.6,
                    "lab_triglycerides_mean": 210,
                    "lab_chol_ratio_mean": 5.8,
                    "lab_hdl_mean": 38,
                    "lab_ntprobnp_mean": 720,
                    "lab_ldl_measured_mean": 145,
                    "lab_platelets_mean": 275,
                    "lab_troponin_t_mean": 0.02,
                    "lab_glucose_mean": 162,
                    "lab_chol_total_mean": 224,
                    "lab_ldl_calc_mean": 148,
                },
                "symptoms": {
                    "symptom_chest_pain": False,
                    "symptom_shortness_of_breath": True,
                    "symptom_palpitations": False,
                    "symptom_syncope": False,
                    "symptom_dizziness": True,
                    "symptom_edema": True,
                },
                "symptom_text": "პაციენტს აქვს ხანგრძლივი მაღალი წნევა, ქოშინი კიბეზე ასვლისას, თავბრუსხვევა და მსუბუქი შეშუპება. მკვეთრ გულმკერდის ტკივილს უარყოფს.",
                "ecg_finding": "other_abnormal",
                "ecg_note": "სავარაუდოა მარცხენა პარკუჭის დატვირთვის სურათი; მწვავე ST სეგმენტის აწევა აღწერილი არ არის.",
            },
            "demo-6": {
                "label": "სატესტო პაციენტი 6",
                "source": "კომპლექსური დემო პაციენტი: ჰიპერტენზიული კრიზის მსგავსი პროფილი",
                "values": {
                    "age": 58,
                    "gender_male": 1,
                    "history_diabetes": 0,
                    "history_chronic_kidney_disease": 1,
                    "history_obesity": 0,
                    "history_tobacco_or_nicotine": 1,
                    "omr_weight_lbs_mean": 186.0,
                    "omr_height_inches_mean": 70.0,
                    "omr_bmi_mean": 26.7,
                    "omr_sbp_mean": 196,
                    "omr_dbp_mean": 118,
                    "ed_triage_temperature_f_mean": 98.7,
                    "ed_triage_heart_rate_mean": 104,
                    "ed_triage_resp_rate_mean": 23,
                    "ed_triage_spo2_mean": 96,
                    "ed_triage_sbp_mean": 214,
                    "ed_triage_dbp_mean": 126,
                    "ed_triage_acuity_mean": 2,
                    "triage_pain_mean": 5,
                    "ed_arrived_by_ambulance": 1,
                    "lab_creatinine_mean": 1.75,
                    "lab_hemoglobin_mean": 13.4,
                    "lab_triglycerides_mean": 180,
                    "lab_chol_ratio_mean": 5.2,
                    "lab_hdl_mean": 40,
                    "lab_ntprobnp_mean": 620,
                    "lab_ldl_measured_mean": 136,
                    "lab_platelets_mean": 290,
                    "lab_troponin_t_mean": 0.05,
                    "lab_glucose_mean": 128,
                    "lab_chol_total_mean": 208,
                    "lab_ldl_calc_mean": 136,
                },
                "symptoms": {
                    "symptom_chest_pain": True,
                    "symptom_shortness_of_breath": True,
                    "symptom_palpitations": False,
                    "symptom_syncope": False,
                    "symptom_dizziness": True,
                    "symptom_edema": False,
                },
                "symptom_text": "პაციენტი სასწრაფოთი მოყვანილია ძალიან მაღალი წნევით, ძლიერი თავის ტკივილით, თავბრუსხვევით, ქოშინით და გულმკერდის დისკომფორტით.",
                "ecg_finding": "st_depression",
                "ecg_note": "აღინიშნება არასპეციფიკური ST-T ცვლილებები; triage-ზე დაფიქსირდა მძიმე ჰიპერტენზია.",
            },
            "demo-7": {
                "label": "სატესტო პაციენტი 7",
                "source": "კომპლექსური დემო პაციენტი: ქრონიკული იშემიური დაავადების/სტენოკარდიის მსგავსი პროფილი",
                "values": {
                    "age": 70,
                    "gender_male": 1,
                    "history_diabetes": 1,
                    "history_chronic_kidney_disease": 0,
                    "history_obesity": 0,
                    "history_tobacco_or_nicotine": 1,
                    "omr_weight_lbs_mean": 174.0,
                    "omr_height_inches_mean": 67.0,
                    "omr_bmi_mean": 27.3,
                    "omr_sbp_mean": 154,
                    "omr_dbp_mean": 88,
                    "ed_triage_temperature_f_mean": 98.2,
                    "ed_triage_heart_rate_mean": 92,
                    "ed_triage_resp_rate_mean": 20,
                    "ed_triage_spo2_mean": 97,
                    "ed_triage_sbp_mean": 158,
                    "ed_triage_dbp_mean": 90,
                    "ed_triage_acuity_mean": 3,
                    "triage_pain_mean": 6,
                    "ed_arrived_by_ambulance": 0,
                    "lab_creatinine_mean": 1.1,
                    "lab_hemoglobin_mean": 13.0,
                    "lab_triglycerides_mean": 240,
                    "lab_chol_ratio_mean": 6.0,
                    "lab_hdl_mean": 36,
                    "lab_ntprobnp_mean": 390,
                    "lab_ldl_measured_mean": 170,
                    "lab_platelets_mean": 260,
                    "lab_troponin_t_mean": 0.02,
                    "lab_glucose_mean": 155,
                    "lab_chol_total_mean": 246,
                    "lab_ldl_calc_mean": 168,
                },
                "symptoms": {
                    "symptom_chest_pain": True,
                    "symptom_shortness_of_breath": True,
                    "symptom_palpitations": False,
                    "symptom_syncope": False,
                    "symptom_dizziness": False,
                    "symptom_edema": False,
                },
                "symptom_text": "პაციენტს აქვს განმეორებითი გულმკერდის ტკივილი დატვირთვაზე, ქოშინი სიარულისას და მაღალი ქოლესტერინის ისტორია.",
                "ecg_finding": "st_depression",
                "ecg_note": "სიმპტომების დროს აღინიშნება ST სეგმენტის დაწევა; გასათვალისწინებელია ქრონიკული იშემიური სურათი.",
            },
            "demo-8": {
                "label": "სატესტო პაციენტი 8",
                "source": "კომპლექსური დემო პაციენტი: ცერებროვასკულური/ინსულტის მსგავსი პროფილი",
                "values": {
                    "age": 81,
                    "gender_male": 0,
                    "history_diabetes": 1,
                    "history_chronic_kidney_disease": 1,
                    "history_obesity": 0,
                    "history_tobacco_or_nicotine": 0,
                    "omr_weight_lbs_mean": 158.0,
                    "omr_height_inches_mean": 63.0,
                    "omr_bmi_mean": 28.0,
                    "omr_sbp_mean": 182,
                    "omr_dbp_mean": 96,
                    "ed_triage_temperature_f_mean": 98.5,
                    "ed_triage_heart_rate_mean": 88,
                    "ed_triage_resp_rate_mean": 20,
                    "ed_triage_spo2_mean": 95,
                    "ed_triage_sbp_mean": 190,
                    "ed_triage_dbp_mean": 100,
                    "ed_triage_acuity_mean": 2,
                    "triage_pain_mean": 1,
                    "ed_arrived_by_ambulance": 1,
                    "lab_creatinine_mean": 1.55,
                    "lab_hemoglobin_mean": 11.8,
                    "lab_triglycerides_mean": 170,
                    "lab_chol_ratio_mean": 5.4,
                    "lab_hdl_mean": 39,
                    "lab_ntprobnp_mean": 1100,
                    "lab_ldl_measured_mean": 142,
                    "lab_platelets_mean": 220,
                    "lab_troponin_t_mean": 0.03,
                    "lab_glucose_mean": 168,
                    "lab_chol_total_mean": 214,
                    "lab_ldl_calc_mean": 140,
                },
                "symptoms": {
                    "symptom_chest_pain": False,
                    "symptom_shortness_of_breath": False,
                    "symptom_palpitations": True,
                    "symptom_syncope": False,
                    "symptom_dizziness": True,
                    "symptom_edema": False,
                },
                "symptom_text": "პაციენტი სასწრაფოთი მოყვანილია უეცარი თავბრუსხვევით, სისუსტით და მეტყველების გაძნელებით. გულმკერდის ტკივილს უარყოფს.",
                "ecg_finding": "atrial_fibrillation",
                "ecg_note": "აღწერილია წინაგულთა ფიბრილაციის სურათი; კლინიკურად გასათვალისწინებელია ცერებროვასკულური მოვლენის რისკი.",
            },
        }

        profile = profiles.get(sample_id, profiles["demo-1"])
        for key, value in profile["values"].items():
            set_demo_value(features, key, value, count=2.0 if key.startswith("lab_") else 1.0)

        for key, present in profile["symptoms"].items():
            set_demo_symptom(features, key, present)

        recompute_interactions(features)
        for key in [
            "interaction_age_omr_sbp",
            "interaction_bmi_omr_sbp",
            "interaction_glucose_bmi",
            "interaction_ntprobnp_age",
        ]:
            if f"{key}_missing" in features:
                features[f"{key}_missing"] = 0.0

        return {
            "source": profile["source"],
            "sample_id": sample_id if sample_id in profiles else "demo-1",
            "sample_label": profile["label"],
            "row_index": -1,
            "original_csv_index": int(source_row.name),
            "actual_target": 1,
            "features": features,
            "symptom_text": profile["symptom_text"],
            "ecg_finding": profile["ecg_finding"],
            "ecg_note": profile["ecg_note"],
        }

    def validate_features(self, features: dict[str, float]) -> None:
        expected = set(self.feature_columns)
        received = set(features)
        missing = sorted(expected - received)
        extra = sorted(received - expected)
        if missing or extra:
            raise FeatureValidationError(missing=missing, extra=extra)

    def make_frame(self, features: dict[str, float]) -> pd.DataFrame:
        self.validate_features(features)
        row = {column: features[column] for column in self.feature_columns}
        return pd.DataFrame([row], columns=self.feature_columns)

    def probability_for_row(self, row: dict[str, float]) -> float:
        frame = pd.DataFrame(
            [{column: row[column] for column in self.feature_columns}],
            columns=self.feature_columns,
        )
        return float(self.model.predict_proba(frame)[:, 1][0])

    def explain_with(self, explainer: Any, patient: pd.DataFrame, top_n: int) -> list[dict[str, Any]]:
        shap_values = explainer.shap_values(patient)
        values = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]

        rows = []
        for feature, value, contribution in zip(patient.columns, patient.iloc[0], values):
            rows.append(
                {
                    "feature": feature,
                    "feature_group": feature_group(feature),
                    "value": float(value),
                    "shap_value": float(contribution),
                    "direction": "increases_risk" if contribution > 0 else "decreases_risk",
                }
            )

        rows.sort(key=lambda item: abs(item["shap_value"]), reverse=True)
        return rows[:top_n]

    def explain(self, patient: pd.DataFrame, top_n: int) -> list[dict[str, Any]]:
        return self.explain_with(self.explainer, patient, top_n)

    def subtype_explanation(
        self, display_name: str, probability: float, level: str, factors: list[dict[str, Any]]
    ) -> str:
        clinical_factors = user_facing_factors(factors)
        increasing = [factor for factor in clinical_factors if factor["shap_value"] > 0]
        decreasing = [factor for factor in clinical_factors if factor["shap_value"] < 0]
        increasing_text = join_phrases([factor_phrase(factor) for factor in increasing[:3]])
        decreasing_text = join_phrases([factor_phrase(factor) for factor in decreasing[:2]])
        probability_text = f"{round(probability * 100, 1)}%"

        if level == "high":
            strength = "ამ დაავადების მაღალი რისკის ჯგუფში ხვდება"
        elif level == "medium":
            strength = "ამ დაავადების საშუალო რისკის ჯგუფში ხვდება"
        else:
            strength = "ამ დაავადების დაბალი რისკის ჯგუფში ხვდება"

        return (
            f"{display_name}: {probability_text}. პაციენტი {strength}. "
            f"დიაგნოსტიკურ სიგნალს ზრდის: {increasing_text}. "
            f"სიგნალს ამცირებს ან ნაკლებად ამყარებს: {decreasing_text}."
        )

    def predict_subtypes(self, patient: pd.DataFrame) -> list[dict[str, Any]]:
        risks = []
        row = {column: float(patient.iloc[0][column]) for column in patient.columns}
        for target, model in self.subtype_models.items():
            probability = float(model.predict_proba(patient)[:, 1][0])
            level = risk_level(probability)
            display_name = SUBTYPE_LABELS[target]
            threshold = float(self.diagnosis_thresholds.get(target, {}).get("threshold", 0.5))
            confidence = diagnosis_confidence(probability, threshold)
            support = clinical_support_for_target(target, row)
            precision = subtype_precision(self.diagnosis_thresholds, target)
            factors = self.explain_with(self.subtype_explainers[target], patient, 12)
            reason_factors = [
                short_factor_label(factor)
                for factor in factors
                if is_user_facing_positive_factor(factor)
            ][:3]
            clinical_factors = user_facing_factors(factors)
            risks.append(
                {
                    "target_name": target,
                    "display_name": display_name,
                    "risk_probability": round(probability, 4),
                    "risk_level": level,
                    "diagnosis_label": display_name,
                    "diagnosis_probability": round(probability, 4),
                    "diagnosis_threshold": round(threshold, 4),
                    "diagnosis_status": calibrated_diagnosis_status(confidence, support["level"], precision),
                    "diagnosis_confidence": confidence,
                    "diagnosis_interpretation": diagnosis_interpretation(
                        display_name, probability, threshold, confidence, clinical_factors, support, precision
                    ),
                    "suggested_clinical_checks": CLINICAL_CHECKS.get(target, []),
                    "clinical_support_score": support["score"],
                    "clinical_support_level": support["level"],
                    "clinical_support_reasons": support["reasons"],
                    "reliability_note": reliability_note(precision),
                    "verification_priority": verification_priority(confidence, support["level"], precision),
                    "explanation": self.subtype_explanation(display_name, probability, level, clinical_factors),
                    "reason_factors": reason_factors,
                }
            )

        priority_rank = {
            "კლინიკურად გამყარებული სავარაუდო მიმართულება": 4,
            "სასწრაფოდ გადასამოწმებელი სიგნალი": 3,
            "მოდელის სიგნალი სუსტი კლინიკური მხარდაჭერით": 2,
            "საზღვრული სიგნალი": 1,
            "დაბალი პრიორიტეტი": 0,
        }
        risks.sort(
            key=lambda item: (
                priority_rank.get(item["verification_priority"], 0),
                item["clinical_support_score"],
                item["risk_probability"],
            ),
            reverse=True,
        )
        return risks

    def patient_counterfactual_analysis(
        self, features: dict[str, float], baseline_probability: float
    ) -> tuple[str, list[dict[str, Any]]]:
        impacts = []

        for group in COUNTERFACTUAL_GROUPS:
            candidate = {column: features[column] for column in self.feature_columns}
            changed = False
            for feature, reference_value in group["values"].items():
                if feature in candidate and abs(float(candidate[feature]) - float(reference_value)) > 1e-9:
                    candidate[feature] = float(reference_value)
                    if f"{feature}_missing" in candidate:
                        candidate[f"{feature}_missing"] = 0.0
                    changed = True

            if not changed:
                continue

            recompute_interactions(candidate)
            reference_probability = self.probability_for_row(candidate)
            risk_delta = baseline_probability - reference_probability
            if abs(risk_delta) < 0.01:
                continue

            direction = "ზრდის" if risk_delta > 0 else "ამცირებს"
            impacts.append(
                {
                    "factor_group": group["factor_group"],
                    "current_profile": group["current_profile"],
                    "reference_profile": group["reference_profile"],
                    "risk_delta": round(float(risk_delta), 4),
                    "explanation": (
                        f"ამ პაციენტში {group['factor_group']} საერთო რისკს {direction} "
                        f"{abs(risk_delta) * 100:.1f} პროცენტული პუნქტით, როდესაც მოდელი "
                        f"არსებულ პროფილს reference პროფილს ადარებს."
                    ),
                }
            )

        impacts.sort(key=lambda item: abs(item["risk_delta"]), reverse=True)
        top_impacts = impacts[:5]
        if top_impacts:
            top_text = join_phrases([impact["factor_group"] for impact in top_impacts[:3]])
            summary = (
                f"ახალი პაციენტის მოდელურმა ანალიზმა აჩვენა, რომ ამ კონკრეტული "
                f"პროგნოზისთვის ყველაზე მნიშვნელოვანი კლინიკური კომბინაციებია: {top_text}. "
                f"ეს ანალიზი ითვლის, როგორ შეიცვლებოდა რისკი იგივე პაციენტში, თუ ეს "
                f"ფაქტორები reference პროფილთან ახლოს იქნებოდა."
            )
        else:
            summary = (
                "ამ პაციენტში არც ერთმა ცალკე კლინიკურმა ჯგუფმა reference პროფილთან "
                "შედარებით მკვეთრი ცვლილება არ აჩვენა; პროგნოზი რამდენიმე მცირე "
                "სიგნალის ერთობლიობით არის მიღებული."
            )

        return summary, top_impacts

    def predict(self, features: dict[str, float], top_n: int) -> dict[str, Any]:
        patient = self.make_frame(features)
        probability = float(self.model.predict_proba(patient)[:, 1][0])
        level = risk_level(probability)
        factors = self.explain(patient, top_n)
        patient_analysis_summary, clinical_impacts = self.patient_counterfactual_analysis(
            features, probability
        )

        return {
            "target_name": TARGET_NAME,
            "display_target_name": DISPLAY_TARGET_NAME,
            "target_description": TARGET_DESCRIPTION,
            "risk_probability": round(probability, 4),
            "predicted_class": int(probability >= 0.5),
            "risk_level": level,
            "risk_explanation": risk_explanation(level),
            "analytical_summary": analytical_summary(probability, level, factors),
            "patient_analysis_summary": patient_analysis_summary,
            "clinical_impacts": clinical_impacts,
            "method_note": METHOD_NOTE,
            "subtype_note": SUBTYPE_NOTE,
            "subtype_risks": self.predict_subtypes(patient),
            "top_factors": factors,
        }


service = ModelService()
