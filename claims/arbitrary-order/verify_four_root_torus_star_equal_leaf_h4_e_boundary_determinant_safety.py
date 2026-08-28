#!/usr/bin/env python3
"""Verify the exact GLD94 determinant-safe exclusion on the H4 e-boundary.

The calculation is over ``QQ`` and therefore extends to characteristic zero.
It starts from the fixed GLD71 37-row syndrome map and the GLD86 base/Fitting
bridge.  On

    e = 2*p*q**2 - 2*p*q - p - q**2 - 2*q + 2 = 0

the complete normalized H4 chart is parameterised by ``q=t`` and
``p=(t**2+2*t-2)/(2*t**2-2*t-1)``.  Away from the collision/denominator
values, the two old six-pivots either give an explicit forced family or both
vanish.  In the latter case two auxiliary six-pivots and exact resultants give
an impossible residual equation.  In the former case the entire 37-by-9
syndrome matrix has three block-supported kernel vectors, forcing every
compatible centre to be singular.  The unsaturated leaf family is retained;
only its centre-frame intersection is excluded.

This is a scoped low-rank/determinant result.  It does not compute the full
GLD83 intrinsic Fitting pullback, close the other H4 boundaries/charts/ranks,
or resolve the global conjecture.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)

PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
OLD_ROWS = (0, 1, 2, 17, 19, 32)
ALTERNATE_ROWS = (0, 1, 17, 19, 28, 32)
CHART_A_ROWS = (0, 1, 2, 17, 19, 25)
CHART_B_ROWS = (0, 1, 17, 19, 25, 28)
GENERIC_FACTORS = (
    "t",
    "t-1",
    "t-2",
    "t+1",
    "2*t-1",
    "t**2-t+1",
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def bordered_numerator(
    matrix: sp.Matrix,
    pivot_rows: tuple[int, ...],
    target: tuple[int, int],
) -> sp.Expr:
    """Return the numerator of the exact Schur residual at ``target``."""

    pivot = matrix.extract(pivot_rows, PIVOT_COLUMNS)
    pivot_determinant = sp.cancel(pivot.det(method="domain-ge"))
    row, column = target
    bordered = matrix.extract(
        (*pivot_rows, row), (*PIVOT_COLUMNS, column)
    )
    residual = sp.cancel(
        bordered.det(method="domain-ge") / pivot_determinant
    )
    return sp.factor(residual.as_numer_denom()[0])


def q6_polynomial(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
    return (
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


def assert_zero(value: sp.Expr) -> None:
    assert sp.cancel(value) == 0


def normalized_residual(
    matrix: sp.Matrix,
    rows: tuple[int, ...],
    target: tuple[int, int],
    p: sp.Symbol,
    q: sp.Symbol,
    t: sp.Symbol,
    p_on_e: sp.Expr,
) -> sp.Expr:
    """Specialize the exact bordered quotient, retaining its rational value."""

    pivot = matrix.extract(rows, PIVOT_COLUMNS)
    determinant = sp.cancel(pivot.det(method="domain-ge"))
    row, column = target
    bordered = matrix.extract(
        (*rows, row), (*PIVOT_COLUMNS, column)
    )
    quotient = sp.cancel(
        bordered.det(method="domain-ge") / determinant
    )
    return sp.factor(sp.cancel(quotient.subs({p: p_on_e, q: t})))


def check() -> dict[str, object]:
    gld71 = load_module(GLD71, "gld71_for_gld94")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    assert len(relations) == 37

    p, q, a, b, c = sp.symbols("p q a b c")
    t = sp.symbols("t")
    d0 = p + q - 1
    pnorm = p**2 - p + 1
    l1 = p**2 + 2 * p * q - 2 * p - q
    l2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    total_pivot_factor = 2 * p * q - p - q + 2
    q6 = q6_polynomial(p, q)
    curve = residual_curve(p, q)
    s = (p + q - p * q) / d0
    leaf = sp.Matrix([[1, 1, 1], [p, q, s], [a, 1 + b, 1 + c]])
    syndrome = gld71.coefficient_matrix(
        parent, relations, (leaf, leaf, leaf)
    )
    assert syndrome.shape == (37, 9)

    # Exact e=0 parameterisation and all frame factors used below.
    denominator = 2 * t**2 - 2 * t - 1
    numerator = t**2 + 2 * t - 2
    p_on_e = numerator / denominator
    assert_zero(e.subs({p: p_on_e, q: t}))
    assert sp.gcd(
        sp.Poly(denominator, t, domain=sp.QQ),
        sp.Poly(numerator, t, domain=sp.QQ),
    ).degree() == 0
    e_factors = {
        "d0": (2 * t - 1) * (t**2 - t + 1) / denominator,
        "p_minus_q": -(t - 2) * (t + 1) * (2 * t - 1) / denominator,
        "p_minus_s": 9 * t * (t - 1) / ((2 * t - 1) * denominator),
        "q_minus_s": 2 * (t**2 - t + 1) / (2 * t - 1),
        "P": 3 * (t**2 - t + 1) ** 2 / denominator**2,
        "L1": 9 * t * (t - 1) * (t**2 - t + 1) / denominator**2,
        "L2": 2 * (t**2 - t + 1) ** 2 / denominator,
        "Q6": 8 * (t**2 - t + 1) ** 6 / denominator**4,
        "T": 9 * t * (t - 1) / denominator,
    }
    factor_sources = {
        "d0": d0,
        "p_minus_q": p - q,
        "p_minus_s": p - s,
        "q_minus_s": q - s,
        "P": pnorm,
        "L1": l1,
        "L2": l2,
        "Q6": q6,
        "T": total_pivot_factor,
    }
    for name, expected in e_factors.items():
        assert_zero(factor_sources[name].subs({p: p_on_e, q: t}) - expected)
    curve_on_e = sp.factor(sp.cancel(curve.subs({p: p_on_e, q: t})))
    assert curve_on_e == (
        -6
        * t
        * (t - 2)
        * (t - 1)
        * (t + 1)
        * (t**2 - t + 1) ** 2
        / denominator**2
    )

    # The raw six-pivots are the two GLD90 pivots, reconstructed here.
    x0 = a * (p**2 - 1) - (b + 1) * (q**2 - 1)
    x1 = a * p * (p - 2) - b * q * (q - 2) - p * (p - 2)
    old_pivot = sp.factor(
        sp.cancel(
            syndrome.extract(OLD_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            )
        )
    )
    alternate_pivot = sp.factor(
        sp.cancel(
            syndrome.extract(ALTERNATE_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            )
        )
    )
    assert_zero(old_pivot + 6 * (p - q) ** 2 * x0 * q6)
    assert_zero(alternate_pivot + 6 * (p - q) ** 2 * x1 * q6)

    # On a one-pivot branch, both bordered residuals vanish.  Their exact
    # e-specialisations are the displayed affine equations F25,F31.
    old_residual_25 = normalized_residual(
        syndrome, OLD_ROWS, (25, 5), p, q, t, p_on_e
    )
    old_residual_31 = normalized_residual(
        syndrome, OLD_ROWS, (31, 5), p, q, t, p_on_e
    )
    alternate_residual_25 = normalized_residual(
        syndrome, ALTERNATE_ROWS, (25, 5), p, q, t, p_on_e
    )
    alternate_residual_31 = normalized_residual(
        syndrome, ALTERNATE_ROWS, (31, 5), p, q, t, p_on_e
    )
    f25 = (
        2 * denominator**2 * a
        - 9 * t * (t - 1) * b
        + (t - 2) * (t + 1) * (2 * t - 1) ** 2 * c
        - 2 * t**4
        + 4 * t**3
        - 6 * t**2
        + 4 * t
        - 2
    )
    f31 = (
        2
        * denominator
        * (t**4 - 8 * t**3 + 6 * t**2 + 4 * t - 2)
        * a
        + 9 * t * (t - 1) * (t**2 + 2 * t - 2) * b
        + (
            -4 * t**6
            + 27 * t**4
            - 17 * t**3
            - 18 * t**2
            + 18 * t
            - 4
        )
        * c
        - 4 * t**6
        + 12 * t**5
        + 6 * t**4
        - 8 * t**3
        - 24 * t**2
        + 24 * t
        - 4
    )
    assert_zero(
        old_residual_25
        + 3 * f25 / ((t - 2) * (t + 1) * (2 * t - 1) ** 3)
    )
    assert_zero(
        alternate_residual_25
        + 3 * f25 / ((t - 2) * (t + 1) * (2 * t - 1) ** 3)
    )
    assert_zero(
        old_residual_31
        - 18 * f31 / ((t - 2) * (t + 1) * (2 * t - 1) ** 4)
    )
    assert_zero(
        alternate_residual_31
        - 18 * f31 / ((t - 2) * (t + 1) * (2 * t - 1) ** 4)
    )

    a25 = sp.diff(f25, a)
    b25 = sp.diff(f25, b)
    a31 = sp.diff(f31, a)
    b31 = sp.diff(f31, b)
    elimination_a = sp.factor(b31 * f25 - b25 * f31)
    elimination_b = sp.factor(a31 * f25 - a25 * f31)
    expected_elimination_a = (
        54
        * t**2
        * (t - 2)
        * (t - 1) ** 2
        * (t + 1)
        * (denominator * a - (t**2 - 1))
    )
    expected_elimination_b = (
        6
        * t
        * (t - 2)
        * (t - 1)
        * (t + 1)
        * denominator
        * (
            -9 * t**2 * b
            + 9 * t * b
            + (t - 2) * (t + 1) * (2 * t - 1) ** 2 * c
            + 2 * t**4
            - 12 * t**2
            + 8 * t
        )
    )
    assert sp.expand(elimination_a - expected_elimination_a) == 0
    assert sp.expand(elimination_b - expected_elimination_b) == 0
    forced_a = (t**2 - 1) / denominator
    forced_b = (
        (t - 2)
        * ((t + 1) * (2 * t - 1) ** 2 * c + 2 * t * (t**2 + 2 * t - 2))
        / (9 * t * (t - 1))
    )

    # The simultaneous X0=X1 branch has a two-chart pivot cover.
    double_coefficient = sp.Matrix((x0, x1)).jacobian((a, b))
    assert sp.factor(double_coefficient.det()) == (p - q) * total_pivot_factor
    double_a = (t + 1) * (2 * t**2 - 5 * t + 5) / 9
    double_b = -(
        (t - 2)
        * (t**2 + 2 * t - 2)
        * (2 * t**2 + t + 2)
        / (3 * denominator**2)
    )
    assert_zero(x0.subs({p: p_on_e, q: t, a: double_a, b: double_b}))
    assert_zero(x1.subs({p: p_on_e, q: t, a: double_a, b: double_b}))
    double_syndrome = syndrome.subs(
        {p: p_on_e, q: t, a: double_a, b: double_b}
    )
    pivot_a = sp.factor(
        sp.cancel(
            double_syndrome.extract(CHART_A_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            )
        )
    )
    pivot_b = sp.factor(
        sp.cancel(
            double_syndrome.extract(CHART_B_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            )
        )
    )
    expected_pivot_a = -(
        8
        * (t - 2) ** 3
        * (t - 1)
        * (t + 1) ** 5
        * (2 * t - 1) ** 4
        * (t**2 - 4 * t + 1)
        * (t**2 - t + 1) ** 7
        * (2 * t**2 - 5 * t + 5)
        / denominator**10
    )
    expected_pivot_b = (
        8
        * t
        * (t - 2) ** 5
        * (t + 1) ** 3
        * (2 * t - 1) ** 4
        * (t**2 - t + 1) ** 7
        * (t**2 + 2 * t - 2)
        * (2 * t**2 + t + 2)
        / denominator**10
    )
    assert_zero(pivot_a - expected_pivot_a)
    assert_zero(pivot_b - expected_pivot_b)
    gcd_pivots = sp.gcd(
        sp.Poly(
            sp.cancel(pivot_a).as_numer_denom()[0], t, domain=sp.QQ
        ),
        sp.Poly(
            sp.cancel(pivot_b).as_numer_denom()[0], t, domain=sp.QQ
        ),
    )
    expected_gcd = sp.Poly(
        (t - 2) ** 3
        * (t + 1) ** 3
        * (2 * t - 1) ** 4
        * (t**2 - t + 1) ** 7,
        t,
        domain=sp.QQ,
    )
    assert gcd_pivots.monic() == expected_gcd.monic()

    # Compute bordered numerators before e-specialisation.  Taking a
    # numerator after specialization can rescale a resultant by powers of D;
    # the generic identities below retain the exact Schur normalization.
    double_a_generic = (q - 1) * (q + 1) * (p + q - 2) / total_pivot_factor
    double_b_generic = p * (p - 2) * (p + q) / total_pivot_factor
    double_syndrome_generic = syndrome.subs(
        {a: double_a_generic, b: double_b_generic}
    )
    chart_a_residuals = {
        target: bordered_numerator(
            double_syndrome_generic, CHART_A_ROWS, target
        )
        for target in ((28, 2), (32, 8))
    }
    chart_b_residuals = {
        target: bordered_numerator(
            double_syndrome_generic, CHART_B_ROWS, target
        )
        for target in ((2, 8), (32, 8))
    }
    chart_a_resultant = sp.factor(
        sp.resultant(
            chart_a_residuals[(28, 2)],
            chart_a_residuals[(32, 8)],
            c,
        )
    )
    chart_b_resultant = sp.factor(
        sp.resultant(
            chart_b_residuals[(2, 8)],
            chart_b_residuals[(32, 8)],
            c,
        )
    )
    assert_zero(
        chart_a_resultant
        + 6 * l1 * total_pivot_factor * l2 * curve
    )
    chart_b_factor = p * q * (p - 2) * (q - 2) * (p + q)
    assert_zero(
        chart_b_resultant
        + 6 * chart_b_factor * l1 * l2 * curve
    )

    # The one-pivot family is a common kernel for every one of the three leaf
    # blocks.  The raw pivot in either branch supplies rank >= 6, while the
    # three independent block vectors supply rank <= 6.
    family_substitution = {
        p: p_on_e,
        q: t,
        a: forced_a,
        b: forced_b,
    }
    family_syndrome = syndrome.subs(family_substitution)
    kernel = sp.Matrix(
        [
            -2 * denominator**3,
            27 * t * (t - 1),
            (t - 2) * (t + 1) * (2 * t - 1) ** 4,
        ]
    )
    for block in range(3):
        assert (
            family_syndrome[:, 3 * block : 3 * block + 3] * kernel
        ).applyfunc(sp.cancel) == sp.zeros(37, 1)
    block_minor = sp.factor(
        sp.cancel(
            family_syndrome.extract((1, 17), (0, 1)).det(
                method="domain-ge"
            )
        )
    )
    expected_block_minor = (
        (t - 2)
        * (t + 1)
        * (2 * t - 1) ** 2
        * (t**2 - t + 1)
        / denominator**2
    )
    assert_zero(block_minor - expected_block_minor)
    family_leaf = leaf.subs(family_substitution)
    leaf_determinant = sp.factor(sp.cancel(family_leaf.det()))
    expected_leaf_determinant = (
        2
        * (t - 2)
        * (t + 1)
        * ((2 * t - 1) * c + t)
        / denominator
    )
    assert_zero(leaf_determinant - expected_leaf_determinant)

    # A rational point witnesses that the unsaturated leaf family itself is
    # nonempty, while the centre family is singular.
    sample = {t: 3, c: 0}
    sample_substitution = {key: value.subs(sample) for key, value in family_substitution.items()}
    sample_leaf = family_leaf.subs(sample)
    sample_syndrome = family_syndrome.subs(sample)
    sample_kernel = kernel.subs(sample)
    assert sample_substitution == {
        p: sp.Rational(13, 11),
        q: 3,
        a: sp.Rational(8, 11),
        b: sp.Rational(13, 9),
    }
    assert sample_leaf.det() == sp.Rational(24, 11)
    assert sample_syndrome.rank() == 6
    assert sample_syndrome[:, :8].rank() == 6
    assert tuple(sample_kernel) == (-2662, 162, 2500)
    assert sample_kernel[2] != 0
    assert sp.factor(
        sp.Matrix(
            [
                [0, 0, 0],
                [0, 0, 0],
                [
                    sample_kernel[0] / sample_kernel[2],
                    sample_kernel[1] / sample_kernel[2],
                    1,
                ],
            ]
        ).det()
    ) == 0

    # The e=0 generic open is nonempty; each listed exceptional value is
    # retained and delegated to the already published collision theorems.
    exceptional_values = {
        "t=2,-1": "p=q (H1), GLD87",
        "t=0,1": "p=s (H2), GLD87",
        "t**2-t+1=0": "q=s and P=0 (H3), GLD87/GLD89",
        "t=1/2": "d0=0 and p=q, GLD89",
        "2*t**2-2*t-1=0": "no affine e=0 point because gcd(D,N)=1",
    }

    return {
        "status": "exact_scoped_H4_e_boundary_determinant_safe_exclusion",
        "gld_identifier": "GLD94",
        "field": "Q_characteristic_zero_then_C",
        "syndrome_shape": list(syndrome.shape),
        "pivot_columns": list(PIVOT_COLUMNS),
        "old_pivot_rows": list(OLD_ROWS),
        "alternate_pivot_rows": list(ALTERNATE_ROWS),
        "auxiliary_chart_rows": [list(CHART_A_ROWS), list(CHART_B_ROWS)],
        "e_parameterization": {
            "parameter": "t=q",
            "D": str(denominator),
            "N": str(numerator),
            "p": str(p_on_e),
            "gcd_D_N": "1",
        },
        "generic_open_factors": GENERIC_FACTORS,
        "e_factor_restrictions": {name: str(value) for name, value in e_factors.items()},
        "curve_restriction": str(curve_on_e),
        "raw_pivots": {
            "old": "-6*(p-q)^2*X0*Q6",
            "alternate": "-6*(p-q)^2*X1*Q6",
        },
        "one_pivot_residuals": {
            "F25": str(f25),
            "F31": str(f31),
            "forced_a": str(forced_a),
            "forced_b": str(forced_b),
        },
        "simultaneous_pivot_obstruction": {
            "double_a": str(double_a),
            "double_b": str(double_b),
            "pivot_A": str(expected_pivot_a),
            "pivot_B": str(expected_pivot_b),
            "pivot_numerator_gcd": str(expected_gcd.as_expr()),
            "resultant_A": "-6*L1*T*L2*R",
            "resultant_B": "-6*p*q*(p-2)*(q-2)*(p+q)*L1*L2*R",
            "R_on_e": str(curve_on_e),
        },
        "all_block_kernel": [str(value) for value in kernel],
        "unsaturated_family_nonempty": True,
        "center_family_singular": True,
        "sample": {
            "t": "3",
            "p": "13/11",
            "q": "3",
            "a": "8/11",
            "b": "13/9",
            "c": "0",
            "leaf_determinant": "24/11",
            "syndrome_rank": 6,
            "base_syndrome_rank": 6,
            "kernel": [str(value) for value in sample_kernel],
        },
        "exceptional_values": exceptional_values,
        "dependencies": ["GLD71", "GLD75", "GLD86", "GLD87", "GLD89", "GLD90"],
        "full_intrinsic_fitting_pullback_computed": False,
        "other_H4_boundaries_and_charts_open": True,
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    result = check()
    print("GLD94 H4 e-boundary determinant-safe verifier: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
