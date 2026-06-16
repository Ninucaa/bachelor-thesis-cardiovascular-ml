from __future__ import annotations

import json
from functools import cached_property
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


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
    "target_myocardial_infarction": "მიოკარდიუმის ინფარქტი",
    "target_heart_failure": "გულის უკმარისობა",
    "target_stroke": "ინსულტი / ცერებროვასკულური დაავადება",
    "target_arrhythmia": "გულის არითმია",
    "target_hypertension": "ჰიპერტენზიული დაავადება",
    "target_coronary_artery_disease": "კორონარული არტერიის დაავადება",
}

CLINICAL_CHECKS = {
    "target_myocardial_infarction": [
        "ECG და ST/T ცვლილებების შეფასება",
        "Troponin-ის განმეორებითი კონტროლი",
        "გულმკერდის ტკივილის კლინიკური შეფასება",
    ],
    "target_heart_failure": [
        "NT-proBNP/BNP მაჩვენებლის გადამოწმება",
        "ფილტვების შეშუპებისა და პერიფერიული შეშუპების შეფასება",
        "ექოკარდიოგრაფიის განხილვა",
    ],
    "target_stroke": [
        "ნევროლოგიური სტატუსის შეფასება",
        "თავის ტვინის CT/MRI საჭიროების განხილვა",
        "არტერიული წნევისა და რისკ-ფაქტორების გადამოწმება",
    ],
    "target_arrhythmia": [
        "ECG rhythm strip-ის შეფასება",
        "ელექტროლიტებისა და გულისცემის მონიტორინგი",
        "პალპიტაციის/სინკოპეს ისტორიის გადამოწმება",
    ],
    "target_hypertension": [
        "არტერიული წნევის განმეორებითი გაზომვა",
        "თირკმლის ფუნქციისა და მეტაბოლური რისკების შეფასება",
        "ჰიპერტენზიის ისტორიის გადამოწმება",
    ],
    "target_coronary_artery_disease": [
        "იშემიური სიმპტომების და დატვირთვასთან კავშირის შეფასება",
        "ლიპიდური პროფილის და რისკ-ფაქტორების გადამოწმება",
        "ECG/ტროპონინის ან დამატებითი კარდიოლოგიური კვლევის განხილვა",
    ],
}

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
        return "საზღვრული დიაგნოსტიკური სიგნალი"
    return "დაბალი დიაგნოსტიკური მხარდაჭერა"


def diagnosis_interpretation(
    display_name: str,
    probability: float,
    threshold: float,
    confidence: str,
    factors: list[dict[str, Any]],
) -> str:
    probability_text = f"{round(probability * 100, 1)}%"
    threshold_text = f"{round(threshold * 100, 1)}%"
    increasing = [factor for factor in factors if factor["shap_value"] > 0]
    increasing_text = join_phrases([factor_phrase(factor) for factor in increasing[:3]])

    if confidence in {"high", "diagnostic_signal"}:
        return (
            f"{display_name}: მოდელის ალბათობა არის {probability_text}, რაც აჭარბებს "
            f"დიაგნოსტიკურ threshold-ს ({threshold_text}). ამიტომ სისტემა ამ შემთხვევას "
            f"აფასებს როგორც სავარაუდო ICD-კოდირებულ დიაგნოზის ჯგუფს. მხარდამჭერი ნიშნებია: "
            f"{increasing_text}."
        )
    if confidence == "borderline":
        return (
            f"{display_name}: მოდელის ალბათობა არის {probability_text}; ეს ახლოსაა "
            f"დიაგნოსტიკურ threshold-თან ({threshold_text}), მაგრამ საკმარისად არ აჭარბებს მას. "
            f"შედეგი უნდა ჩაითვალოს საზღვრულ სიგნალად. მხარდამჭერი ნიშნებია: {increasing_text}."
        )
    return (
        f"{display_name}: მოდელის ალბათობა არის {probability_text}, რაც დაბალია "
        f"დიაგნოსტიკურ threshold-ზე ({threshold_text}). ამ მონაცემებით დიაგნოზის ჯგუფის "
        f"მხარდაჭერა სუსტია."
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


def factor_phrase(factor: dict[str, Any]) -> str:
    return (
        f"{feature_label(factor['feature'])} "
        f"({format_feature_value(factor['feature'], factor['value'])})"
    )


def short_factor_label(factor: dict[str, Any]) -> str:
    if factor["feature"].endswith("_missing") and factor["value"] < 0.5:
        return f"{feature_label(factor['feature'].removesuffix('_missing'))} მითითებულია"
    return feature_label(factor["feature"])


def is_user_facing_positive_factor(factor: dict[str, Any]) -> bool:
    if factor["shap_value"] <= 0:
        return False
    if factor["feature"].endswith("_missing") and factor["value"] < 0.5:
        return False
    if factor["feature"].endswith("_count_missing") and factor["value"] < 0.5:
        return False
    return True


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
    def sample_patient(self) -> dict[str, Any]:
        df = pd.read_csv(DATA_PATH)
        test_df = df[df["split_hint"].eq("test")]
        row = test_df.iloc[0]
        return {
            "source": "cardio_time_aware_model_ready.csv ფაილის test split-ის პირველი ჩანაწერი",
            "row_index": 0,
            "original_csv_index": int(row.name),
            "actual_target": int(row["target_cvd"]),
            "features": {
                column: float(row[column])
                for column in self.feature_columns
            },
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
        increasing = [factor for factor in factors if factor["shap_value"] > 0]
        decreasing = [factor for factor in factors if factor["shap_value"] < 0]
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
        for target, model in self.subtype_models.items():
            probability = float(model.predict_proba(patient)[:, 1][0])
            level = risk_level(probability)
            display_name = SUBTYPE_LABELS[target]
            threshold = float(self.diagnosis_thresholds.get(target, {}).get("threshold", 0.5))
            confidence = diagnosis_confidence(probability, threshold)
            factors = self.explain_with(self.subtype_explainers[target], patient, 5)
            reason_factors = [
                short_factor_label(factor)
                for factor in factors
                if is_user_facing_positive_factor(factor)
            ][:3]
            risks.append(
                {
                    "target_name": target,
                    "display_name": display_name,
                    "risk_probability": round(probability, 4),
                    "risk_level": level,
                    "diagnosis_label": display_name,
                    "diagnosis_probability": round(probability, 4),
                    "diagnosis_threshold": round(threshold, 4),
                    "diagnosis_status": diagnosis_status(confidence),
                    "diagnosis_confidence": confidence,
                    "diagnosis_interpretation": diagnosis_interpretation(
                        display_name, probability, threshold, confidence, factors
                    ),
                    "suggested_clinical_checks": CLINICAL_CHECKS.get(target, []),
                    "explanation": self.subtype_explanation(display_name, probability, level, factors),
                    "reason_factors": reason_factors,
                }
            )

        risks.sort(key=lambda item: item["risk_probability"], reverse=True)
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
