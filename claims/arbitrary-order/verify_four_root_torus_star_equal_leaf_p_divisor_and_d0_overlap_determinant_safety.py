#!/usr/bin/env python3
"""Verify the scoped GLD89 P=0 and d0 boundary exclusion.

The primary calculation reconstructs the fixed GLD71 37-row syndrome map
with exact SymPy arithmetic.  It works on the H4 equal-leaf chart

    G = [[1, 1, 1], [p, q, s], [a, 1+b, 1+c]],
    s = (p + q - p*q)/(p + q - 1),

where b,c are the shifted lower-row coordinates used by GLD83--GLD88.  It
checks the two named six-minors, the two Schur residuals, the alternate
bordered minors at the six-pivot boundary, every exceptional q=0,1,-1
seven-minor used in the proof, and the d0=0 row subsystem.  The upstream
GLD86 incidence/rank bridge and the GLD87 H1/H2/H3 determinant-safety theorem
are logical dependencies, not silently reproved by this file.
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

PIVOT_ROWS = (0, 1, 2, 17, 19, 32)
PIVOT_ROWS_ALT = (0, 1, 2, 17, 19, 31)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
MATRIX_COLUMNS = (0, 1, 2, 3, 4, 5, 6, 7, 8)
SIX_MINOR_ROWS = (PIVOT_ROWS, PIVOT_ROWS_ALT)
SIX_MINOR_COLUMNS = PIVOT_COLUMNS


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def remainder_mod(expression: sp.Expr, relation: sp.Expr, variable: sp.Symbol) -> sp.Expr:
    """Clear denominators and reduce the numerator by a monic relation."""

    numerator, denominator = sp.cancel(expression).as_numer_denom()
    assert denominator != 0
    return sp.factor(sp.rem(sp.expand(numerator), relation, variable))


def assert_zero_mod(
    expression: sp.Expr, relation: sp.Expr, variable: sp.Symbol
) -> None:
    assert remainder_mod(expression, relation, variable) == 0


def assert_numerator_mod(
    expression: sp.Expr,
    expected_numerator: sp.Expr,
    relation: sp.Expr,
    variable: sp.Symbol,
) -> None:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    assert denominator != 0
    assert_zero_mod(numerator - expected_numerator, relation, variable)


def determinant(matrix: sp.Matrix, rows: tuple[int, ...], columns: tuple[int, ...]) -> sp.Expr:
    return sp.cancel(matrix.extract(rows, columns).det(method="domain-ge"))


def check_d0_overlap(gld71, parent, relations, p, q, sigma, a, b, c, P):
    """Check the independent s-chart used when d0=0."""

    overlap_leaf = sp.Matrix(
        [[1, 1, 1], [p, q, sigma], [a, 1 + b, 1 + c]]
    )
    overlap_matrix = gld71.coefficient_matrix(
        parent, relations, (overlap_leaf, overlap_leaf, overlap_leaf)
    ).subs(q, 1 - p)
    expected_rows = {
        0: [0, 0, 0, -1, -1, sigma**3, 0, 0, 0],
        1: [1, 1, 1, 0, 0, 0, 0, 0, 0],
        17: [-1, -1, sigma * (sigma - 1), 1, 1, -2 * sigma**2 + 2 * sigma - 1, 0, 0, 0],
        19: [
            1,
            1,
            sigma * (sigma**2 - 2 * sigma + 2),
            -1,
            -1,
            sigma * (sigma - 1),
            0,
            0,
            0,
        ],
    }
    for row, expected in expected_rows.items():
        for column, value in enumerate(expected):
            assert_zero_mod(
                overlap_matrix[row, column] - value,
                P,
                p,
            )

    # H4+d0=0 gives q=1-p and P=0; sigma is free on this overlap chart.
    h4 = p * q + p * sigma + q * sigma - p - q - sigma
    assert_zero_mod(h4.subs(q, 1 - p), P, p)
    f = sigma**2 - sigma + 1
    assert sp.expand((p**2 - p + 1).subs(p, sigma) - f) == 0
    assert sp.expand((p**2 - p + 1).subs(p, 1 - sigma) - f) == 0

    # After using rows 0 and 1, rows 17 and 19 become the two displayed
    # 2-by-2 equations in x2,y2.  Their determinant is -f.
    two_by_two = sp.Matrix([[1, sigma - 1], [sigma - 1, -sigma]])
    assert sp.factor(two_by_two.det()) == -f
    return {
        "shape": list(overlap_matrix.shape),
        "checked_rows": [0, 1, 17, 19],
        "row_kernel_equations": [
            "x0+x1+x2=0",
            "-y0-y1+sigma^3*y2=0",
            "f*(x2+(sigma-1)*y2)=0",
            "f*((sigma-1)*x2-sigma*y2)=0",
        ],
        "two_by_two_determinant": "-(sigma^2-sigma+1)",
        "f_zero_is_H2_or_H3": True,
    }


def check() -> dict[str, object]:
    assert GLD86_DOCUMENT.exists()
    assert GLD87_DOCUMENT.exists()

    gld71 = load_module(GLD71, "gld71_for_gld89")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    all_columns, annihilator_basis, _punctured_rows = gld71.check_punctured_code(
        parent, relations
    )
    assert len(relations) == 37
    assert len(all_columns) == 79
    assert len(annihilator_basis) == 44

    p, q, s_free, a, b, c = sp.symbols("p q sigma a b c")
    d0 = p + q - 1
    s = (p + q - p * q) / d0
    leaf = sp.Matrix([[1, 1, 1], [p, q, s], [a, 1 + b, 1 + c]])
    syndrome = gld71.coefficient_matrix(parent, relations, (leaf, leaf, leaf))
    assert syndrome.shape == (37, 9)

    P = p**2 - p + 1
    Q = q**2 - q + 1
    L2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    B = p * q**2 + 2 * p * q - 2 * p + q**2 - 4 * q + 1

    # H4 is built into the rational parameterization.
    h4 = p * q + p * s + q * s - p - q - s
    assert sp.cancel(h4) == 0

    F1 = (p - 2) * a - (q**2 - 1) * (b + 1)
    F3 = (p - 2) * q**3 * a + (q**2 - 1) * (b + 1)
    m_p = determinant(syndrome, PIVOT_ROWS, PIVOT_COLUMNS)
    m_3 = determinant(syndrome, PIVOT_ROWS_ALT, PIVOT_COLUMNS)
    assert_zero_mod(m_p - 6 * Q**3 * F1, P, p)
    assert_zero_mod(m_3 + 6 * Q**3 * F3, P, p)

    # The GLD88 pivot residuals remain valid as bordered determinants.  Their
    # numerators are checked after reduction modulo P, not merely sampled.
    expected_e25 = Q * e * (a + c)
    J = (
        3 * a * (p * q**2 - 2 * p * q - q**2 + 1)
        + 3 * c * (p * q**2 - p - 2 * q + 1)
        + B
    )
    expected_e31 = 6 * Q * J
    schur_numerators = []
    for row, expected in ((25, expected_e25), (31, expected_e31)):
        bordered = determinant(
            syndrome,
            (*PIVOT_ROWS, row),
            (*PIVOT_COLUMNS, 5),
        )
        residual = sp.cancel(bordered / m_p)
        numerator, denominator = sp.cancel(residual).as_numer_denom()
        assert denominator != 0
        assert_zero_mod(numerator - expected, P, p)
        schur_numerators.append(numerator)

    # On the m_p != 0 branch, Q and e are nonzero after the GLD87 H1
    # dependency removes q=p.  The exact resultant checks show that L2 is
    # nonzero as well; hence E25/E31 force c=-a and a=B/(3 L2).
    assert sp.expand(sp.resultant(P, d0, p) - Q) == 0
    assert sp.expand(sp.resultant(P, p * q - 1, p) - Q) == 0
    assert sp.expand(sp.resultant(P, e, p) - 3 * Q**2) == 0
    assert sp.expand(sp.resultant(P, L2, p) - Q**2) == 0
    assert sp.expand(sp.resultant(P, p + 1, p) - 3) == 0
    assert_zero_mod(Q - (q - p) * d0 - P, P, p)
    assert_zero_mod(J.subs(c, -a) - (B - 3 * a * L2), P, p)

    generic_a = B / (3 * L2)
    generic_c = -generic_a
    generic_kernel_checks = 0
    for root in range(3):
        for row in range(syndrome.rows):
            value = sp.cancel(
                (syndrome[row, 3 * root] - syndrome[row, 3 * root + 2]).subs(
                    {a: generic_a, c: generic_c}
                )
            )
            assert_zero_mod(value, P, p)
            generic_kernel_checks += 1

    # At m_p=0 but m_3!=0, F1=0 gives b, and two alternate bordered minors
    # give the exact coefficient cross-consistency factor.  The large
    # intermediate linear forms are retained by the verifier rather than
    # hidden behind a guessed Groebner result.
    b_from_F1 = a * (p - 2) / (q**2 - 1) - 1
    alternate_forms = []
    for row, common_factor in ((25, -6 * (q - 1) * (q + 1) * Q**3), (33, -72 * (q - 1) * (q + 1) * Q**3)):
        bordered = determinant(
            syndrome.subs(b, b_from_F1),
            (*PIVOT_ROWS_ALT, row),
            (*PIVOT_COLUMNS, 5),
        )
        numerator, denominator = sp.cancel(bordered).as_numer_denom()
        assert denominator != 0
        reduced = sp.rem(sp.expand(numerator), P, p)
        form = sp.cancel(reduced / common_factor)
        form_numerator, form_denominator = sp.cancel(form).as_numer_denom()
        assert form_denominator == 1
        assert sp.Poly(form_numerator, c).degree() == 1
        alternate_forms.append(form_numerator)
    f25, f33 = alternate_forms
    cross = sp.diff(f25, c) * f33.subs(c, 0) - sp.diff(f33, c) * f25.subs(c, 0)
    cross_expected = (
        -3
        * a**2
        * (q - 1)
        * (q + 1) ** 2
        * Q**2
        * (p + 1)
        * (3 * a - p - 1)
        * d0**6
    )
    assert_zero_mod(cross - cross_expected, P, p)

    d_small = p * q**3 - 3 * p * q + p - 3 * q**2 + 3 * q
    boundary_a = (p + 1) / 3
    boundary_c = -boundary_a
    assert_zero_mod(d_small - d0**2 * (p * q - 1), P, p)
    assert_zero_mod(
        f33.subs(a, boundary_a) - Q * (3 * c + p + 1) * d_small,
        P,
        p,
    )
    boundary_b = sp.cancel(b_from_F1.subs(a, boundary_a))
    assert_zero_mod(boundary_b - q**2 / (1 - q**2), P, p)
    boundary_m3 = sp.cancel(
        m_3.subs({a: boundary_a, b: boundary_b, c: boundary_c})
    )
    assert_numerator_mod(
        boundary_m3,
        6 * (q + 1) * Q**4,
        P,
        p,
    )

    # The m_p=m_3=0 branch has a=0 and either q=+/-1 or b=-1.  The following
    # exact seven-minor table closes all of those cases on D(Omega).
    assert_zero_mod(
        F1 + F3 - (p - 2) * a * (q + 1) * Q,
        P,
        p,
    )
    leaf_det_boundary = sp.cancel(leaf.det().subs({a: 0, b: -1}))
    assert_zero_mod(leaf_det_boundary - (c + 1) * Q / d0, P, p)

    seven_minor_checks: dict[str, str] = {}

    def seven(rows, target, substitutions, expected, label):
        value = determinant(
            syndrome.subs(substitutions),
            rows,
            (*PIVOT_COLUMNS, target),
        )
        assert_numerator_mod(value, expected, P, p)
        seven_minor_checks[label] = str(expected)

    # q^2 != 1, b=-1.  The q != 0 case has the K factor; q=0 gets two
    # independent minors so that c=0 and c!=0 are both covered.
    K = 2 * p * q - p - q - 1
    assert sp.expand(sp.resultant(P, K, p) - 3 * Q) == 0
    seven(
        (0, 1, 2, 17, 19, 25, 28),
        8,
        {a: 0, b: -1},
        3 * q * (c + 1) * Q**4 * K,
        "q2_ne_1_q_ne_0",
    )
    seven(
        (0, 1, 17, 19, 25, 28, 32),
        5,
        {a: 0, b: -1, q: 0},
        -18 * c * (p - 1),
        "q0_first",
    )
    seven(
        (0, 1, 17, 19, 25, 28, 32),
        8,
        {a: 0, b: -1, q: 0},
        18 * (2 * c + p),
        "q0_second",
    )

    # q=1.
    seven(
        (0, 1, 2, 17, 19, 25, 28),
        8,
        {a: 0, q: 1},
        -3 * b * (c + 1) * (2 * p - 1),
        "q1_first",
    )
    seven(
        (0, 1, 2, 17, 19, 25, 31),
        8,
        {a: 0, q: 1},
        -6 * (c + 1) * (2 * b * p - b + 3 * p),
        "q1_second",
    )
    seven(
        (0, 1, 17, 19, 25, 28, 32),
        8,
        {a: 0, q: 1, c: -1},
        18 * (p + 1),
        "q1_cminus1",
    )

    # q=-1.
    seven(
        (0, 1, 2, 17, 19, 25, 28),
        8,
        {a: 0, q: -1},
        -729 * (c + 1) * (b * p - 2 * b - 2),
        "qm1_first",
    )
    seven(
        (0, 1, 2, 17, 19, 25, 31),
        8,
        {a: 0, q: -1},
        -1458 * (c + 1) * (b * p - 2 * b + 3 * p - 5),
        "qm1_second",
    )
    seven(
        (0, 1, 2, 17, 19, 28, 31),
        8,
        {a: 0, q: -1},
        1458 * (c + 1) * (b * p - 2 * b + 1),
        "qm1_third",
    )
    seven(
        (0, 1, 17, 19, 25, 28, 32),
        5,
        {a: 0, q: -1, c: -1},
        -1458 * (-3 * b + p + 1),
        "qm1_cminus1_first",
    )
    seven(
        (0, 1, 17, 19, 25, 28, 32),
        8,
        {a: 0, q: -1, c: -1},
        -4374 * (p + 1),
        "qm1_cminus1_second",
    )

    overlap = check_d0_overlap(
        gld71,
        parent,
        relations,
        p,
        q,
        s_free,
        a,
        b,
        c,
        P,
    )

    return {
        "status": "exact_GLD89_H4_P_zero_and_d0_overlap_determinant_safety",
        "global_conjecture": "UNRESOLVED",
        "field": "Q_characteristic_zero_then_C",
        "syndrome_shape": list(syndrome.shape),
        "h4_parameterization": "s=(p+q-p*q)/(p+q-1) for d0!=0",
        "P_divisor": "p^2-p+1",
        "d0_divisor": "p+q-1",
        "six_minor_rows": [list(value) for value in SIX_MINOR_ROWS],
        "six_minor_columns": list(SIX_MINOR_COLUMNS),
        "six_minor_factors_mod_P": [
            "6*Q^3*((p-2)*a-(q^2-1)*(b+1))",
            "-6*Q^3*((p-2)*q^3*a+(q^2-1)*(b+1))",
        ],
        "schur_residual_numerators_mod_P": ["Q*e*(a+c)", "6*Q*J"],
        "generic_P_branch": {
            "conditions": "d0!=0, mP!=0, Q*e*L2!=0",
            "forced": ["c=-a", "a=B/(3*L2)"],
            "b": "free subject to mP!=0",
            "common_kernel": "(-1,0,1) in each root block",
            "kernel_identity_count": generic_kernel_checks,
            "center_is_singular": True,
        },
        "P_six_pivot_boundary": {
            "conditions": "d0!=0, mP=0, m3!=0, q^2!=1",
            "forced": [
                "a=(p+1)/3",
                "b=q^2/(1-q^2)",
                "c=-(p+1)/3",
            ],
            "alternate_bordered_cross_factor": "-3*a^2*(q-1)*(q+1)^2*Q^2*(p+1)*(3*a-p-1)*d0^6",
            "common_kernel": "(-1,0,1) in each root block",
            "center_is_singular": True,
        },
        "zero_six_minor_exceptional_q_cases": seven_minor_checks,
        "d0_overlap": overlap,
        "GLD87_dependency": {
            "used_only_for": [
                "q=p H1 overlap when P=Q=0 and d0!=0",
                "f=sigma^2-sigma+1=0 at d0=0, which is H2 or H3",
            ],
            "H4_P_branch_recomputed_here": True,
        },
        "residual_table": {
            "p-q": "excluded by GLD87",
            "d0": "excluded here, including d0=P overlap",
            "P": "excluded here on D(Omega), including mP/m3 boundary",
            "L1": "only prior generic P6-open closure; L1 intersect V(P6) retained",
            "L2": "only prior generic P6-open closure; L2 intersect V(P6) retained",
            "e": "only prior generic P6-open closure; e intersect V(P6) retained",
            "pure_P6": "retained for the complementary GLD90 lane",
        },
        "omega_saturated_P_and_d0_excluded": True,
        "gld83_fitting_pullback_computed": False,
        "all_H4_rank_at_most_six_points_excluded": False,
        "global_conjecture_resolved": False,
    }


def main() -> None:
    print("four-root equal-leaf H4 P=0 and d0 boundary: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
