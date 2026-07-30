#!/usr/bin/env python3
"""Verify the q4_211 marked-Delta2 pair-image obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md"
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_image(left, right):
    columns = []
    for first in left.tolist():
        for second in right.tolist():
            columns.append(
                [
                    sp.expand(
                        first[i] * second[j] + first[j] * second[i]
                    )
                    for i, j in PAIRS
                ]
            )
    return sp.Matrix(columns).T


def main() -> None:
    A, T = sp.symbols("A T", nonzero=True)
    B = sp.symbols("B")
    planes = (
        sp.Matrix([[0, 1, T, -B], [1, 0, 0, -A]]),
        sp.Matrix([[1, 0, 0, A], [0, 1, -T, B]]),
        sp.Matrix([[1, 0, 0, A], [B, A, -A * T, 0]]),
    )
    u0 = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1]])
    e2 = sp.Matrix([[0, 0, 1, 0]])
    e3 = sp.Matrix([[0, 0, 0, 1]])

    assignments = tuple(itertools.permutations(range(3)))
    full_pair_ranks = []
    opposite_pair_ranks = []
    full_minors = []
    opposite_minors = []
    full_column_choices = (
        (0, 2, 4, 5, 6, 7),
        (0, 2, 4, 5, 6, 7),
        (0, 2, 4, 5, 6, 7),
        (0, 1, 2, 4, 7, 8),
        (0, 2, 4, 5, 6, 7),
        (0, 1, 2, 4, 7, 8),
    )
    opposite_rows = (1, 2, 3, 4)

    for assignment, columns in zip(
        assignments,
        full_column_choices,
        strict=True,
    ):
        at_h1, at_h2, remaining = assignment
        row_h1 = sp.Matrix.vstack(planes[at_h1], e3)
        row_h2 = sp.Matrix.vstack(planes[at_h2], e2)
        full = pair_image(row_h1, row_h2)
        opposite = pair_image(u0, planes[remaining])
        full_pair_ranks.append(full.rank())
        opposite_pair_ranks.append(opposite.rank())
        full_minors.append(sp.factor(full[:, list(columns)].det()))
        opposite_minors.append(
            sp.factor(opposite[list(opposite_rows), :].det())
        )

    assert full_pair_ranks == [6] * 6
    assert opposite_pair_ranks == [4] * 6
    assert full_minors == [
        4 * A * T,
        4 * A**3 * T,
        -4 * A * T,
        -4 * A**4 * T,
        -4 * A**3 * T,
        -4 * A**2 * T,
    ]
    assert opposite_minors == [-A**2, -1, -A**2, -1, -1, -1]
    flattening_rank_lower_bounds = [
        left + right - 6
        for left, right in zip(
            full_pair_ranks,
            opposite_pair_ranks,
            strict=True,
        )
    ]
    assert flattening_rank_lower_bounds == [4] * 6

    # No marked plane itself contains either incidence coordinate row.
    for plane in planes:
        assert sp.Matrix.vstack(plane, e2).rank() == 3
        assert sp.Matrix.vstack(plane, e3).rank() == 3

    output = {
        "verified": True,
        "field": "C",
        "plane_assignments_checked": len(assignments),
        "full_pair_image_ranks": full_pair_ranks,
        "opposite_pair_image_ranks": opposite_pair_ranks,
        "full_pair_witness_minors": [str(value) for value in full_minors],
        "opposite_pair_witness_minors": [
            str(value) for value in opposite_minors
        ],
        "forced_flattening_rank_lower_bound": 4,
        "Delta2_flattening_rank": 2,
        "all_rank_two_marked_family_excluded": True,
        "rank_one_normal_pencil_gates_retained": True,
        "adjacent_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_marked_delta2_pair_image_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
