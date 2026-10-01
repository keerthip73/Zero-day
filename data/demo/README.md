# Demo Data

`security_events_sample.csv` is a small, safe, synthetic dataset for local development.

It is not real network capture data. It contains no packet payloads, exploit content, credentials, malware, or offensive instructions.

The demo labels are workflow fixtures:

- `NORMAL`
- `SUSPICIOUS`
- `HIGH_RISK`
- `POTENTIAL_UNKNOWN_THREAT`

Later phases will use this file to exercise preprocessing, ML inference, backend ingestion, alerts, and dashboard charts before a full public dataset is downloaded.

