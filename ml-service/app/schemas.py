from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SecurityEventFeatures(BaseModel):
    event_id: str | None = None
    timestamp: datetime | None = None
    source_identifier: str | None = None
    destination_identifier: str | None = None
    protocol: str = Field(default="TCP")
    source_port: int = Field(ge=0, le=65535)
    destination_port: int = Field(ge=0, le=65535)
    duration_ms: float = Field(ge=0)
    forward_packets: float = Field(ge=0)
    backward_packets: float = Field(ge=0)
    forward_bytes: float = Field(ge=0)
    backward_bytes: float = Field(ge=0)
    flow_bytes_per_sec: float = Field(ge=0)
    flow_packets_per_sec: float = Field(ge=0)
    packet_length_mean: float = Field(ge=0)
    packet_length_std: float = Field(ge=0)
    flow_iat_mean_ms: float = Field(ge=0)
    tcp_syn_count: float = Field(ge=0)
    tcp_ack_count: float = Field(ge=0)
    tcp_rst_count: float = Field(ge=0)


class PredictionResponse(BaseModel):
    anomaly: bool
    riskScore: float
    severity: str
    modelName: str
    modelVersion: str
    confidence: float
    reasons: list[str]
    anomalyScore: float


class BatchPredictionRequest(BaseModel):
    events: list[SecurityEventFeatures] = Field(min_length=1, max_length=100)


class ModelInfo(BaseModel):
    modelName: str
    modelVersion: str
    status: str
    featureCount: int
    threshold: float | None = None

