#!/usr/bin/env python3
"""Verify the regular middle-coordinate pivot-complement obstruction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

import sympy as sp

import sys

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
THEOREM = (
    ROOT / "P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md"
)
DENSE = REPO_ROOT / 'claims/p5/h31/elliptic-middle-coordinate-rank-drop/P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md'
ROWS_0 = (0, 1, 2, 3, 4, 5, 9)
ROWS_F = (0, 1, 2, 3, 4, 6, 9)
ROWS_L = (0, 1, 2, 3, 5, 6, 9)
ROWS_H = (0, 1, 2, 3, 5, 7, 9)
ROWS_4 = (0, 1, 2, 3, 5, 9, 11)
ROWS_5 = (0, 1, 2, 3, 6, 7, 9)
ROWS_6 = (0, 1, 2, 3, 6, 9, 11)
ROWS_7 = (0, 1, 2, 3, 5, 9, 10)
ROWS_8 = (0, 1, 2, 3, 6, 9, 10)
ROWS_Y0 = (0, 3, 4, 5, 6, 11, 13)
ROWS_Y1 = (2, 3, 4, 5, 6, 11, 13)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reduce_quadratic(expression, variable, relation) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    remainder = sp.rem(
        sp.Poly(numerator, variable),
        sp.Poly(relation, variable),
    ).as_expr()
    return sp.factor(remainder / denominator)


def direct_system_builder(distinguished, alpha, beta):
    return mixed_matrix(distinguished, alpha, beta)


def verify_middle(
    distinguished: int,
    sigma: int,
    system_builder: Callable = direct_system_builder,
) -> dict:
    assert (distinguished, sigma) in ((1, -1), (2, 1))
    r, x, Y = sp.symbols("r x Y")
    t0, t1, t2, t3 = sp.symbols("t0:4")
    D = x + r**2 - 1
    f = x * (
        (1 - r**2) * x**2
        + (3 * r**2 - 2) * x
        + (r**2 - 1) ** 2
    )
    relation = Y**2 - f
    Q = (
        -r**4
        + r**2 * x**2
        - 3 * r**2 * x
        + 2 * r**2
        - x**2
        + 2 * x
        - 1
    )
    assert sp.factor(Q + f / x) == 0
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
    mixed, _diagonal_a, _diagonal_b = system_builder(
        distinguished,
        alpha,
        beta,
    )
    quotient = mixed[:, [0, 1, 3, 4, 5, 6, 7]]

    cache = {}

    def determinant(rows) -> sp.Expr:
        if rows not in cache:
            cache[rows] = reduce_quadratic(
                quotient.extract(rows, range(7)).det(method="domain-ge"),
                Y,
                relation,
            )
        return cache[rows]

    F = (
        (x - 1) * (r**3 - r + sigma)
        + sigma * r**2 * (x + 1)
    )
    L = Y * r**2 * D + t1 * Q
    G = t3 * F + (r - sigma) * D
    A = (
        2 * sigma * r**2 * x
        + r * t2
        + r * x**2
        - r * x
        - sigma * t2
        + sigma * x**2
        - sigma * x
    )
    H = (
        r**4 * t0 * x**2
        + sigma * r**3 * t0 * x**2
        + r**2 * t0 * x**3
        - r**2 * t0 * x**2
        - r**2 * t3 * x
        + r**2 * x
        + sigma * r * t0 * x**3
        - sigma * r * t0 * x**2
        + t2 * t3
        - t2
    )
    outside_0 = (
        128
        * r**3
        * t3
        * x**5
        * (r + sigma) ** 2
        * (x - 1)
        * D**2
        * Q
    )
    assert sp.factor(determinant(ROWS_0) - outside_0 * F * L) == 0
    assert sp.factor(determinant(ROWS_F) - outside_0 * L * G) == 0

    outside_L = (
        128
        * r**3
        * x**4
        * (r + sigma) ** 2
        * (x - 1)
        * D**3
        * Q
    )
    B = sp.factor(sp.cancel(determinant(ROWS_L) / (outside_L * A)))
    assert sp.degree(sp.fraction(B)[0], t1) == 1
    t1_L = r**2 * D * x / Y
    B_on_L = reduce_quadratic(
        B.subs(t1, t1_L),
        Y,
        relation,
    )
    assert sp.factor(
        B_on_L
        - x * (r - sigma) * (x - 1) * Q * G / Y
    ) == 0

    outside_H = (
        128
        * r**2
        * x**3
        * (r + sigma)
        * (x - 1)
        * D
        * Q**2
        * F
    )
    assert sp.factor(determinant(ROWS_H) - outside_H * H) == 0
    assert sp.factor(A.subs(t2, r**2 * x)) == x * (r + sigma) * D
    assert sp.factor(G.subs(t3, 1)) == r**2 * x * (r + sigma)
    assert sp.factor(
        H.subs(t0, 0) - (t3 - 1) * (t2 - r**2 * x)
    ) == 0
    assert sp.factor(
        H.subs({t2: r**2 * x, t3: 0})
        - r * t0 * x**2 * (r + sigma) * D
    ) == 0

    a = r**3 + sigma * r**2 - r + sigma
    b = r**3 + 3 * sigma * r**2 + 3 * r + 3 * sigma
    constant_F = sp.expand(F).subs(x, 0)
    assert sp.resultant(a, constant_F, r) == 8 * sigma
    x_F = (r + sigma) * (r - sigma) ** 2 / a
    assert sp.factor(F.subs(x, x_F)) == 0
    f_F = sp.factor(f.subs(x, x_F))
    assert f_F == (
        r**4
        * (r + sigma) ** 2
        * (r - sigma) ** 4
        * b
        / a**3
    )
    relation_F = Y**2 - f_F
    t2_A = sp.factor(sp.solve(A, t2)[0])
    B0 = sp.factor(B.subs(t3, 0))
    t1_B0 = sp.factor(sp.solve(B0, t1)[0])
    C = (
        r**5
        - sigma * r**4
        - r**3 * t2
        - r**3
        - sigma * r**2 * t2
        + sigma * r**2
        + r * t2
        - sigma * t2
    )
    t2_C = sp.factor(sp.solve(C, t2)[0])

    def specialized(
        rows,
        substitutions,
        on_F=False,
    ) -> sp.Expr:
        matrix = quotient.subs(substitutions)
        active_relation = relation
        if on_F:
            matrix = matrix.subs(x, x_F)
            active_relation = relation_F
        value = matrix.extract(rows, range(7)).det(method="domain-ge")
        return reduce_quadratic(value, Y, active_relation)

    unit_AF = specialized(
        ROWS_5,
        {t0: 0, t3: 0, t2: t2_A},
        on_F=True,
    )
    expected_AF = (
        -256
        * sigma
        * r**18
        * (r + sigma) ** 14
        * (r - sigma) ** 15
        * b**2
        / a**12
    )
    assert sp.factor(unit_AF - expected_AF) == 0

    B_F = specialized(
        ROWS_5,
        {t0: 0, t3: 0, t1: t1_B0},
        on_F=True,
    )
    expected_B_F = (
        -256
        * sigma
        * r**16
        * (r + sigma) ** 10
        * (r - sigma) ** 13
        * b**2
        * C
        / a**11
    )
    assert sp.factor(B_F - expected_B_F) == 0

    unit_BFC = specialized(
        ROWS_8,
        {t0: 0, t3: 0, t1: t1_B0, t2: t2_C},
        on_F=True,
    )
    expected_BFC = (
        -256
        * sigma
        * r**19
        * (r + sigma) ** 15
        * (r - sigma) ** 18
        * b**2
        / a**13
    )
    assert sp.factor(unit_BFC - expected_BFC) == 0

    B_t2 = specialized(
        ROWS_7,
        {t0: 0, t3: 0, t1: t1_B0, t2: r**2 * x},
    )
    expected_B_t2 = (
        128
        * r**3
        * x**5
        * (r + sigma) ** 2
        * (x - 1)
        * D**2
        * Q**2
        * F
    )
    assert sp.factor(B_t2 - expected_B_t2) == 0
    unit_B_t2_F = specialized(
        ROWS_8,
        {t0: 0, t3: 0, t1: t1_B0, t2: r**2 * x},
        on_F=True,
    )
    assert sp.factor(unit_B_t2_F - expected_BFC) == 0

    LA_F = specialized(
        ROWS_5,
        {t0: 0, t1: t1_L, t2: t2_A},
        on_F=True,
    )
    expected_LA_F = (
        256
        * sigma
        * r**18
        * (r + sigma) ** 14
        * (r - sigma) ** 15
        * (t3 - 1)
        * b**2
        / a**12
    )
    assert sp.factor(LA_F - expected_LA_F) == 0

    LA_t3 = specialized(
        ROWS_4,
        {t0: 0, t3: 1, t1: t1_L, t2: t2_A},
    )
    expected_LA_t3 = (
        128
        * r**3
        * x**5
        * (r + sigma) ** 2
        * (x - 1)
        * D**3
        * Q**2
        * F
        / Y
    )
    assert reduce_quadratic(
        LA_t3 - expected_LA_t3,
        Y,
        relation,
    ) == 0

    unit_LAF_t3 = specialized(
        ROWS_6,
        {t0: 0, t3: 1, t1: t1_L, t2: t2_A},
        on_F=True,
    )
    expected_LAF_t3 = (
        -256
        * sigma
        * r**21
        * (r + sigma) ** 17
        * (r - sigma) ** 19
        * b**2
        / (Y * a**14)
    )
    assert reduce_quadratic(
        unit_LAF_t3 - expected_LAF_t3,
        Y,
        relation_F,
    ) == 0

    t3_LAF = specialized(
        ROWS_5,
        {t3: 1, t1: t1_L, t2: t2_A},
        on_F=True,
    )
    expected_t3_LAF = (
        -256
        * sigma
        * r**19
        * t0
        * (r + sigma) ** 15
        * (r - sigma) ** 18
        * b**2
        / a**13
    )
    assert sp.factor(t3_LAF - expected_t3_LAF) == 0

    t3_G = sp.factor(sp.solve(G, t3)[0])
    unit_LG_t2 = specialized(
        ROWS_7,
        {t0: 0, t1: t1_L, t2: r**2 * x, t3: t3_G},
    )
    expected_LG_t2 = (
        128
        * r**5
        * x**6
        * (r + sigma) ** 3
        * (x - 1)
        * D**2
        * Q**2
    )
    assert sp.factor(unit_LG_t2 - expected_LG_t2) == 0

    # The regular Y=0 bisection has its own two-minor full-rank pivot.
    y0_first = sp.factor(
        quotient.subs(Y, 0)
        .extract(ROWS_Y0, range(7))
        .det(method="domain-ge")
    )
    expected_y0_first = (
        -384
        * r**11
        * t3
        * x**6
        * (r + sigma)
        * (x - 1) ** 2
        * (x - 1 + sigma * r)
        * D**4
    )
    assert sp.factor(y0_first - expected_y0_first) == 0
    y0_second = sp.factor(
        quotient.subs({Y: 0, t3: 0})
        .extract(ROWS_Y1, range(7))
        .det(method="domain-ge")
    )
    expected_y0_second = (
        384
        * sigma
        * r**10
        * x**7
        * (r + sigma)
        * (x - 1) ** 3
        * (x - 1 + sigma * r)
        * D**4
    )
    assert sp.factor(y0_second - expected_y0_second) == 0

    return {
        "distinguished_coordinate": distinguished,
        "sigma": sigma,
        "regular_marking_divisors_closed": [
            "t0=0",
            "t3=1",
            "t2=r^2*x",
        ],
        "regular_two_torsion_slice_closed": True,
        "auxiliary_F_curve_is_not_a_survivor": True,
        "binary_survivor_on_regular_middle_chart": False,
    }


def main() -> None:
    cases = {
        "1": verify_middle(1, -1),
        "2": verify_middle(2, 1),
    }
    output = {
        "verified": True,
        "field": "C",
        "distinguished_coordinates": [1, 2],
        "cases": cases,
        "whole_regular_middle_pivot_complement_closed": True,
        "all_regular_elliptic_marked_fibres_closed": True,
        "dependencies": {DENSE.name: sha256(DENSE)},
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_elliptic_middle_coordinate_pivot_complement_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
