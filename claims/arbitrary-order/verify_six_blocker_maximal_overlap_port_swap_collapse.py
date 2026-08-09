#!/usr/bin/env python3
"""Verify the maximal six-blocker overlap port-swap collapse."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "SIX_BLOCKER_MAXIMAL_OVERLAP_PORT_SWAP_COLLAPSE.md"


def profile(rows: sp.Matrix) -> int:
    rank = rows.rank()
    result = 0
    for colour in range(3):
        coordinate = sp.eye(3).row(colour)
        if rows.col_join(coordinate).rank() == rank:
            result |= 1 << colour
    return result


def blocker_rows() -> tuple[sp.Matrix, ...]:
    e0, e1, e2 = (sp.eye(3).row(index) for index in range(3))
    exceptional = (
        sp.Matrix.vstack(e1, e2, e1 + e2, e1 + 2 * e2, e1 - e2, e0),
        sp.Matrix.vstack(e0, e2, e0 + e2, e0 + 2 * e2, e0 - e2, e1),
        sp.Matrix.vstack(e0, e1, e0 + e1, e0 + 2 * e1, e0 - e1, e2),
    )
    full = sp.Matrix.vstack(
        e0,
        e1,
        e2,
        e0 + e1 + e2,
        e0 + 2 * e1 + 3 * e2,
        3 * e0 + 2 * e1 + e2,
    )
    return (*exceptional, full, full.copy(), full.copy())


def permanent_support_swap() -> None:
    support = set(itertools.permutations(range(6)))
    swap = (0, 1, 2, 3, 5, 4)
    moved = {tuple(swap[value] for value in word) for word in support}
    assert moved == support


def ghz_coefficients() -> None:
    coordinates = sp.symbols("x0:18")
    roots = tuple(coordinates[3 * root : 3 * root + 3] for root in range(6))
    for colour in range(3):
        left = roots[5][colour] * sp.prod(
            roots[root][colour] for root in (0, 1, 2, 3, 4)
        )
        right = roots[4][colour] * sp.prod(
            roots[root][colour] for root in (0, 1, 2, 3, 5)
        )
        common = sp.prod(roots[root][colour] for root in range(6))
        assert sp.expand(left - common) == 0
        assert sp.expand(right - common) == 0


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "not two independent tensor constraints" in theorem
    assert "B_ab(x_a,x_b) != 0" in theorem
    assert "UNRESOLVED" in theorem
    for dependency in (
        HERE / "ONE_NONBLOCKER_SURPLUS_PERMANENT_EXTRACTION.md",
        HERE / "TWO_PORT_SEVEN_BLOCKER_REDUCTION.md",
        REPO_ROOT / "claims/p6/P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md",
    ):
        assert dependency.exists()

    permanent_support_swap()
    ghz_coefficients()

    rows = blocker_rows()
    swap_matrix = sp.eye(6)
    swap_matrix.row_swap(4, 5)
    for matrix in rows:
        assert matrix.rank() == 3
        assert swap_matrix * matrix == matrix[[0, 1, 2, 3, 5, 4], :]

    # Natural root/port markings: R deletes b (row 5), R' deletes a (row 4).
    left_profiles = tuple(profile(matrix[:5, :]) for matrix in rows)
    right_profiles = tuple(profile(matrix[[0, 1, 2, 3, 5], :]) for matrix in rows)
    assert left_profiles == (6, 5, 3, 7, 7, 7)
    assert right_profiles == (7, 7, 7, 7, 7, 7)
    assert tuple(matrix[:5, :].rank() for matrix in rows) == (2, 2, 2, 3, 3, 3)
    assert tuple(matrix[[0, 1, 2, 3, 5], :].rank() for matrix in rows) == (
        3,
        3,
        3,
        3,
        3,
        3,
    )

    # Honest rational incident edge blocks realize every desired row.
    root = sp.Matrix([1, 1, 1])
    section = sp.Matrix([sp.Rational(1, 3)] * 3)
    assert (root.T * section)[0] == 1
    incident_blocks = []
    for matrix in rows:
        mode_blocks = []
        for root_index in range(6):
            covector = matrix.row(root_index)
            block = section * covector
            assert block != sp.zeros(3)
            assert root.T * block == covector
            mode_blocks.append(block)
        incident_blocks.append(tuple(mode_blocks))

    # All six roots can be pairwise zero-coupled through nonzero blocks.
    root_block = sp.diag(1, -1, 0)
    assert root_block != sp.zeros(3)
    assert (root.T * root_block * root)[0] == 0
    root_covector = root.T * root_block
    assert root_covector == sp.Matrix([[1, -1, 0]])
    assert (root_covector * root)[0] == 0
    assert profile(root_covector) == 0

    # Therefore the exchanged root is a torus simultaneous-kernel vector and
    # blocks no colour for the opposite five-root configuration.
    repeated_nonblocker_rows = sp.Matrix.vstack(*(root_covector for _ in range(5)))
    assert repeated_nonblocker_rows.rank() == 1
    assert profile(repeated_nonblocker_rows) == 0
    assert repeated_nonblocker_rows * root == sp.zeros(5, 1)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "root_overlap": 4,
                "shared_blockers": 6,
                "left_profiles": left_profiles,
                "right_profiles": right_profiles,
                "left_root_map_ranks": tuple(matrix[:5, :].rank() for matrix in rows),
                "right_root_map_ranks": tuple(
                    matrix[[0, 1, 2, 3, 5], :].rank() for matrix in rows
                ),
                "p6_restrictions_independent": False,
                "local_incident_blocks_realized": True,
                "global_matching_identity_realized": False,
                "nonzero_cross_coupling_residual_open": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
