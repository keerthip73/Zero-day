"""Reusable preprocessing for safe demo and CICIDS-style flow data.

This module intentionally avoids packet payload processing. It operates on
flow-level metadata only.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any

from zeroguard_ml.features import (
    BENIGN_LABELS,
    CATEGORICAL_FEATURES,
    IDENTIFIER_COLUMNS,
    LABEL_COLUMN,
    NUMERIC_FEATURES,
    SEVERITY_FIXTURE_COLUMN,
)


@dataclass(frozen=True)
class SplitRatios:
    train: float = 0.70
    validation: float = 0.15
    test: float = 0.15

    def validate(self) -> None:
        total = self.train + self.validation + self.test
        if not math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Split ratios must add up to 1.0")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [dict(row) for row in reader]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_column_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("/", "_per_")


def standardize_columns(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {normalize_column_name(column): value for column, value in row.items()}
        for row in rows
    ]


def remove_duplicate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    deduplicated: list[dict[str, str]] = []

    for row in rows:
        fingerprint = tuple(sorted(row.items()))
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        deduplicated.append(row)

    return deduplicated


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        number = float(value)
    else:
        text = str(value).strip()
        if text == "":
            return None
        try:
            number = float(text)
        except ValueError:
            return None

    if math.isinf(number) or math.isnan(number):
        return None
    return number


def normalize_label(value: Any) -> str:
    text = str(value or "").strip().upper()
    return text if text else "UNKNOWN"


def add_binary_label(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        label = normalize_label(row.get(LABEL_COLUMN))
        row[LABEL_COLUMN] = label
        row["is_anomaly_label"] = str(label not in BENIGN_LABELS).lower()


def stratified_split(
    rows: list[dict[str, Any]],
    ratios: SplitRatios,
    seed: int,
) -> dict[str, list[dict[str, Any]]]:
    ratios.validate()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rng = random.Random(seed)

    for row in rows:
        grouped[str(row.get("is_anomaly_label", "false"))].append(row)

    splits = {"train": [], "validation": [], "test": []}

    for group_rows in grouped.values():
        shuffled = list(group_rows)
        rng.shuffle(shuffled)
        total = len(shuffled)
        if total >= 3:
            validation_count = max(1, round(total * ratios.validation))
            test_count = max(1, round(total * ratios.test))
            train_count = total - validation_count - test_count
            if train_count < 1:
                train_count = 1
                if validation_count >= test_count and validation_count > 1:
                    validation_count -= 1
                elif test_count > 1:
                    test_count -= 1
        else:
            train_count = max(1, total - 1)
            validation_count = total - train_count
            test_count = 0

        train_end = train_count
        validation_end = train_count + validation_count

        splits["train"].extend(shuffled[:train_end])
        splits["validation"].extend(shuffled[train_end:validation_end])
        splits["test"].extend(shuffled[validation_end:])

    for split_rows in splits.values():
        split_rows.sort(key=lambda row: str(row.get("event_id", "")))

    return splits


def fit_preprocessor(train_rows: list[dict[str, Any]]) -> dict[str, Any]:
    medians: dict[str, float] = {}
    means: dict[str, float] = {}
    standard_deviations: dict[str, float] = {}

    for feature in NUMERIC_FEATURES:
        values = [
            parsed
            for row in train_rows
            if (parsed := parse_float(row.get(feature))) is not None
        ]
        fallback_values = values or [0.0]
        feature_median = float(median(fallback_values))
        medians[feature] = feature_median

        completed = [parse_float(row.get(feature)) for row in train_rows]
        imputed = [value if value is not None else feature_median for value in completed]
        mean = sum(imputed) / len(imputed) if imputed else 0.0
        variance = (
            sum((value - mean) ** 2 for value in imputed) / len(imputed)
            if imputed
            else 0.0
        )
        standard_deviation = math.sqrt(variance)
        means[feature] = mean
        standard_deviations[feature] = standard_deviation if standard_deviation > 0 else 1.0

    categories: dict[str, list[str]] = {}
    for feature in CATEGORICAL_FEATURES:
        category_values = sorted(
            {
                str(row.get(feature, "")).strip().upper() or "UNKNOWN"
                for row in train_rows
            }
        )
        categories[feature] = category_values or ["UNKNOWN"]

    output_features = list(NUMERIC_FEATURES)
    for feature in CATEGORICAL_FEATURES:
        output_features.extend(
            f"{feature}_{category.lower()}" for category in categories[feature]
        )

    return {
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "identifier_columns": IDENTIFIER_COLUMNS,
        "label_column": LABEL_COLUMN,
        "severity_fixture_column": SEVERITY_FIXTURE_COLUMN,
        "numeric_medians": medians,
        "numeric_means": means,
        "numeric_standard_deviations": standard_deviations,
        "categories": categories,
        "output_features": output_features,
        "normalization": "z_score",
        "fit_scope": "training_split_only",
    }


def transform_rows(
    rows: list[dict[str, Any]],
    artifact: dict[str, Any],
) -> list[dict[str, Any]]:
    transformed: list[dict[str, Any]] = []

    for row in rows:
        output: dict[str, Any] = {}

        for column in IDENTIFIER_COLUMNS:
            output[column] = row.get(column, "")

        for feature in NUMERIC_FEATURES:
            value = parse_float(row.get(feature))
            if value is None:
                value = float(artifact["numeric_medians"][feature])
            mean = float(artifact["numeric_means"][feature])
            standard_deviation = float(artifact["numeric_standard_deviations"][feature])
            output[feature] = round((value - mean) / standard_deviation, 8)

        for feature in CATEGORICAL_FEATURES:
            raw_value = str(row.get(feature, "")).strip().upper() or "UNKNOWN"
            for category in artifact["categories"][feature]:
                output[f"{feature}_{category.lower()}"] = 1 if raw_value == category else 0

        output[LABEL_COLUMN] = row.get(LABEL_COLUMN, "UNKNOWN")
        output["is_anomaly_label"] = row.get("is_anomaly_label", "false")
        output[SEVERITY_FIXTURE_COLUMN] = row.get(SEVERITY_FIXTURE_COLUMN, "")
        transformed.append(output)

    return transformed


def prepare_dataset(
    input_path: Path,
    output_dir: Path,
    artifact_path: Path,
    seed: int = 42,
    ratios: SplitRatios | None = None,
) -> dict[str, Any]:
    ratios = ratios or SplitRatios()
    rows = remove_duplicate_rows(standardize_columns(load_csv(input_path)))
    if not rows:
        raise ValueError(f"No rows found in {input_path}")

    add_binary_label(rows)
    splits = stratified_split(rows, ratios=ratios, seed=seed)
    artifact = fit_preprocessor(splits["train"])
    artifact.update(
        {
            "source_file": str(input_path),
            "random_seed": seed,
            "split_counts": {name: len(split_rows) for name, split_rows in splits.items()},
            "total_rows_after_deduplication": len(rows),
        }
    )

    fieldnames = (
        IDENTIFIER_COLUMNS
        + artifact["output_features"]
        + [LABEL_COLUMN, "is_anomaly_label", SEVERITY_FIXTURE_COLUMN]
    )

    for split_name, split_rows in splits.items():
        transformed = transform_rows(split_rows, artifact)
        write_csv(output_dir / f"{split_name}.csv", transformed, fieldnames)

    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    return artifact


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare ZeroGuard AI flow datasets.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/demo/security_events_sample.csv"),
        help="Input CSV path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/demo"),
        help="Directory for processed train, validation, and test CSV files.",
    )
    parser.add_argument(
        "--artifact",
        type=Path,
        default=Path("models/preprocessor_demo.json"),
        help="Path for the fitted preprocessing artifact.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic split seed.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    artifact = prepare_dataset(
        input_path=args.input,
        output_dir=args.output_dir,
        artifact_path=args.artifact,
        seed=args.seed,
    )
    print("Prepared dataset successfully.")
    print(f"Source: {artifact['source_file']}")
    print(f"Rows: {artifact['total_rows_after_deduplication']}")
    print(f"Splits: {artifact['split_counts']}")
    print(f"Features: {len(artifact['output_features'])}")


if __name__ == "__main__":
    main()
