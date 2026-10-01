# ZeroGuard AI Architecture

This document will grow as each implementation phase is completed. Phase 1 defines the target architecture and boundaries.

## System Architecture

```mermaid
flowchart LR
    analyst[Security Analyst] --> frontend[React + TypeScript Dashboard]
    frontend --> backend[Spring Boot REST API]
    backend --> db[(PostgreSQL)]
    backend --> ml[FastAPI ML Service]
    ml --> engine[ML Detection Engine]
    engine --> isolation[Isolation Forest]
    engine --> autoencoder[Autoencoder / LSTM Autoencoder]
```

## Event Detection Flow

```mermaid
sequenceDiagram
    participant UI as React Dashboard
    participant API as Spring Boot Backend
    participant ML as FastAPI ML Service
    participant DB as PostgreSQL

    UI->>API: Submit security event
    API->>API: Validate request
    API->>ML: Request anomaly prediction
    ML-->>API: Risk score, severity, explanation
    API->>DB: Store event and detection
    API->>DB: Create alert when threshold is met
    API-->>UI: Return detection result
```

## Planned Database Relationships

```mermaid
erDiagram
    USERS ||--o{ ALERTS : assigned_to
    SECURITY_EVENTS ||--|| DETECTIONS : has
    DETECTIONS ||--o{ ALERTS : raises
    SECURITY_EVENTS ||--o{ ANALYST_NOTES : has
    USERS ||--o{ ANALYST_NOTES : writes
    MODEL_VERSIONS ||--o{ DETECTIONS : produced
```

## Deployment Direction

Local development will use Docker Compose. AWS deployment documentation will be prepared later, but the project will not be deployed to AWS in this academic build.

```mermaid
flowchart TB
    browser[Browser] --> cloudfront[S3 + CloudFront]
    cloudfront --> api[ECS/Fargate Backend]
    api --> rds[(RDS PostgreSQL)]
    api --> ml[ECS/Fargate ML Service]
    api --> logs[CloudWatch Logs]
    ml --> logs
    secrets[Secrets Manager / Parameter Store] --> api
    secrets --> ml
```

