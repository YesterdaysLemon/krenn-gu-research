#!/usr/bin/env python3
"""Verify the endpoint t3=1 divisor obstruction."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Callable

import sympy as sp


for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.p5_marked_basis import mixed_matrix


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md"
END_INTERSECTION = (
    REPO_ROOT / 'claims/p5/h31/elliptic-end-genus-two-exception/P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md'
)
Q3_HELPER = REPO_ROOT / 'claims/p5/h31/elliptic-end-t3-divisor-q3/verify_p5_h31_elliptic_end_t3_divisor_q3.py'
ROWS_A = (0, 1, 3, 4, 5, 6, 9)
ROWS_E = (0, 1, 3, 4, 5, 12, 9)
ROWS_J1 = (0, 1, 3, 4, 5, 11, 9)
ROWS_J2 = (0, 1, 3, 4, 5, 13, 9)
ROWS_T0 = (0, 1, 3, 4, 6, 7, 9)
ROWS_H11 = (0, 1, 3, 4, 6, 9, 11)
ROWS_H12 = (0, 1, 3, 4, 6, 9, 12)
ROWS_H13 = (0, 1, 3, 4, 6, 13, 9)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reduce_quadratic(expression, variable, relation) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, variable),
        sp.Poly(relation, variable),
    ).as_expr()
    return sp.factor(remainder / denominator)


def dependent_factor(expression, variables) -> sp.Expr:
    if not isinstance(variables, tuple):
        variables = (variables,)
    numerator = sp.factor(sp.fraction(sp.cancel(expression))[0])
    factors = [
        factor
        for factor, multiplicity in sp.factor_list(numerator)[1]
        if any(factor.has(variable) for variable in variables)
        for _ in range(multiplicity)
    ]
    assert len(factors) == 1, factors
    return factors[0]


def canonical_numerator(expression) -> sp.Expr:
    return sp.factor(sp.fraction(sp.cancel(expression))[0])


def associate(left, right, *variables) -> bool:
    quotient = sp.cancel(left / right)
    return not any(quotient.has(variable) for variable in variables)


def strip_factors(expression, factors, *variables) -> sp.Expr:
    result = canonical_numerator(expression)
    for factor in factors:
        while True:
            quotient, remainder = sp.div(
                sp.Poly(result, *variables),
                sp.Poly(factor, *variables),
            )
            if remainder.as_expr() != 0:
                break
            result = sp.factor(quotient.as_expr())
    return sp.factor(result)


def direct_system_builder(distinguished, alpha, beta):
    return mixed_matrix(distinguished, alpha, beta)


def verify_endpoint(
    distinguished: int,
    epsilon: int,
    system_builder: Callable = direct_system_builder,
) -> dict:
    assert (distinguished, epsilon) in ((0, 1), (3, -1))
    r, x, Y = sp.symbols("r x Y")
    t0, t1, t2, t3 = sp.symbols("t0:4")
    D = x + r**2 - 1
    f = x * (
        (1 - r**2) * x**2
        + (3 * r**2 - 2) * x
        + (r**2 - 1) ** 2
    )
    elliptic_relation = Y**2 - f
    alpha = (
        (
            Y + r**2 * x,
            -r * x - r**2 * x,
            -r * x + r**2 * x,
            -Y + r**2 * x,
        ),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (r, -1, -1, r),
    )
    beta_zero = (
        (1, -1, 1, 1),
        (D, r * x + D, r * x - D, D),
        (x * (1 - x) + Y, r * x, r * x, x * (1 - x) - Y),
        (0, 1, 1, 0),
    )
    shifts = (t0, t1, t2, t3)
    beta = tuple(
        tuple(
            beta_zero[mode][coordinate]
            + shifts[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    mixed, diagonal_a, diagonal_b = system_builder(
        distinguished,
        alpha,
        beta,
    )
    quotient = mixed[:, [0, 2, 3, 4, 5, 6, 7]]
    divisor = quotient.subs(t3, 1)

    determinant_cache = {}

    def determinant(rows) -> sp.Expr:
        if rows not in determinant_cache:
            determinant_cache[rows] = reduce_quadratic(
                divisor.extract(rows, range(7)).det(method="domain-ge"),
                Y,
                elliptic_relation,
            )
        return determinant_cache[rows]

    A = dependent_factor(determinant(ROWS_A), (t1, t2))
    E = dependent_factor(determinant(ROWS_E), (t1, t2))
    assert sp.degree(A, t1) == sp.degree(E, t1) == 1
    compatibility = reduce_quadratic(
        sp.diff(A, t1) * E.subs(t1, 0)
        - sp.diff(E, t1) * A.subs(t1, 0),
        Y,
        elliptic_relation,
    )
    assert sp.degree(canonical_numerator(compatibility), t2) == 2

    Z = epsilon * Y
    t2_minus = -x * (-Z + r**2 * x - r**2 - x + 1) / D
    t2_plus = (
        r**2
        * x
        * (2 * Z + r**2 * x + r**2 + x - 1)
        / ((r**2 - 1) * (x - 1) ** 2)
    )
    for root in (t2_minus, t2_plus):
        assert reduce_quadratic(
            compatibility.subs(t2, root),
            Y,
            elliptic_relation,
        ) == 0

    R = (
        r**8
        - r**6 * x
        - 4 * r**6
        + 3 * r**4 * x**2
        - 9 * r**4 * x
        + 6 * r**4
        + r**2 * x**3
        - 6 * r**2 * x**2
        + 9 * r**2 * x
        - 4 * r**2
        - x**3
        + 3 * x**2
        - 3 * x
        + 1
    )
    K = (
        r**8
        + 2 * r**6 * x**2
        + 9 * r**6 * x
        - 4 * r**6
        + r**4 * x**4
        - 9 * r**4 * x**3
        + 24 * r**4 * x**2
        - 22 * r**4 * x
        + 6 * r**4
        - 2 * r**2 * x**4
        + 13 * r**2 * x**3
        - 24 * r**2 * x**2
        + 17 * r**2 * x
        - 4 * r**2
        + x**4
        - 4 * x**3
        + 6 * x**2
        - 4 * x
        + 1
    )
    compatibility_numerator = canonical_numerator(compatibility)
    discriminant = reduce_quadratic(
        sp.discriminant(compatibility_numerator, t2),
        Y,
        elliptic_relation,
    )
    discriminant_norm = reduce_quadratic(
        discriminant * discriminant.subs(Y, -Y),
        Y,
        elliptic_relation,
    )
    expected_discriminant_norm = (
        x**4
        * (r - 1) ** 6
        * (r + 1) ** 6
        * (x - 1) ** 2
        * (x - 1 - r) ** 2
        * (x - 1 + r) ** 2
        * D**8
        * R**2
        * K**2
    )
    # The chosen primitive compatibility carries the square chart unit
    # x^2(x-1)^2.  Removing it gives the intrinsic norm below.
    assert associate(
        canonical_numerator(discriminant_norm),
        x**4 * (x - 1) ** 4 * expected_discriminant_norm,
        r,
        x,
    )

    J1 = determinant(ROWS_J1)
    J2 = determinant(ROWS_J2)
    t1_minus = reduce_quadratic(
        -A.subs({t2: t2_minus, t1: 0})
        / sp.diff(A, t1).subs(t2, t2_minus),
        Y,
        elliptic_relation,
    )
    expected_t1_minus = -(
        Y * r**2
        - Y * x
        + Y
        - 2 * r**4
        + 2 * r**2 * x**2
        - 6 * r**2 * x
        + 4 * r**2
        - 2 * x**2
        + 4 * x
        - 2
    ) / D
    compact_t1_minus = (
        epsilon * expected_t1_minus.subs(Y, epsilon * Y)
    )
    assert reduce_quadratic(
        t1_minus - compact_t1_minus,
        Y,
        elliptic_relation,
    ) == 0
    t1_minus = compact_t1_minus
    assert reduce_quadratic(
        E.subs({t2: t2_minus, t1: t1_minus}),
        Y,
        elliptic_relation,
    ) == 0

    def norm_on_branch(expression, substitutions) -> sp.Expr:
        value = reduce_quadratic(
            expression.subs(substitutions),
            Y,
            elliptic_relation,
        )
        return canonical_numerator(reduce_quadratic(
            value * value.subs(Y, -Y),
            Y,
            elliptic_relation,
        ))

    minus_norms = [
        norm_on_branch(J, {t2: t2_minus, t1: t1_minus})
        for J in (J1, J2)
    ]
    minus_gcd = sp.factor(sp.gcd(*minus_norms))
    chart_factors = (
        r,
        x,
        r - 1,
        r + 1,
        x - 1,
        x - 1 - r,
        x - 1 + r,
        D,
    )
    minus_essential = strip_factors(
        minus_gcd,
        chart_factors,
        r,
        x,
    )
    assert associate(minus_essential, R, r, x), minus_essential
    minus_essential = R

    # On the plus branch the A-pivot may vanish.  Resultants retain those
    # fibres and avoid dividing by its coefficient.
    plus_norms = []
    for J in (J1, J2):
        resultant = sp.resultant(E, J, t1)
        plus_norms.append(norm_on_branch(resultant, {t2: t2_plus}))
    plus_gcd = sp.factor(sp.gcd(*plus_norms))
    plus_essential = strip_factors(
        plus_gcd,
        chart_factors,
        r,
        x,
    )
    assert associate(plus_essential, R**2, r, x), plus_essential
    plus_essential = R**2

    s, u, v = sp.symbols("s u v")
    d = s**3 + 3 * s**2 - s + 1
    n = s**3 + 3 * s**2 + 3 * s + 5
    h = sp.expand(n * d)
    u_parameter = n / d
    x_parameter = (s + 1) ** 4 / d
    Y_parameter = (s - 1) * (s + 1) ** 3 * n / d**2
    hyperelliptic_relation = v**2 - h
    assert sp.factor(R.subs(r**2, u).subs({
        u: u_parameter,
        x: x_parameter,
    })) == 0
    assert sp.factor(sp.discriminant(h, s)) == 2**24 * 3**3 * 11

    def even_part(expression) -> sp.Expr:
        numerator, denominator = sp.fraction(sp.cancel(expression))
        polynomial = sp.Poly(sp.expand(numerator), r)
        minimum_power = min(monomial[0] for monomial, _ in polynomial.terms())
        numerator = sp.cancel(numerator / r**minimum_power)
        in_u_numerator = sp.expand(numerator).subs(r**2, u)
        in_u_denominator = sp.expand(denominator).subs(r**2, u)
        assert not in_u_numerator.has(r)
        assert not in_u_denominator.has(r)
        return sp.cancel(in_u_numerator / in_u_denominator)

    even_cache = {}

    def pull(
        expression,
        sigma: int,
        substitutions=None,
    ) -> sp.Expr:
        key = id(expression)
        if key not in even_cache:
            even_cache[key] = even_part(expression)
        values = {
            u: u_parameter,
            x: x_parameter,
            Y: epsilon * sigma * Y_parameter,
        }
        if substitutions:
            values.update(substitutions)
        return sp.factor(even_cache[key].subs(values))

    t1_main = epsilon * (
        (s - 1) ** 2 * (s + 1) * (s + 3) * n / d**2
    )
    candidates = {
        ("positive", "minus"): {
            "sigma": 1,
            "t2": (
                (s + 1) ** 4
                * (s**3 + s**2 - 5 * s - 1)
                / d**2
            ),
            "t1": t1_main,
            "t0": -d**2 / (2 * s * (s + 1) ** 3 * n),
        },
        ("positive", "plus"): {
            "sigma": 1,
            "t2": (s + 1) ** 4 * (s + 2) / d,
            "t1": t1_main,
            "t0": -d**2 / (2 * s * (s + 1) ** 3 * n),
        },
        ("negative", "minus"): {
            "sigma": -1,
            "t2": -(
                (s + 1) ** 4
                * (s**3 + s**2 + 3 * s - 1)
                / d**2
            ),
            "t1": -epsilon * (
                (s - 1) ** 3 * (s + 1) * n / d**2
            ),
            "t0": -d**2 / (2 * (s + 1) ** 3 * n),
        },
    }
    P = 2 * s**5 + 7 * s**4 + 6 * s**3 + 4 * s**2 + 1
    N = (
        2 * s**6
        + 5 * s**5
        + 7 * s**4
        + 6 * s**3
        - 4 * s**2
        + s
        - 1
    )
    candidates[("negative", "plus")] = {
        "sigma": -1,
        "t2": (
            (s + 1) ** 4 * (s**2 + s + 1) / (s**2 * d)
        ),
        "t1": -epsilon * n * N / (d * P),
        "t0": -(
            d**2
            * (s**5 + 3 * s**4 + 4 * s**3 + 4 * s**2 - s + 1)
            / ((s + 1) ** 4 * n * P)
        ),
    }
    assert sp.gcd(P, N) == 1
    assert sp.resultant(P, N, s) == 2**19

    determinant_expressions = {
        "A": A,
        "E": E,
        "J1": J1,
        "J2": J2,
        "T0": determinant(ROWS_T0),
        "H11": determinant(ROWS_H11),
        "H12": determinant(ROWS_H12),
        "H13": determinant(ROWS_H13),
    }

    pulled = {}
    for key, candidate in candidates.items():
        substitutions = {
            t0: candidate["t0"],
            t1: candidate["t1"],
            t2: candidate["t2"],
        }
        sigma = candidate["sigma"]
        for source in ("A", "E", "T0"):
            assert pull(
                determinant_expressions[source],
                sigma,
                substitutions,
            ) == 0
        pulled[key] = {
            source: pull(
                determinant_expressions[source],
                sigma,
                substitutions,
            )
            for source in ("J1", "J2", "H11", "H12", "H13")
        }

    s_chart_factors = (s + 1, d, n)

    def residual_gcd(expressions) -> sp.Expr:
        nonzero = [
            canonical_numerator(expression)
            for expression in expressions
            if expression != 0
        ]
        result = sp.factor(sp.gcd(*nonzero))
        return strip_factors(result, s_chart_factors, s)

    quadratic_exception = s**2 + 2 * s - 1
    assert associate(
        residual_gcd([
            pulled[("positive", "minus")]["H11"],
            pulled[("positive", "minus")]["H12"],
            pulled[("positive", "minus")]["H13"],
        ]),
        quadratic_exception,
        s,
    )
    assert associate(
        residual_gcd([
            pulled[("positive", "plus")]["H11"],
            pulled[("positive", "plus")]["H12"],
            pulled[("positive", "plus")]["H13"],
        ]),
        1,
        s,
    )
    negative_exception = s * (s - 1) * (s**2 + 1)
    for branch in ("minus", "plus"):
        branch_gcd = residual_gcd([
            pulled[("negative", branch)]["J1"],
            pulled[("negative", branch)]["J2"],
        ])
        branch_gcd_squarefree = sp.factor(
            sp.sqf_part(sp.Poly(branch_gcd, s)).as_expr()
        )
        assert associate(
            branch_gcd_squarefree,
            negative_exception,
            s,
        ), (branch, branch_gcd)

    def rank_at(candidate, s_value, v_sign):
        sigma = candidate["sigma"]
        substitutions_s = {
            s: s_value,
        }
        d_value = sp.simplify(d.subs(substitutions_s))
        h_value = sp.simplify(h.subs(substitutions_s))
        v_value = v_sign * sp.sqrt(h_value)
        substitutions = {
            r: v_value / d_value,
            x: sp.simplify(x_parameter.subs(substitutions_s)),
            Y: sp.simplify(
                epsilon
                * sigma
                * Y_parameter.subs(substitutions_s)
            ),
            t0: sp.simplify(candidate["t0"].subs(substitutions_s)),
            t1: sp.simplify(candidate["t1"].subs(substitutions_s)),
            t2: sp.simplify(candidate["t2"].subs(substitutions_s)),
            t3: 1,
        }
        evaluated_mixed = mixed.subs(substitutions).applyfunc(sp.simplify)
        evaluated_a = diagonal_a.subs(substitutions).applyfunc(sp.simplify)
        evaluated_b = diagonal_b.subs(substitutions).applyfunc(sp.simplify)
        return (
            evaluated_mixed.rank(),
            evaluated_mixed.col_join(evaluated_a).rank(),
            evaluated_mixed.col_join(evaluated_b).rank(),
        )

    finite_ranks = {}
    for s_value in (-1 + sp.sqrt(2), -1 - sp.sqrt(2)):
        for v_sign in (-1, 1):
            ranks = rank_at(
                candidates[("positive", "minus")],
                s_value,
                v_sign,
            )
            assert ranks == (6, 7, 6)
            finite_ranks[f"positive-minus:{s_value}:{v_sign}"] = ranks

    for branch in ("minus", "plus"):
        for s_value in (sp.Integer(1), sp.I, -sp.I):
            for v_sign in (-1, 1):
                ranks = rank_at(
                    candidates[("negative", branch)],
                    s_value,
                    v_sign,
                )
                expected = (7, 7, 8) if s_value == 1 else (6, 7, 6)
                assert ranks == expected
                finite_ranks[
                    f"negative-{branch}:{s_value}:{v_sign}"
                ] = ranks

    return {
        "distinguished_coordinate": distinguished,
        "epsilon": epsilon,
        "split_marking_cover": True,
        "generic_branch_obstructions": {
            "minus_essential_gcd": str(minus_essential),
            "plus_essential_gcd": str(plus_essential),
        },
        "genus_two_sheet_obstructions": {
            "positive_minus": str(quadratic_exception),
            "positive_plus": "1",
            "negative": str(negative_exception),
        },
        "finite_exception_ranks": {
            key: list(value) for key, value in finite_ranks.items()
        },
        "binary_survivor_on_regular_t3_divisor": False,
    }


def main() -> None:
    q0 = verify_endpoint(0, 1)
    q3_completed = subprocess.run(
        [sys.executable, str(Q3_HELPER)],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=300,
    )
    if q3_completed.returncode != 0:
        raise AssertionError(
            ("q=3 helper failed", q3_completed.stdout, q3_completed.stderr)
        )
    q3 = json.loads(q3_completed.stdout)
    assert q3["verified"] is True
    assert q3["binary_survivor_on_regular_t3_divisor"] is False

    output = {
        "verified": True,
        "field": "C",
        "distinguished_coordinates": [0, 3],
        "marking_divisor": "t3=1",
        "q0": q0,
        "q3": q3,
        "whole_regular_t3_divisor_closed": True,
        "all_regular_end_coordinate_marking_divisors_closed": True,
        "dependencies": {
            END_INTERSECTION.name: sha256(END_INTERSECTION),
            Q3_HELPER.name: sha256(Q3_HELPER),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_elliptic_end_t3_divisor_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
