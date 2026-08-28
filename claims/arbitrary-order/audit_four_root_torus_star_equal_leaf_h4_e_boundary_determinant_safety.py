#!/usr/bin/env python3
"""Independent selected-row audit of the GLD94 e-boundary calculation.

This audit deliberately does not import the GLD94 verifier, GLD71, GLD86, or
GLD90.  It contracts a separately transcribed sparse subset of the fixed
annihilator directly and recomputes the determinants with SymPy.  The subset
contains every row used by the old/alternate pivots, both auxiliary pivots,
and all displayed bordered residuals.  The primary verifier, which constructs
all 37 rows, owns the universal three-block kernel identity; this audit is an
independent check of the determinant algebra and an exact rational sample.
"""

from __future__ import annotations

import json

import sympy as sp

ROWS = (0, 1, 2, 17, 19, 25, 28, 31, 32)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
OLD_ROWS = (0, 1, 2, 17, 19, 32)
ALTERNATE_ROWS = (0, 1, 17, 19, 28, 32)
CHART_A_ROWS = (0, 1, 2, 17, 19, 25)
CHART_B_ROWS = (0, 1, 17, 19, 25, 28)

# These are the fixed GLD71 sparse annihilator rows, transcribed independently
# rather than imported.  Each entry is ((root, leaf_i, leaf_j, leaf_k), coeff).
SELECTED_RELATIONS = (
    (((1, 1, 1, 1), 1),),
    (((0, 0, 0, 0), 1),),
    (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
    (((0, 0, 1, 1), 1), ((0, 1, 0, 0), -1), ((1, 0, 0, 0), -1), ((1, 1, 0, 0), 2), ((1, 1, 0, 1), -1), ((1, 1, 1, 0), -1)),
    (((0, 0, 1, 0), 1), ((0, 1, 0, 0), 1), ((0, 1, 1, 0), -2), ((0, 1, 1, 1), 1), ((1, 0, 0, 1), -1), ((1, 1, 1, 0), 1)),
    (((1, 1, 0, 0), 1), ((1, 1, 0, 1), -1), ((1, 1, 1, 0), -1), ((1, 2, 0, 0), -1), ((1, 2, 0, 1), 1), ((1, 2, 1, 0), 1), ((2, 1, 0, 0), -1), ((2, 1, 0, 1), 1), ((2, 1, 1, 0), 1), ((2, 2, 0, 0), 1), ((2, 2, 0, 1), -1), ((2, 2, 1, 0), -1)),
    (((0, 0, 1, 0), 1), ((0, 0, 1, 2), -1), ((0, 1, 0, 0), 1), ((0, 1, 0, 2), -1), ((0, 1, 1, 0), -1), ((0, 1, 1, 2), 1), ((2, 0, 1, 0), -1), ((2, 0, 1, 2), 1), ((2, 1, 0, 0), -1), ((2, 1, 0, 2), 1), ((2, 1, 1, 0), 1), ((2, 1, 1, 2), -1)),
    (((1, 0, 0, 0), 8), ((1, 0, 0, 1), -4), ((1, 0, 1, 0), -4), ((1, 0, 1, 1), 2), ((1, 1, 0, 0), 2), ((1, 1, 0, 1), -1), ((1, 1, 1, 0), -1), ((1, 1, 1, 2), 3), ((1, 1, 2, 1), 3), ((1, 2, 0, 0), -12), ((1, 2, 0, 1), 6), ((1, 2, 1, 0), 6), ((2, 1, 1, 1), 6)),
    (((0, 0, 0, 1), 1), ((0, 0, 0, 2), -3), ((0, 0, 1, 0), -2), ((0, 0, 1, 1), 4), ((0, 0, 2, 1), -6), ((0, 1, 0, 0), 1), ((0, 1, 0, 1), -2), ((0, 1, 1, 0), 4), ((0, 1, 1, 1), -8), ((0, 1, 2, 0), -6), ((0, 1, 2, 1), 12), ((0, 2, 0, 0), -3), ((2, 0, 0, 0), -6)),
)
ROW_INDEX = {row: index for index, row in enumerate(ROWS)}


def select(matrix: sp.Matrix, rows: tuple[int, ...], columns: tuple[int, ...]) -> sp.Matrix:
    return matrix.extract(tuple(ROW_INDEX[row] for row in rows), columns)


def coefficient_matrix(leaves: tuple[sp.Matrix, ...]) -> sp.Matrix:
    return sp.Matrix(
        [
            [
                sum(
                    coefficient
                    * leaves[0][indices[1], component]
                    * leaves[1][indices[2], component]
                    * leaves[2][indices[3], component]
                    for indices, coefficient in support
                    if indices[0] == root
                )
                for root in range(3)
                for component in range(3)
            ]
            for support in SELECTED_RELATIONS
        ]
    )


def bordered_numerator(
    matrix: sp.Matrix,
    pivot_rows: tuple[int, ...],
    target: tuple[int, int],
) -> sp.Expr:
    pivot = select(matrix, pivot_rows, PIVOT_COLUMNS)
    denominator = sp.cancel(pivot.det(method="domain-ge"))
    row, column = target
    bordered = select(matrix, (*pivot_rows, row), (*PIVOT_COLUMNS, column))
    quotient = sp.cancel(bordered.det(method="domain-ge") / denominator)
    return sp.factor(quotient.as_numer_denom()[0])


def bordered_quotient(
    matrix: sp.Matrix,
    pivot_rows: tuple[int, ...],
    target: tuple[int, int],
) -> sp.Expr:
    pivot = select(matrix, pivot_rows, PIVOT_COLUMNS)
    denominator = sp.cancel(pivot.det(method="domain-ge"))
    row, column = target
    bordered = select(matrix, (*pivot_rows, row), (*PIVOT_COLUMNS, column))
    return sp.cancel(bordered.det(method="domain-ge") / denominator)


def assert_zero(value: sp.Expr) -> None:
    assert sp.cancel(value) == 0


def check() -> dict[str, object]:
    p, q, a, b, c, t = sp.symbols("p q a b c t")
    d0 = p + q - 1
    pnorm = p**2 - p + 1
    l1 = p**2 + 2 * p * q - 2 * p - q
    l2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    total_pivot_factor = 2 * p * q - p - q + 2
    q6 = (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4 + 2 * p**3 * q**3
        - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3 + 2 * p**2 * q**4
        - 7 * p**2 * q**3 + 12 * p**2 * q**2 - 7 * p**2 * q + 2 * p**2
        - 2 * p * q**4 + 5 * p * q**3 - 7 * p * q**2 + 2 * p * q
        + q**4 - 2 * q**3 + 2 * q**2
    )
    curve = (
        2 * p**4 * q**2 - 2 * p**4 * q - p**4 + 2 * p**3 * q**3
        - 7 * p**3 * q**2 + p**3 * q + 4 * p**3 + 2 * p**2 * q**4
        - 7 * p**2 * q**3 + 6 * p**2 * q**2 + 5 * p**2 * q - 4 * p**2
        - 2 * p * q**4 + p * q**3 + 5 * p * q**2 - 4 * p * q
        - q**4 + 4 * q**3 - 4 * q**2
    )
    s = (p + q - p * q) / d0
    leaf = sp.Matrix([[1, 1, 1], [p, q, s], [a, 1 + b, 1 + c]])
    syndrome = coefficient_matrix((leaf, leaf, leaf))

    old_pivot = sp.factor(select(syndrome, OLD_ROWS, PIVOT_COLUMNS).det())
    alternate_pivot = sp.factor(
        select(syndrome, ALTERNATE_ROWS, PIVOT_COLUMNS).det()
    )
    x0 = a * (p**2 - 1) - (b + 1) * (q**2 - 1)
    x1 = a * p * (p - 2) - b * q * (q - 2) - p * (p - 2)
    assert_zero(old_pivot + 6 * (p - q) ** 2 * x0 * q6)
    assert_zero(alternate_pivot + 6 * (p - q) ** 2 * x1 * q6)

    denominator = 2 * t**2 - 2 * t - 1
    p_on_e = (t**2 + 2 * t - 2) / denominator
    assert_zero(e.subs({p: p_on_e, q: t}))
    assert sp.gcd(
        sp.Poly(denominator, t, domain=sp.QQ),
        sp.Poly(t**2 + 2 * t - 2, t, domain=sp.QQ),
    ).degree() == 0
    restricted = {
        "d0": (2 * t - 1) * (t**2 - t + 1) / denominator,
        "p_minus_q": -(t - 2) * (t + 1) * (2 * t - 1) / denominator,
        "P": 3 * (t**2 - t + 1) ** 2 / denominator**2,
        "Q6": 8 * (t**2 - t + 1) ** 6 / denominator**4,
        "curve": -6 * t * (t - 2) * (t - 1) * (t + 1) * (t**2 - t + 1) ** 2 / denominator**2,
    }
    for expression, expected in (
        (d0, restricted["d0"]),
        (p - q, restricted["p_minus_q"]),
        (pnorm, restricted["P"]),
        (q6, restricted["Q6"]),
        (curve, restricted["curve"]),
    ):
        assert_zero(expression.subs({p: p_on_e, q: t}) - expected)

    f25 = (
        2 * denominator**2 * a - 9 * t * (t - 1) * b
        + (t - 2) * (t + 1) * (2 * t - 1) ** 2 * c
        - 2 * t**4 + 4 * t**3 - 6 * t**2 + 4 * t - 2
    )
    f31 = (
        2 * denominator * (t**4 - 8 * t**3 + 6 * t**2 + 4 * t - 2) * a
        + 9 * t * (t - 1) * (t**2 + 2 * t - 2) * b
        + (-4 * t**6 + 27 * t**4 - 17 * t**3 - 18 * t**2 + 18 * t - 4) * c
        - 4 * t**6 + 12 * t**5 + 6 * t**4 - 8 * t**3 - 24 * t**2 + 24 * t - 4
    )
    old_25 = bordered_quotient(syndrome, OLD_ROWS, (25, 5))
    old_31 = bordered_quotient(syndrome, OLD_ROWS, (31, 5))
    alternate_25 = bordered_quotient(syndrome, ALTERNATE_ROWS, (25, 5))
    alternate_31 = bordered_quotient(syndrome, ALTERNATE_ROWS, (31, 5))
    for actual, expected in (
        (old_25, f25),
        (alternate_25, f25),
    ):
        assert_zero(
            sp.cancel(actual.subs({p: p_on_e, q: t}))
            + 3 * expected / ((t - 2) * (t + 1) * (2 * t - 1) ** 3)
        )
    for actual, expected in (
        (old_31, f31),
        (alternate_31, f31),
    ):
        assert_zero(
            sp.cancel(actual.subs({p: p_on_e, q: t}))
            - 18 * expected / ((t - 2) * (t + 1) * (2 * t - 1) ** 4)
        )

    # Recompute both simultaneous-pivot resultants from the selected rows,
    # before specializing e=0, so their Schur numerator normalization is fixed.
    double_a = (q - 1) * (q + 1) * (p + q - 2) / total_pivot_factor
    double_b = p * (p - 2) * (p + q) / total_pivot_factor
    double_syndrome = syndrome.subs({a: double_a, b: double_b})
    chart_a = {
        target: bordered_numerator(double_syndrome, CHART_A_ROWS, target)
        for target in ((28, 2), (32, 8))
    }
    chart_b = {
        target: bordered_numerator(double_syndrome, CHART_B_ROWS, target)
        for target in ((2, 8), (32, 8))
    }
    chart_a_resultant = sp.factor(sp.resultant(chart_a[(28, 2)], chart_a[(32, 8)], c))
    chart_b_resultant = sp.factor(sp.resultant(chart_b[(2, 8)], chart_b[(32, 8)], c))
    assert_zero(chart_a_resultant + 6 * l1 * total_pivot_factor * l2 * curve)
    chart_b_factor = p * q * (p - 2) * (q - 2) * (p + q)
    assert_zero(chart_b_resultant + 6 * chart_b_factor * l1 * l2 * curve)

    forced_a = (t**2 - 1) / denominator
    forced_b = (
        (t - 2)
        * ((t + 1) * (2 * t - 1) ** 2 * c + 2 * t * (t**2 + 2 * t - 2))
        / (9 * t * (t - 1))
    )
    kernel = sp.Matrix(
        [-2 * denominator**3, 27 * t * (t - 1), (t - 2) * (t + 1) * (2 * t - 1) ** 4]
    )
    family_syndrome = syndrome.subs(
        {p: p_on_e, q: t, a: forced_a, b: forced_b}
    )
    for block in range(3):
        assert (
            family_syndrome[:, 3 * block : 3 * block + 3] * kernel
        ).applyfunc(sp.cancel) == sp.zeros(len(ROWS), 1)

    sample = {t: 3, c: 0}
    sample_matrix = family_syndrome.subs(sample)
    sample_leaf = leaf.subs(
        {
            p: sp.Rational(13, 11),
            q: 3,
            a: sp.Rational(8, 11),
            b: sp.Rational(13, 9),
            c: 0,
        }
    )
    assert sample_leaf.det() == sp.Rational(24, 11)
    assert sample_matrix.rank() == 6
    assert tuple(kernel.subs(sample)) == (-2662, 162, 2500)

    return {
        "status": "independent_selected_row_GLD94_audit",
        "imports_primary_or_GLD71": False,
        "selected_global_rows": list(ROWS),
        "pivot_columns": list(PIVOT_COLUMNS),
        "parameterization_replayed": True,
        "raw_pivots_replayed": True,
        "one_pivot_residuals_replayed": True,
        "simultaneous_resultants_replayed": True,
        "selected_rows_all_block_kernel_replayed": True,
        "sample": {
            "p": "13/11",
            "q": "3",
            "a": "8/11",
            "b": "13/9",
            "c": "0",
            "leaf_determinant": "24/11",
            "selected_matrix_rank": 6,
            "kernel": [str(value) for value in kernel.subs(sample)],
        },
        "full_37_row_kernel_independently_replayed": False,
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    result = check()
    print("independent selected-row GLD94 audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
