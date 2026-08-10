#!/usr/bin/env python3
"""Low-level audit of component 22's H=f2=f7 intersection closure."""

from __future__ import annotations

import json

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)



A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
s = 2 * A + R
FIRST_ROWS = (0, 1, 2, 3, 4, 7, 8, 9)
SECOND_ROWS = (0, 1, 2, 3, 4, 7, 8, 10)
TERMINAL_ROWS = (0, 1, 2, 3, 4, 7, 8, 11)


def gaussian_determinant(matrix, rows, generators):
    field = sp.QQ.frac_field(*generators)
    work = [
        [field.from_sympy(sp.cancel(matrix[rows[i], column])) for column in range(8)]
        for i in range(8)
    ]
    sign = field.one
    for column in range(8):
        pivot_row = next(
            (index for index in range(column, 8) if work[index][column]), None
        )
        if pivot_row is None:
            return sp.S.Zero
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, 8):
            if not work[row][column]:
                continue
            multiplier = work[row][column] / pivot
            for index in range(column, 8):
                work[row][index] -= multiplier * work[column][index]
    value = sign
    for index in range(8):
        value *= work[index][index]
    return sp.cancel(value.as_expr())


def exact_equal(left, right):
    assert sp.cancel(left - right) == 0


def main() -> None:
    alpha, canonical = component_rows(A, R, D)
    marked = shifted(canonical, alpha, (h0, h1, h2, h3))
    model = build_model(alpha, marked, x, "D23", "finite", rho)
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in model["mixed"]]
    )

    denominator = A * D + A + R
    rho7 = -(A * D - A - R) / denominator
    base = matrix.subs(
        {h1: -1 / (2 * A), h2: -1 / s, rho: rho7}, simultaneous=True
    )
    cap_q0 = 4 * A * D * h0 - 3 * A * D + A + 2 * D * R * h0 - D * R + R
    first_unit = (
        -256
        * A**3
        * D**4
        * R**2
        * (A + R) ** 2
        * s**6
        * (D - 1)
        * (D + 1) ** 2
        * (A * D - A - R) ** 2
        / denominator**6
    )
    first = gaussian_determinant(base, FIRST_ROWS, (A, R, D, h0, h3))
    exact_equal(first, first_unit * cap_q0)

    h0_value = (3 * A * D - A + D * R - R) / (2 * D * s)
    second_matrix = base.subs(h0, h0_value)
    second_unit = (
        256
        * A**3
        * D**4
        * R
        * (A + R) ** 3
        * s**7
        * (D - 1)
        * (D + 1) ** 3
        * (A * D - A - R) ** 2
        / denominator**6
    )
    second = gaussian_determinant(second_matrix, SECOND_ROWS, (A, R, D, h3))
    exact_equal(second, second_unit * (s + 2 * h3))

    cap_t7 = (
        4 * A**2 * D**2
        - 4 * A**2
        + 6 * A * D**2 * R
        + 2 * A * R
        + D**2 * R**2
        + 3 * R**2
    )
    terminal_unit = (
        -128
        * A**2
        * D**4
        * R**2
        * (A + R) ** 3
        * s**5
        * (D + 1) ** 2
        * (A * D - A - R) ** 2
        / denominator**6
    )
    terminal = gaussian_determinant(
        second_matrix.subs(h3, -s / 2), TERMINAL_ROWS, (A, R, D)
    )
    exact_equal(terminal, terminal_unit * cap_t7)

    print(
        json.dumps(
            {
                "status": "PASS",
                "method": "low-level model build and explicit Gaussian determinants",
                "field": "Q(A,R,D)",
                "component": 22,
                "closed_branch": "H=f2=f7=0",
                "eight_by_eight_determinants": 3,
                "terminal_coefficient_unit": str(sp.factor(cap_t7)),
                "other_f2_branches_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
