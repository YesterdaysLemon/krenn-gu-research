#!/usr/bin/env python3
"""Verify the exact H=0, h2=0 three-divisor partial closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H1_NONZERO_"
    "H2_ZERO_PARTIAL_CLOSURE.md"
)
RHO1_ROWS = (1, 2, 3, 5, 6, 7, 10, 11)
RHO1_TERMINAL_ROWS = (2, 3, 5, 6, 10, 11, 12, 13)
SLOPE_ROWS = (0, 1, 2, 3, 6, 7, 9, 11)
LINEAR_ROWS = (0, 1, 2, 3, 6, 7, 9, 10)
TERMINAL_ROWS = (0, 1, 2, 3, 6, 7, 9, 12)


def determinant(matrix, clearing_factor):
    symbols = sorted(
        set().union(*(entry.free_symbols for entry in matrix)), key=str
    )
    field = sp.QQ.frac_field(*symbols)
    rows = [
        [field.from_sympy(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]
    value = DomainMatrix(rows, matrix.shape, field).det().as_expr()
    return sp.cancel(value * clearing_factor**matrix.rows)


def exact_equal(left, right):
    assert sp.cancel(left - right) == 0


def main():
    theorem = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero partial closure theorem",
        "Every other `h2=0` case remains **UNKNOWN**",
        "No finite field",
        "conjecture remain **UNRESOLVED**",
    ):
        assert phrase in theorem

    base = V.mixed_matrix.subs({V.h1: -1 / (2 * V.A), V.h2: 0}, simultaneous=True)
    q1 = V.D * V.h0 + 1
    rho1 = base.subs(V.rho, 1)
    rho1_expected = 2**16 * V.A**9 * V.D**4 * (V.A + V.R) ** 2 * V.s**2 * (V.D + 1) * q1
    rho1_det = determinant(rho1.extract(RHO1_ROWS, range(8)), 2 * V.A)
    exact_equal(rho1_det, rho1_expected)
    rho1_terminal = determinant(
        rho1.extract(RHO1_TERMINAL_ROWS, range(8)).subs(V.h0, -1 / V.D),
        2 * V.A,
    )
    rho1_terminal_expected = (
        2**12 * V.A**7 * V.D**3 * (V.A - V.R) * (V.A + V.R) * V.s**3 * (V.D + 1) ** 3
    )
    exact_equal(rho1_terminal, rho1_terminal_expected)
    print("STAGE:rho_1_closed:pass", flush=True)

    rho6 = -(V.D + 1) / (V.D - 1)
    q6 = V.D * V.s * V.h0 + V.A - V.D * (V.A + V.R)
    matrix6 = base.subs(V.rho, rho6)
    slope6_expected = (
        2**17 * V.A**9 * V.D**4 * V.s**5 * (V.D - 1) ** 2 * (V.D + 1) ** 3 * q6
    )
    slope6 = determinant(matrix6.extract(SLOPE_ROWS, range(8)), 2 * V.A * (V.D - 1))
    exact_equal(slope6, slope6_expected)
    h0_6 = (V.D * (V.A + V.R) - V.A) / (V.D * V.s)
    p6 = (
        6 * V.A**2 * V.D**2
        - 2 * V.A**2
        + V.A * V.D**4 * V.R
        + 5 * V.A * V.D**2 * V.R
        + 2 * V.A * V.D**2 * V.h3
        - 2 * V.A * V.R
        - 6 * V.A * V.h3
        + 2 * V.D**2 * V.R**2
        + 2 * V.D**2 * V.R * V.h3
        - V.R**2
        - 4 * V.R * V.h3
    )
    linear6_expected = (
        -(2**16) * V.A**10 * V.D**4 * V.s**4 * (V.D - 1) * (V.D + 1) ** 3 * p6
    )
    linear6 = determinant(
        matrix6.extract(LINEAR_ROWS, range(8)).subs(V.h0, h0_6),
        2 * V.A * (V.D - 1),
    )
    exact_equal(linear6, linear6_expected)
    e6 = (V.A + V.R) * V.D**2 - 3 * V.A - 2 * V.R
    h3_6 = -sp.Poly(p6, V.h3).nth(0) / (2 * e6)
    terminal6_expected = (
        -(2**15)
        * V.A**9
        * V.D**4
        * V.s**6
        * (V.D - 1) ** 2
        * (V.D + 1) ** 4
        * (V.A * V.D**2 - 5 * V.A - 2 * V.R)
        * e6**7
        * (V.A * V.D**2 + V.A + 2 * V.D**2 * V.R - V.R)
    )
    terminal6 = determinant(
        matrix6.extract(TERMINAL_ROWS, range(8)).subs(
            {V.h0: h0_6, V.h3: h3_6}, simultaneous=True
        ),
        2 * V.A * (V.D - 1) * e6,
    )
    exact_equal(terminal6, terminal6_expected)
    print("STAGE:f6_closed:pass", flush=True)

    n8 = V.A * V.D - V.A + V.R * V.D
    d8 = V.A * V.D + V.A + V.R * V.D
    rho8 = -n8 / d8
    q8 = V.D * V.R * V.s * V.h0 - V.A**2 * (V.D + 1) - V.D * V.R * V.s
    matrix8 = base.subs(V.rho, rho8)
    slope8_expected = (
        -(2**10)
        * V.A**4
        * V.D**4
        * (V.A + V.R) ** 2
        * V.s**5
        * (V.D - 1)
        * (V.D + 1) ** 2
        * n8
        * d8
        * q8
    )
    slope8 = determinant(matrix8.extract(SLOPE_ROWS, range(8)), d8)
    exact_equal(slope8, slope8_expected)
    h0_8 = (V.A**2 * (V.D + 1) + V.D * V.R * V.s) / (V.D * V.R * V.s)
    p8 = (
        V.A**2 * V.D**2
        + 5 * V.A**2
        + V.A * V.D**2 * V.R
        + 4 * V.A * V.R
        + 2 * V.A * V.h3
        + V.R**2
        + 2 * V.R * V.h3
    )
    linear8_expected = (
        2**9
        * V.A**5
        * V.D**4
        * V.R**9
        * (V.A + V.R) ** 2
        * V.s**4
        * (V.D - 1)
        * (V.D + 1) ** 3
        * n8
        * d8
        * p8
    )
    linear8 = determinant(
        matrix8.extract(LINEAR_ROWS, range(8)).subs(V.h0, h0_8), V.R * d8
    )
    exact_equal(linear8, linear8_expected)
    h3_8 = -sp.Poly(p8, V.h3).nth(0) / (2 * (V.A + V.R))
    c81 = V.A**2 * V.D**2 - V.A**2 + V.A * V.D**2 * V.R - 5 * V.A * V.R - 2 * V.R**2
    c82 = (
        V.A**2 * V.D**2
        - V.A**2
        + 3 * V.A * V.D**2 * V.R
        + V.A * V.R
        + 2 * V.D**2 * V.R**2
    )
    terminal8_expected = (
        2**8
        * V.A**4
        * V.D**4
        * V.R**8
        * (V.A + V.R) ** 8
        * V.s**6
        * (V.D + 1) ** 2
        * n8
        * d8
        * c81
        * c82
    )
    terminal8 = determinant(
        matrix8.extract(TERMINAL_ROWS, range(8)).subs(
            {V.h0: h0_8, V.h3: h3_8}, simultaneous=True
        ),
        V.R * (V.A + V.R) * d8,
    )
    exact_equal(terminal8, terminal8_expected)
    print("STAGE:f8_closed:pass", flush=True)

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "Q(A,R,D)",
                "component": 22,
                "slice": "H=0, h2=0, rho*(rho+1)!=0",
                "closed_divisors": ["rho=1", "f6=0", "f8=0"],
                "other_h2_zero_cases_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
