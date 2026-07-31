#!/usr/bin/env python3
"""Verify the weighted H22 obstruction on the eleventh P4 component."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = ROOT / "P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(coefficient * entry) for entry in row)


def component_rows(
    p: sp.Symbol,
    q: sp.Symbol,
    r: sp.Symbol,
    shifts: tuple[sp.Symbol, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    radius = r + 1
    Q = 1 + q * radius
    u = add(a, scale(p, b))
    v = add(a_bar, scale(q, b))
    alpha = (
        add(scale(Q, u), scale(-p * radius, v)),
        a,
        a,
        b_bar,
    )
    canonical_beta = (
        u,
        add(a_bar, b),
        add(scale(r, a_bar), b),
        a_bar,
    )
    beta = tuple(
        tuple(
            sp.expand(
                canonical_beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def weighted_01_row(
    row: tuple[sp.Expr, ...],
    extension: sp.Expr,
    source_scales: tuple[sp.Symbol, ...],
    merge_weights: tuple[sp.Symbol, sp.Symbol],
) -> tuple[sp.Expr, ...]:
    t0, t1, t2, t3 = source_scales
    lam, mu = merge_weights
    return (
        sp.expand(lam * t0 * row[0] + mu * t1 * row[1]),
        sp.expand(t2 * row[2]),
        sp.expand(t3 * row[3]),
        extension,
    )


def main() -> None:
    p, q, r = sp.symbols("p q r")
    shifts = sp.symbols("h0:4")
    source_scales = sp.symbols("t0:4")
    merge_weights = sp.symbols("lambda mu")
    extensions = sp.symbols("x0:4")
    alpha, beta = component_rows(p, q, r, shifts)

    expected_alpha_0 = (
        1 + q * (r + 1) - p * (r + 1),
        1 + q * (r + 1) + p * (r + 1),
        p,
        p,
    )
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(alpha[0], expected_alpha_0, strict=True)
    )

    pure = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] + 4 * p * (r + 1)) == 0
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))

    weighted_alpha = tuple(
        weighted_01_row(
            alpha[mode],
            extensions[mode],
            source_scales,
            merge_weights,
        )
        for mode in range(4)
    )
    t0, t1, t2, t3 = source_scales
    lam, mu = merge_weights
    common = lam * t0 + mu * t1
    assert weighted_alpha[1] == (common, 0, 0, extensions[1])
    assert weighted_alpha[2] == (common, 0, 0, extensions[2])
    assert weighted_alpha[0][1:3] == (p * t2, p * t3)
    assert weighted_alpha[3][1:3] == (t2, -t3)

    residual_permanent = sp.expand(
        weighted_alpha[0][1] * weighted_alpha[3][2]
        + weighted_alpha[0][2] * weighted_alpha[3][1]
    )
    assert residual_permanent == 0
    all_kernel_diagonal = sp.factor(permanent(weighted_alpha))
    assert all_kernel_diagonal == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "theorem": THEOREM.name,
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "pure_coefficient": "-4*p*(r+1)",
                "merge_weights": "homogeneous (lambda:mu)",
                "source_scalings": [str(value) for value in source_scales],
                "residual_two_by_two_permanent": str(residual_permanent),
                "weighted_01_all_kernel_diagonal_identically_zero": True,
                "all_markings": True,
                "all_weighted_slopes": True,
                "generic_weighted_H22_fibre_empty": True,
                "known_components_generically_H22_closed_at_this_checkpoint": 10,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
