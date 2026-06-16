from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.api.model_service import service

REPORT_JSON_PATH = PROJECT_DIR / "reports" / "demo_patient_tests.json"
REPORT_MD_PATH = PROJECT_DIR / "reports" / "demo_patient_tests_ge.md"


def set_value(features: dict[str, float], key: str, value: float) -> None:
    if key not in features:
        return
    features[key] = float(value)
    missing_key = f"{key}_missing"
    count_key = f"{key}_count"
    count_missing_key = f"{count_key}_missing"
    if missing_key in features:
        features[missing_key] = 0.0
    if count_key in features:
        features[count_key] = 1.0
    if count_missing_key in features:
        features[count_missing_key] = 0.0


def set_missing(features: dict[str, float], key: str) -> None:
    if key not in features:
        return
    missing_key = f"{key}_missing"
    count_key = f"{key}_count"
    count_missing_key = f"{count_key}_missing"
    if missing_key in features:
        features[missing_key] = 1.0
    if count_key in features:
        features[count_key] = 0.0
    if count_missing_key in features:
        features[count_missing_key] = 1.0


def set_symptom(features: dict[str, float], key: str, value: bool) -> None:
    if key in features:
        features[key] = 1.0 if value else 0.0
    missing_key = f"{key}_missing"
    if missing_key in features:
        features[missing_key] = 0.0


def recompute_interactions(features: dict[str, float]) -> None:
    if {"age", "omr_sbp_mean", "interaction_age_omr_sbp"}.issubset(features):
        features["interaction_age_omr_sbp"] = features["age"] * features["omr_sbp_mean"]
        features["interaction_age_omr_sbp_missing"] = 0.0
    if {"omr_bmi_mean", "omr_sbp_mean", "interaction_bmi_omr_sbp"}.issubset(features):
        features["interaction_bmi_omr_sbp"] = features["omr_bmi_mean"] * features["omr_sbp_mean"]
        features["interaction_bmi_omr_sbp_missing"] = 0.0
    if {"lab_glucose_mean", "omr_bmi_mean", "interaction_glucose_bmi"}.issubset(features):
        features["interaction_glucose_bmi"] = features["lab_glucose_mean"] * features["omr_bmi_mean"]
        features["interaction_glucose_bmi_missing"] = 0.0
    if {"lab_ntprobnp_mean", "age", "interaction_ntprobnp_age"}.issubset(features):
        features["interaction_ntprobnp_age"] = features["lab_ntprobnp_mean"] * features["age"]
        features["interaction_ntprobnp_age_missing"] = 0.0


def base_features() -> dict[str, float]:
    sample = service.sample_patient["features"]
    features = {key: float(value) for key, value in sample.items()}

    for key in [
        "symptom_chest_pain",
        "symptom_shortness_of_breath",
        "symptom_palpitations",
        "symptom_syncope",
        "symptom_dizziness",
        "symptom_edema",
    ]:
        set_symptom(features, key, False)

    return features


def scenario_low_risk() -> dict[str, Any]:
    features = base_features()
    set_value(features, "age", 34)
    set_value(features, "gender_male", 0)
    set_value(features, "omr_bmi_mean", 23.5)
    set_value(features, "omr_weight_lbs_mean", 143)
    set_value(features, "omr_height_inches_mean", 66)
    set_value(features, "omr_sbp_mean", 116)
    set_value(features, "omr_dbp_mean", 74)
    set_value(features, "ed_triage_heart_rate_mean", 72)
    set_value(features, "ed_triage_sbp_mean", 118)
    set_value(features, "ed_triage_dbp_mean", 76)
    set_value(features, "ed_triage_resp_rate_mean", 16)
    set_value(features, "ed_triage_spo2_mean", 99)
    set_value(features, "ed_triage_acuity_mean", 4)
    set_value(features, "triage_pain_mean", 0)
    set_value(features, "lab_troponin_t_mean", 0.01)
    set_value(features, "lab_ntprobnp_mean", 80)
    set_value(features, "lab_creatinine_mean", 0.8)
    set_value(features, "lab_glucose_mean", 92)
    set_value(features, "lab_hemoglobin_mean", 13.8)
    set_value(features, "lab_platelets_mean", 260)
    set_value(features, "lab_chol_total_mean", 170)
    set_value(features, "lab_hdl_mean", 55)
    set_value(features, "lab_ldl_calc_mean", 95)
    set_value(features, "lab_triglycerides_mean", 110)
    for key in ["history_diabetes", "history_chronic_kidney_disease", "history_obesity", "history_tobacco_or_nicotine", "ed_arrived_by_ambulance"]:
        set_value(features, key, 0)
    recompute_interactions(features)
    return {
        "name": "დაბალი რისკის/დაბალი დიაგნოსტიკური სიგნალის პაციენტი",
        "expected": "დაბალი საერთო სიგნალი და subtype-ებში threshold-ის გადაუკვეთავი შედეგები.",
        "symptom_text": "პაციენტი უარყოფს გულმკერდის ტკივილს, ქოშინს და გულის ფრიალს.",
        "features": features,
    }


