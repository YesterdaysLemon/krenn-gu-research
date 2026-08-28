#!/usr/bin/env python3
"""Independent exact audit of GLD93.

This audit imports neither the primary verifier nor the GLD71 builder.  It
stores the nine sparse GLD71 relations needed by the displayed certificates
in a separate representation, contracts them directly against the equal-leaf
frame, and recomputes every selected six- and seven-minor with SymPy.  The
primary's full 37-row reconstruction is therefore not duplicated here; the
audit checks the exact row contractions and all divisor-case identities by a
different construction.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
THEOREM = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_L1_L2_RANK_SEVEN_EXCLUSION_THEOREM.md"
)

PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
OLD_ROWS = (0, 1, 2, 17, 19, 32)
ALTERNATE_ROWS = (0, 1, 17, 19, 28, 32)
AUXILIARY_ROWS = (0, 1, 2, 17, 19, 25)

# These are the nine relation supports touched by all GLD93 minors.  The
# first coordinate is the root index; it is selected against the output
# root column during the direct contraction below.
SELECTED_RELATIONS = {
    0: (((1, 1, 1, 1), 1),),
    1: (((0, 0, 0, 0), 1),),
    2: (((2, 2, 0, 0), 1), ((2, 2, 1, 1), -1)),
    17: (
        ((0, 0, 1, 1), 1),
        ((0, 1, 0, 0), -1),
        ((1, 0, 0, 0), -1),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
    ),
    19: (
        ((0, 0, 1, 0), 1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 1, 0), -2),
        ((0, 1, 1, 1), 1),
        ((1, 0, 0, 1), -1),
        ((1, 1, 1, 0), 1),
    ),
    25: (
        ((1, 1, 0, 0), 1),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 2, 0, 0), -1),
        ((1, 2, 0, 1), 1),
        ((1, 2, 1, 0), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 1), 1),
        ((2, 1, 1, 0), 1),
        ((2, 2, 0, 0), 1),
        ((2, 2, 0, 1), -1),
        ((2, 2, 1, 0), -1),
    ),
    28: (
        ((0, 0, 1, 0), 1),
        ((0, 0, 1, 2), -1),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 2), -1),
        ((0, 1, 1, 0), -1),
        ((0, 1, 1, 2), 1),
        ((2, 0, 1, 0), -1),
        ((2, 0, 1, 2), 1),
        ((2, 1, 0, 0), -1),
        ((2, 1, 0, 2), 1),
        ((2, 1, 1, 0), 1),
        ((2, 1, 1, 2), -1),
    ),
    31: (
        ((1, 0, 0, 0), 8),
        ((1, 0, 0, 1), -4),
        ((1, 0, 1, 0), -4),
        ((1, 0, 1, 1), 2),
        ((1, 1, 0, 0), 2),
        ((1, 1, 0, 1), -1),
        ((1, 1, 1, 0), -1),
        ((1, 1, 1, 2), 3),
        ((1, 1, 2, 1), 3),
        ((1, 2, 0, 0), -12),
        ((1, 2, 0, 1), 6),
        ((1, 2, 1, 0), 6),
        ((2, 1, 1, 1), 6),
    ),
    32: (
        ((0, 0, 0, 1), 1),
        ((0, 0, 0, 2), -3),
        ((0, 0, 1, 0), -2),
        ((0, 0, 1, 1), 4),
        ((0, 0, 2, 1), -6),
        ((0, 1, 0, 0), 1),
        ((0, 1, 0, 1), -2),
        ((0, 1, 1, 0), 4),
        ((0, 1, 1, 1), -8),
        ((0, 1, 2, 0), -6),
        ((0, 1, 2, 1), 12),
        ((0, 2, 0, 0), -3),
        ((2, 0, 0, 0), -6),
    ),
}


def direct_matrix(
    p: sp.Expr,
    q: sp.Expr,
    s: sp.Expr,
    a: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
) -> tuple[tuple[int, tuple[sp.Expr, ...]], ...]:
    """Contract the selected sparse relations directly against equal leaves."""

    leaf = ((1, 1, 1), (p, q, s), (a, 1 + b, 1 + c))
    rows = []
    for row, support in SELECTED_RELATIONS.items():
        entries = []
        for root in range(3):
            for component in range(3):
                entries.append(
                    sp.expand(
                        sum(
                            coefficient
                            * leaf[i][component]
                            * leaf[j][component]
                            * leaf[k][component]
                            for (support_root, i, j, k), coefficient in support
                            if support_root == root
                        )
                    )
                )
        rows.append((row, tuple(entries)))
    return tuple(rows)


def matrix_lookup(
    matrix: tuple[tuple[int, tuple[sp.Expr, ...]], ...],
) -> dict[int, tuple[sp.Expr, ...]]:
    return dict(matrix)


def determinant(
    matrix: dict[int, tuple[sp.Expr, ...]],
    rows: tuple[int, ...],
    columns: tuple[int, ...],
) -> sp.Expr:
    selected = sp.Matrix(
        [[matrix[row][column] for column in columns] for row in rows]
    )
    return sp.factor(sp.cancel(selected.det(method="domain-ge")))


def assert_identity(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.cancel(left - right) == 0, sp.factor(left - right)


def check() -> dict[str, object]:
    assert THEOREM.exists()
    p, q, a, b, c = sp.symbols("p q a b c")
    s = (p + q - p * q) / (p + q - 1)
    pnorm = p**2 - p + 1
    qnorm = q**2 - q + 1

    # The selected row supports are pairwise distinct and cover exactly the
    # row labels named by the GLD93 certificates.
    assert tuple(dict(SELECTED_RELATIONS)) == (0, 1, 2, 17, 19, 25, 28, 31, 32)
    matrix = matrix_lookup(direct_matrix(p, q, s, a, b, c))
    assert len(matrix) == 9 and all(len(row) == 9 for row in matrix.values())

    q_on_l1 = p * (2 - p) / (2 * p - 1)
    l1_matrix = matrix_lookup(
        direct_matrix(p, q_on_l1, p, a, b, c)
    )
    h10 = (
        4 * a * p**2
        - 4 * a * p
        + a
        - b * p**2
        + 4 * b * p
        - b
        - p**2
        + 4 * p
        - 1
    )
    h11 = (
        4 * a * p**2
        - 4 * a * p
        + a
        - b * p**2
        - 2 * b * p
        + 2 * b
        - 4 * p**2
        + 4 * p
        - 1
    )
    l1_old = determinant(l1_matrix, OLD_ROWS, PIVOT_COLUMNS)
    l1_old_7 = determinant(l1_matrix, OLD_ROWS + (25,), PIVOT_COLUMNS + (5,))
    l1_alt = determinant(l1_matrix, ALTERNATE_ROWS, PIVOT_COLUMNS)
    l1_alt_7 = determinant(
        l1_matrix, ALTERNATE_ROWS + (25,), PIVOT_COLUMNS + (5,)
    )
    assert_identity(
        l1_old,
        -324
        * p**4
        * (p - 1) ** 5
        * (p + 1)
        * pnorm**3
        * h10
        / (2 * p - 1) ** 8,
    )
    assert_identity(
        l1_old_7,
        324
        * p**4
        * (p - 1) ** 5
        * (p + 1)
        * pnorm**3
        * (a - c - 1)
        * h10
        / (2 * p - 1) ** 7,
    )
    assert_identity(
        l1_alt,
        -324
        * p**5
        * (p - 2)
        * (p - 1) ** 4
        * pnorm**3
        * h11
        / (2 * p - 1) ** 8,
    )
    assert_identity(
        l1_alt_7,
        324
        * p**5
        * (p - 2)
        * (p - 1) ** 4
        * pnorm**3
        * (a - c - 1)
        * h11
        / (2 * p - 1) ** 7,
    )

    l1_a = -(p - 1) ** 2 * (p**2 - 4 * p + 1) / (2 * p - 1) ** 3
    l1_b = -p**2 / (2 * p - 1)
    l1_double = matrix_lookup(
        direct_matrix(p, q_on_l1, p, l1_a, l1_b, c)
    )
    f1 = (
        (8 * p**3 - 12 * p**2 + 6 * p - 1) * c
        + p**4
        + 2 * p**3
        - 2 * p**2
    )
    g_l1 = sp.Matrix(
        [[1, 1, 1], [p, q_on_l1, p], [l1_a, 1 + l1_b, 1 + c]]
    )
    assert_identity(g_l1.det(), -3 * p * (p - 1) * f1 / (2 * p - 1) ** 4)
    assert_identity(
        determinant(l1_double, AUXILIARY_ROWS + (32,), PIVOT_COLUMNS + (8,)),
        -2916
        * p**5
        * (p - 1) ** 6
        * (p + 1)
        * pnorm**4
        * f1
        / (2 * p - 1) ** 11,
    )

    l1_exceptional = {
        "(2,0)": determinant(
            matrix_lookup(direct_matrix(2, 0, 2, a, b, c)),
            (0, 1, 2, 17, 19, 32, 31),
            PIVOT_COLUMNS + (8,),
        ),
        "(-1,1)": determinant(
            matrix_lookup(direct_matrix(-1, 1, -1, a, b, c)),
            (0, 1, 17, 19, 28, 32, 31),
            PIVOT_COLUMNS + (8,),
        ),
    }
    assert_identity(l1_exceptional["(2,0)"], -27648 * (a - c - 1))
    assert_identity(l1_exceptional["(-1,1)"], 6912 * (a - c - 1))

    p_on_l2 = q * (2 - q) / (2 * q - 1)
    l2_matrix = matrix_lookup(
        direct_matrix(p_on_l2, q, q, a, b, c)
    )
    h20 = (
        a * q**2
        - 4 * a * q
        + a
        - 4 * b * q**2
        + 4 * b * q
        - b
        - 4 * q**2
        + 4 * q
        - 1
    )
    h21 = (
        a * q**2
        + 2 * a * q
        - 2 * a
        - 4 * b * q**2
        + 4 * b * q
        - b
        - q**2
        - 2 * q
        + 2
    )
    l2_old = determinant(l2_matrix, OLD_ROWS, PIVOT_COLUMNS)
    l2_old_7 = determinant(l2_matrix, OLD_ROWS + (25,), PIVOT_COLUMNS + (5,))
    l2_alt = determinant(l2_matrix, ALTERNATE_ROWS, PIVOT_COLUMNS)
    l2_alt_7 = determinant(
        l2_matrix, ALTERNATE_ROWS + (25,), PIVOT_COLUMNS + (5,)
    )
    assert_identity(
        l2_old,
        -324
        * q**4
        * (q - 1) ** 5
        * (q + 1)
        * qnorm**3
        * h20
        / (2 * q - 1) ** 8,
    )
    assert_identity(
        l2_old_7,
        324
        * q**4
        * (q - 1) ** 5
        * (q + 1)
        * qnorm**3
        * (b - c)
        * h20
        / (2 * q - 1) ** 7,
    )
    assert_identity(
        l2_alt,
        -324
        * q**5
        * (q - 2)
        * (q - 1) ** 4
        * qnorm**3
        * h21
        / (2 * q - 1) ** 8,
    )
    assert_identity(
        l2_alt_7,
        324
        * q**5
        * (q - 2)
        * (q - 1) ** 4
        * qnorm**3
        * (b - c)
        * h21
        / (2 * q - 1) ** 7,
    )

    l2_a = -(q - 1) ** 2 / (2 * q - 1)
    l2_b = -q**2 * (q**2 + 2 * q - 2) / (2 * q - 1) ** 3
    l2_double = matrix_lookup(
        direct_matrix(p_on_l2, q, q, l2_a, l2_b, c)
    )
    f2 = (
        (8 * q**3 - 12 * q**2 + 6 * q - 1) * c
        + q**4
        + 2 * q**3
        - 2 * q**2
    )
    g_l2 = sp.Matrix(
        [[1, 1, 1], [p_on_l2, q, q], [l2_a, 1 + l2_b, 1 + c]]
    )
    assert_identity(g_l2.det(), 3 * q * (q - 1) * f2 / (2 * q - 1) ** 4)
    assert_identity(
        determinant(l2_double, AUXILIARY_ROWS + (32,), PIVOT_COLUMNS + (8,)),
        2916
        * q**5
        * (q - 1) ** 6
        * (q + 1)
        * qnorm**4
        * f2
        / (2 * q - 1) ** 11,
    )

    q2_first = determinant(
        matrix_lookup(direct_matrix(0, 2, 2, -3 * b - 3, b, c)),
        (0, 1, 17, 19, 25, 31, 32),
        (0, 1, 2, 3, 4, 5, 6),
    )
    q2_second = determinant(
        matrix_lookup(direct_matrix(0, 2, 2, -3 * b - 3, b, c)),
        (0, 1, 17, 19, 25, 31, 32),
        (0, 1, 2, 3, 4, 5, 7),
    )
    qm1_first = determinant(
        matrix_lookup(direct_matrix(1, -1, -1, 1 - 3 * b, b, c)),
        (0, 1, 17, 19, 25, 28, 32),
        (0, 1, 2, 3, 4, 5, 6),
    )
    qm1_second = determinant(
        matrix_lookup(direct_matrix(1, -1, -1, 1 - 3 * b, b, c)),
        (0, 1, 17, 19, 25, 31, 32),
        (0, 1, 2, 3, 4, 5, 7),
    )
    assert_identity(q2_first, -62208 * (b + 1) * (b - c) ** 2)
    assert_identity(q2_second, -20736 * (3 * b + 1) * (b - c) ** 2)
    assert_identity(qm1_first, -1728 * (3 * b - 1) * (b - c) ** 2)
    assert_identity(qm1_second, -10368 * (3 * b + 7) * (b - c) ** 2)

    # The four exceptional linear factors have no common root, which is the
    # exact final step after D(Omega) supplies a-c-1 or b-c nonzero.
    assert sp.gcd(sp.Poly(b + 1, b), sp.Poly(3 * b + 1, b)).degree() == 0
    assert sp.gcd(sp.Poly(3 * b - 1, b), sp.Poly(3 * b + 7, b)).degree() == 0

    return {
        "status": "independent_selected_relation_contraction_audit",
        "gld_identifier": "GLD93",
        "imports_primary_or_GLD71_builder": False,
        "selected_relation_count": len(SELECTED_RELATIONS),
        "selected_relation_rows": list(SELECTED_RELATIONS),
        "l1_six_and_seven_minor_identities_replayed": True,
        "l1_double_pivot_and_exceptional_points_replayed": True,
        "l2_six_and_seven_minor_identities_replayed": True,
        "l2_double_pivot_and_exceptional_points_replayed": True,
        "naive_pq_symmetry_used": False,
        "full_37_row_reconstruction_independent": False,
        "remaining_H4_boundaries": [
            "Q6=0",
            "e=0",
            "pulled-back GLD83 Fitting ideal",
            "other charts/components/gauges/source branches",
        ],
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    result = check()
    print("independent GLD93 selected-relation contraction audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
