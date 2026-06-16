from __future__ import annotations

import os

os.environ.setdefault("PYDANTIC_DISABLE_PLUGINS", "1")

from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_health_reports_loaded_model() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model_loaded"] is True
    assert payload["feature_count"] > 0


def test_features_endpoint_matches_health_count() -> None:
    health = client.get("/health").json()
    response = client.get("/features")

    assert response.status_code == 200
    features = response.json()
    assert len(features) == health["feature_count"]
    assert all(item["required"] is True for item in features)
    assert {"name": "age", "required": True} in features


def test_sample_patient_contains_full_feature_payload() -> None:
    feature_count = client.get("/health").json()["feature_count"]
    response = client.get("/sample-patient")

    assert response.status_code == 200
    payload = response.json()
    assert payload["source"]
    assert isinstance(payload["features"], dict)
    assert len(payload["features"]) == feature_count


def test_predict_returns_diagnosis_groups_for_sample_patient() -> None:
    sample = client.get("/sample-patient").json()
    response = client.post("/predict", json={"features": sample["features"], "top_n": 5})

    assert response.status_code == 200
    payload = response.json()
    assert 0 <= payload["risk_probability"] <= 1
    assert payload["risk_level"] in {"low", "medium", "high"}
    assert len(payload["top_factors"]) <= 5
    assert len(payload["subtype_risks"]) >= 6
    assert payload["display_target_name"]
    assert payload["patient_analysis_summary"]


def test_predict_rejects_incomplete_payload() -> None:
    response = client.post("/predict", json={"features": {"age": 60}, "top_n": 5})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["missing_count"] > 0
    assert detail["extra_count"] == 0
