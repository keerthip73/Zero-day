from __future__ import annotations

import csv
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import joblib
from fastapi import FastAPI, HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "ml-service"))

from app.schemas import BatchPredictionRequest, ModelInfo, PredictionResponse, SecurityEventFeatures
from zeroguard_ml.modeling import predict_with_bundle
from zeroguard_ml.preprocessing import transform_rows

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("zeroguard-ml")

MODEL_PATH = Path(os.getenv("MODEL_PATH", PROJECT_ROOT / "models/isolation_forest_demo.joblib"))
PREPROCESSOR_PATH = Path(os.getenv("PREPROCESSOR_PATH", PROJECT_ROOT / "models/preprocessor_demo.json"))

app = FastAPI(
    title="ZeroGuard AI ML Service",
    description="Defensive anomaly detection inference service.",
    version="0.1.0",
)

model_bundle: dict[str, Any] | None = None
preprocessor: dict[str, Any] | None = None


@app.on_event("startup")
def load_artifacts() -> None:
    global model_bundle, preprocessor
    if MODEL_PATH.exists() and PREPROCESSOR_PATH.exists():
        model_bundle = joblib.load(MODEL_PATH)
        preprocessor = json.loads(PREPROCESSOR_PATH.read_text(encoding="utf-8"))
        logger.info("Loaded model artifacts from %s", MODEL_PATH)
    else:
        logger.warning("Model artifacts are missing. Run prepare_data.py and train_baseline.py.")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "modelLoaded": str(model_bundle is not None).lower()}


@app.get("/model/info", response_model=ModelInfo)
def model_info() -> ModelInfo:
    if model_bundle is None:
        return ModelInfo(modelName="Isolation Forest", modelVersion="untrained", status="missing", featureCount=0)
    return ModelInfo(
        modelName=model_bundle["model_name"],
        modelVersion=model_bundle["model_version"],
        status="loaded",
        featureCount=len(model_bundle["feature_names"]),
        threshold=float(model_bundle["threshold"]),
    )


def event_to_processed_row(event: SecurityEventFeatures) -> dict[str, Any]:
    if model_bundle is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Model artifacts are not loaded")
    raw = event.model_dump(mode="json")
    raw["label"] = "UNKNOWN"
    raw["severity_fixture"] = ""
    raw["is_anomaly_label"] = "false"
    processed_rows = transform_rows([raw], preprocessor)
    return processed_rows[0]


@app.post("/predict", response_model=PredictionResponse)
def predict(event: SecurityEventFeatures) -> PredictionResponse:
    processed = event_to_processed_row(event)
    assert model_bundle is not None
    result = predict_with_bundle(model_bundle, processed)
    logger.info(
        "prediction event_id=%s severity=%s risk_score=%s",
        event.event_id,
        result["severity"],
        result["riskScore"],
    )
    return PredictionResponse(**result)


@app.post("/predict/batch", response_model=list[PredictionResponse])
def predict_batch(request: BatchPredictionRequest) -> list[PredictionResponse]:
    return [predict(event) for event in request.events]


@app.get("/demo/events")
def demo_events() -> list[dict[str, str]]:
    demo_path = PROJECT_ROOT / "data/demo/security_events_sample.csv"
    with demo_path.open("r", encoding="utf-8", newline="") as csv_file:
        return [dict(row) for row in csv.DictReader(csv_file)]

