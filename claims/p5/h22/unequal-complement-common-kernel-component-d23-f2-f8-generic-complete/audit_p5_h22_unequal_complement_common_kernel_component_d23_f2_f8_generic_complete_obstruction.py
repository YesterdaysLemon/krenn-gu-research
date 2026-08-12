#!/usr/bin/env python3
"""No-repository-import audit of the generic component-22 F2/F8 closure."""

from __future__ import annotations

import itertools
import json

import sympy as sp

A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
s = 2 * A + R
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
H0_ROWS = (0, 1, 2, 3, 4, 7, 8, 11)
H3_ROWS_A = (0, 1, 2, 3, 4, 7, 8, 9)
H3_ROWS_B = (0, 1, 2, 3, 4, 7, 8, 13)


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def component_rows():
    u = (1 - D) / 2
    v = (1 + D) / 2
    g = -s / 2
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    mr = add(m, c, R)
    d = (g, g, u, v)
    y0 = (0, D * s, -u, v)
    x0 = (-A * v, A * (u + 1) + R, 1, 0)
    return (y0, m, mr, c), (x0, a, a, d)


def project(row, extension):
    return (row[0], row[1], rho * row[2] + row[3], extension)


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def reconstruct_mixed_matrix():
    alpha, canonical = component_rows()
    shifts = (h0, h1, h2, h3)
    marked = tuple(
        add(canonical[index], alpha[index], shifts[index]) for index in range(4)
    )
    projected_alpha = tuple(project(alpha[index], x[index]) for index in range(4))
    projected_beta = tuple(project(marked[index], x[4 + index]) for index in range(4))
    coefficients = []
    for word in WORDS:
        selected = tuple(
            projected_beta[index] if word[index] else projected_alpha[index]
            for index in range(4)
        )
        coefficients.append(
            sp.expand(
                sum(
                    selected[index][3]
                    * permanent3(
                        tuple(
                            selected[other][:3] for other in range(4) if other != index
                        )
                    )
                    for index in range(4)
                )
            )
        )
    return sp.Matrix(
        [
            [sp.diff(coefficient, variable) for variable in x]
            for word, coefficient in zip(WORDS, coefficients, strict=True)
            if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
        ]
    )


def gaussian_determinant(matrix, rows, generators):
    field = sp.QQ.frac_field(*generators)
    work = [
        [field.from_sympy(sp.cancel(matrix[rows[row], column])) for column in range(8)]
        for row in range(8)
    ]
    sign = field.one
    for column in range(8):
        pivot_row = next(
            (row for row in range(column, 8) if work[row][column]),
            None,
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
    result = sign
    for index in range(8):
        result *= work[index][index]
    return sp.cancel(result.as_expr())


def exact_equal(left, right):
    assert sp.cancel(left - right) == 0


def main() -> None:
    mixed = reconstruct_mixed_matrix()
    assert mixed.shape == (14, 8)

    denominator = A * D + A + D * R
    numerator = A * D - A + D * R
    rho8 = -numerator / denominator
    base = mixed.subs(
        {h1: -1 / (2 * A), h2: -1 / s, rho: rho8},
        simultaneous=True,
    )

    q11 = (
        4 * A**2 * D * h0
        - 3 * A**2 * D
        + A**2
        + 4 * A * D * R * h0
        - 3 * A * D * R
        + A * R
        + D * R**2 * h0
        - D * R**2
    )
    unit11 = (
        512
        * A**4
        * D**4
        * R**2
        * (A + R) ** 3
        * s**4
        * (4 * A + R)
        * (D - 1) ** 2
        * (D + 1) ** 3
        * numerator
        / denominator**7
    )
    det11 = gaussian_determinant(base, H0_ROWS, (A, R, D, h0, h3))
    exact_equal(det11, unit11 * q11)

    h0_value = (D * (3 * A**2 + 3 * A * R + R**2) - A * (A + R)) / (D * s**2)
    reduced = base.subs(h0, h0_value)

    cap_c = 8 * A**3 + 16 * A**2 * R + 11 * A * R**2 + 2 * R**3
    cap_b9 = (
        32 * A**5
        - 4 * A**4 * D**2 * R
        + 100 * A**4 * R
        - 8 * A**3 * D**2 * R**2
        + 116 * A**3 * R**2
        - 6 * A**2 * D**2 * R**3
        + 66 * A**2 * R**3
        - 2 * A * D**2 * R**4
        + 19 * A * R**4
        + 2 * R**5
    )
    cap_b13 = (
        16 * A**4
        + 2 * A**3 * D**2 * R
        + 38 * A**3 * R
        + 34 * A**2 * R**2
        - 2 * A * D**2 * R**3
        + 15 * A * R**3
        + 2 * R**4
    )
    cap_l9 = 2 * s * cap_c * h3 + cap_b9
    cap_l13 = 2 * cap_c * h3 + cap_b13
    unit9 = (
        -512
        * A**5
        * D**4
        * R
        * (A + R) ** 2
        * s**3
        * (D - 1)
        * (D + 1) ** 3
        * numerator
        / denominator**7
    )
    unit13 = (
        256
        * A**4
        * D**4
        * R
        * (A + R) ** 2
        * s**4
        * (D - 1)
        * (D + 1) ** 3
        * numerator
        / denominator**7
    )
    det9 = gaussian_determinant(reduced, H3_ROWS_A, (A, R, D, h3))
    det13 = gaussian_determinant(reduced, H3_ROWS_B, (A, R, D, h3))
    exact_equal(det9, unit9 * cap_l9)
    exact_equal(det13, unit13 * cap_l13)

    incompatibility = -2 * A**2 * R * (A + R) * (4 * A + R) * (D - 1) * (D + 1)
    exact_equal(cap_b9 - s * cap_b13, incompatibility)
    expected_resultant = (
        4 * A**2 * R * (A + R) * (4 * A + R) * (D - 1) * (D + 1) * cap_c
    )
    exact_equal(sp.resultant(cap_l9, cap_l13, h3), expected_resultant)
    assert sp.Poly(expected_resultant, A, R, D) != 0

    print(
        json.dumps(
            {
                "status": "PASS",
                "method": (
                    "no repository imports; independent component rows, "
                    "finite-D23 projection, permanent expansion, mixed "
                    "matrix, and explicit Gaussian elimination"
                ),
                "field": "Q(A,R,D)",
                "component": 22,
                "closed_branch": "H=f2=f8=0",
                "mixed_matrix_shape": mixed.shape,
                "maximal_minors_checked": 3,
                "h3_resultant": str(sp.factor(expected_resultant)),
                "pointwise_special_fibres_closed": False,
                "remaining_f2_residual_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
