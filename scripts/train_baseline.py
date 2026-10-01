from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ML_SERVICE_ROOT = PROJECT_ROOT / "ml-service"
sys.path.insert(0, str(ML_SERVICE_ROOT))

from zeroguard_ml.modeling import train_isolation_forest


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the ZeroGuard AI Isolation Forest baseline.")
    parser.add_argument("--processed-dir", type=Path, default=PROJECT_ROOT / "data/processed/demo")
    parser.add_argument("--preprocessor", type=Path, default=PROJECT_ROOT / "models/preprocessor_demo.json")
    parser.add_argument("--model", type=Path, default=PROJECT_ROOT / "models/isolation_forest_demo.joblib")
    parser.add_argument("--metadata", type=Path, default=PROJECT_ROOT / "models/isolation_forest_demo.metadata.json")
    parser.add_argument("--metrics", type=Path, default=PROJECT_ROOT / "models/isolation_forest_demo.metrics.json")
    args = parser.parse_args()

    result = train_isolation_forest(
        train_path=args.processed_dir / "train.csv",
        validation_path=args.processed_dir / "validation.csv",
        test_path=args.processed_dir / "test.csv",
        preprocessor_path=args.preprocessor,
        model_path=args.model,
        metadata_path=args.metadata,
        metrics_path=args.metrics,
    )
    metrics = result["metrics"]
    print("Trained Isolation Forest baseline successfully.")
    print(f"Model: {args.model}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall: {metrics['recall']:.3f}")
    print(f"F1: {metrics['f1']:.3f}")
    print(f"False positive rate: {metrics['false_positive_rate']:.3f}")


if __name__ == "__main__":
    main()

