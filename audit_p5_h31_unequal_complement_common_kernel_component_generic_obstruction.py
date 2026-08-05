#!/usr/bin/env python3
"""Independent rational audit of component-22 generic H31 obstruction."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import mixed_matrix

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py"
THEOREM = ROOT / "P5_H31_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_GENERIC_OBSTRUCTION.md"


def add(left, right, coefficient=1):
    return tuple(left[i] + coefficient * right[i] for i in range(4))


def rows(A, R, D, h):
    u, v = (1 - D) / 2, (1 + D) / 2
    a, c = (1, 1, 0, 0), (1, -1, 0, 0)
    alpha = (
        (0, D * (2 * A + R), -u, v),
        (2 * A, 0, 1, 1),
        (2 * A + R, -R, 1, 1),
        c,
    )
    canonical = (
        (-A * v, A * (u + 1) + R, 1, 0),
        a,
        a,
        (-(2 * A + R) / 2, -(2 * A + R) / 2, u, v),
    )
    beta = tuple(add(canonical[i], alpha[i], h[i]) for i in range(4))
    return alpha, beta


def main():
    primary = PRIMARY.read_text(encoding="utf-8")
    theorem = THEOREM.read_text(encoding="utf-8")
    assert '"generic_H31_fibre_empty": True' in primary
    assert "only four marking" in theorem
    assert "UNRESOLVED" in theorem

    diagnostics = []
    for A, R, D in ((sp.Rational(1), sp.Rational(1), sp.Rational(2)), (sp.Rational(2), sp.Rational(1), sp.Rational(3))):
        s = 2 * A + R
        markings = (
            (0, ((D - 3) / (4 * D), 0, 0, -s / 2)),
            (0, ((A * (D - 3) - 2 * R) / (2 * D * s), 0, 0, -(2 * A + 3 * R) / 2)),
            (1, ((D - 3) / (4 * D), 0, 0, s / 2)),
            (1, (-1 / D, 0, -1 / R, s / 2)),
        )
        branch_ranks = []
        for q, marking in markings:
            alpha, beta = rows(A, R, D, marking)
            mixed, d0, d1 = mixed_matrix(q, alpha, beta)
            branch_ranks.append(
                (
                    mixed.rank(),
                    mixed.col_join(d0).rank(),
                    mixed.col_join(d1).rank(),
                    mixed.col_join(d0).col_join(d1).rank(),
                )
            )
        assert branch_ranks == [(6, 7, 7, 8)] * 4
        module_ranks = []
        for q in (2, 3):
            for marking in ((0, 0, 0, 0), (1, 2, 3, 4)):
                alpha, beta = rows(A, R, D, marking)
                mixed, d0, d1 = mixed_matrix(q, alpha, beta)
                module_ranks.append(
                    (
                        mixed.rank(),
                        mixed.col_join(d0).rank(),
                        mixed.col_join(d1).rank(),
                        mixed.col_join(d0).col_join(d1).rank(),
                    )
                )
        assert module_ranks == [(7, 7, 8, 8)] * 4
        diagnostics.append({"point": [int(A), int(R), int(D)], "branch_ranks": branch_ranks})

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "rational_diagnostics": diagnostics,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
