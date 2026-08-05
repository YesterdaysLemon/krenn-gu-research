#!/usr/bin/env python3
"""Verify component 22's H=f2=f8=2h3+s intersection closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_"
    "F2_F8_H3_SLOPE_INTERSECTION_OBSTRUCTION.md"
)
FIRST_ROWS = (0, 1, 2, 3, 4, 7, 8, 9)
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
    denominator = V.A * V.D + V.A + V.D * V.R
    numerator = V.A * V.D - V.A + V.D * V.R
    rho8 = -numerator / denominator
    base = V.mixed_matrix.subs(
        {
            V.h1: -1 / (2 * V.A),
            V.h2: -1 / V.s,
            V.h3: -V.s / 2,
            V.rho: rho8,
        },
        simultaneous=True,
    )

    cap_q8 = (
        2 * V.A * V.D**2 * V.h0
        - V.A * V.D**2
        - 2 * V.A * V.D * V.h0
        + 2 * V.A * V.D
        - V.A
        + 2 * V.D**2 * V.R * V.h0
        - V.D**2 * V.R
        - 2 * V.D * V.R * V.h0
        + 2 * V.D * V.R
    )
    first_unit = (
        1024
        * V.A**6
        * V.D**4
        * V.R**2
        * (V.A + V.R) ** 2
        * V.s**5
        * (V.D - 1)
        * (V.D + 1) ** 3
        * numerator
        / denominator**7
    )
    first = determinant(base, FIRST_ROWS, (V.A, V.R, V.D, V.h0))
    exact_equal(first, first_unit * cap_q8)

    h0_value = (
        V.A * (V.D - 1) ** 2 + V.D * (V.D - 2) * V.R
    ) / (2 * V.D * (V.D - 1) * (V.A + V.R))
    cap_t8 = (
        2 * V.A**3 * V.D**2
        - 2 * V.A**3
        + 4 * V.A**2 * V.D**2 * V.R
        + 3 * V.A * V.D**2 * V.R**2
        + V.A * V.R**2
        + V.D**2 * V.R**3
    )
    terminal_unit = (
        -256
        * V.A**4
        * V.D**4
        * V.R**2
        * (V.A + V.R) ** 2
        * V.s**4
        * (4 * V.A + V.R)
        * (V.D - 1)
        * (V.D + 1) ** 3
        * numerator
        / denominator**7
    )
    terminal = determinant(
        base.subs(V.h0, h0_value), TERMINAL_ROWS, (V.A, V.R, V.D)
    )
    exact_equal(terminal, terminal_unit * cap_t8)
    assert sp.Poly(cap_t8, V.A, V.R, V.D) != 0

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero generic-component branch closure",
        "rest of `f2=f8=0`",
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
                "closed_branch": "H=f2=f8=2*h3+s=0",
                "first_rows": FIRST_ROWS,
                "first_forces": "Q8=0",
                "terminal_rows": TERMINAL_ROWS,
                "terminal_coefficient_unit": str(sp.factor(cap_t8)),
                "other_f2_f8_branches_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
