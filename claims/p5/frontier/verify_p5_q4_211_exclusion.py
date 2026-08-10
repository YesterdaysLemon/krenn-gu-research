#!/usr/bin/env python3
"""Package the complete normalized q4_211 exclusion theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = HERE
THEOREM = ROOT / "P5_Q4_211_EXCLUSION_THEOREM.md"
CONSTITUENTS = (
    (
        "generic",
        "P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md",
        "verify_p5_q4_211_generic_exclusion.py",
        "audit_p5_q4_211_generic_exclusion.py",
    ),
    (
        "parallel_reselection",
        "P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md",
        "verify_p5_q4_211_parallel_incidence.py",
        "audit_p5_q4_211_parallel_incidence.py",
    ),
    (
        "b0_c0",
        "P5_Q4_211_B0_FINAL_OBSTRUCTION.md",
        "verify_p5_q4_211_b0_final.py",
        "audit_p5_q4_211_b0_final.py",
    ),
    (
        "a0_adjacent_reduction",
        "P5_Q4_211_A0_ADJACENT_REDUCTION.md",
        "verify_p5_q4_211_a0_adjacent.py",
        "audit_p5_q4_211_a0_adjacent.py",
    ),
    (
        "a0_adjacent_grassmann",
        "P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md",
        "verify_p5_q4_211_a0_adjacent_grassmann.py",
        "audit_p5_q4_211_a0_adjacent_grassmann.py",
    ),
    (
        "a0_disjoint_p3",
        "P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md",
        "verify_p5_q4_211_a0_disjoint_p3.py",
        "audit_p5_q4_211_a0_disjoint_p3.py",
    ),
    (
        "zero_row",
        "P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md",
        "verify_p5_two_singleton_coordinate_obstruction.py",
        "audit_p5_two_singleton_coordinate_obstruction.py",
    ),
)


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
    parameter_cover = {}
    for zero_mask in itertools.product((False, True), repeat=3):
        nonzero_count = 3 - sum(zero_mask)
        if nonzero_count == 1:
            continue
        if nonzero_count == 0:
            theorem_key = "zero_row_two_singleton"
        elif zero_mask == (False, False, False):
            theorem_key = "generic"
        elif zero_mask == (True, False, False):
            theorem_key = "a0_adjacent_or_disjoint"
        elif zero_mask == (False, True, False):
            theorem_key = "b0"
        elif zero_mask == (False, False, True):
            theorem_key = "c0_by_singleton_symmetry"
        else:
            raise AssertionError("unexpected admissible parameter mask")
        parameter_cover["".join("0" if zero else "*" for zero in zero_mask)] = (
            theorem_key
        )
    assert parameter_cover == {
        "***": "generic",
        "**0": "c0_by_singleton_symmetry",
        "*0*": "b0",
        "0**": "a0_adjacent_or_disjoint",
        "000": "zero_row_two_singleton",
    }

    constituent_hashes = {}
    for key, theorem_name, verifier_name, audit_name in CONSTITUENTS:
        files = {
            "theorem": resolve_repo_file(theorem_name),
            "verifier": resolve_repo_file(verifier_name),
            "audit": resolve_repo_file(audit_name),
        }
        if not all(path.is_file() for path in files.values()):
            raise AssertionError(f"missing constituent for {key}")
        constituent_hashes[key] = {
            label: {
                "file": path.name,
                "sha256": sha256(path),
            }
            for label, path in files.items()
        }

    output = {
        "verified": True,
        "field": "C",
        "normal_form": "q4_211",
        "admissible_nonzero_parameter_counts": [0, 2, 3],
        "parameter_strata": parameter_cover,
        "incidence_types_on_bc_nonzero": [
            "exact_disjoint",
            "adjacent",
            "parallel_reselects_as_adjacent",
        ],
        "constituents": constituent_hashes,
        "q4_211_excluded": True,
        "P5_to_Delta3_excluded": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_q4_211_exclusion_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
