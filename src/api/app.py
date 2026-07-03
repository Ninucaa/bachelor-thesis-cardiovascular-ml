from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.api.model_service import FeatureValidationError, service
from src.api.schemas import (
    FeatureInfo,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    SamplePatientResponse,
)


app = FastAPI(
    title="გულ-სისხლძარღვთა რისკის პროგნოზირების API",
    description=(
        "მანქანური სწავლების გადაწყვეტილების დამხმარე პროტოტიპი "
        "გულ-სისხლძარღვთა რისკის პროგნოზირებისთვის SHAP ახსნებით."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ALLOW_ORIGINS",
        ",".join(
            [
                "http://127.0.0.1:5173",
                "http://localhost:5173",
            ]
        ),
    ).split(","),
    allow_origin_regex=os.getenv(
        "CORS_ALLOW_ORIGIN_REGEX",
        r"http://(127\.0\.0\.1|localhost):517\d",
    ),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model_loaded=service.model is not None,
        feature_count=len(service.feature_columns),
    )


@app.get("/features", response_model=list[FeatureInfo])
def features() -> list[FeatureInfo]:
    return [FeatureInfo(name=name) for name in service.feature_columns]


@app.get("/sample-patient", response_model=SamplePatientResponse)
def sample_patient(sample_id: str = Query("demo-1")) -> SamplePatientResponse:
    return SamplePatientResponse(**service.sample_patient_by_id(sample_id))


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    try:
        result = service.predict(payload.features, payload.top_n)
    except FeatureValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "გადაცემული მახასიათებლები გაწვრთნილ მოდელს არ ემთხვევა.",
                "missing_count": len(exc.missing),
                "extra_count": len(exc.extra),
                "missing_first_20": exc.missing[:20],
                "extra_first_20": exc.extra[:20],
            },
        ) from exc

    return PredictionResponse(**result)
