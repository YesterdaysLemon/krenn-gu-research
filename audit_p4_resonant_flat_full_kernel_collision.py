#!/usr/bin/env python3
"""Independent subset-product audit of the full-kernel collision theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def squarefree_product(rows: tuple[sp.Matrix, ...]) -> sp.Matrix:
    degree = len(rows)
    values = []
    for support in itertools.combinations(range(4), degree):
        states = {0: sp.Integer(1)}
        for row in rows:
            next_states = {}
            for mask, coefficient in states.items():
                for local, source in enumerate(support):
                    if not mask & (1 << local):
                        target = mask | (1 << local)
                        next_states[target] = next_states.get(target, 0) + coefficient * row[source]
            states = next_states
        values.append(sp.expand(states[(1 << degree) - 1]))
    return sp.Matrix(list(reversed(values))) if degree == 3 else sp.Matrix(values)


def build_C(planes: tuple[tuple[sp.Matrix, sp.Matrix], ...]) -> sp.Matrix:
    (y, x), (y2, x2), (y3, x3) = planes
    return sp.Matrix.hstack(
        squarefree_product((y, y2, y3)),
        squarefree_product((x, y2, y3)),
        squarefree_product((y, x2, x3)),
        squarefree_product((x, x2, x3)),
    )


def build_pair(left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]) -> sp.Matrix:
    return sp.Matrix.hstack(
        *[squarefree_product((a, b)) for a in left for b in right]
    )


def all_minors(matrix: sp.Matrix, size: int) -> list[sp.Expr]:
    return [
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    ]


def main() -> None:
    R, S, T, U = sp.symbols("R S T U")
    y = sp.ones(4, 1)
    x = sp.Matrix((0, 0, 1, 1))
    dy = sp.Matrix((-S, S, -R, R))
    dx = sp.Matrix((-S, S, 0, 0))
    second = (y + T * dy, x + T * dx)
    third = (y + U * dy, x + U * dx)
    C = build_C(((y, x), second, third))

    triples = tuple(itertools.combinations(range(4), 3))
    compression = [sp.factor(C.extract(rows, (0, 1, 2)).det()) for rows in triples]
    assert all(value.has(T + U) or sp.factor(value / (T + U)).is_polynomial() for value in compression)
    assert sp.factor(C.det()) == -64 * R * S * (T + U) ** 2

    opposite = C.subs(U, -T)
    assert all(value == 0 for value in all_minors(opposite, 3))
    first_two = all_minors(opposite[:, :3], 2)
    assert sp.factor(4 * (S * T - 1) * (S * T + 1)) in first_two
    assert sp.factor(4 * (R**2 * S**2 * T**4 + 2 * S**2 * T**2 - 3)) in first_two

    seam = {}
    for epsilon in (-1, 1):
        for eta in (-1, 1):
            substitution = {R: epsilon, S: eta, T: 1, U: -1}
            specialized = C.subs(substitution)
            partner_pair = build_pair(
                (second[0].subs(substitution), second[1].subs(substitution)),
                (third[0].subs(substitution), third[1].subs(substitution)),
            )
            assert all(value == 0 for value in all_minors(specialized[:, :3], 2))
            assert any(value != 0 for value in all_minors(specialized, 2))
            assert all(value == 0 for value in all_minors(partner_pair, 3))
            assert any(value != 0 for value in all_minors(partner_pair, 2))
            seam[f"{epsilon},{eta}"] = "pure (1,2), partner pair rank 2"

    one_infinity = build_C(((y, x), (dy, dx), (y + U * dy, x + U * dx)))
    double_infinity = build_C(((y, x), (dy, dx), (dy, dx)))
    assert all(value == 0 for value in all_minors(one_infinity, 3))
    assert 8 * R**2 * S * U in all_minors(one_infinity[:, :3], 2)
    assert sp.factor(4 * R * S * (R * S * U**2 - 1)) in all_minors(one_infinity[:, :3], 2)
    assert all(value == 0 for value in all_minors(double_infinity, 3))
    assert 4 * R**2 * S**2 in all_minors(double_infinity[:, :3], 2)

    x211 = sp.Matrix((0, 0, 1, sp.Symbol("L")))
    x31 = sp.Matrix((0, 0, 0, 1))
    assert squarefree_product((x211, x211, x211)) == sp.zeros(4, 1)
    assert squarefree_product((x31, x31, x31)) == sp.zeros(4, 1)

    result = {
        "independent_product": "subset dynamic programming",
        "2+2_pure_seam": seam,
        "projective_endpoints": "compressed/full ranks incompatible",
        "2+1+1_and_3+1": "active cubes vanish",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
