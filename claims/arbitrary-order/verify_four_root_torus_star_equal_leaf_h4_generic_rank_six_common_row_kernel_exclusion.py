#!/usr/bin/env python3
"""Verify the scoped GLD88 H4 rank-six principal-open exclusion.

The calculation is exact over Q(i).  It constructs the fixed GLD71 syndrome
matrix on the fourth GLD86 divisor.  Two bordered linear Schur residuals force every
rank-at-most-six point on a named six-pivot open into an explicit rational
three-parameter family.  Three independent row-supported kernel vectors then
make the full kernel exactly the matrices with proportional rows, hence every
compatible center is singular.  Exceptional denominator and pivot loci are
retained.
"""

from __future__ import annotations

import hashlib
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
PIVOT_ROWS = (0, 1, 2, 17, 19, 32)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
SCHUR_TARGETS = ((25, 5), (31, 5))
PIVOT_NUMERATOR_SHA256 = "656128e97aa9b6e08ba57532aad1e8762eb201217cba15be58865e187214d5b5"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical_polynomial_digest(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> tuple[str, int]:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=sp.QQ)
    encoded = [
        [list(monomial), int(coefficient.p), int(coefficient.q)]
        for monomial, coefficient in polynomial.terms()
    ]
    payload = json.dumps(encoded, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), len(encoded)


def h4_family(p: sp.Symbol, q: sp.Symbol, a: sp.Symbol) -> dict[str, sp.Expr]:
    h4_denominator = p + q - 1
    rank_denominator = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    b_numerator = (
        -2 * a * p**2 * q**3
        + 3 * a * p**2 * q**2
        - 3 * a * p**2 * q
        + a * p**2
        + 2 * a * p * q**3
        + 2 * a * p
        + a * q**3
        - 3 * a * q**2
        + 3 * a * q
        - 2 * a
        + p**3 * q**2
        - p**3
        + p**2 * q**3
        - 3 * p**2 * q**2
        + p**2
        - 2 * p * q**3
        + 3 * p * q**2
        - 2 * p
        + q**2
        - 3 * q
        + 2
    )
    c_numerator = (
        2 * a * p * q**3
        - 3 * a * p * q**2
        + 3 * a * p * q
        - a * p
        - a * q**3
        + 3 * a * q**2
        - 3 * a * q
        + 2 * a
        + p**2 * q**2
        - 2 * p**2 * q
        - 3 * p * q**2
        + p * q
        + p
        - q**2
        + 3 * q
        - 2
    )
    kernel_denominator = (p - q) * h4_denominator**3
    kernel_u_numerator = (q**2 - q + 1) * (2 * p * q - p + q**2 - 2 * q)
    kernel_v_numerator = -(p**2 - p + 1) * (p**2 + 2 * p * q - 2 * p - q)
    return {
        "s": sp.factor((p + q - p * q) / h4_denominator),
        "b": sp.factor(-b_numerator / ((p**2 - p + 1) * rank_denominator)),
        "c": sp.factor(-c_numerator / (h4_denominator * rank_denominator)),
        "u": sp.factor(kernel_u_numerator / kernel_denominator),
        "v": sp.factor(kernel_v_numerator / kernel_denominator),
        "h4_denominator": h4_denominator,
        "rank_denominator": rank_denominator,
        "b_denominator_factor": p**2 - p + 1,
        "kernel_denominator": kernel_denominator,
    }


