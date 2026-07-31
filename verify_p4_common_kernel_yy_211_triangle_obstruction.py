#!/usr/bin/env python3
"""Verify the dense common-kernel YY (2,1,1) triangle obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


MASKS3 = (14, 13, 11, 7)


def squarefree_multiply(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return result


def linear(values: tuple[sp.Expr, ...]) -> dict[int, sp.Expr]:
    return {1 << index: value for index, value in enumerate(values) if value != 0}


def product(*rows: tuple[sp.Expr, ...]) -> dict[int, sp.Expr]:
    value: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        value = squarefree_multiply(value, linear(row))
    return value


def covector(*rows: tuple[sp.Expr, ...]) -> sp.Matrix:
    value = product(*rows)
    return sp.Matrix([sp.expand(value.get(mask, 0)) for mask in MASKS3])


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(coefficient * entry) for entry in row)


def main() -> None:
    beta, r, u, v, p, q, gamma, delta = sp.symbols(
        "beta r u v p q gamma delta"
    )
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    s = (0, 0, u, v)
    t = (0, 0, p, q)
    m = add(scale(beta, c), s)
    m_r = add(m, scale(r, c))
    d = add(scale(gamma, a), scale(delta, c), t)

    assert covector(a, c, d) == sp.zeros(4, 1)
    cubics = sp.Matrix.hstack(
        covector(a, a, d),
        covector(a, m, d),
        covector(m, m_r, c),
    )
    polar = u * q + v * p
    determinant = u * q - v * p
    energy = (2 * beta + r) * polar
    minors = tuple(
        sp.factor(cubics.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(4), 3)
    )
    expected = (
        8 * q * u * v * polar,
        8 * p * u * v * polar,
        4 * determinant * (energy - 2 * gamma * u * v),
        4 * determinant * (energy + 2 * gamma * u * v),
    )
    assert all(sp.factor(left - right) == 0 for left, right in zip(minors, expected))

    # On the forced polarity sheet q=-vp/u and gamma=0, the active cubic is
    # exactly delta*C2-beta(beta+r)*C0.
    polarity = {q: -v * p / u, gamma: 0}
    C0 = covector(a, a, d).subs(polarity)
    C1 = covector(a, m, d).subs(polarity)
    C2 = covector(m, m_r, c).subs(polarity)
    active = covector(m, m_r, d).subs(polarity)
    assert C1 == sp.zeros(4, 1)
    assert all(
        sp.factor(active[index] - delta * C2[index] + beta * (beta + r) * C0[index])
        == 0
        for index in range(4)
    )
    assert sp.Matrix.hstack(C0, C2).rank() == 2
    assert sp.Matrix.hstack(C0, C2, active).rank() == 2

    print(
        json.dumps(
            {
                "status": "pass",
                "orientation": "common-kernel YY (2,1,1) triangle",
                "dense_chart": "u*v*p*q!=0",
                "polarity_invariants": {"A": str(polar), "Q": str(determinant)},
                "apolar_minors": [str(value) for value in expected],
                "forced_conditions": ["A=0", "gamma=0"],
                "active_cubic_in_kernel_rich_span": True,
                "nonzero_pure_restriction": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
