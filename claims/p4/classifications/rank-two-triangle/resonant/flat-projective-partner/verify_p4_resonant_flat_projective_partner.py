#!/usr/bin/env python3
"""Exact replay of the Borel-generic projective-partner classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def triple(*rows: sp.Matrix) -> sp.Matrix:
    values = []
    for omitted in range(4):
        columns = [index for index in range(4) if index != omitted]
        values.append(
            sp.expand(
                sum(
                    sp.prod(rows[index][columns[permutation[index]]] for index in range(3))
                    for permutation in itertools.permutations(range(3))
                )
            )
        )
    return sp.Matrix(values)


def minors(matrix: sp.Matrix, size: int) -> list[sp.Expr]:
    return [
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    ]


def coefficient_matrix(
    y: sp.Matrix,
    x: sp.Matrix,
    y2: sp.Matrix,
    x2: sp.Matrix,
    y3: sp.Matrix,
    x3: sp.Matrix,
) -> sp.Matrix:
    return sp.Matrix.hstack(
        triple(y, y2, y3),
        triple(x, y2, y3),
        triple(y, x2, x3),
        triple(x, x2, x3),
    )


def main() -> None:
    p, q, u = sp.symbols("p q u")
    y = sp.ones(4, 1)
    x = sp.Matrix((0, 1, p, q))
    sharp_y = sp.Matrix((0, p + q - 1, p * (1 - p + q), q * (1 + p - q)))
    sharp_x = p * q * sp.Matrix((-1, 1, 1, 1))
    finite_y, finite_x = y + u * sharp_y, x + u * sharp_x

    assert pair(y, sharp_x) == pair(x, sharp_y)
    assert pair(sharp_y, finite_x) == pair(sharp_x, finite_y)

    # One synchronized partner is [A^#] and the other is [A+u A^#].
    C = coefficient_matrix(y, x, sharp_y, sharp_x, finite_y, finite_x)
    triples4 = tuple(itertools.combinations(range(4), 3))
    H = p**2 - 2 * p * q - 2 * p + q**2 - 2 * q + 1
    G = p * q * H * u**2 - 6 * p * q * u - p - q - 1
    A0 = (p - q + 1) * (q * (p - q + 1) * u + 1)
    A1 = (p - q - 1) * (p * (p - q - 1) * u - 1)
    A2 = (p + q - 1) * ((p + q - 1) * u + 1)

    compression = [sp.factor(C.extract(rows, (0, 1, 2)).det()) for rows in triples4]
    expected_compression = [
        8 * p**2 * q**2 * (p - 1) * A0 * G,
        8 * p**2 * q**2 * (q - 1) * A1 * G,
        -8 * p**2 * q**2 * (p - q) * A2 * G,
        0,
    ]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(compression, expected_compression)
    )

    compound = minors(C, 3)
    divisor = sp.Poly(G, p, q, u)
    assert all(sp.div(sp.Poly(value, p, q, u), divisor)[1].is_zero for value in compound)

    first_three = C[:, :3]
    first_two = minors(first_three, 2)
    selected_first_two = (
        -4 * p * q * (p - 1) * A0,
        -4 * p * q * (q - 1) * A1,
        4 * p * q * (p - q) * A2,
    )
    assert all(sp.factor(value) in first_two for value in selected_first_two)

    # A0=A1=A2=0 is the union of eight factor choices.  Exact Groebner
    # bases leave one excluded collision, three rational curves, and four
    # empty choices.  G reduces to zero on every choice.
    outer = (p - q + 1, p - q - 1, p + q - 1)
    inner = (
        q * (p - q + 1) * u + 1,
        p * (p - q - 1) * u - 1,
        (p + q - 1) * u + 1,
    )
    expected_bases = {
        0: {u + 1, q - 1, p - 1},
        1: {2 * u * p + 1, q - p - 1},
        2: {2 * u * p - 2 * u + 1, q - p + 1},
        3: {sp.Integer(1)},
        4: {2 * u * p**2 - 2 * u * p - 1, q + p - 1},
        5: {sp.Integer(1)},
        6: {sp.Integer(1)},
        7: {sp.Integer(1)},
    }
    branch_bases = {}
    for mask in range(8):
        equations = [outer[index] if mask & (1 << index) else inner[index] for index in range(3)]
        basis = sp.groebner(equations, u, q, p)
        expressions = {sp.expand(poly.as_expr()) for poly in basis.polys}
        assert expressions == {sp.expand(value) for value in expected_bases[mask]}
        assert sp.expand(basis.reduce(G)[1]) == 0
        branch_bases[mask] = expressions

    curves = {
        "03|12": ({q: p + 1, u: -1 / (2 * p)}, p, -2 * p**2 * (p - 1) * (p + 1)),
        "02|13": ({p: q + 1, u: -1 / (2 * q)}, q, -2 * q**2 * (q - 1) * (q + 1)),
        "01|23": (
            {p: 1 - q, u: 1 / (2 * q * (q - 1))},
            q,
            -2 * q**2 * (q - 1) ** 2 * (2 * q - 1),
        ),
    }
    curve_ranks = {}
    partner_pair = sp.Matrix.hstack(
        pair(sharp_y, finite_y),
        pair(sharp_y, finite_x),
        pair(sharp_x, finite_y),
        pair(sharp_x, finite_x),
    )
    for label, (substitution, parameter, pair_minor) in curves.items():
        specialized_C = sp.simplify(C.subs(substitution))
        specialized_first = specialized_C[:, :3]
        specialized_pair = sp.simplify(partner_pair.subs(substitution))
        assert all(value == 0 for value in minors(specialized_first, 2))
        assert all(value == 0 for value in minors(specialized_C, 3))
        assert any(value != 0 for value in minors(specialized_C, 2))
        assert all(value == 0 for value in minors(specialized_pair, 3))
        assert sp.factor(pair_minor) in minors(specialized_pair, 2)
        curve_ranks[label] = {
            "parameter": str(parameter),
            "compressed_rank": 1,
            "full_rank": 2,
            "partner_pair_rank": 2,
        }

    # Both partners at infinity: compression forces H=0; then all full
    # 3-minors vanish, but two selected compressed 2-minors would force
    # p-q=-1 and p-q=+1 simultaneously.
    C_double = coefficient_matrix(y, x, sharp_y, sharp_x, sharp_y, sharp_x)
    double_compression = [
        sp.factor(C_double.extract(rows, (0, 1, 2)).det()) for rows in triples4
    ]
    expected_double = [
        8 * p**3 * q**4 * (p - 1) * (p - q + 1) ** 2 * H,
        8 * p**4 * q**3 * (q - 1) * (p - q - 1) ** 2 * H,
        -8 * p**3 * q**3 * (p - q) * (p + q - 1) ** 2 * H,
        0,
    ]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(double_compression, expected_double)
    )
    Hpoly = sp.Poly(H, p, q)
    assert all(
        sp.div(sp.Poly(value, p, q), Hpoly)[1].is_zero
        for value in minors(C_double, 3)
    )
    double_first_two = minors(C_double[:, :3], 2)
    incompatible = (
        4 * p**2 * q**3 * (p - 1) * (p - q + 1) ** 2,
        4 * p**3 * q**2 * (q - 1) * (p - q - 1) ** 2,
    )
    assert all(sp.factor(value) in double_first_two for value in incompatible)

    result = {
        "chart": "full kernel support and four distinct affine ratios",
        "finite_finite_sheet": "excluded by the companion generic theorem",
        "one_infinity_pure_curves": curve_ranks,
        "additive_interpretation": "one repeated disjoint pair sum among {0,1,p,q}",
        "triangle_interpretation": "every pure curve has partner pair-image rank two",
        "double_infinity_sheet": "empty",
        "conclusion": "the complete projective-partner sheet is empty in the rank-three-relation triangle stratum",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
