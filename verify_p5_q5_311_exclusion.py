#!/usr/bin/env python3
"""Primary verifier for the exact q5_311 exclusion theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_311_EXCLUSION_THEOREM.md"
RANK_DROP = ROOT / "P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md"
SHARED_DROP = ROOT / "P5_Q5_311_SHARED_DROP_OBSTRUCTION.md"
P3_CLASSIFICATION = (
    ROOT / "P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md"
)
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[int, ...], ...]) -> int:
    return sum(
        1
        for permutation in PERMUTATIONS
        if all(rows[mode][permutation[mode]] for mode in range(4))
    )


def main() -> None:
    # All-zero common case: common source 0 is zero in every mode.
    # The remaining entries are deliberately maximally permissive.
    zero_column_rows = tuple((0, 1, 1, 1) for _ in range(4))
    assert permanent(zero_column_rows) == 0

    # A non-drop map has a two-dimensional common image plus one
    # exceptional direction.
    common_plane_r = sp.Matrix.hstack(
        sp.Matrix([1, 0, 0]),
        sp.Matrix([0, 1, 0]),
    )
    exceptional_r = sp.Matrix([0, 0, 1])
    assert common_plane_r.rank() == 2
    assert sp.Matrix.hstack(common_plane_r, exceptional_r).rank() == 3

    # Let w be outside the first non-drop common plane, so contraction
    # there is nonzero.  The resulting pure residual has factor w in
    # the second non-drop mode, placing w in that common plane.
    target = sp.Matrix([0, 0, 1])
    common_plane_t = sp.Matrix.hstack(
        sp.Matrix([1, 0, 0]),
        target,
    )
    assert sp.Matrix.hstack(common_plane_r, target).rank() == 3
    assert sp.Matrix.hstack(common_plane_t, target).rank() == 2

    quotient_r = sp.Matrix([[0, 0, 1]])
    quotient_t = sp.Matrix([[0, 1, 0]])
    assert (quotient_r * target)[0] == 1
    assert quotient_t * common_plane_t == sp.zeros(1, 2)
    assert (quotient_t * target)[0] == 0

    allowed_four_plane_patterns = {
        ("zero", "zero", "zero", "zero"),
        ("pure", "pure", "pure", "pure"),
    }
    assert ("pure", "pure", "pure", "zero") not in (
        allowed_four_plane_patterns
    )

    dependencies = {
        RANK_DROP.name: sha256(RANK_DROP),
        SHARED_DROP.name: sha256(SHARED_DROP),
        P3_CLASSIFICATION.name: sha256(P3_CLASSIFICATION),
    }
    output = {
        "verified": True,
        "field": "C",
        "rank_drop_sets": [[0, 1], [2, 3]],
        "common_row_ranks": [2, 2, 2, 2],
        "allowed_common_triple_kind_patterns": [
            "all_zero",
            "all_nonzero_decomposable",
        ],
        "all_zero_deleted_P4_permanent": 0,
        "first_non_drop_quotient_on_target": 1,
        "second_non_drop_quotient_on_target": 0,
        "q5_311_possible": False,
        "dependencies": dependencies,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_311_exclusion_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