def check() -> dict[str, object]:
    gld71 = load_module(GLD71, "gld71_for_gld88")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    all_columns, annihilator_basis, _punctured_rows = gld71.check_punctured_code(
        parent, relations
    )
    assert len(relations) == 37
    assert len(all_columns) == 79
    assert len(annihilator_basis) == 44

    p, q, a = variables = sp.symbols("p q a")
    b, c = sp.symbols("b c")
    family = h4_family(p, q, a)
    s = family["s"]
    kernel = sp.Matrix([family["u"], family["v"], 1])
    h4_leaf = sp.Matrix([[1, 1, 1], [p, q, s], [a, 1 + b, 1 + c]])

    h4 = sp.cancel(p * q + p * s + q * s - p - q - s)
    assert h4 == 0
    h4_syndrome = gld71.coefficient_matrix(
        parent, relations, (h4_leaf, h4_leaf, h4_leaf)
    )
    assert h4_syndrome.shape == (37, 9)

    pivot = h4_syndrome.extract(PIVOT_ROWS, PIVOT_COLUMNS)
    pivot_determinant = sp.cancel(pivot.det(method="domain-ge"))
    schur_numerators = []
    for row, column in SCHUR_TARGETS:
        bordered = h4_syndrome.extract(
            (*PIVOT_ROWS, row), (*PIVOT_COLUMNS, column)
        )
        residual = sp.cancel(
            bordered.det(method="domain-ge") / pivot_determinant
        )
        numerator = residual.as_numer_denom()[0]
        schur_numerators.append(numerator)
    assert all(
        sp.Poly(value, b, c).total_degree() == 1 for value in schur_numerators
    )
    schur_equations = sp.Matrix(schur_numerators)
    schur_coefficient = schur_equations.jacobian((b, c))
    schur_constant = schur_equations.subs({b: 0, c: 0})
    schur_linear_determinant = sp.factor(schur_coefficient.det())
    expected_schur_linear_determinant = sp.factor(
        -6
        * (p - q)
        * (p + q - 1)
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * family["rank_denominator"]
    )
    assert schur_linear_determinant == expected_schur_linear_determinant
    schur_solution = -schur_coefficient.inv() * schur_constant
    assert sp.cancel(schur_solution[0] - family["b"]) == 0
    assert sp.cancel(schur_solution[1] - family["c"]) == 0

    family_substitution = {b: family["b"], c: family["c"]}
    leaf = h4_leaf.subs(family_substitution)
    syndrome = h4_syndrome.subs(family_substitution)
    assert syndrome.shape == (37, 9)

    block_kernel_checks = []
    for root in range(3):
        block = syndrome[:, 3 * root : 3 * root + 3]
        residual = tuple(sp.cancel(value) for value in block * kernel)
        assert all(value == 0 for value in residual)
        block_kernel_checks.append(True)

    family_pivot = syndrome.extract(PIVOT_ROWS, PIVOT_COLUMNS)
    family_pivot_determinant = sp.cancel(family_pivot.det(method="domain-ge"))
    pivot_numerator, pivot_denominator = family_pivot_determinant.as_numer_denom()
    assert pivot_numerator != 0 and pivot_denominator != 0
    pivot_digest, pivot_terms = canonical_polynomial_digest(
        pivot_numerator, variables
    )
    assert pivot_digest == PIVOT_NUMERATOR_SHA256
    assert pivot_terms == 176

    leaf_determinant = sp.factor(sp.cancel(leaf.det()))
    expected_leaf_determinant = sp.factor(
        -(
            (p - q)
            * (-3 * a + p + 1)
            * (p**2 + 2 * p * q - 2 * p - q)
            * (2 * p * q - p + q**2 - 2 * q)
        )
        /
        (
            (p + q - 1)
            * (p**2 - p + 1)
            * family["rank_denominator"]
        )
    )
    assert sp.cancel(leaf_determinant - expected_leaf_determinant) == 0
    assert leaf_determinant != 0

    sample_substitution = {p: 0, q: 3, a: 0}
    sample_leaf = leaf.subs(sample_substitution)
    sample_kernel = kernel.subs(sample_substitution)
    sample_syndrome = syndrome.subs(sample_substitution)
    sample_pivot = family_pivot_determinant.subs(sample_substitution)
    sample_schur_linear_determinant = schur_linear_determinant.subs(
        sample_substitution
    )
    assert sample_leaf == sp.Matrix(
        [[1, 1, 1], [0, 3, sp.Rational(3, 2)], [0, sp.Rational(15, 13), sp.Rational(12, 13)]]
    )
    assert sample_kernel == sp.Matrix(
        [sp.Rational(-7, 8), sp.Rational(-1, 8), 1]
    )
    assert sample_leaf.det() == sp.Rational(27, 26)
    assert sample_pivot != 0
    assert sample_schur_linear_determinant != 0
    assert sample_syndrome.rank() == 6
    assert all(
        sample_syndrome[:, 3 * root : 3 * root + 3].rank() == 2
        for root in range(3)
    )

    lambdas = sp.symbols("lambda0:3")
    general_center = sp.Matrix(
        3,
        3,
        [lambdas[row] * kernel[column] for row in range(3) for column in range(3)],
    )
    assert sp.expand(general_center.det()) == 0
    row_kernel_vectors = []
    for root in range(3):
        vector = sp.zeros(9, 1)
        vector[3 * root : 3 * root + 3, 0] = kernel
        assert all(sp.cancel(value) == 0 for value in syndrome * vector)
        row_kernel_vectors.append(vector)
    assert sp.Matrix.hstack(*row_kernel_vectors).rank() == 3

    return {
        "status": "exact_GLD88_H4_rank_six_principal_open_common_row_kernel_exclusion",
        "global_conjecture": "UNRESOLVED",
        "field": "Q_characteristic_zero_then_C",
        "family_parameters": [str(value) for value in variables],
        "h4_identity": "p*q+p*s+q*s-p-q-s=0",
        "syndrome_shape": list(syndrome.shape),
        "pivot_rows": list(PIVOT_ROWS),
        "pivot_columns": list(PIVOT_COLUMNS),
        "schur_targets": [list(value) for value in SCHUR_TARGETS],
        "schur_residuals_linear_in": ["b", "c"],
        "schur_linear_coefficient_determinant": str(
            schur_linear_determinant
        ),
        "rank_at_most_six_on_named_pivot_forced_to_family": True,
        "pivot_numerator_sha256": pivot_digest,
        "pivot_numerator_terms": pivot_terms,
        "block_kernel_identity_count": 3 * syndrome.rows,
        "generic_syndrome_rank_on_pivot_open": 6,
        "generic_kernel_dimension": 3,
        "generic_center_rank_upper_bound": 1,
        "sample": {
            "p_q_a": [0, 3, 0],
            "s_b_c": [
                str(s.subs(sample_substitution)),
                str(family["b"].subs(sample_substitution)),
                str(family["c"].subs(sample_substitution)),
            ],
            "kernel": [str(value) for value in sample_kernel],
            "leaf_determinant": str(sample_leaf.det()),
            "pivot_determinant": str(sample_pivot),
            "schur_linear_determinant": str(
                sample_schur_linear_determinant
            ),
            "syndrome_rank": sample_syndrome.rank(),
        },
        "exceptional_denominator_or_pivot_loci_retained": True,
        "all_H4_rank_at_most_six_points_excluded": False,
        "omega_saturated_H4_named_principal_open_excluded": True,
        "gld83_fitting_pullback_computed": False,
        "global_conjecture_resolved": False,
    }


def main() -> None:
    print("four-root equal-leaf generic H4 rank-six common-row-kernel exclusion: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
