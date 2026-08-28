#!/usr/bin/env python3
"""Verify the GLD90 H4 low-rank exclusion on the Q6-open stratum."""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
PIVOT_COLUMNS = (0, 1, 3, 4, 6, 7)
OLD_ROWS = (0, 1, 2, 17, 19, 32)
ALTERNATE_ROWS = (0, 1, 17, 19, 28, 32)
CHART_A_ROWS = (0, 1, 2, 17, 19, 25)
CHART_B_ROWS = (0, 1, 17, 19, 25, 28)


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


def assert_polynomial_divisible(
    expression: sp.Expr,
    divisor: sp.Expr,
    variables: tuple[sp.Symbol, ...],
) -> sp.Expr:
    numerator = sp.cancel(expression).as_numer_denom()[0]
    quotient, remainder = sp.div(
        sp.Poly(numerator, *variables, domain=sp.QQ),
        sp.Poly(divisor, *variables, domain=sp.QQ),
    )
    assert remainder.is_zero
    return sp.factor(quotient.as_expr())


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


def corner_check(gld71, parent, relations) -> list[dict[str, object]]:
    c = sp.symbols("c")
    points = ((1, 2), (-1, 0), (2, 1), (0, -1))
    records = []
    for pv, qv in points:
        d0 = pv + qv - 1
        t_value = 2 * pv * qv - pv - qv + 2
        sv = sp.Rational(pv + qv - pv * qv, d0)
        av = sp.Rational(
            (qv - 1) * (qv + 1) * (pv + qv - 2), t_value
        )
        bv = sp.Rational(pv * (pv - 2) * (pv + qv), t_value)
        leaf = sp.Matrix(
            [[1, 1, 1], [pv, qv, sv], [av, 1 + bv, 1 + c]]
        )
        syndrome = gld71.coefficient_matrix(
            parent, relations, (leaf, leaf, leaf)
        )
        witnesses: list[tuple[tuple[int, ...], tuple[int, ...]]] = [
            (
                (
                    (0, 1, 17, 19, 25, 28, 32)
                    if (pv, qv) == (0, -1)
                    else (0, 1, 17, 19, 25, 28, 31)
                ),
                (0, 1, 2, 3, 4, 5, 6),
            ),
            (
                (0, 1, 17, 19, 25, 31, 32),
                (
                    (0, 1, 2, 3, 4, 5, 7)
                    if (pv, qv) == (0, -1)
                    else (0, 1, 2, 3, 4, 5, 6)
                ),
            ),
        ]
        if (pv, qv) in ((-1, 0), (2, 1)):
            witnesses.append(
                (
                    (0, 1, 17, 19, 25, 28, 32),
                    (0, 1, 2, 3, 4, 5, 6),
                )
            )
        minors = [
            sp.factor(syndrome.extract(rows, columns).det(method="domain-ge"))
            for rows, columns in witnesses
        ]
        gcd = sp.Poly(minors[0], c, domain=sp.QQ)
        for minor in minors[1:]:
            gcd = sp.gcd(gcd, sp.Poly(minor, c, domain=sp.QQ))
        assert gcd.degree() == 0
        records.append(
            {
                "point": [pv, qv],
                "s_a_b": [str(sv), str(av), str(bv)],
                "leaf_determinant": str(sp.factor(leaf.det())),
                "seven_minor_witnesses": [str(value) for value in minors],
                "minor_gcd": str(gcd.as_expr()),
            }
        )
    return records


