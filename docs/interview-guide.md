# Interview Guide

## What problem does this solve?

ZeroGuard AI demonstrates how a defensive monitoring platform can identify unusual network-flow behavior and route high-risk detections to analysts.

## What is a zero-day vulnerability?

A zero-day is a vulnerability unknown to the vendor or defenders at the time it is used or discovered. This project does not prove a zero-day; it flags anomalous behavior that may deserve investigation.

## Why not signatures alone?

Signatures are useful for known threats, but unknown behavior may not match an existing signature. Anomaly detection learns a baseline of expected behavior and highlights deviations.

## Why Isolation Forest?

Isolation Forest is a practical unsupervised baseline. It isolates unusual records faster than common records and works well for tabular flow features.

## Why Autoencoder or LSTM later?

Autoencoders can learn compressed normal-behavior representations and flag high reconstruction error. LSTM only makes sense when the dataset has meaningful temporal sequences.

## How is threshold chosen?

The baseline uses validation score distributions rather than a hard-coded magic number. For real datasets, the threshold should balance recall with analyst false-positive workload.

## How do you reduce false positives?

Use validation data, analyst feedback, better feature engineering, severity bands, contextual rules, and periodic offline review. Do not automatically retrain production models from raw feedback.

## Why FastAPI?

FastAPI keeps ML inference isolated from the main backend, provides Pydantic validation, and is natural for Python ML artifacts.

## Why Spring Boot?

Spring Boot is a strong fit for authentication, persistence, validation, service layering, and enterprise-style REST APIs.

## What happens if ML fails?

The backend catches ML-service failures, stores the event, and marks it suspicious for analyst review instead of crashing.

## Limitations

The demo fixture is synthetic and tiny. Real claims require evaluation on held-out public datasets such as CICIDS2017.

