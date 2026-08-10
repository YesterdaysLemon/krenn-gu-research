#!/usr/bin/env python3
"""Independent logical audit of the complete q4_211 case cover."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = HERE
THEOREM = ROOT / "P5_Q4_211_EXCLUSION_THEOREM.md"
PRIMARY = ROOT / "verify_p5_q4_211_exclusion.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_repo_file(path_key: str) -> Path:
    direct = ROOT / path_key
    if direct.exists():
        return direct
    manifest = json.loads(
        (REPO_ROOT / "catalog" / "moved-paths.json").read_text(
            encoding="utf-8"
        )
    )
    for move in manifest.get("moves", []):
        if (
            move.get("status") == "moved"
            and move.get("old_path") == path_key
        ):
            candidate = REPO_ROOT / move["new_path"]
            if candidate.exists():
                return candidate
    return direct


def main() -> None:
    admissible_masks = []
    for zero_mask in itertools.product((False, True), repeat=3):
        if 3 - sum(zero_mask) != 1:
            admissible_masks.append(zero_mask)
    expected_masks = {
        (False, False, False),
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, True),
    }
    if set(admissible_masks) != expected_masks:
        raise AssertionError("q4 parameter cover changed")

    modes = frozenset(range(4))
    containment_sets = [
        frozenset(subset)
        for size in range(2, 5)
        for subset in itertools.combinations(modes, size)
    ]
    incidence_counts: Counter[str] = Counter()
    incidence_examples = {}
    for first in containment_sets:
        for second in containment_sets:
            common = first & second
            if not common:
                if len(first) != 2 or len(second) != 2 or first | second != modes:
                    raise AssertionError("non-partition disjoint incidence found")
                kind = "exact_disjoint"
            elif len(common) == 1:
                kind = "adjacent"
            else:
                kind = "parallel_reselects_as_adjacent"
            incidence_counts[kind] += 1
            incidence_examples.setdefault(
                kind,
                [sorted(first), sorted(second)],
            )
    if sum(incidence_counts.values()) != len(containment_sets) ** 2:
        raise AssertionError("incidence cover is incomplete")
    if set(incidence_counts) != {
        "exact_disjoint",
        "adjacent",
        "parallel_reselects_as_adjacent",
    }:
        raise AssertionError("unexpected incidence type")

    stratum_routes = {
        "abc_nonzero": {
            "incidence_cover": sorted(incidence_counts),
            "theorem": "P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md",
        },
        "a_zero": {
            "exact_disjoint": (
                "P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md"
            ),
            "adjacent": (
                "P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md"
            ),
            "parallel": (
                "P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md"
            ),
        },
        "b_zero": {
            "theorem": "P5_Q4_211_B0_FINAL_OBSTRUCTION.md",
        },
        "c_zero": {
            "theorem": (
                "singleton-colour image of "
                "P5_Q4_211_B0_FINAL_OBSTRUCTION.md"
            ),
        },
        "zero_row": {
            "theorem": "P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md",
        },
    }
    required_files = {
        "P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md",
        "P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md",
        "P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md",
        "P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md",
        "P5_Q4_211_B0_FINAL_OBSTRUCTION.md",
        "P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md",
    }
    if not all(resolve_repo_file(filename).is_file() for filename in required_files):
        raise AssertionError("case-cover theorem file missing")

    output = {
        "audited": True,
        "field": "C",
        "admissible_parameter_zero_masks": [
            ["zero" if value else "nonzero" for value in mask]
            for mask in admissible_masks
        ],
        "normal_containment_sets": len(containment_sets),
        "ordered_incidence_pairs": len(containment_sets) ** 2,
        "incidence_counts": dict(incidence_counts),
        "incidence_examples": incidence_examples,
        "stratum_routes": stratum_routes,
        "unrouted_parameter_strata": 0,
        "unrouted_incidence_pairs": 0,
        "q4_211_excluded": True,
        "P5_to_Delta3_excluded": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_q4_211_exclusion_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
