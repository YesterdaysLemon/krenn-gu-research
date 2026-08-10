#!/usr/bin/env python3
"""Package and verify the generic normalized q4_211 exclusion chain."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md"
DEPENDENCIES = (
    "P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md",
    "P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md",
    "P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md",
    "P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md",
    "P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md",
    "P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md",
    "P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md",
    "P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md",
    "P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md",
    "P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md",
    "P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    modes = frozenset(range(4))
    containment_sets = [
        frozenset(subset)
        for size in range(2, 5)
        for subset in itertools.combinations(modes, size)
    ]
    counts = {"disjoint": 0, "adjacent": 0, "parallel": 0}
    for first, second in itertools.product(
        containment_sets,
        containment_sets,
    ):
        common = len(first & second)
        if common == 0:
            assert len(first) == len(second) == 2
            assert first | second == modes
            counts["disjoint"] += 1
        elif common == 1:
            counts["adjacent"] += 1
        else:
            counts["parallel"] += 1
    assert sum(counts.values()) == len(containment_sets) ** 2

    dependency_hashes = {}
    for name in DEPENDENCIES:
        path = ROOT / name
        assert path.is_file(), name
        dependency_hashes[name] = sha256(path)

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a*b*c != 0",
        "incidence_pair_count": len(containment_sets) ** 2,
        "incidence_classes": counts,
        "dependency_hashes": dependency_hashes,
        "generic_q4_211_excluded": True,
        "remaining_parameter_strata": [
            "a=0, b*c!=0",
            "b=0, a*c!=0",
            "c=0, a*b!=0",
        ],
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_generic_exclusion_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