def scenario_mi_like() -> dict[str, Any]:
    features = base_features()
    set_value(features, "age", 68)
    set_value(features, "gender_male", 1)
    set_value(features, "omr_bmi_mean", 31)
    set_value(features, "omr_sbp_mean", 168)
    set_value(features, "omr_dbp_mean", 96)
    set_value(features, "ed_triage_heart_rate_mean", 108)
    set_value(features, "ed_triage_sbp_mean", 176)
    set_value(features, "ed_triage_dbp_mean", 98)
    set_value(features, "ed_triage_resp_rate_mean", 24)
    set_value(features, "ed_triage_spo2_mean", 94)
    set_value(features, "ed_triage_acuity_mean", 2)
    set_value(features, "triage_pain_mean", 8)
    set_value(features, "lab_troponin_t_mean", 2.8)
    set_value(features, "lab_ntprobnp_mean", 900)
    set_value(features, "lab_creatinine_mean", 1.3)
    set_value(features, "lab_glucose_mean", 178)
    set_value(features, "lab_chol_total_mean", 245)
    set_value(features, "lab_hdl_mean", 36)
    set_value(features, "lab_ldl_calc_mean", 165)
    set_value(features, "lab_triglycerides_mean", 230)
    set_value(features, "history_diabetes", 1)
    set_value(features, "history_tobacco_or_nicotine", 1)
    set_value(features, "ed_arrived_by_ambulance", 1)
    set_symptom(features, "symptom_chest_pain", True)
    set_symptom(features, "symptom_shortness_of_breath", True)
    recompute_interactions(features)
    return {
        "name": "ინფარქტის მსგავსი პაციენტი",
        "expected": "მიოკარდიუმის ინფარქტის ან კორონარული დაავადების მიმართულებით მაღალი/საზღვრული სიგნალი.",
        "symptom_text": "პაციენტს აქვს ძლიერი გულმკერდის ტკივილი, ქოშინი და ოფლიანობა. სასწრაფოთი მოყვანილია.",
        "features": features,
    }


def scenario_hf_like() -> dict[str, Any]:
    features = base_features()
    set_value(features, "age", 76)
    set_value(features, "gender_male", 0)
    set_value(features, "omr_bmi_mean", 34)
    set_value(features, "omr_sbp_mean", 156)
    set_value(features, "omr_dbp_mean", 88)
    set_value(features, "ed_triage_heart_rate_mean", 112)
    set_value(features, "ed_triage_sbp_mean", 158)
    set_value(features, "ed_triage_dbp_mean", 90)
    set_value(features, "ed_triage_resp_rate_mean", 30)
    set_value(features, "ed_triage_spo2_mean", 88)
    set_value(features, "ed_triage_acuity_mean", 2)
    set_value(features, "lab_ntprobnp_mean", 12000)
    set_value(features, "lab_troponin_t_mean", 0.08)
    set_value(features, "lab_creatinine_mean", 1.8)
    set_value(features, "lab_glucose_mean", 150)
    set_value(features, "lab_hemoglobin_mean", 10.5)
    set_value(features, "history_diabetes", 1)
    set_value(features, "history_chronic_kidney_disease", 1)
    set_value(features, "history_obesity", 1)
    set_value(features, "ed_arrived_by_ambulance", 1)
    set_symptom(features, "symptom_shortness_of_breath", True)
    set_symptom(features, "symptom_edema", True)
    recompute_interactions(features)
    return {
        "name": "გულის უკმარისობის მსგავსი პაციენტი",
        "expected": "გულის უკმარისობის მიმართულებით დიაგნოსტიკური სიგნალი.",
        "symptom_text": "პაციენტს აქვს ქოშინი, ფეხების შეშუპება და დაბალი ჟანგბადის სატურაცია.",
        "features": features,
    }


