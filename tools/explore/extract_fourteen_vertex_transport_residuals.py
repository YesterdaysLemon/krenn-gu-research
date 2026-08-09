"""Extract one saved residual support per orbit from a transport-rule scan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("coverage", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    coverage = json.loads(
        args.coverage.read_text(encoding="utf-8")
    )
    full_scan = coverage.get("full_scan")
    if not full_scan:
        raise AssertionError("coverage has no full scan")
    survivors = []
    for row in full_scan["per_orbit"]:
        examples = row.get("residual_examples")
        if examples is None:
            example = row.get("residual_example")
            examples = [] if example is None else [example]
        for example_id, example in enumerate(examples):
            survivors.append(
                {
                    "orbit_id": int(row["orbit_id"]),
                    "orbit_example_id": example_id,
                    **example,
                }
            )
    payload = {
        "status": "transport_rule_residual_samples",
        "partition": coverage["partition"],
        "source_coverage": str(args.coverage),
        "survivors": survivors,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "partition": payload["partition"],
                "residual_samples": len(survivors),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
