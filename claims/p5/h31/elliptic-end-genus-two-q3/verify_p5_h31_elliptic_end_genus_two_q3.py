#!/usr/bin/env python3
"""Verify the q=3 conjugate of the endpoint genus-two obstruction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/elliptic-end-genus-two-exception")

from verify_p5_h31_elliptic_end_genus_two_exception import (
    ROOT,
    ROWS_11,
    ROWS_12,
    ROWS_A,
    ROWS_C,
    ROWS_T0,
    THEOREM,
    dependent_factor,
    reduce_quadratic,
)
from krenn_gu.p5_marked_basis import mixed_matrix


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
    quotient = mixed_matrix(3, alpha, beta)[0][
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
    Y_on_J = -r**2 * x * (x - r**2 - 1) / D
    assert sp.factor(Y_on_J**2 - f) == x * (x - 1) * R / D**2
    expected_t1 = (
        -r**2
        * x
        * (x - r**2 - 1) ** 2
        * (x + 3 * r**2 - 1)
        / D**3
    )
    t1_solution = sp.factor(
        -factors["A"].subs({Y: Y_on_J, t1: 0})
        / sp.diff(factors["A"], t1).subs(Y, Y_on_J)
    )
    solution_numerator = sp.fraction(
        sp.cancel(t1_solution - expected_t1)
    )[0]
    assert sp.rem(
        sp.Poly(solution_numerator, x),
        sp.Poly(R, x),
    ).as_expr() == 0

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
        t1: t1_parameter,
        t2: x_parameter,
        t3: 1,
    }
    hyperelliptic_relation = v**2 - h
    t0_determinant = reduce_quadratic(
        quotient.extract(ROWS_T0, range(7)).det(
            method="domain-ge"
        ).subs(substitution),
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
        -2048 * v * (s + 1) ** 27 * n**6 * L0 / d**17
    )
    assert sp.factor(t0_determinant - expected_t0_determinant) == 0
    assert sp.factor(
        -L0.subs(t0, 0) / sp.diff(L0, t0) - t0_parameter
    ) == 0

    candidate = {**substitution, t0: t0_parameter}
    determinant_11 = reduce_quadratic(
        quotient.extract(ROWS_11, range(7)).det(
            method="domain-ge"
        ).subs(candidate),
        v,
        hyperelliptic_relation,
    )
    determinant_12 = reduce_quadratic(
        quotient.extract(ROWS_12, range(7)).det(
            method="domain-ge"
        ).subs(candidate),
        v,
        hyperelliptic_relation,
    )
    cubic = s**3 + 2 * s**2 - 3 * s + 2
    quadratic = s**2 + 1
    common = 4096 * v * (s + 1) ** 28 * n**7 / d**17
    assert sp.factor(determinant_11 + common * cubic) == 0
    assert sp.factor(determinant_12 + common * quadratic) == 0
    assert sp.gcd(cubic, quadratic) == 1

    output = {
        "verified": True,
        "field": "C",
        "distinguished_coordinate": 3,
        "elliptic_conjugate_of_q0": True,
        "forced_t1_sign": -1,
        "forced_t0_sign": 1,
        "binary_survivor_on_regular_genus_two_chart": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_elliptic_end_genus_two_q3_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
