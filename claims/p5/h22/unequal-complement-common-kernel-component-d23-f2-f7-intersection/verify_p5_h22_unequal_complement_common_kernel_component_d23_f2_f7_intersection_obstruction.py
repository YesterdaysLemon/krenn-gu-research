#!/usr/bin/env python3
"""Verify component 22's exact H=f2=f7 intersection closure."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/unequal-complement-common-kernel-component-d23-pair-orbit-partial")

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V



import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_"
    "F2_F7_INTERSECTION_OBSTRUCTION.md"
)
FIRST_ROWS = (0, 1, 2, 3, 4, 7, 8, 9)
SECOND_ROWS = (0, 1, 2, 3, 4, 7, 8, 10)
TERMINAL_ROWS = (0, 1, 2, 3, 4, 7, 8, 11)


def determinant(matrix, rows, generators):
    field = sp.QQ.frac_field(*generators)
    data = [
        [
            field.from_sympy(sp.cancel(matrix[rows[i], column]))
            for column in range(8)
        ]
        for i in range(8)
    ]
    return sp.cancel(DomainMatrix(data, (8, 8), field).det().as_expr())


def exact_equal(left, right):
    assert sp.cancel(left - right) == 0


def main() -> None:
    denominator = V.A * V.D + V.A + V.R
    rho7 = -(V.A * V.D - V.A - V.R) / denominator
    base = V.mixed_matrix.subs(
        {V.h1: -1 / (2 * V.A), V.h2: -1 / V.s, V.rho: rho7},
        simultaneous=True,
    )

    cap_q0 = (
        4 * V.A * V.D * V.h0
        - 3 * V.A * V.D
        + V.A
        + 2 * V.D * V.R * V.h0
        - V.D * V.R
        + V.R
    )
    first_unit = (
        -256
        * V.A**3
        * V.D**4
        * V.R**2
        * (V.A + V.R) ** 2
        * V.s**6
        * (V.D - 1)
        * (V.D + 1) ** 2
        * (V.A * V.D - V.A - V.R) ** 2
        / denominator**6
    )
    first = determinant(base, FIRST_ROWS, (V.A, V.R, V.D, V.h0, V.h3))
    exact_equal(first, first_unit * cap_q0)

    h0_value = (
        3 * V.A * V.D - V.A + V.D * V.R - V.R
    ) / (2 * V.D * V.s)
    second_matrix = base.subs(V.h0, h0_value)
    second_unit = (
        256
        * V.A**3
        * V.D**4
        * V.R
        * (V.A + V.R) ** 3
        * V.s**7
        * (V.D - 1)
        * (V.D + 1) ** 3
        * (V.A * V.D - V.A - V.R) ** 2
        / denominator**6
    )
    second = determinant(
        second_matrix, SECOND_ROWS, (V.A, V.R, V.D, V.h3)
    )
    exact_equal(second, second_unit * (V.s + 2 * V.h3))

    cap_t7 = (
        4 * V.A**2 * V.D**2
        - 4 * V.A**2
        + 6 * V.A * V.D**2 * V.R
        + 2 * V.A * V.R
        + V.D**2 * V.R**2
        + 3 * V.R**2
    )
    terminal_unit = (
        -128
        * V.A**2
        * V.D**4
        * V.R**2
        * (V.A + V.R) ** 3
        * V.s**5
        * (V.D + 1) ** 2
        * (V.A * V.D - V.A - V.R) ** 2
        / denominator**6
    )
    terminal_matrix = second_matrix.subs(V.h3, -V.s / 2)
    terminal = determinant(terminal_matrix, TERMINAL_ROWS, (V.A, V.R, V.D))
    exact_equal(terminal, terminal_unit * cap_t7)
    assert sp.Poly(cap_t7, V.A, V.R, V.D) != 0

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero generic-component branch closure",
        "remaining `f2*f8*P=0` residual",
        "remain **UNKNOWN**",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
        "No finite field",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "Q(A,R,D)",
                "component": 22,
                "closed_branch": "H=f2=f7=0",
                "first_rows": FIRST_ROWS,
                "first_forces": "Q0=0",
                "second_rows": SECOND_ROWS,
                "second_forces": "s+2*h3=0",
                "terminal_rows": TERMINAL_ROWS,
                "terminal_coefficient_unit": str(sp.factor(cap_t7)),
                "other_f2_branches_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
