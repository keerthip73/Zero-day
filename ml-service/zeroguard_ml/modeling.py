"""Training, evaluation, and inference helpers for ZeroGuard AI."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from time import perf_counter
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        return [dict(row) for row in csv.DictReader(csv_file)]


def feature_matrix(rows: list[dict[str, str]], feature_names: list[str]) -> np.ndarray:
    return np.array(
        [[float(row.get(feature, 0.0) or 0.0) for feature in feature_names] for row in rows],
        dtype=np.float64,
    )


def labels(rows: list[dict[str, str]]) -> np.ndarray:
    return np.array([str(row.get("is_anomaly_label", "false")).lower() == "true" for row in rows])


def normalize_scores(raw_scores: np.ndarray, normal_reference_scores: np.ndarray) -> np.ndarray:
    low = float(np.percentile(normal_reference_scores, 5))
    high = float(np.percentile(normal_reference_scores, 99))
    if math.isclose(low, high):
        high = low + 1.0
    normalized = (raw_scores - low) / (high - low)
    return np.clip(normalized * 100.0, 0.0, 100.0)


def severity_for_score(score: float) -> str:
    if score >= 80:
        return "POTENTIAL_UNKNOWN_THREAT"
    if score >= 60:
        return "HIGH_RISK"
    if score >= 30:
        return "SUSPICIOUS"
    return "NORMAL"


def reasons_for_row(row: dict[str, Any], score: float) -> list[str]:
    reasons: list[str] = []
    packet_rate = float(row.get("flow_packets_per_sec", 0.0) or 0.0)
    byte_rate = float(row.get("flow_bytes_per_sec", 0.0) or 0.0)
    syn_count = float(row.get("tcp_syn_count", 0.0) or 0.0)
    rst_count = float(row.get("tcp_rst_count", 0.0) or 0.0)

    if packet_rate > 2.5:
        reasons.append("Flow packet rate is far above the training baseline")
    if byte_rate > 2.5:
        reasons.append("Flow byte rate is far above the training baseline")
    if syn_count > 2.5:
        reasons.append("TCP SYN count is unusually high compared with normal samples")
    if rst_count > 2.0:
        reasons.append("TCP reset activity is elevated compared with normal samples")
    if score >= 80 and not reasons:
        reasons.append("Combined feature pattern is outside the learned normal region")
    if not reasons:
        reasons.append("Feature pattern is close to the learned normal baseline")
    return reasons


def train_isolation_forest(
    train_path: Path,
    validation_path: Path,
    test_path: Path,
    preprocessor_path: Path,
    model_path: Path,
    metadata_path: Path,
    metrics_path: Path,
    contamination: float = 0.15,
    random_state: int = 42,
) -> dict[str, Any]:
    preprocessor = json.loads(preprocessor_path.read_text(encoding="utf-8"))
    feature_names = list(preprocessor["output_features"])
    train_rows = load_rows(train_path)
    validation_rows = load_rows(validation_path)
    test_rows = load_rows(test_path)

    normal_train_rows = [
        row for row in train_rows if str(row.get("is_anomaly_label", "false")).lower() == "false"
    ]
    training_source = normal_train_rows or train_rows
    train_matrix = feature_matrix(training_source, feature_names)

    model = IsolationForest(
        n_estimators=150,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )
    started = perf_counter()
    model.fit(train_matrix)
    training_seconds = perf_counter() - started

    validation_matrix = feature_matrix(validation_rows, feature_names)
    validation_raw_scores = -model.score_samples(validation_matrix)
    validation_labels = labels(validation_rows)

    if validation_labels.any():
        threshold = float(np.percentile(validation_raw_scores[~validation_labels], 95)) if (~validation_labels).any() else float(np.percentile(validation_raw_scores, 85))
    else:
        threshold = float(np.percentile(validation_raw_scores, 95))

    normal_reference_scores = -model.score_samples(train_matrix)
    test_matrix = feature_matrix(test_rows, feature_names)
    test_raw_scores = -model.score_samples(test_matrix)
    test_labels = labels(test_rows)
    predicted_anomalies = test_raw_scores >= threshold
    risk_scores = normalize_scores(test_raw_scores, normal_reference_scores)

    precision = precision_score(test_labels, predicted_anomalies, zero_division=0)
    recall = recall_score(test_labels, predicted_anomalies, zero_division=0)
    f1 = f1_score(test_labels, predicted_anomalies, zero_division=0)
    confusion = confusion_matrix(test_labels, predicted_anomalies, labels=[False, True])
    tn, fp, fn, tp = confusion.ravel()
    false_positive_rate = float(fp / (fp + tn)) if (fp + tn) else 0.0
    roc_auc = None
    if len(set(test_labels.tolist())) > 1:
        roc_auc = float(roc_auc_score(test_labels, test_raw_scores))

    model_bundle = {
        "model": model,
        "feature_names": feature_names,
        "threshold": threshold,
        "normal_reference_scores": normal_reference_scores,
        "model_name": "Isolation Forest",
        "model_version": "0.1.0-demo",
    }
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_bundle, model_path)

    metadata = {
        "model_name": "Isolation Forest",
        "model_version": "0.1.0-demo",
        "dataset": "safe synthetic demo dataset",
        "feature_names": feature_names,
        "threshold": threshold,
        "contamination": contamination,
        "training_rows": len(training_source),
        "validation_rows": len(validation_rows),
        "test_rows": len(test_rows),
        "training_seconds": round(training_seconds, 6),
        "severity_mapping": {
            "0-29": "NORMAL",
            "30-59": "SUSPICIOUS",
            "60-79": "HIGH_RISK",
            "80-100": "POTENTIAL_UNKNOWN_THREAT",
        },
    }
    metrics = {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": roc_auc,
        "false_positive_rate": false_positive_rate,
        "confusion_matrix": {
            "true_negative": int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive": int(tp),
        },
        "threshold": threshold,
        "note": "Demo metrics are from a tiny synthetic fixture and are not research claims.",
    }

    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return {"metadata": metadata, "metrics": metrics}


def predict_with_bundle(bundle: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    feature_names = bundle["feature_names"]
    matrix = feature_matrix([{feature: row.get(feature, 0.0) for feature in feature_names}], feature_names)
    raw_score = float(-bundle["model"].score_samples(matrix)[0])
    risk_score = float(normalize_scores(np.array([raw_score]), bundle["normal_reference_scores"])[0])
    anomaly = bool(raw_score >= float(bundle["threshold"]))
    severity = severity_for_score(risk_score)
    return {
        "anomaly": anomaly,
        "riskScore": round(risk_score, 2),
        "severity": severity,
        "modelName": bundle["model_name"],
        "modelVersion": bundle["model_version"],
        "confidence": round(min(max(risk_score / 100.0, 0.01), 0.99), 2),
        "reasons": reasons_for_row(row, risk_score),
        "anomalyScore": round(raw_score, 6),
    }

