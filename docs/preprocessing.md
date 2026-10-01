# Preprocessing Pipeline

Phase 3 adds the first reusable preprocessing pipeline. It is intentionally small and runnable with Python's standard library so the project can be verified before installing heavier ML dependencies.

## What It Builds

Input:

```text
data/demo/security_events_sample.csv
```

Output:

```text
data/processed/demo/train.csv
data/processed/demo/validation.csv
data/processed/demo/test.csv
models/preprocessor_demo.json
```

The processed CSV files are generated artifacts and are ignored by Git. The preprocessor artifact is also ignored by Git because later model artifacts may become large or environment-specific.

## Current Feature Contract

Numeric features:

- `source_port`
- `destination_port`
- `duration_ms`
- `forward_packets`
- `backward_packets`
- `forward_bytes`
- `backward_bytes`
- `flow_bytes_per_sec`
- `flow_packets_per_sec`
- `packet_length_mean`
- `packet_length_std`
- `flow_iat_mean_ms`
- `tcp_syn_count`
- `tcp_ack_count`
- `tcp_rst_count`

Categorical features:

- `protocol`

Identifier columns are retained for traceability but are not scaled as model features:

- `event_id`
- `timestamp`
- `source_identifier`
- `destination_identifier`

## Leakage Prevention

The pipeline splits the dataset before fitting preprocessing values. Median imputation, means, standard deviations, and categorical levels are fit from the training split only. Validation and test rows are transformed using the training artifact.

## Windows PowerShell Commands

Run these from the project root:

```powershell
python scripts/prepare_data.py
python -m unittest discover -s ml-service/tests
```

Expected output from the prepare command:

```text
Prepared dataset successfully.
Source: data\demo\security_events_sample.csv
Rows: 20
Splits: {'train': 14, 'validation': 3, 'test': 3}
Features: 17
```

## Later Extension

When Phase 4 starts, the Isolation Forest training script will consume `data/processed/demo/train.csv` and `models/preprocessor_demo.json`.

When full CICIDS2017 files are used, the project will add a dataset adapter that maps CICIDS2017 column names into the same feature contract.
