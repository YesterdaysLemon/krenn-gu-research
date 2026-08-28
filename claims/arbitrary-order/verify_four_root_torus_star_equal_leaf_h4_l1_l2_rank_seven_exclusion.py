#!/usr/bin/env python3
"""Verify the GLD93 H4 L1/L2 rank-seven exclusion.

The calculation is deliberately direct on both coefficient divisors.  It
reconstructs the fixed 37-row GLD71 syndrome map, specializes the H4 chart
to L1=0 and L2=0 separately, and checks the displayed six- and seven-minor
identities with exact SymPy arithmetic over Q.  The L2 identities are not
obtained by assuming a symmetry of the fixed carrier.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
GLD71 = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD86_DOCUMENT = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_SYNDROME_BOUNDARY_CONTAINMENT_THEOREM.md"
)
GLD87_DOCUMENT = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_THREE_COLLISION_DIVISOR_DETERMINANT_SAFETY_THEOREM.md"
)
GLD89_DOCUMENT = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_P_DIVISOR_AND_D0_OVERLAP_DETERMINANT_SAFETY_THEOREM.md"
)

PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
OLD_ROWS = (0, 1, 2, 17, 19, 32)
ALTERNATE_ROWS = (0, 1, 17, 19, 28, 32)
AUXILIARY_ROWS = (0, 1, 2, 17, 19, 25)
FULL_COLUMNS = (0, 1, 2, 3, 4, 5, 6, 7, 8)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def determinant(
    matrix: sp.Matrix,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
) -> sp.Expr:
    return sp.factor(
        sp.cancel(matrix.extract(rows, columns).det(method="domain-ge"))
    )


def assert_identity(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.cancel(left - right) == 0, sp.factor(left - right)


def l1_data(p: sp.Symbol, q: sp.Symbol):
    """Return the exact L1=0 parameterization and its factor restrictions."""

    q_on = p * (2 - p) / (2 * p - 1)
    return {
        "q": q_on,
        "s": p,
        "p_minus_q": 3 * p * (p - 1) / (2 * p - 1),
        "d0": (p**2 - p + 1) / (2 * p - 1),
        "P": p**2 - p + 1,
        "L2": -3 * p * (p - 1) * (p**2 - p + 1) / (2 * p - 1) ** 2,
        "e": (p - 2) * (p + 1) * (p**2 - p + 1) / (2 * p - 1),
        "T": -(p - 2) * (p + 1),
        "Q6": 6 * p**2 * (p - 1) ** 2 * (p**2 - p + 1) ** 3 / (2 * p - 1) ** 4,
    }


def l2_data(p: sp.Symbol, q: sp.Symbol):
    """Return the exact L2=0 parameterization and its factor restrictions."""

    p_on = q * (2 - q) / (2 * q - 1)
    Q = q**2 - q + 1
    return {
        "p": p_on,
        "s": q,
        "p_minus_q": -3 * q * (q - 1) / (2 * q - 1),
        "d0": Q / (2 * q - 1),
        "P": Q**2 / (2 * q - 1) ** 2,
        "L1": -3 * q * (q - 1) * Q / (2 * q - 1) ** 2,
        "e": -2 * Q**2 / (2 * q - 1),
        "T": -(q - 2) * (q + 1),
        "Q6": 6 * q**2 * (q - 1) ** 2 * Q**3 / (2 * q - 1) ** 4,
    }


def check() -> dict[str, object]:
    assert GLD86_DOCUMENT.exists()
    assert GLD87_DOCUMENT.exists()
    assert GLD89_DOCUMENT.exists()

    gld71 = load_module(GLD71, "gld71_for_gld93")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    assert len(relations) == 37

    p, q, a, b, c = sp.symbols("p q a b c")
    d0 = p + q - 1
    s = (p + q - p * q) / d0
    leaf = sp.Matrix([[1, 1, 1], [p, q, s], [a, 1 + b, 1 + c]])
    syndrome = gld71.coefficient_matrix(
        parent, relations, (leaf, leaf, leaf)
    )
    assert syndrome.shape == (37, 9)

    # The H4 equation is identically zero in this chart.  These factors are
    # named here so the specialization checks cannot silently leave the H4
    # divisor or its upstream localization.
    h4 = p * q + p * s + q * s - p - q - s
    assert sp.cancel(h4) == 0
    pnorm = p**2 - p + 1
    qnorm = q**2 - q + 1
    l1 = p**2 + 2 * p * q - 2 * p - q
    l2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    t = 2 * p * q - p - q + 2

    # L1=0 is parameterized by q=p(2-p)/(2p-1).  The denominator cannot
    # vanish on L1 because its numerator equation is then -3/4.
    l1_branch = l1_data(p, q)
    q_on_l1 = l1_branch["q"]
    assert_identity(l1.subs(q, q_on_l1), 0)
    assert_identity(s.subs(q, q_on_l1), p)
    for name, polynomial in (
        ("p_minus_q", p - q),
        ("d0", d0),
        ("P", pnorm),
        ("L2", l2),
        ("e", e),
        ("T", t),
    ):
        assert_identity(polynomial.subs(q, q_on_l1), l1_branch[name])
    q6 = (
        2 * p**4 * q**2
        - 2 * p**4 * q
        + p**4
        + 2 * p**3 * q**3
        - 7 * p**3 * q**2
        + 5 * p**3 * q
        - 2 * p**3
        + 2 * p**2 * q**4
        - 7 * p**2 * q**3
        + 12 * p**2 * q**2
        - 7 * p**2 * q
        + 2 * p**2
        - 2 * p * q**4
        + 5 * p * q**3
        - 7 * p * q**2
        + 2 * p * q
        + q**4
        - 2 * q**3
        + 2 * q**2
    )
    assert_identity(q6.subs(q, q_on_l1), l1_branch["Q6"])

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
    l1_syndrome = syndrome.subs(q, q_on_l1)
    l1_old = determinant(l1_syndrome, OLD_ROWS, PIVOT_COLUMNS)
    l1_old_7 = determinant(
        l1_syndrome, OLD_ROWS + (25,), PIVOT_COLUMNS + (5,)
    )
    l1_alt = determinant(l1_syndrome, ALTERNATE_ROWS, PIVOT_COLUMNS)
    l1_alt_7 = determinant(
        l1_syndrome, ALTERNATE_ROWS + (25,), PIVOT_COLUMNS + (5,)
    )
    l1_prefactor = p**4 * (p - 1) ** 5 * pnorm**3
    assert_identity(
        l1_old,
        -324 * l1_prefactor * (p + 1) * h10 / (2 * p - 1) ** 8,
    )
    assert_identity(
        l1_old_7,
        324
        * l1_prefactor
        * (p + 1)
        * (a - c - 1)
        * h10
        / (2 * p - 1) ** 7,
    )
    l1_alt_prefactor = p**5 * (p - 1) ** 4 * pnorm**3
    assert_identity(
        l1_alt,
        -324 * l1_alt_prefactor * (p - 2) * h11 / (2 * p - 1) ** 8,
    )
    assert_identity(
        l1_alt_7,
        324
        * l1_alt_prefactor
        * (p - 2)
        * (a - c - 1)
        * h11
        / (2 * p - 1) ** 7,
    )

    # If both raw pivots vanish away from p=2,-1, solve their two linear
    # brackets and use one auxiliary seven-minor.
    l1_double_a = -((p - 1) ** 2 * (p**2 - 4 * p + 1)) / (2 * p - 1) ** 3
    l1_double_b = -p**2 / (2 * p - 1)
    l1_double = syndrome.subs(
        {q: q_on_l1, a: l1_double_a, b: l1_double_b}
    )
    f1 = (
        (8 * p**3 - 12 * p**2 + 6 * p - 1) * c
        + p**4
        + 2 * p**3
        - 2 * p**2
    )
    l1_double_leaf = leaf.subs(
        {q: q_on_l1, a: l1_double_a, b: l1_double_b}
    )
    assert_identity(
        l1_double_leaf.det(),
        -3 * p * (p - 1) * f1 / (2 * p - 1) ** 4,
    )
    l1_double_7 = determinant(
        l1_double,
        AUXILIARY_ROWS + (32,),
        PIVOT_COLUMNS + (8,),
    )
    assert_identity(
        l1_double_7,
        -2916
        * p**5
        * (p - 1) ** 6
        * (p + 1)
        * pnorm**4
        * f1
        / (2 * p - 1) ** 11,
    )

    # The only L1 points at which e=T=0 are p=2,-1.  These witnesses do not
    # divide by the vanished old/alternate prefactor or by T.
    l1_exceptional = {}
    for p_value, q_value, rows, coefficient in (
        (
            2,
            0,
            (0, 1, 2, 17, 19, 32, 31),
            -27648,
        ),
        (
            -1,
            1,
            (0, 1, 17, 19, 28, 32, 31),
            6912,
        ),
    ):
        witness = determinant(
            syndrome.subs({p: p_value, q: q_value}),
            rows,
            PIVOT_COLUMNS + (8,),
        )
        expected = coefficient * (
            a - c - 1
        )
        assert_identity(witness, expected)
        l1_exceptional[str((p_value, q_value))] = str(witness)

    # L2=0 is calculated directly, with q as the free parameter.  No
    # carrier or color-permutation equivariance is assumed here.
    l2_branch = l2_data(p, q)
    p_on_l2 = l2_branch["p"]
    assert_identity(l2.subs(p, p_on_l2), 0)
    assert_identity(s.subs(p, p_on_l2), q)
    for name, polynomial in (
        ("p_minus_q", p - q),
        ("d0", d0),
        ("P", pnorm),
        ("L1", l1),
        ("e", e),
        ("T", t),
    ):
        assert_identity(polynomial.subs(p, p_on_l2), l2_branch[name])
    assert_identity(q6.subs(p, p_on_l2), l2_branch["Q6"])

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
    l2_syndrome = syndrome.subs(p, p_on_l2)
    l2_old = determinant(l2_syndrome, OLD_ROWS, PIVOT_COLUMNS)
    l2_old_7 = determinant(
        l2_syndrome, OLD_ROWS + (25,), PIVOT_COLUMNS + (5,)
    )
    l2_alt = determinant(l2_syndrome, ALTERNATE_ROWS, PIVOT_COLUMNS)
    l2_alt_7 = determinant(
        l2_syndrome, ALTERNATE_ROWS + (25,), PIVOT_COLUMNS + (5,)
    )
    l2_prefactor = q**4 * (q - 1) ** 5 * qnorm**3
    assert_identity(
        l2_old,
        -324 * l2_prefactor * (q + 1) * h20 / (2 * q - 1) ** 8,
    )
    assert_identity(
        l2_old_7,
        324
        * l2_prefactor
        * (q + 1)
        * (b - c)
        * h20
        / (2 * q - 1) ** 7,
    )
    l2_alt_prefactor = q**5 * (q - 1) ** 4 * qnorm**3
    assert_identity(
        l2_alt,
        -324 * l2_alt_prefactor * (q - 2) * h21 / (2 * q - 1) ** 8,
    )
    assert_identity(
        l2_alt_7,
        324
        * l2_alt_prefactor
        * (q - 2)
        * (b - c)
        * h21
        / (2 * q - 1) ** 7,
    )

    l2_double_a = -(q - 1) ** 2 / (2 * q - 1)
    l2_double_b = -q**2 * (q**2 + 2 * q - 2) / (2 * q - 1) ** 3
    l2_double = syndrome.subs(
        {p: p_on_l2, a: l2_double_a, b: l2_double_b}
    )
    f2 = (
        (8 * q**3 - 12 * q**2 + 6 * q - 1) * c
        + q**4
        + 2 * q**3
        - 2 * q**2
    )
    l2_double_leaf = leaf.subs(
        {p: p_on_l2, a: l2_double_a, b: l2_double_b}
    )
    assert_identity(
        l2_double_leaf.det(),
        3 * q * (q - 1) * f2 / (2 * q - 1) ** 4,
    )
    l2_double_7 = determinant(
        l2_double,
        AUXILIARY_ROWS + (32,),
        PIVOT_COLUMNS + (8,),
    )
    assert_identity(
        l2_double_7,
        2916
        * q**5
        * (q - 1) ** 6
        * (q + 1)
        * qnorm**4
        * f2
        / (2 * q - 1) ** 11,
    )

    l2_exceptional = {}
    for q_value, p_value, branch, witnesses in (
        (
            2,
            0,
            {a: -3 * b - 3},
            (
                (
                    (0, 1, 17, 19, 25, 31, 32),
                    (0, 1, 2, 3, 4, 5, 6),
                    -62208 * (b + 1) * (b - c) ** 2,
                ),
                (
                    (0, 1, 17, 19, 25, 31, 32),
                    (0, 1, 2, 3, 4, 5, 7),
                    -20736 * (3 * b + 1) * (b - c) ** 2,
                ),
            ),
        ),
        (
            -1,
            1,
            {a: 1 - 3 * b},
            (
                (
                    (0, 1, 17, 19, 25, 28, 32),
                    (0, 1, 2, 3, 4, 5, 6),
                    -1728 * (3 * b - 1) * (b - c) ** 2,
                ),
                (
                    (0, 1, 17, 19, 25, 31, 32),
                    (0, 1, 2, 3, 4, 5, 7),
                    -10368 * (3 * b + 7) * (b - c) ** 2,
                ),
            ),
        ),
    ):
        branch_records = []
        for rows, columns, expected in witnesses:
            witness = determinant(
                syndrome.subs({p: p_value, q: q_value}).subs(branch),
                rows,
                columns,
            )
            assert_identity(witness, expected)
            branch_records.append(str(witness))
        l2_exceptional[str((p_value, q_value))] = branch_records

    return {
        "status": "exact_scoped_H4_L1_L2_rank_seven_exclusion",
        "gld_identifier": "GLD93",
        "scope": "characteristic-zero H4 equal-leaf chart on D(Omega*(p-q)*d0*P)",
        "syndrome_shape": list(syndrome.shape),
        "pivot_columns": list(PIVOT_COLUMNS),
        "l1_old_and_alternate_six_and_seven_minor_identities": True,
        "l1_double_pivot_auxiliary_seven_minor": True,
        "l1_exceptional_witnesses": l1_exceptional,
        "l2_direct_old_and_alternate_six_and_seven_minor_identities": True,
        "l2_double_pivot_auxiliary_seven_minor": True,
        "l2_exceptional_witnesses": l2_exceptional,
        "naive_pq_symmetry_used": False,
        "upstream_dependencies": ["GLD86", "GLD87", "GLD89"],
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
    print("GLD93 H4 L1/L2 rank-seven verifier: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
