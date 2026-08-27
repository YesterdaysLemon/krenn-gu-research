#!/usr/bin/env python3
"""Independent GLD75-basis audit of the GLD88 forced H4 family.

This audit does not import the GLD88 verifier, the GLD71 syndrome builder, or
any repository Python module.  It parses the immutable sparse GLD75 basis
carrier directly, reconstructs the ten scale-fixed center-linear equations,
and checks that the family forced by the primary Schur classifier has the
displayed proportional-row center family as its complete affine solution on
an independently selected rank-six principal open.  It does not claim a
second derivation of the primary four-residual Groebner classification.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
)
CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"
PIVOT_ROWS = (0, 1, 2, 3, 4, 6)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)


def parse_gaussian(raw: str) -> sp.Expr:
    value = sp.expand(sp.sympify(str(raw).replace("^", "**"), locals={"i": sp.I}))
    real, imaginary = value.as_real_imag()
    assert real.is_Rational and imaginary.is_Rational
    return value


def sparse_polynomial(encoded, symbols: tuple[sp.Symbol, ...]) -> sp.Poly:
    terms = {}
    for raw_coefficient, raw_sparse_exponent in encoded:
        exponent = [0] * len(symbols)
        for raw_index, raw_power in raw_sparse_exponent:
            exponent[int(raw_index)] = int(raw_power)
        key = tuple(exponent)
        assert key not in terms
        terms[key] = parse_gaussian(raw_coefficient)
    return sp.Poly.from_dict(terms, *symbols, domain=sp.QQ_I)


def family_values(p: sp.Symbol, q: sp.Symbol, a: sp.Symbol) -> tuple[sp.Expr, ...]:
    d0 = p + q - 1
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    nb = (
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
    nc = (
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
    s = sp.factor((p + q - p * q) / d0)
    b = sp.factor(-nb / ((p**2 - p + 1) * e))
    c = sp.factor(-nc / (d0 * e))
    dk = (p - q) * d0**3
    u = sp.factor((q**2 - q + 1) * (2 * p * q - p + q**2 - 2 * q) / dk)
    v = sp.factor(
        -(p**2 - p + 1) * (p**2 + 2 * p * q - 2 * p - q) / dk
    )
    return s, b, c, u, v


def check() -> dict[str, object]:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw)
    assert payload["format"] == "sparse-bidirectional-ideal-Qi-v1"
    assert payload["variable_order"] == [f"x{index}" for index in range(15)]
    assert payload["basis_generator_count"] == 10

    shifts = tuple(sp.symbols("x0:15"))
    generators = tuple(
        sp.expand(sparse_polynomial(encoded, shifts).as_expr())
        for encoded in payload["basis"]
    )
    scale_fixed = sp.Matrix([value.subs(shifts[8], 0) for value in generators])
    center_shifts = sp.Matrix(shifts[:8])
    coefficient = scale_fixed.jacobian(center_shifts)
    inhomogeneous = scale_fixed.subs({value: 0 for value in center_shifts})
    assert (
        scale_fixed - coefficient * center_shifts - inhomogeneous
    ).applyfunc(sp.expand) == sp.zeros(10, 1)

    p, q, a = sp.symbols("p q a")
    b, c = sp.symbols("b c")
    s, family_b, family_c, u, v = family_values(p, q, a)
    h4_leaf_substitution = {
        shifts[9]: p,
        shifts[10]: q,
        shifts[11]: s - 1 - sp.I,
        shifts[12]: a,
        shifts[13]: b,
        shifts[14]: c,
    }
    h4_denominator = p + q - 1
    h4_coefficient = coefficient.subs(h4_leaf_substitution).applyfunc(
        lambda value: sp.cancel(h4_denominator**3 * value)
    )
    h4_inhomogeneous = inhomogeneous.subs(h4_leaf_substitution).applyfunc(
        lambda value: sp.cancel(h4_denominator**3 * value)
    )
    assert all(value.as_numer_denom()[1] == 1 for value in h4_coefficient)
    assert all(value.as_numer_denom()[1] == 1 for value in h4_inhomogeneous)

    family_substitution = {b: family_b, c: family_c}
    family_coefficient = h4_coefficient.subs(family_substitution)
    family_inhomogeneous = h4_inhomogeneous.subs(family_substitution)
    family_sample = {p: 0, q: 3, a: 0}
    numeric_coefficient = family_coefficient.subs(family_sample).applyfunc(sp.cancel)
    assert numeric_coefficient.rank() == 6
    pivot_rows = PIVOT_ROWS
    pivot_columns = PIVOT_COLUMNS
    sample_pivot_determinant = numeric_coefficient.extract(
        pivot_rows, pivot_columns
    ).det()
    assert sample_pivot_determinant != 0
    print("selected pivot", pivot_rows, pivot_columns, flush=True)

    base_center = sp.Matrix(
        [[-2 - 2 * sp.I, -1 + 2 * sp.I, 3], [0, -3 + 3 * sp.I, 0], [0, -1 + 2 * sp.I, 1]]
    )
    kernel = sp.Matrix([[u, v, 1]])
    lambda0, lambda1 = sp.symbols("lambda0 lambda1")
    actual_center = sp.Matrix.vstack(lambda0 * kernel, lambda1 * kernel, kernel)
    assert sp.expand(actual_center.det()) == 0
    shift_vector = sp.Matrix(list(actual_center - base_center)[:8])
    residual = (
        family_coefficient * shift_vector + family_inhomogeneous
    ).applyfunc(sp.cancel)
    assert residual == sp.zeros(10, 1)
    direction_matrix = shift_vector.jacobian((lambda0, lambda1))
    assert direction_matrix.rank() == 2

    sample_actual = actual_center.subs(
        family_sample | {lambda0: 2, lambda1: 3}
    )
    assert sample_actual.det() == 0
    assert (
        numeric_coefficient
        * shift_vector.subs(family_sample | {lambda0: 2, lambda1: 3})
        + family_inhomogeneous.subs(family_sample)
    ).applyfunc(sp.cancel) == sp.zeros(10, 1)

    return {
        "status": "independent_GLD75_basis_GLD88_audit",
        "certificate_sha256": CERTIFICATE_SHA256,
        "center_coefficient_shape": list(family_coefficient.shape),
        "pivot_rows": list(pivot_rows),
        "pivot_columns": list(pivot_columns),
        "sample_pivot_determinant": str(sample_pivot_determinant),
        "primary_h4_schur_classification_independently_replayed": False,
        "forced_family_reconstructed_from_gld75_carrier": True,
        "generic_center_shift_rank_on_pivot_open": 6,
        "complete_affine_solution_dimension": 2,
        "all_compatible_actual_centers_singular": True,
        "exceptional_denominator_or_pivot_loci_retained": True,
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    result = check()
    print("independent GLD75-basis GLD88 audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
