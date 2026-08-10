#!/usr/bin/env python3
"""Independent DP-permanent audit of the q=0,3 genus-two obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_h31_elliptic_end_genus_two_exception.py"
Q3_AUDIT = ROOT / "audit_p5_h31_elliptic_end_genus_two_q3.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
ROWS_A = (0, 1, 3, 4, 5, 6, 9)
ROWS_C = (0, 1, 3, 5, 6, 9, 13)
ROWS_11 = (0, 1, 3, 4, 6, 9, 11)
ROWS_12 = (0, 1, 3, 4, 6, 9, 12)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows) -> sp.Expr:
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                next_states[next_mask] = (
                    next_states.get(next_mask, sp.Integer(0))
                    + coefficient * entry
                )
        states = next_states
    return sp.expand(states[15])


def mixed_system(distinguished, alpha, beta):
    extension = sp.symbols("a0:4") + sp.symbols("b0:4")
    common = tuple(
        coordinate
        for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_extended = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extension[mode],)
        for mode, row in enumerate(alpha)
    )
    beta_extended = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode, row in enumerate(beta)
    )
    coefficients = {
        word: permanent_dp(tuple(
            beta_extended[mode] if word[mode] else alpha_extended[mode]
            for mode in range(4)
        ))
        for word in WORDS
    }
    return sp.Matrix([
        [sp.diff(coefficients[word], variable) for variable in extension]
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])


def reduce_quadratic(expression, variable, relation):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    return sp.factor(
        sp.rem(
            sp.Poly(numerator, variable),
            sp.Poly(relation, variable),
        ).as_expr()
        / denominator
    )


def dependent_factor(expression, variable):
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
    quotient = mixed_system(0, alpha, beta)[
        :,
        [0, 2, 3, 4, 5, 6, 7],
    ]
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
    expected_compatibility = reduce_quadratic(
        -(r - 1) * (r + 1) * (Y - x**2 + x) * J,
        Y,
        elliptic_relation,
    )
    assert sp.factor(compatibility - expected_compatibility) == 0

    s, v = sp.symbols("s v")
    d = s**3 + 3 * s**2 - s + 1
    n = s**3 + 3 * s**2 + 3 * s + 5
    h = sp.expand(n * d)
    x_parameter = (s + 1) ** 4 / d
    Y_parameter = (s - 1) * (s + 1) ** 3 * n / d**2
    t1_parameter = (s - 1) ** 2 * (s + 1) * (s + 3) * n / d**2
    t0_parameter = -d**2 / (2 * s * (s + 1) ** 3 * n)
    substitution = {
        r: v / d,
        x: x_parameter,
        Y: Y_parameter,
        t0: t0_parameter,
        t1: t1_parameter,
        t2: x_parameter,
        t3: 1,
    }
    relation = v**2 - h
    determinant_11 = reduce_quadratic(
        quotient.extract(ROWS_11, range(7)).det(
            method="domain-ge"
        ).subs(substitution),
        v,
        relation,
    )
    determinant_12 = reduce_quadratic(
        quotient.extract(ROWS_12, range(7)).det(
            method="domain-ge"
        ).subs(substitution),
        v,
        relation,
    )
    cubic = s**3 + 2 * s**2 - 3 * s + 2
    quadratic = s**2 + 1
    common = 4096 * v * (s + 1) ** 28 * n**7 / d**17
    assert sp.factor(determinant_11 - common * cubic) == 0
    assert sp.factor(determinant_12 - common * quadratic) == 0
    assert sp.gcd(cubic, quadratic) == 1
    assert sp.factor(sp.discriminant(h, s)) == 2**24 * 3**3 * 11

    q3_completed = subprocess.run(
        [sys.executable, str(Q3_AUDIT)],
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
            (
                "independent q=3 audit failed",
                q3_completed.stdout,
                q3_completed.stderr,
            )
        )
    q3_output = json.loads(q3_completed.stdout)
    assert q3_output["audited"] is True
    assert q3_output["coprime_full_rank_minors_verified"] is True

    completed = subprocess.run(
        [sys.executable, str(PRIMARY)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=240,
    )
    if completed.returncode != 0:
        raise AssertionError(
            ("primary verifier failed", completed.stdout, completed.stderr)
        )
    primary_output = json.loads(completed.stdout)
    assert primary_output["verified"] is True
    assert primary_output[
        "binary_survivor_on_regular_genus_two_charts"
    ] == {"q0": False, "q3": False}

    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        "distinguished_coordinates": [0, 3],
        "genus_two_normalization_verified": True,
        "coprime_full_rank_minors_verified": {
            "q0": True,
            "q3": True,
        },
        "primary_replay_verified": True,
        "whole_marking_divisors_closed": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "q3_audit": Q3_AUDIT.name,
        "q3_audit_sha256": sha256(Q3_AUDIT),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp"
        / "p5_h31_elliptic_end_genus_two_exception_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
