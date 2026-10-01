from __future__ import annotations

import csv
import json
import sys
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = PROJECT_ROOT / "data/demo/security_events_sample.csv"
API_URL = "http://localhost:8080/api/events"


def to_payload(row: dict[str, str]) -> dict[str, object]:
    return {
        "timestamp": row["timestamp"],
        "sourceIdentifier": row["source_identifier"],
        "destinationIdentifier": row["destination_identifier"],
        "protocol": row["protocol"],
        "sourcePort": int(row["source_port"]),
        "destinationPort": int(row["destination_port"]),
        "durationMs": float(row["duration_ms"]),
        "forwardPackets": float(row["forward_packets"]),
        "backwardPackets": float(row["backward_packets"]),
        "forwardBytes": float(row["forward_bytes"]),
        "backwardBytes": float(row["backward_bytes"]),
        "flowBytesPerSec": float(row["flow_bytes_per_sec"]),
        "flowPacketsPerSec": float(row["flow_packets_per_sec"]),
        "packetLengthMean": float(row["packet_length_mean"]),
        "packetLengthStd": float(row["packet_length_std"]),
        "flowIatMeanMs": float(row["flow_iat_mean_ms"]),
        "tcpSynCount": float(row["tcp_syn_count"]),
        "tcpAckCount": float(row["tcp_ack_count"]),
        "tcpRstCount": float(row["tcp_rst_count"]),
    }


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/simulate_events.py <jwt-token>")
    token = sys.argv[1]
    with DEMO_PATH.open("r", encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))
    for row in rows:
        payload = json.dumps(to_payload(row)).encode("utf-8")
        request = urllib.request.Request(
            API_URL,
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            print(response.status, row["event_id"])


if __name__ == "__main__":
    main()

