from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: dict[str, float] = Field(
        ...,
        description="მოდელისთვის მომზადებული პაციენტის მახასიათებლები feature-ის სახელების მიხედვით.",
    )
    top_n: int = Field(
        8,
        ge=1,
        le=20,
        description="რამდენი მთავარი SHAP ახსნის ფაქტორი დაბრუნდეს.",
    )


class FeatureInfo(BaseModel):
    name: str
    required: bool = True


class ShapFactor(BaseModel):
    feature: str
    feature_group: str | None = None
    value: float
    shap_value: float
    direction: str


class SubtypeRisk(BaseModel):
    target_name: str
    display_name: str
    risk_probability: float
    risk_level: str
    diagnosis_label: str
    diagnosis_probability: float
    diagnosis_threshold: float
    diagnosis_status: str
    diagnosis_confidence: str
    diagnosis_interpretation: str
    suggested_clinical_checks: list[str]
    explanation: str
    reason_factors: list[str]


class ClinicalImpact(BaseModel):
    factor_group: str
    current_profile: str
    reference_profile: str
    risk_delta: float
    explanation: str


class PredictionResponse(BaseModel):
    target_name: str
    display_target_name: str
    target_description: str
    risk_probability: float
    predicted_class: int
    risk_level: str
    risk_explanation: str
    analytical_summary: str
    patient_analysis_summary: str
    clinical_impacts: list[ClinicalImpact]
    method_note: str
    subtype_note: str
    subtype_risks: list[SubtypeRisk]
    top_factors: list[ShapFactor]


class SamplePatientResponse(BaseModel):
    source: str
    row_index: int
    original_csv_index: int
    actual_target: int
    features: dict[str, float]
    symptom_text: str | None = None
    ecg_finding: str | None = None
    ecg_note: str | None = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    feature_count: int