def check() -> dict[str, object]:
    gld71 = load_module(GLD71, "gld71_for_gld90")
    gld88 = load_module(GLD88, "gld88_for_gld90")
    parent = gld71.load_parent()
    relations = gld71.full_relations(parent)
    assert len(relations) == 37

    p, q, a, b, c = sp.symbols("p q a b c")
    d0 = p + q - 1
    pnorm = p**2 - p + 1
    l1 = p**2 + 2 * p * q - 2 * p - q
    l2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    t = 2 * p * q - p - q + 2
    q6 = q6_polynomial(p, q)
    curve = residual_curve(p, q)
    s = (p + q - p * q) / d0
    leaf = sp.Matrix([[1, 1, 1], [p, q, s], [a, 1 + b, 1 + c]])
    syndrome = gld71.coefficient_matrix(
        parent, relations, (leaf, leaf, leaf)
    )

    old_pivot = sp.factor(
        sp.cancel(
            syndrome.extract(OLD_ROWS, PIVOT_COLUMNS).det(method="domain-ge")
        )
    )
    alternate_pivot = sp.factor(
        sp.cancel(
            syndrome.extract(ALTERNATE_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            )
        )
    )
    x0 = a * (p**2 - 1) - (b + 1) * (q**2 - 1)
    x1 = a * p * (p - 2) - b * q * (q - 2) - p * (p - 2)
    assert sp.cancel(old_pivot + 6 * (p - q) ** 2 * x0 * q6) == 0
    assert sp.cancel(alternate_pivot + 6 * (p - q) ** 2 * x1 * q6) == 0

    alternate_residuals = sp.Matrix(
        [
            bordered_numerator(syndrome, ALTERNATE_ROWS, target)
            for target in ((25, 5), (31, 5))
        ]
    )
    alternate_coefficient = alternate_residuals.jacobian((b, c))
    alternate_determinant = sp.factor(alternate_coefficient.det())
    expected_delta = sp.factor(
        -6 * (p - q) * d0 * pnorm * l1 * l2 * e
    )
    assert alternate_determinant == expected_delta
    alternate_solution = -alternate_coefficient.inv() * alternate_residuals.subs(
        {b: 0, c: 0}
    )
    generic_family = gld88.h4_family(p, q, a)
    assert sp.cancel(alternate_solution[0] - generic_family["b"]) == 0
    assert sp.cancel(alternate_solution[1] - generic_family["c"]) == 0

    # The T=0 boundary is not a residual.  Since T is linear in q and is
    # inconsistent when 2*p-1=0, every T-point has the following chart.
    q_on_t = (p - 2) / (2 * p - 1)
    assert sp.cancel(t.subs(q, q_on_t)) == 0
    assert sp.cancel(q6.subs(q, q_on_t) - 8 * pnorm**4 / (2 * p - 1) ** 4) == 0
    assert sp.cancel((p - q).subs(q, q_on_t) - 2 * pnorm / (2 * p - 1)) == 0
    assert sp.cancel(l1.subs(q, q_on_t) - (p - 2) * (p + 1)) == 0
    assert sp.cancel(
        l2.subs(q, q_on_t) + 9 * p * (p - 1) / (2 * p - 1) ** 2
    ) == 0
    assert sp.cancel(
        e.subs(q, q_on_t) + 3 * (p - 2) * (p + 1) / (2 * p - 1)
    ) == 0
    x0_on_t = sp.factor(sp.cancel(x0.subs(q, q_on_t)))
    x1_on_t = sp.factor(sp.cancel(x1.subs(q, q_on_t)))
    t_bracket_0 = (2 * p - 1) ** 2 * a + 3 * b + 3
    t_bracket_1 = (2 * p - 1) ** 2 * (a - 1) + 3 * b
    assert sp.cancel(
        x0_on_t
        - (p - 1) * (p + 1) * t_bracket_0 / (2 * p - 1) ** 2
    ) == 0
    assert sp.cancel(
        x1_on_t
        - p * (p - 2) * t_bracket_1 / (2 * p - 1) ** 2
    ) == 0
    assert sp.expand(t_bracket_0 - t_bracket_1) == 4 * pnorm

    double_coefficient = sp.Matrix((x0, x1)).jacobian((a, b))
    assert sp.factor(double_coefficient.det()) == (p - q) * t
    double_solution = -double_coefficient.inv() * sp.Matrix((x0, x1)).subs(
        {a: 0, b: 0}
    )
    double_a = sp.factor(
        (q - 1) * (q + 1) * (p + q - 2) / t
    )
    double_b = sp.factor(p * (p - 2) * (p + q) / t)
    assert sp.cancel(double_solution[0] - double_a) == 0
    assert sp.cancel(double_solution[1] - double_b) == 0

    double_leaf = leaf.subs({a: double_a, b: double_b})
    double_syndrome = syndrome.subs({a: double_a, b: double_b})
    chart_a_pivot = sp.factor(
        sp.cancel(
            double_syndrome.extract(CHART_A_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            )
        )
    )
    chart_b_pivot = sp.factor(
        sp.cancel(
            double_syndrome.extract(CHART_B_ROWS, PIVOT_COLUMNS).det(
                method="domain-ge"
            )
        )
    )
    chart_a_factor = (p - 1) * (p + 1) * (q - 1) * (q + 1) * (p + q - 2)
    chart_b_factor = p * q * (p - 2) * (q - 2) * (p + q)
    assert sp.cancel(
        chart_a_pivot + 3 * (p - q) ** 3 * d0 * q6 * chart_a_factor / t
    ) == 0
    assert sp.cancel(
        chart_b_pivot - 3 * (p - q) ** 3 * d0 * q6 * chart_b_factor / t
    ) == 0

    chart_a_residuals = {
        target: bordered_numerator(double_syndrome, CHART_A_ROWS, target)
        for target in ((28, 2), (32, 8))
    }
    chart_b_residuals = {
        target: bordered_numerator(double_syndrome, CHART_B_ROWS, target)
        for target in ((32, 8), (31, 5))
    }
    chart_a_resultant = sp.factor(
        sp.resultant(
            chart_a_residuals[(28, 2)],
            chart_a_residuals[(32, 8)],
            c,
        )
    )
    chart_b_classifier = bordered_numerator(
        double_syndrome, CHART_B_ROWS, (2, 8)
    )
    chart_b_resultant = sp.factor(
        sp.resultant(
            chart_b_classifier,
            chart_b_residuals[(32, 8)],
            c,
        )
    )
    assert sp.cancel(chart_a_resultant + 6 * l1 * t * l2 * curve) == 0
    assert sp.cancel(
        chart_b_resultant + 6 * chart_b_factor * l1 * l2 * curve
    ) == 0

    curve_family = gld88.h4_family(p, q, double_a)
    b_difference = sp.cancel(double_b - curve_family["b"])
    assert_polynomial_divisible(b_difference, curve, (p, q))
    for residual in (*chart_a_residuals.values(), *chart_b_residuals.values()):
        assert_polynomial_divisible(
            residual.subs(c, curve_family["c"]), curve, (p, q)
        )

    u = p * q - p - q
    v = p * q + p + q - 2
    chart_a_anchor_coefficient = sp.factor(
        sp.diff(chart_a_residuals[(28, 2)], c)
    )
    chart_a_backup_coefficient = sp.factor(
        sp.diff(chart_a_residuals[(32, 8)], c)
    )
    assert sp.cancel(chart_a_anchor_coefficient - u * v * t) == 0
    assert sp.cancel(
        chart_a_backup_coefficient
        - 6 * (p * q - 1) * (p * q - 2 * p - 2 * q + 1) * t
    ) == 0
    chart_b_anchor_coefficient = sp.factor(
        sp.diff(chart_b_residuals[(32, 8)], c)
    )
    assert sp.cancel(chart_b_anchor_coefficient - 6 * u * v * t) == 0

    # On U=0 or V=0, the curve equation leaves only already excluded factors,
    # except V=0 and p^2+2=0.  Chart A remains open there and its backup
    # coefficient is nonzero, so that residual still forces c.
    u_curve = sp.factor(
        sp.cancel(curve.subs(q, p / (p - 1))).as_numer_denom()[0]
    )
    v_curve = sp.factor(
        sp.cancel(curve.subs(q, (2 - p) / (p + 1))).as_numer_denom()[0]
    )
    assert u_curve == -p**2 * (p - 2) ** 2 * pnorm**2
    assert v_curve == 3 * p * (p - 2) * (p**2 + 2) * pnorm**2
    chart_a_factor_on_special = sp.cancel(
        chart_a_factor.subs(q, (2 - p) / (p + 1))
    ).as_numer_denom()[0]
    assert sp.gcd(
        sp.Poly(chart_a_factor_on_special, p, domain=sp.QQ),
        sp.Poly(p**2 + 2, p, domain=sp.QQ),
    ).degree() == 0
    backup_on_special = sp.cancel(
        chart_a_backup_coefficient.subs(q, (2 - p) / (p + 1))
    ).as_numer_denom()[0]
    _special_quotient, special_remainder = sp.div(
        sp.Poly(backup_on_special, p, domain=sp.QQ),
        sp.Poly(p**2 + 2, p, domain=sp.QQ),
    )
    assert sp.factor(special_remainder.as_expr()) != 0
    assert sp.gcd(
        special_remainder, sp.Poly(p**2 + 2, p, domain=sp.QQ)
    ).degree() == 0

    boundary_product = sp.factor(
        (p - q) * d0 * pnorm * l1 * l2 * e * q6 * t
    )
    first_factors = (p - 1, p + 1, q - 1, q + 1, p + q - 2)
    second_factors = (p, q, p - 2, q - 2, p + q)
    surviving_corners = set()
    for first, second in itertools.product(first_factors, second_factors):
        solutions = sp.solve((first, second), (p, q), dict=True)
        for solution in solutions:
            if sp.simplify(boundary_product.subs(solution)) != 0:
                surviving_corners.add((solution[p], solution[q]))
    assert surviving_corners == {(1, 2), (-1, 0), (2, 1), (0, -1)}
    corner_records = corner_check(gld71, parent, relations)

    # The GLD88 block-kernel identities apply after the exact modulo-R
    # identification above.  This independent algebraic sample confirms that
    # the retained curve open is nonempty over Q(sqrt(-2)).
    root = sp.sqrt(2) * sp.I
    sample = {p: 2, q: root}
    assert sp.simplify(curve.subs(sample)) == 0
    sample_a = sp.simplify(double_a.subs(sample))
    sample_b = sp.simplify(double_b.subs(sample))
    sample_c = sp.simplify(curve_family["c"].subs(sample))
    assert (sample_a, sample_b, sample_c) == (-1, 0, 0)
    sample_with_leaf = sample | {a: sample_a, b: sample_b, c: sample_c}
    assert sp.simplify(x0.subs(sample_with_leaf)) == 0
    assert sp.simplify(x1.subs(sample_with_leaf)) == 0
    for open_factor in (p - q, d0, pnorm, l1, l2, e, q6, t):
        assert sp.simplify(open_factor.subs(sample)) != 0
    sample_leaf = double_leaf.subs(c, curve_family["c"]).subs(sample)
    assert sp.simplify(sample_leaf.det()) != 0

    # An exact point on T=0 and the old-pivot boundary shows that the new
    # alternate-pivot case is nonempty before imposing the center determinant.
    t_sample = {
        p: sp.Integer(3),
        q: sp.Rational(1, 5),
        a: sp.Rational(48, 1331),
    }
    t_sample_family = {
        b: sp.simplify(generic_family["b"].subs(t_sample)),
        c: sp.simplify(generic_family["c"].subs(t_sample)),
    }
    assert t_sample_family == {
        b: sp.Rational(-1731, 1331),
        c: sp.Rational(-3, 11),
    }
    t_sample_full = t_sample | t_sample_family
    assert sp.simplify(t.subs(t_sample_full)) == 0
    assert sp.simplify(x0.subs(t_sample_full)) == 0
    assert sp.simplify(x1.subs(t_sample_full)) != 0
    for open_factor in (p - q, d0, pnorm, l1, l2, e, q6):
        assert sp.simplify(open_factor.subs(t_sample_full)) != 0
    t_sample_leaf = leaf.subs(t_sample_full)
    t_sample_syndrome = syndrome.subs(t_sample_full)
    assert sp.simplify(t_sample_leaf.det()) != 0
    assert t_sample_syndrome.rank() == 6
    t_kernel = sp.Matrix(
        [[
            sp.simplify(generic_family["u"].subs(t_sample)),
            sp.simplify(generic_family["v"].subs(t_sample)),
            1,
        ]]
    )
    for block in range(3):
        assert (
            t_sample_syndrome[:, 3 * block : 3 * block + 3] * t_kernel.T
        ) == sp.zeros(37, 1)

    return {
        "status": "exact_scoped_H4_Q6_open_low_rank_exclusion",
        "gld_identifier": "GLD90",
        "old_pivot_rows": list(OLD_ROWS),
        "alternate_pivot_rows": list(ALTERNATE_ROWS),
        "auxiliary_chart_rows": [list(CHART_A_ROWS), list(CHART_B_ROWS)],
        "pivot_columns": list(PIVOT_COLUMNS),
        "old_and_alternate_raw_pivots_factored": True,
        "alternate_chart_rederives_GLD88_family": True,
        "double_pivot_solution": {"a": str(double_a), "b": str(double_b)},
        "residual_curve": str(curve),
        "curve_family_identified_modulo_residual": True,
        "T_boundary": {
            "closed_on_D_Delta": True,
            "q_parameterization": str(q_on_t),
            "Q6_restriction": str(sp.factor(q6.subs(q, q_on_t))),
            "simultaneous_pivot_obstruction": str(
                sp.expand(t_bracket_0 - t_bracket_1)
            ),
            "old_pivot_boundary_sample": {
                "p": "3",
                "q": "1/5",
                "a": "48/1331",
                "b": "-1731/1331",
                "c": "-3/11",
                "syndrome_rank": 6,
                "common_kernel": [str(value) for value in t_kernel],
            },
        },
        "corner_records": corner_records,
        "nonempty_algebraic_sample": {
            "p": "2",
            "q": "sqrt(2)*I",
            "a": str(sample_a),
            "b": str(sample_b),
            "c": str(sample_c),
            "leaf_determinant": str(sp.simplify(sample_leaf.det())),
        },
        "remaining_H4_boundary": ["Q6=0", "L1=0", "L2=0", "e=0"],
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    result = check()
    print("GLD90 H4 Q6-open low-rank verifier: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
