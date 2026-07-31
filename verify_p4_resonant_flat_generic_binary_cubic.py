#!/usr/bin/env python3
"""Exact replay of the generic flat binary-cubic obstruction."""

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
    coefficients = []
    for missing in range(4):
        columns = [index for index in range(4) if index != missing]
        coefficient = sum(
            sp.prod(rows[row][columns[permutation[row]]] for row in range(3))
            for permutation in itertools.permutations(range(3))
        )
        coefficients.append(sp.expand(coefficient))
    return sp.Matrix(coefficients)


def main() -> None:
    lam, t, u = sp.symbols("lambda t u")

    y = sp.Matrix((1, 0, 1, 1))
    x = sp.Matrix((0, 1, 1, lam))
    y_sharp = sp.Matrix((0, 1, -1, -lam))
    x_sharp = sp.Matrix((lam, 0, -lam, -lam))

    # The six synchronization equations have precisely this pencil.
    a, b, c, d, e, f, g, h = sp.symbols("a b c d e f g h")
    y_partner = sp.Matrix((a, b, c, d))
    x_partner = sp.Matrix((e, f, g, h))
    equations = pair(y, x_partner) - pair(x, y_partner)
    coefficient_matrix, _ = sp.linear_eq_to_matrix(
        list(equations), (a, b, c, d, e, f, g, h)
    )
    expected_kernel = sp.Matrix.hstack(
        sp.Matrix.vstack(y, x), sp.Matrix.vstack(y_sharp, x_sharp)
    )
    assert coefficient_matrix.rank() == 6
    assert coefficient_matrix * expected_kernel == sp.zeros(6, 2)
    assert expected_kernel.rank() == 2

    def pencil(parameter: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
        return y + parameter * y_sharp, x + parameter * x_sharp

    y1, x1 = y, x
    y2, x2 = pencil(t)
    y3, x3 = pencil(u)
    assert pair(y1, x2) == pair(x1, y2)
    assert pair(y1, x3) == pair(x1, y3)
    assert pair(y2, x3) == pair(x2, y3)

    Y = triple(y1, y2, y3)
    K = triple(x1, y2, y3)
    J = triple(y1, x2, x3)
    X = triple(x1, x2, x3)
    assert K == triple(y1, x2, y3) == triple(y1, y2, x3)
    assert J == triple(x1, y2, x3) == triple(x1, x2, y3)
    cubic = sp.Matrix.hstack(Y, K, J, X)

    displayed = 2 * sp.Matrix(
        (
            (
                -(lam * t * u + t * u - t - u),
                -(lam * t * u - 1),
                -(lam * t + lam * u - lam - 1),
                lam * (lam * t * u - lam * t - lam * u - t - u + 3),
            ),
            (
                lam * t * u - lam * t - lam * u - t - u + 3,
                -(lam * t + lam * u - lam - 1),
                -lam * (lam * t * u - 1),
                -lam**2 * (lam * t * u + t * u - t - u),
            ),
            (
                -(lam * t * u - t - u),
                1,
                lam,
                -lam**2 * (t * u - t - u),
            ),
            (
                -(t * u - t - u),
                1,
                1,
                -lam * (lam * t * u - t - u),
            ),
        )
    )
    assert sp.simplify(cubic - displayed) == sp.zeros(4)

    independent_minor = sp.factor(cubic.extract((2, 3), (1, 2)).det())
    assert sp.expand(independent_minor + 4 * (lam - 1)) == 0

    F = (
        lam**2 * t**2 * u**2
        - lam * t**2
        - 4 * lam * t * u
        + 2 * lam * t
        - lam * u**2
        + 2 * lam * u
        + 2 * t
        + 2 * u
        - 3
    )
    compression_minor = sp.factor(cubic.extract((1, 2, 3), (0, 1, 2)).det())
    assert sp.expand(compression_minor - 8 * (lam - 1) * F) == 0

    P = lam**2 * t * u + 2 * lam * t * u - 2 * lam * t - 2 * lam * u - t - u + 3
    Q = 2 * lam * t * u - lam * t - lam * u + t * u - 2 * t - 2 * u + 3
    compound_quotient = sp.Matrix(
        (
            (
                -(lam * t - 1) * (lam * u - 1),
                -lam * P,
                -lam**2 * Q,
                -lam**3 * (t - 1) * (u - 1),
            ),
            (
                -lam * (t - 1) * (u - 1),
                -lam * Q,
                -lam * P,
                -lam * (lam * t - 1) * (lam * u - 1),
            ),
            (
                0,
                lam * t * u * (lam - 1),
                lam * (lam - 1) * (t + u),
                lam * (lam - 1),
            ),
            (
                lam - 1,
                lam * (lam - 1) * (t + u),
                lam**2 * t * u * (lam - 1),
                0,
            ),
        )
    )
    triples = tuple(itertools.combinations(range(4), 3))
    compound = sp.Matrix(
        4,
        4,
        lambda row, column: sp.factor(
            cubic.extract(triples[row], triples[column]).det()
        ),
    )
    assert all(
        sp.expand(compound[row, column] - 8 * F * compound_quotient[row, column])
        == 0
        for row in range(4)
        for column in range(4)
    )

    # One projective partner: A_2=A_sharp, A_3=A+u*A_sharp.
    Y_inf = triple(y1, y_sharp, y3)
    K_inf = triple(x1, y_sharp, y3)
    J_inf = triple(y1, x_sharp, x3)
    X_inf = triple(x1, x_sharp, x3)
    assert K_inf == triple(y1, x_sharp, y3) == triple(y1, y_sharp, x3)
    assert J_inf == triple(x1, y_sharp, x3) == triple(x1, x_sharp, y3)
    cubic_inf = sp.Matrix.hstack(Y_inf, K_inf, J_inf, X_inf)
    displayed_inf = 2 * sp.Matrix(
        (
            (
                -(lam * u + u - 1),
                -lam * u,
                -lam,
                lam * (lam * u - lam - 1),
            ),
            (
                lam * u - lam - 1,
                -lam,
                -lam**2 * u,
                -lam**2 * (lam * u + u - 1),
            ),
            (
                -(lam * u - 1),
                0,
                0,
                -lam**2 * (u - 1),
            ),
            (
                -(u - 1),
                0,
                0,
                -lam * (lam * u - 1),
            ),
        )
    )
    assert sp.simplify(cubic_inf - displayed_inf) == sp.zeros(4)
    inf_compression = [
        sp.factor(cubic_inf.extract(rows, (0, 1, 2)).det())
        for rows in triples
    ]
    assert sp.expand(
        inf_compression[0]
        + 8 * lam**2 * (lam * u - 1) * (lam * u**2 - 1)
    ) == 0
    assert sp.expand(
        inf_compression[1]
        + 8 * lam**2 * (u - 1) * (lam * u**2 - 1)
    ) == 0
    infinity_factor = sp.Poly(lam * u**2 - 1, lam, u)
    for rows in triples:
        for columns in triples:
            minor = sp.Poly(cubic_inf.extract(rows, columns).det(), lam, u)
            _, remainder = sp.div(minor, infinity_factor)
            assert remainder.is_zero
    inf_rank_two_minor = sp.factor(cubic_inf.extract((0, 2), (0, 1)).det())
    assert sp.expand(inf_rank_two_minor + 4 * lam * u * (lam * u - 1)) == 0

    # Both partners on the projective sheet.
    cubic_double_inf = sp.Matrix.hstack(
        triple(y, y_sharp, y_sharp),
        triple(x, y_sharp, y_sharp),
        triple(y, x_sharp, x_sharp),
        triple(x, x_sharp, x_sharp),
    )
    double_compression = sp.factor(
        cubic_double_inf.extract((0, 1, 2), (0, 1, 2)).det()
    )
    assert sp.expand(double_compression + 8 * lam**4) == 0

    result = {
        "base_cross_ratio": "lambda*(lambda-1) != 0",
        "synchronization_kernel_dimension": 2,
        "pencil": "A+t*A_sharp",
        "KJ_minor": str(independent_minor),
        "compression_minor": "8*(lambda-1)*F",
        "full_compound_factor": "8*F",
        "one_infinite_partner_factor": "lambda*u^2-1",
        "double_infinite_compression_minor": "-8*lambda^4",
        "conclusion": "generic flat binary-cubic triangle is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
