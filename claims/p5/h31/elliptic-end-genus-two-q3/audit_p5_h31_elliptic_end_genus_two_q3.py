#!/usr/bin/env python3
"""Independent DP-permanent audit of the q=3 genus-two endpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from audit_p5_h31_elliptic_end_genus_two_exception import (
    ROOT,
    ROWS_11,
    ROWS_12,
    ROWS_A,
    ROWS_C,
    THEOREM,
    dependent_factor,
    mixed_system,
    reduce_quadratic,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    quotient = mixed_system(3, alpha, beta)[
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
    J = Y * D + r**2 * x * (x - r**2 - 1)
    expected_compatibility = reduce_quadratic(
        (r - 1) * (r + 1) * (Y + x**2 - x) * J,
        Y,
        elliptic_relation,
    )
    assert sp.factor(compatibility - expected_compatibility) == 0

    s, v = sp.symbols("s v")
    d = s**3 + 3 * s**2 - s + 1
    n = s**3 + 3 * s**2 + 3 * s + 5
    h = sp.expand(n * d)
    x_parameter = (s + 1) ** 4 / d
    Y_parameter = -(s - 1) * (s + 1) ** 3 * n / d**2
    t1_parameter = -(s - 1) ** 2 * (s + 1) * (s + 3) * n / d**2
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
    assert sp.factor(determinant_11 + common * cubic) == 0
    assert sp.factor(determinant_12 + common * quadratic) == 0
    assert sp.gcd(cubic, quadratic) == 1

    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        "distinguished_coordinate": 3,
        "compatibility_divisor_verified": True,
        "coprime_full_rank_minors_verified": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp"
        / "p5_h31_elliptic_end_genus_two_q3_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
