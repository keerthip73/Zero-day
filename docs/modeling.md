# Modeling

Phase 4 adds the first anomaly detection baseline: Isolation Forest.

## Baseline

The baseline trains on processed safe demo flow features from:

```text
data/processed/demo/train.csv
```

The script prefers normal training rows for unsupervised normal-behavior learning. It uses validation scores to choose a threshold, then evaluates on the held-out test split.

## Commands

Run from the project root:

```powershell
python scripts/prepare_data.py
python scripts/train_baseline.py
python scripts/evaluate.py
```

Outputs:

```text
models/isolation_forest_demo.joblib
models/isolation_forest_demo.metadata.json
models/isolation_forest_demo.metrics.json
```

These files are generated and ignored by Git.

## Important Limitation

The current metrics use a tiny synthetic demo fixture. They prove that the pipeline runs; they do not prove real-world detection performance.

The README and dashboard must avoid claims such as "detects every zero-day attack" or "100% detection." The correct framing is:

> The system identifies anomalous network behavior that may indicate previously unseen threats.

## Autoencoder Plan

The LSTM Autoencoder will be added after the MVP path is working end to end. A true LSTM model requires meaningful temporal sequences. For flat flow fixtures, a dense autoencoder is a better fallback than pretending temporal order exists.

