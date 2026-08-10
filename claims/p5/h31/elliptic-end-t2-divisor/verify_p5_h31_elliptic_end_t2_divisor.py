#!/usr/bin/env python3
"""Verify the endpoint t2=x divisor obstruction."""

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
THEOREM = ROOT / "P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md"
END_INTERSECTION = (
    REPO_ROOT / 'claims/p5/h31/elliptic-end-genus-two-exception/P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md'
)
Q3_HELPER = REPO_ROOT / 'claims/p5/h31/elliptic-end-t2-divisor-q3/verify_p5_h31_elliptic_end_t2_divisor_q3.py'
ROWS_A = (0, 1, 3, 4, 5, 6, 9)
ROWS_K = (0, 1, 3, 4, 5, 10, 9)
ROWS_T0 = (0, 1, 3, 4, 6, 7, 9)
ROWS_11 = (0, 1, 3, 4, 6, 9, 11)
ROWS_12 = (0, 1, 3, 4, 6, 9, 12)
ROWS_FINAL = (0, 1, 3, 4, 6, 8, 9)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reduce_quadratic(expression, variable, relation) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, variable),
        sp.Poly(relation, variable),
    ).as_expr()
    return sp.factor(remainder / denominator)


def dependent_factor(expression, variable) -> sp.Expr:
    numerator = sp.factor(sp.fraction(sp.cancel(expression))[0])
    factors = [
        factor
        for factor, multiplicity in sp.factor_list(numerator)[1]
        if factor.has(variable)
        for _ in range(multiplicity)
    ]
    assert len(factors) == 1
    return factors[0]


def direct_mixed_builder(
    distinguished: int,
    alpha,
    beta,
) -> sp.Matrix:
    return mixed_matrix(distinguished, alpha, beta)[0]


