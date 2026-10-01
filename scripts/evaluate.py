from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = PROJECT_ROOT / "models/isolation_forest_demo.metrics.json"


def main() -> None:
    if not METRICS_PATH.exists():
        raise SystemExit("No metrics file found. Run: python scripts/train_baseline.py")
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

