from __future__ import annotations

import csv
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "ml-service"))

from zeroguard_ml.preprocessing import prepare_dataset


class PreprocessingTests(unittest.TestCase):
    def test_prepare_demo_dataset_writes_splits_and_artifact(self) -> None:
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            artifact = prepare_dataset(
                input_path=PROJECT_ROOT / "data/demo/security_events_sample.csv",
                output_dir=temp_path / "processed",
                artifact_path=temp_path / "preprocessor.json",
                seed=42,
            )

            self.assertEqual(artifact["total_rows_after_deduplication"], 20)
            self.assertEqual(artifact["split_counts"], {"train": 14, "validation": 3, "test": 3})
            self.assertIn("duration_ms", artifact["output_features"])
            self.assertIn("protocol_tcp", artifact["output_features"])

            train_path = temp_path / "processed/train.csv"
            validation_path = temp_path / "processed/validation.csv"
            test_path = temp_path / "processed/test.csv"
            self.assertTrue(train_path.exists())
            self.assertTrue(validation_path.exists())
            self.assertTrue(test_path.exists())

            with train_path.open("r", encoding="utf-8", newline="") as csv_file:
                rows = list(csv.DictReader(csv_file))
            self.assertEqual(len(rows), 14)
            self.assertIn("is_anomaly_label", rows[0])

            with test_path.open("r", encoding="utf-8", newline="") as csv_file:
                test_rows = list(csv.DictReader(csv_file))
            self.assertIn("true", {row["is_anomaly_label"] for row in test_rows})
            self.assertIn("false", {row["is_anomaly_label"] for row in test_rows})

            saved_artifact = json.loads((temp_path / "preprocessor.json").read_text(encoding="utf-8"))
            self.assertEqual(saved_artifact["fit_scope"], "training_split_only")


if __name__ == "__main__":
    unittest.main()