def scenario_arrhythmia_like() -> dict[str, Any]:
    features = base_features()
    set_value(features, "age", 71)
    set_value(features, "gender_male", 1)
    set_value(features, "omr_bmi_mean", 29)
    set_value(features, "omr_sbp_mean", 138)
    set_value(features, "omr_dbp_mean", 82)
    set_value(features, "ed_triage_heart_rate_mean", 142)
    set_value(features, "ed_triage_sbp_mean", 132)
    set_value(features, "ed_triage_dbp_mean", 80)
    set_value(features, "ed_triage_resp_rate_mean", 22)
    set_value(features, "ed_triage_spo2_mean", 96)
    set_value(features, "ed_triage_acuity_mean", 2)
    set_value(features, "lab_troponin_t_mean", 0.03)
    set_value(features, "lab_ntprobnp_mean", 1300)
    set_value(features, "lab_creatinine_mean", 1.1)
    set_value(features, "lab_glucose_mean", 118)
    set_value(features, "history_tobacco_or_nicotine", 1)
    set_value(features, "ed_arrived_by_ambulance", 1)
    set_symptom(features, "symptom_palpitations", True)
    set_symptom(features, "symptom_syncope", True)
    set_symptom(features, "symptom_dizziness", True)
    recompute_interactions(features)
    return {
        "name": "არითმიის მსგავსი პაციენტი",
        "expected": "გულის არითმიის მიმართულებით დიაგნოსტიკური სიგნალი.",
        "symptom_text": "პაციენტს აქვს გულის ფრიალი, სინკოპე და თავბრუსხვევა. გულისცემა მკვეთრად აჩქარებულია.",
        "features": features,
    }


def run_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    prediction = service.predict(scenario["features"], top_n=6)
    top = prediction["subtype_risks"][0]
    return {
        "name": scenario["name"],
        "expected": scenario["expected"],
        "symptom_text": scenario["symptom_text"],
        "overall_probability": prediction["risk_probability"],
        "overall_level": prediction["risk_level"],
        "top_diagnosis": {
            "label": top["display_name"],
            "probability": top["diagnosis_probability"],
            "threshold": top["diagnosis_threshold"],
            "status": top["diagnosis_status"],
            "confidence": top["diagnosis_confidence"],
            "reasons": top["reason_factors"],
            "checks": top["suggested_clinical_checks"],
        },
        "subtypes": [
            {
                "label": item["display_name"],
                "probability": item["diagnosis_probability"],
                "threshold": item["diagnosis_threshold"],
                "status": item["diagnosis_status"],
                "confidence": item["diagnosis_confidence"],
                "reasons": item["reason_factors"],
            }
            for item in prediction["subtype_risks"]
        ],
    }


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def write_markdown(results: list[dict[str, Any]]) -> None:
    lines = [
        "# Demo Patient Test Suite",
        "",
        "ეს ფაილი აჩვენებს ოთხ ხელოვნურ demo პაციენტს და სისტემის პასუხს. სცენარები გამოიყენება frontend/API ლოგიკის შესამოწმებლად და დაცვის დროს დემოს მოსამზადებლად.",
        "",
    ]

    for result in results:
        top = result["top_diagnosis"]
        lines.extend(
            [
                f"## {result['name']}",
                "",
                f"**სცენარის მიზანი:** {result['expected']}",
                "",
                f"**სიმპტომების ტექსტი:** {result['symptom_text']}",
                "",
                f"**საერთო დიაგნოსტიკური სიგნალი:** {pct(result['overall_probability'])} (`{result['overall_level']}`)",
                "",
                f"**ყველაზე მაღალი მიმართულება:** {top['label']} - {pct(top['probability'])}",
                f"**Threshold:** {pct(top['threshold'])}",
                f"**სტატუსი:** {top['status']}",
                f"**მთავარი განმსაზღვრელი ფაქტორები:** {', '.join(top['reasons']) if top['reasons'] else 'მკვეთრად არ გამოიყო'}",
                f"**ექიმმა გადაამოწმოს:** {'; '.join(top['checks']) if top['checks'] else 'არ არის მითითებული'}",
                "",
                "| დიაგნოზის ჯგუფი | Probability | Threshold | Status | მთავარი ფაქტორები |",
                "|---|---:|---:|---|---|",
            ]
        )
        for item in result["subtypes"]:
            reasons = ", ".join(item["reasons"]) if item["reasons"] else "მკვეთრად არ გამოიყო"
            lines.append(
                f"| {item['label']} | {pct(item['probability'])} | {pct(item['threshold'])} | {item['status']} | {reasons} |"
            )
        lines.append("")

    REPORT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    scenarios = [
        scenario_low_risk(),
        scenario_mi_like(),
        scenario_hf_like(),
        scenario_arrhythmia_like(),
    ]
    results = [run_scenario(deepcopy(scenario)) for scenario in scenarios]
    REPORT_JSON_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(results)
    print(f"Wrote {REPORT_JSON_PATH}")
    print(f"Wrote {REPORT_MD_PATH}")


if __name__ == "__main__":
    main()
