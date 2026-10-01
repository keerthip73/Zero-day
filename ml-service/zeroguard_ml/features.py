"""Feature definitions shared by preprocessing, training, and inference."""

from __future__ import annotations

IDENTIFIER_COLUMNS = [
    "event_id",
    "timestamp",
    "source_identifier",
    "destination_identifier",
]

CATEGORICAL_FEATURES = [
    "protocol",
]

NUMERIC_FEATURES = [
    "source_port",
    "destination_port",
    "duration_ms",
    "forward_packets",
    "backward_packets",
    "forward_bytes",
    "backward_bytes",
    "flow_bytes_per_sec",
    "flow_packets_per_sec",
    "packet_length_mean",
    "packet_length_std",
    "flow_iat_mean_ms",
    "tcp_syn_count",
    "tcp_ack_count",
    "tcp_rst_count",
]

LABEL_COLUMN = "label"
SEVERITY_FIXTURE_COLUMN = "severity_fixture"

BENIGN_LABELS = {"BENIGN", "NORMAL"}

