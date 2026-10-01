# Dataset Guide

Phase 2 defines the dataset strategy for ZeroGuard AI. The goal is to use legitimate defensive network-flow datasets and a small safe demo dataset. The project must never include exploit code, malware samples, credentials, packet payloads, or offensive scanning tools.

## Recommended Dataset

Primary recommendation: CICIDS2017 from the Canadian Institute for Cybersecurity.

Why this dataset is a good fit:

- It contains labeled network-flow CSV data suitable for intrusion-detection research.
- It includes benign traffic and multiple attack categories, which helps evaluate anomaly detection against labels.
- It has commonly used flow features such as duration, packet counts, byte counts, packet length statistics, inter-arrival-time statistics, and flag counts.
- It can support a normal-behavior Isolation Forest baseline by training on benign records and evaluating on held-out labeled records.

Official source:

- Canadian Institute for Cybersecurity CICIDS2017 dataset page: https://www.unb.ca/cic/datasets/ids-2017.html

## Alternative Datasets

UNSW-NB15:

- Official source: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- Good for academic intrusion-detection experimentation.
- Includes labels and attack categories.
- Feature names differ from CICIDS2017, so a dataset adapter will be needed.

CSE-CIC-IDS2018:

- Official source: https://www.unb.ca/cic/datasets/ids-2018.html
- Larger and newer than CICIDS2017.
- Useful for later extension, but heavier for a first local MVP.

## Selected MVP Dataset Path

The first MVP will target CICIDS2017-style flow CSVs. Later phases can add adapters for UNSW-NB15 or CSE-CIC-IDS2018.

Expected local folder:

```text
data/
|-- raw/
|   |-- cicids2017/
|   |   |-- Monday-WorkingHours.pcap_ISCX.csv
|   |   |-- Tuesday-WorkingHours.pcap_ISCX.csv
|   |   |-- Wednesday-workingHours.pcap_ISCX.csv
|   |   |-- Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
|   |   |-- Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
|   |   |-- Friday-WorkingHours-Morning.pcap_ISCX.csv
|   |   |-- Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
|   |   |-- Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
|-- processed/
```

Do not commit downloaded dataset files. The `.gitignore` keeps `data/raw` and `data/processed` generated content out of Git.

## Required Label Handling

CICIDS2017 includes a `Label` column. Expected values include benign traffic and attack category names. For ZeroGuard AI, labels will be normalized into two views:

- `label`: original dataset label retained for evaluation.
- `is_anomaly_label`: boolean evaluation label where benign traffic is `false` and non-benign traffic is `true`.

The application detection labels will remain analyst-friendly:

- `Normal`
- `Suspicious`
- `High Risk`
- `Potential Unknown Threat`

An anomaly detection result is not automatically a confirmed zero-day attack.

## Feature Groups

The preprocessing pipeline will select network-flow features from these groups when available:

| Group | Example Features | Reason |
| --- | --- | --- |
| Protocol | `Protocol` | Different protocols have different normal behavior patterns. |
| Duration | `Flow Duration` | Very short or unusually long flows can be suspicious depending on context. |
| Volume | `Total Fwd Packets`, `Total Backward Packets`, byte counts | Captures traffic size and direction balance. |
| Rate | `Flow Bytes/s`, `Flow Packets/s` | High or unusual rates can indicate abnormal behavior. |
| Packet lengths | min, max, mean, std packet length fields | Helps detect unusual packet-size distributions. |
| Inter-arrival time | flow, forward, backward IAT fields | Captures timing irregularity. |
| TCP flags | SYN, ACK, RST, PSH, URG counts | Useful for identifying unusual TCP connection patterns. |
| Header and activity stats | header length, active/idle means | Adds behavioral context without storing payloads. |

IP addresses must not be treated as simple continuous numeric features. If identifiers are needed later, they should be bucketed, hashed, or used only for analyst context, not raw model training.

## Preprocessing Assumptions

Phase 3 will implement this pipeline:

1. Load one or more CSV files from `data/raw/cicids2017`.
2. Standardize column names.
3. Remove exact duplicate rows.
4. Convert numeric feature columns safely.
5. Replace infinite values with missing values.
6. Impute missing numeric values using training-data statistics only.
7. Encode categorical variables such as protocol if needed.
8. Scale numeric features using transformations fit only on training data.
9. Split train, validation, and test data without leaking validation or test information into training.
10. Save processed datasets and preprocessing artifacts.

## Demo Dataset

The repository includes a small safe synthetic dataset at:

```text
data/demo/security_events_sample.csv
```

This file is not real network capture data. It contains synthetic flow-like records for development and dashboard testing. It has no packet payloads, no exploit strings, no credentials, and no offensive instructions.

The demo labels are fixtures for the project workflow. They are not model-performance claims.

## Dataset Verification Checklist

Before Phase 3, verify:

- You can open the official dataset page for the dataset you plan to use.
- Downloaded files stay under `data/raw/...`.
- Raw dataset files are not staged in Git.
- `data/demo/security_events_sample.csv` is present for local demo mode.
- You understand that all detections are investigation leads, not confirmed attacks.

