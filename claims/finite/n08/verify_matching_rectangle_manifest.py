"""Audit two-monomial rectangles inside learned exact conflict cubes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from cancellation_transport import (
    cube_two_monomial_rectangle_certificates,
)
from search_witness import EquationSystem
from krenn_gu.verify_laurent_batch_manifest import structural_zero_indices


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    batch = json.loads(args.manifest.read_text(encoding="utf-8"))
    conflicts = batch.get("conflicts", [])
    if not isinstance(conflicts, list):
        raise AssertionError("batch does not contain explicit conflicts")
    center_degree = int(batch.get("center_degree", 4))
    system = EquationSystem(8, 3)
    structural_zero = structural_zero_indices(system, center_degree)

    certified: list[dict[str, object]] = []
    for conflict_index, conflict in enumerate(conflicts):
        positive = set(map(int, conflict["positive_entries"]))
        negative = set(map(int, conflict["negative_entries"]))
        if positive & (negative | structural_zero):
            raise AssertionError("conflict cube has inconsistent entry signs")
        certificates = cube_two_monomial_rectangle_certificates(
            system,
            map(int, conflict["used_equation_indices"]),
            positive,
            negative | structural_zero,
        )
        if certificates:
            certified.append(
                {
                    "conflict_index": conflict_index,
                    "recorded_conflict_index": int(
                        conflict["conflict_index"]
                    ),
                    "role_index": int(conflict["role_index"]),
                    "certificates": certificates,
                }
            )

    payload = {
        "verified": True,
        "scope": (
            "two-monomial rectangle certificates within exact "
            "conflict cubes"
        ),
        "source_manifest": str(args.manifest),
        "source_manifest_sha256": sha256(args.manifest),
        "center_degree": center_degree,
        "conflicts_checked": len(conflicts),
        "conflicts_with_rectangle_certificate": len(certified),
        "certified_conflict_indices": [
            row["conflict_index"] for row in certified
        ],
        "rows": certified,
    }
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
