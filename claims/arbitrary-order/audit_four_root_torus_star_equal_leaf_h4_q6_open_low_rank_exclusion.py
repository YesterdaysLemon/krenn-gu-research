#!/usr/bin/env python3
"""Independent audit of the GLD90 H4 Q6-open low-rank exclusion."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "claims" / "arbitrary-order" / (
    "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
)
CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"


def parse_gaussian(raw: str) -> sp.Expr:
    value = sp.expand(
        sp.sympify(str(raw).replace("^", "**"), locals={"i": sp.I})
    )
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


def family_values(
    p: sp.Symbol, q: sp.Symbol, a: sp.Expr
) -> tuple[sp.Expr, ...]:
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
    denominator = (p - q) * d0**3
    u = sp.factor(
        (q**2 - q + 1) * (2 * p * q - p + q**2 - 2 * q)
        / denominator
    )
    v = sp.factor(
        -(p**2 - p + 1) * (p**2 + 2 * p * q - 2 * p - q)
        / denominator
    )
    return s, b, c, u, v


def residual_curve(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    return (
        2 * p**4 * q**2
        - 2 * p**4 * q
        - p**4
        + 2 * p**3 * q**3
        - 7 * p**3 * q**2
        + p**3 * q
        + 4 * p**3
        + 2 * p**2 * q**4
        - 7 * p**2 * q**3
        + 6 * p**2 * q**2
        + 5 * p**2 * q
        - 4 * p**2
        - 2 * p * q**4
        + p * q**3
        + 5 * p * q**2
        - 4 * p * q
        - q**4
        + 4 * q**3
        - 4 * q**2
    )


def assert_divisible(
    expression: sp.Expr, divisor: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> None:
    numerator = sp.cancel(expression).as_numer_denom()[0]
    _quotient, remainder = sp.div(
        sp.Poly(numerator, *variables, domain=sp.QQ),
        sp.Poly(divisor, *variables, domain=sp.QQ),
    )
    assert remainder.is_zero


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
    inhomogeneous = scale_fixed.subs(
        {value: 0 for value in center_shifts}
    )
    assert (
        scale_fixed - coefficient * center_shifts - inhomogeneous
    ).applyfunc(sp.expand) == sp.zeros(10, 1)

    p, q = sp.symbols("p q")
    d0 = p + q - 1
    t = 2 * p * q - p - q + 2
    double_a = sp.factor((q - 1) * (q + 1) * (p + q - 2) / t)
    double_b = sp.factor(p * (p - 2) * (p + q) / t)
    curve = residual_curve(p, q)
    s, family_b, family_c, kernel_u, kernel_v = family_values(
        p, q, double_a
    )
    assert_divisible(double_b - family_b, curve, (p, q))

    # Independently replay the T=0 two-pivot obstruction from the raw scalar
    # formulas, without importing the primary or the GLD71 matrix builder.
    alpha, beta = sp.symbols("alpha beta")
    pnorm = p**2 - p + 1
    q_on_t = (p - 2) / (2 * p - 1)
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
    assert sp.cancel(q6.subs(q, q_on_t) - 8 * pnorm**4 / (2 * p - 1) ** 4) == 0
    x0 = alpha * (p**2 - 1) - (beta + 1) * (q**2 - 1)
    x1 = alpha * p * (p - 2) - beta * q * (q - 2) - p * (p - 2)
    bracket_0 = (2 * p - 1) ** 2 * alpha + 3 * beta + 3
    bracket_1 = (2 * p - 1) ** 2 * (alpha - 1) + 3 * beta
    assert sp.cancel(
        x0.subs(q, q_on_t)
        - (p - 1) * (p + 1) * bracket_0 / (2 * p - 1) ** 2
    ) == 0
    assert sp.cancel(
        x1.subs(q, q_on_t)
        - p * (p - 2) * bracket_1 / (2 * p - 1) ** 2
    ) == 0
    assert sp.expand(bracket_0 - bracket_1) == 4 * pnorm

    b, c = sp.symbols("b c")
    leaf_substitution = {
        shifts[9]: p,
        shifts[10]: q,
        shifts[11]: s - 1 - sp.I,
        shifts[12]: double_a,
        shifts[13]: b,
        shifts[14]: c,
    }
    clearing_factor = d0**3 * t**3
    h4_coefficient = coefficient.subs(leaf_substitution).applyfunc(
        lambda value: sp.cancel(clearing_factor * value)
    )
    h4_inhomogeneous = inhomogeneous.subs(leaf_substitution).applyfunc(
        lambda value: sp.cancel(clearing_factor * value)
    )
    assert all(value.as_numer_denom()[1] == 1 for value in h4_coefficient)
    assert all(value.as_numer_denom()[1] == 1 for value in h4_inhomogeneous)

    family_coefficient = h4_coefficient.subs({b: family_b, c: family_c})
    family_inhomogeneous = h4_inhomogeneous.subs(
        {b: family_b, c: family_c}
    )
    base_center = sp.Matrix(
        [
            [-2 - 2 * sp.I, -1 + 2 * sp.I, 3],
            [0, -3 + 3 * sp.I, 0],
            [0, -1 + 2 * sp.I, 1],
        ]
    )
    kernel = sp.Matrix([[kernel_u, kernel_v, 1]])
    lambda0, lambda1 = sp.symbols("lambda0 lambda1")
    actual_center = sp.Matrix.vstack(lambda0 * kernel, lambda1 * kernel, kernel)
    assert sp.expand(actual_center.det()) == 0
    shift_vector = sp.Matrix(list(actual_center - base_center)[:8])
    residual = (
        family_coefficient * shift_vector + family_inhomogeneous
    ).applyfunc(sp.cancel)
    assert residual == sp.zeros(10, 1)
    assert shift_vector.jacobian((lambda0, lambda1)).rank() == 2

    algebraic_root = sp.sqrt(2) * sp.I
    sample = {p: 2, q: algebraic_root}
    assert sp.simplify(curve.subs(sample)) == 0
    assert sp.simplify(double_a.subs(sample)) == -1
    assert sp.simplify(double_b.subs(sample)) == 0
    assert sp.simplify(family_b.subs(sample)) == 0
    assert sp.simplify(family_c.subs(sample)) == 0
    numeric_coefficient = family_coefficient.subs(sample).applyfunc(sp.simplify)
    numeric_inhomogeneous = family_inhomogeneous.subs(sample).applyfunc(
        sp.simplify
    )
    assert numeric_coefficient.rank() == 6
    _rref, pivot_columns = numeric_coefficient.rref()
    selected_columns = tuple(pivot_columns[:6])
    _transpose_rref, pivot_rows = numeric_coefficient[:, selected_columns].T.rref()
    selected_rows = tuple(pivot_rows[:6])
    sample_pivot = sp.simplify(
        numeric_coefficient.extract(selected_rows, selected_columns).det()
    )
    assert sample_pivot != 0
    sample_shift = shift_vector.subs(
        sample | {lambda0: sp.Rational(2), lambda1: sp.Rational(3)}
    )
    assert (
        numeric_coefficient * sample_shift + numeric_inhomogeneous
    ).applyfunc(sp.simplify) == sp.zeros(10, 1)

    # A rational T=0 point on the old-pivot boundary independently checks the
    # complete scale-fixed center family in the immutable GLD75 carrier.
    t_sample = {
        p: sp.Integer(3),
        q: sp.Rational(1, 5),
        shifts[9]: sp.Integer(3),
        shifts[10]: sp.Rational(1, 5),
        shifts[11]: sp.Rational(2, 11) - sp.I,
        shifts[12]: sp.Rational(48, 1331),
        shifts[13]: sp.Rational(-1731, 1331),
        shifts[14]: sp.Rational(-3, 11),
    }
    t_coefficient = coefficient.subs(t_sample).applyfunc(sp.simplify)
    t_inhomogeneous = inhomogeneous.subs(t_sample).applyfunc(sp.simplify)
    assert t_coefficient.rank() == 6
    t_kernel = sp.Matrix(
        [[sp.Rational(-81, 1331), sp.Rational(-1250, 1331), 1]]
    )
    t_actual_center = sp.Matrix.vstack(
        lambda0 * t_kernel, lambda1 * t_kernel, t_kernel
    )
    t_shift = sp.Matrix(list(t_actual_center - base_center)[:8])
    assert (
        t_coefficient * t_shift + t_inhomogeneous
    ).applyfunc(sp.simplify) == sp.zeros(10, 1)
    assert t_shift.jacobian((lambda0, lambda1)).rank() == 2
    assert sp.expand(t_actual_center.det()) == 0

    # Independently replay the finite factor cover that leaves four corners.
    pnorm = p**2 - p + 1
    l1 = p**2 + 2 * p * q - 2 * p - q
    l2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    first_factors = (p - 1, p + 1, q - 1, q + 1, p + q - 2)
    second_factors = (p, q, p - 2, q - 2, p + q)
    open_without_q6 = (p - q) * d0 * pnorm * l1 * l2 * e * t
    corners = set()
    for first, second in itertools.product(first_factors, second_factors):
        for solution in sp.solve((first, second), (p, q), dict=True):
            if sp.simplify(open_without_q6.subs(solution)) != 0:
                corners.add((solution[p], solution[q]))
    assert corners == {(1, 2), (-1, 0), (2, 1), (0, -1)}

    return {
        "status": "independent_GLD75_carrier_GLD90_Q6_open_audit",
        "certificate_sha256": CERTIFICATE_SHA256,
        "imports_primary_or_GLD71_builder": False,
        "double_family_matches_GLD88_family_modulo_R": True,
        "sample_field": "Q(sqrt(-2))",
        "sample": {"p": "2", "q": "sqrt(2)*I", "a": "-1", "b": "0", "c": "0"},
        "sample_center_coefficient_rank": 6,
        "sample_pivot_rows": list(selected_rows),
        "sample_pivot_columns": list(selected_columns),
        "sample_pivot_determinant": str(sample_pivot),
        "complete_scale_fixed_solution_dimension": 2,
        "all_displayed_actual_centers_singular": True,
        "finite_corner_cover_replayed": True,
        "T_boundary_two_pivot_obstruction_replayed": True,
        "T_boundary_old_pivot_sample_rank": 6,
        "T_boundary_complete_scale_fixed_solution_dimension": 2,
        "primary_schur_resultants_independently_rederived": False,
        "primary_corner_seven_minors_independently_rederived": False,
        "remaining_boundaries": ["Q6=0", "L1=0", "L2=0", "e=0"],
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    result = check()
    print("independent GLD75-carrier GLD90 Q6-open audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