def verify_endpoint(
    distinguished: int,
    epsilon: int,
    mixed_builder: Callable = direct_mixed_builder,
) -> dict:
    assert (distinguished, epsilon) in ((0, 1), (3, -1))
    r, x, Y = sp.symbols("r x Y")
    t = sp.symbols("t0:4")
    t0, t1, t2, t3 = t
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
    beta = tuple(
        tuple(
            beta_zero[mode][coordinate]
            + t[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    quotient = mixed_builder(distinguished, alpha, beta)[
        :,
        [0, 2, 3, 4, 5, 6, 7],
    ]

    C = (
        -r**6
        + 2 * r**4 * x
        + 3 * r**4
        - r**2 * x**2
        + 4 * r**2 * x
        - 3 * r**2
        + x**2
        - 2 * x
        + 1
    )
    B = (
        r**8 * x
        - 5 * r**6 * x
        + 3 * r**4 * x**3
        - 10 * r**4 * x**2
        + 7 * r**4 * x
        - 3 * r**2 * x**3
        + 6 * r**2 * x**2
        - 3 * r**2 * x
    )
    L = B + epsilon * Y * C
    determinant_K = reduce_quadratic(
        quotient.subs(t2, x).extract(ROWS_K, range(7)).det(
            method="domain-ge"
        ),
        Y,
        elliptic_relation,
    )
    expected_K = (
        128
        * r**5
        * x**6
        * (r - 1)
        * (r + 1)
        * (x - 1)
        * (t3 - 1)
        * L
    )
    assert sp.factor(determinant_K - expected_K) == 0

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
    assert sp.factor(B**2 - C**2 * f) == (
        x
        * (r - 1) ** 2
        * (r + 1) ** 2
        * (x - 1)
        * D**2
        * R
    )
    Y_on_L = epsilon * r**2 * x * (x - r**2 - 1) / D
    assert sp.factor(L.subs(Y, Y_on_L)) == 2 * r**2 * x * R / D

    def interpolate_A() -> sp.Expr:
        values = {}
        for one_value in (0, 1):
            for three_value in (0, 1):
                values[one_value, three_value] = reduce_quadratic(
                    quotient.subs({
                        t1: one_value,
                        t2: x,
                        t3: three_value,
                    }).extract(ROWS_A, range(7)).det(
                        method="domain-ge"
                    ),
                    Y,
                    elliptic_relation,
                )
        return sp.factor(
            values[0, 0]
            + (values[1, 0] - values[0, 0]) * t1
            + (values[0, 1] - values[0, 0]) * t3
            + (
                values[1, 1]
                - values[1, 0]
                - values[0, 1]
                + values[0, 0]
            )
            * t1
            * t3
        )

    A_factor = dependent_factor(interpolate_A(), t1)

    s, u, v = sp.symbols("s u v")
    d = s**3 + 3 * s**2 - s + 1
    n = s**3 + 3 * s**2 + 3 * s + 5
    h = sp.expand(n * d)
    u_parameter = n / d
    x_parameter = (s + 1) ** 4 / d
    Y_parameter = (s - 1) * (s + 1) ** 3 * n / d**2
    t1_parameter = (s - 1) ** 2 * (s + 1) * (s + 3) * n / d**2
    hyperelliptic_relation = v**2 - h

    def pull_even(expression, extra=None) -> sp.Expr:
        in_u = sp.expand(expression).subs(r**2, u)
        assert not in_u.has(r)
        substitutions = {
            u: u_parameter,
            x: x_parameter,
            Y: epsilon * Y_parameter,
        }
        if extra:
            substitutions.update(extra)
        return sp.factor(in_u.subs(substitutions))

    A_on_curve = pull_even(A_factor)
    forced_t1 = epsilon * t1_parameter
    assert sp.factor(A_on_curve.subs(t1, forced_t1)) == 0
    expected_A_slope = (
        epsilon * 2 * s * (s + 1) ** 4 * n**3 / d**4
    )
    assert sp.factor(
        sp.diff(A_on_curve, t1) - expected_A_slope
    ) == 0

    def pulled_minor(rows, outside) -> sp.Expr:
        determinant = reduce_quadratic(
            quotient.subs(t2, x).extract(rows, range(7)).det(
                method="domain-ge"
            ),
            Y,
            elliptic_relation,
        )
        residual = sp.cancel(determinant / outside)
        return pull_even(residual, {t1: forced_t1})

    Phi = (
        2 * s * (s + 1) ** 4 * n * t0
        - ((s - 1) * t3 - 2 * s) * d**2
    )
    pulled_T0 = pulled_minor(
        ROWS_T0,
        -128 * r**5 * x**5,
    )
    expected_T0 = 16 * (s + 1) ** 6 * n**4 * Phi / d**9
    assert sp.factor(pulled_T0 - expected_T0) == 0
    forced_t0 = (
        ((s - 1) * t3 - 2 * s)
        * d**2
        / (2 * s * (s + 1) ** 4 * n)
    )

    L1 = s**4 + 3 * s**3 - s**2 + s + 2 * (1 - s) * t3
    L2 = s**3 + s**2 + 3 * s - 1 + 2 * (1 - s) * t3
    pulled_11 = pulled_minor(
        ROWS_11,
        -128 * r**5 * x**5,
    )
    pulled_12 = pulled_minor(
        ROWS_12,
        -128 * r**5 * t3 * x**5,
    )
    expected_11 = (
        -epsilon * 32 * (s + 1) ** 7 * n**5 * L1 / d**9
    )
    expected_12 = (
        -epsilon * 32 * (s + 1) ** 7 * n**5 * L2 / d**9
    )
    assert sp.factor(pulled_11 - expected_11) == 0
    assert sp.factor(pulled_12 - expected_12) == 0

    resultant = sp.factor(sp.resultant(L1, t3 * L2, t3))
    expected_resultant = (
        -2
        * s
        * (s - 1) ** 2
        * (s + 1)
        * (s**2 + 2 * s - 1)
        * d
    )
    assert sp.factor(resultant - expected_resultant) == 0
    assert sp.factor(L1.subs(s, 1)) == 4
    assert sp.factor((t3 * L2).subs(s, 1)) == 4 * t3
    assert sp.factor(L1.subs({s: 0, t3: 0})) == 0
    assert sp.factor(L2.subs({s: 0, t3: 0})) == -1

    quadratic_exception = s**2 + 2 * s - 1
    assert sp.rem(
        sp.Poly(L1.subs(t3, -s), s),
        sp.Poly(quadratic_exception, s),
    ).as_expr() == 0
    assert sp.rem(
        sp.Poly(L2.subs(t3, -s), s),
        sp.Poly(quadratic_exception, s),
    ).as_expr() == 0

    determinant_final = reduce_quadratic(
        quotient.subs(t2, x).extract(ROWS_FINAL, range(7)).det(
            method="domain-ge"
        ),
        Y,
        elliptic_relation,
    )
    final_substitution = {
        r: v / d,
        x: x_parameter,
        Y: epsilon * Y_parameter,
        t1: forced_t1,
        t0: forced_t0.subs(t3, -s),
        t3: -s,
    }
    final_on_curve = reduce_quadratic(
        determinant_final.subs(final_substitution),
        v,
        hyperelliptic_relation,
    )
    final_numerator = sp.fraction(sp.cancel(final_on_curve))[0]
    final_remainder = sp.factor(sp.rem(
        sp.Poly(final_numerator, s),
        sp.Poly(quadratic_exception, s),
    ).as_expr())
    assert final_remainder == -2**34 * v * (12 * s + 29)
    assert sp.gcd(quadratic_exception, 12 * s + 29) == 1

    return {
        "distinguished_coordinate": distinguished,
        "epsilon": epsilon,
        "genus_two_sheet": f"Y={epsilon}*Y_parameter",
        "forced_t1_sign": epsilon,
        "forced_t0": str(forced_t0),
        "residual_resultant": str(expected_resultant),
        "quadratic_exception_closed": True,
        "binary_survivor_on_regular_t2_divisor": False,
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
        timeout=180,
    )
    if q3_completed.returncode != 0:
        raise AssertionError(
            ("q=3 helper failed", q3_completed.stdout, q3_completed.stderr)
        )
    q3 = json.loads(q3_completed.stdout)
    assert q3["verified"] is True
    assert q3["binary_survivor_on_regular_t2_divisor"] is False

    output = {
        "verified": True,
        "field": "C",
        "distinguished_coordinates": [0, 3],
        "marking_divisor": "t2=x",
        "q0": q0,
        "q3": q3,
        "whole_regular_t2_divisor_closed": True,
        "whole_t3_divisor_closed": False,
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
        REPO_ROOT / 'tmp/p5_h31_elliptic_end_t2_divisor_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
