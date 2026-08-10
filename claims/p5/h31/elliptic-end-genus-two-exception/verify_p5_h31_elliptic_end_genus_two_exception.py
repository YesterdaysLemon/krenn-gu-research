#!/usr/bin/env python3
"""Verify the genus-two q=0,3 exception-curve obstruction."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import mixed_matrix


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md"
END_CHART = ROOT / "P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md"
Q3_HELPER = ROOT / "verify_p5_h31_elliptic_end_genus_two_q3.py"
ROWS_A = (0, 1, 3, 4, 5, 6, 9)
ROWS_C = (0, 1, 3, 5, 6, 9, 13)
ROWS_T0 = (0, 1, 3, 4, 6, 7, 9)
ROWS_11 = (0, 1, 3, 4, 6, 9, 11)
ROWS_12 = (0, 1, 3, 4, 6, 9, 12)


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


def main() -> None:
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
    mixed = mixed_matrix(0, alpha, beta)[0]
    quotient = mixed[:, [0, 2, 3, 4, 5, 6, 7]]
    deepest = quotient.subs({t2: x, t3: 1})

    factors = {}
    for name, rows in (("A", ROWS_A), ("C", ROWS_C)):
        determinant = reduce_quadratic(
            deepest.extract(rows, range(7)).det(method="domain-ge"),
            Y,
            elliptic_relation,
        )
        factors[name] = dependent_factor(determinant, t1)
    compatibility = reduce_quadratic(
        sp.diff(factors["A"], t1) * factors["C"].subs(t1, 0)
        - sp.diff(factors["C"], t1) * factors["A"].subs(t1, 0),
        Y,
        elliptic_relation,
    )
    J = Y * D - r**2 * x * (x - r**2 - 1)
    b2_universal = Y - x**2 + x
    expected_compatibility = reduce_quadratic(
        -(r - 1) * (r + 1) * b2_universal * J,
        Y,
        elliptic_relation,
    )
    assert sp.factor(compatibility - expected_compatibility) == 0

    assert sp.factor((x**2 - x) ** 2 - f) == (
        x * (x - 1 - r) * (x - 1 + r) * D
    )

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
    Y_on_J = r**2 * x * (x - r**2 - 1) / D
    assert sp.factor(Y_on_J**2 - f) == x * (x - 1) * R / D**2

    # The A-minor forces t1 on the residual component.
    t1_solution = sp.factor(
        -factors["A"].subs({Y: Y_on_J, t1: 0})
        / sp.diff(factors["A"], t1).subs(Y, Y_on_J)
    )
    expected_t1 = (
        r**2
        * x
        * (x - r**2 - 1) ** 2
        * (x + 3 * r**2 - 1)
        / D**3
    )
    solution_numerator = sp.fraction(
        sp.cancel(t1_solution - expected_t1)
    )[0]
    assert sp.rem(
        sp.Poly(solution_numerator, x),
        sp.Poly(R, x),
    ).as_expr() == 0

    s, u, v = sp.symbols("s u v")
    d = s**3 + 3 * s**2 - s + 1
    n = s**3 + 3 * s**2 + 3 * s + 5
    u_parameter = n / d
    x_parameter = (s + 1) ** 4 / d
    Y_parameter = (s - 1) * (s + 1) ** 3 * n / d**2
    t1_parameter = (s - 1) ** 2 * (s + 1) * (s + 3) * n / d**2
    t0_parameter = -d**2 / (2 * s * (s + 1) ** 3 * n)
    R_u = sp.factor(R.subs(r**2, u))
    assert sp.factor(R_u.subs({
        u: u_parameter,
        x: x_parameter,
    })) == 0
    assert sp.factor(x_parameter - 1 - s * u_parameter) == 0
    assert sp.factor(
        expected_t1.subs({
            r**2: u_parameter,
            x: x_parameter,
        })
        - t1_parameter
    ) == 0
    assert sp.factor(
        Y_on_J.subs({
            r**2: u_parameter,
            x: x_parameter,
        })
        - Y_parameter
    ) == 0
    hyperelliptic_polynomial = sp.expand(n * d)
    assert sp.factor(sp.discriminant(hyperelliptic_polynomial, s)) == (
        2**24 * 3**3 * 11
    )

    # Work on the genus-two normalization r=v/d, v^2=nd.
    hyperelliptic_relation = v**2 - hyperelliptic_polynomial
    parameter_substitution = {
        r: v / d,
        x: x_parameter,
        Y: Y_parameter,
        t1: t1_parameter,
        t2: x_parameter,
        t3: 1,
    }
    t0_determinant = reduce_quadratic(
        quotient.extract(ROWS_T0, range(7)).det(
            method="domain-ge"
        ).subs(parameter_substitution),
        v,
        hyperelliptic_relation,
    )
    L0 = (
        2 * s**7 * t0
        + 12 * s**6 * t0
        + s**6
        + 30 * s**5 * t0
        + 6 * s**5
        + 48 * s**4 * t0
        + 7 * s**4
        + 54 * s**3 * t0
        - 4 * s**3
        + 36 * s**2 * t0
        + 7 * s**2
        + 10 * s * t0
        - 2 * s
        + 1
    )
    expected_t0_determinant = (
        -2048
        * v
        * (s + 1) ** 27
        * n**6
        * L0
        / d**17
    )
    assert sp.factor(t0_determinant - expected_t0_determinant) == 0
    assert sp.factor(sp.diff(L0, t0)) == (
        2 * s * (s + 1) ** 3 * n
    )
    assert sp.factor(L0.subs(t0, 0)) == d**2
    assert sp.factor(
        -L0.subs(t0, 0) / sp.diff(L0, t0) - t0_parameter
    ) == 0

    candidate_substitution = {
        **parameter_substitution,
        t0: t0_parameter,
    }
    determinant_11 = reduce_quadratic(
        quotient.extract(ROWS_11, range(7)).det(
            method="domain-ge"
        ).subs(candidate_substitution),
        v,
        hyperelliptic_relation,
    )
    determinant_12 = reduce_quadratic(
        quotient.extract(ROWS_12, range(7)).det(
            method="domain-ge"
        ).subs(candidate_substitution),
        v,
        hyperelliptic_relation,
    )
    cubic = s**3 + 2 * s**2 - 3 * s + 2
    quadratic = s**2 + 1
    common_factor = 4096 * v * (s + 1) ** 28 * n**7 / d**17
    assert sp.factor(determinant_11 - common_factor * cubic) == 0
    assert sp.factor(determinant_12 - common_factor * quadratic) == 0
    assert sp.gcd(cubic, quadratic) == 1

    q3_completed = subprocess.run(
        [sys.executable, str(Q3_HELPER)],
        cwd=ROOT,
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
    q3_output = json.loads(q3_completed.stdout)
    assert q3_output["verified"] is True
    assert q3_output["binary_survivor_on_regular_genus_two_chart"] is False

    output = {
        "verified": True,
        "field": "C",
        "distinguished_coordinates": [0, 3],
        "marking_intersection": ["t2=x", "t3=1"],
        "apparent_exception_curve": "smooth genus-2 residual trisection",
        "residual_trace_section": "P+T",
        "forced_candidate_marking_q0": {
            "t0": str(t0_parameter),
            "t1": str(t1_parameter),
            "t2": str(x_parameter),
            "t3": "1",
        },
        "forced_candidate_marking_q3": {
            "t0": str(t0_parameter),
            "t1": str(-t1_parameter),
            "t2": str(x_parameter),
            "t3": "1",
        },
        "coprime_full_rank_minors": [str(cubic), str(quadratic)],
        "binary_survivor_on_regular_genus_two_charts": {
            "q0": False,
            "q3": False,
        },
        "whole_marking_divisors_closed": False,
        "dependencies": {
            END_CHART.name: sha256(END_CHART),
            Q3_HELPER.name: sha256(Q3_HELPER),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp"
        / "p5_h31_elliptic_end_genus_two_exception_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
