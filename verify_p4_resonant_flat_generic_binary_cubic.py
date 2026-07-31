#!/usr/bin/env python3
"""Exact replay of the Borel-generic flat binary-cubic obstruction."""

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
    output = []
    for missing in range(4):
        columns = [index for index in range(4) if index != missing]
        output.append(
            sp.expand(
                sum(
                    sp.prod(rows[index][columns[permutation[index]]] for index in range(3))
                    for permutation in itertools.permutations(range(3))
                )
            )
        )
    return sp.Matrix(output)


def main() -> None:
    p, q, t, u = sp.symbols("p q t u")
    y = sp.ones(4, 1)
    x = sp.Matrix((0, 1, p, q))
    ys = sp.Matrix((0, p + q - 1, p * (1 - p + q), q * (1 + p - q)))
    xs = p * q * sp.Matrix((-1, 1, 1, 1))

    variables = sp.symbols("a0:4 b0:4")
    sync_matrix, _ = sp.linear_eq_to_matrix(
        list(pair(y, sp.Matrix(variables[4:])) - pair(x, sp.Matrix(variables[:4]))),
        variables,
    )
    sync_basis = sp.Matrix.hstack(
        sp.Matrix.vstack(y, x), sp.Matrix.vstack(ys, xs)
    )
    assert sync_matrix.rank() == 6
    assert sp.simplify(sync_matrix * sync_basis) == sp.zeros(6, 2)
    assert sync_basis.rank() == 2

    y2, x2 = y + t * ys, x + t * xs
    y3, x3 = y + u * ys, x + u * xs
    assert pair(y2, x3) == pair(x2, y3)

    Y = triple(y, y2, y3)
    K = triple(x, y2, y3)
    J = triple(y, x2, x3)
    X = triple(x, x2, x3)
    assert K == triple(y, x2, y3) == triple(y, y2, x3)
    assert J == triple(x, y2, x3) == triple(x, x2, y3)
    C = sp.Matrix.hstack(Y, K, J, X)

    H = p**2 - 2 * p * q - 2 * p + q**2 - 2 * q + 1
    F = (
        p**2 * q**2 * H * t**2 * u**2
        - 6 * p**2 * q**2 * (t**2 * u + t * u**2)
        - p * q * (p + q + 1) * (t**2 + 4 * t * u + u**2)
        - 2 * (p * q + p + q) * (t + u)
        - 3
    )
    compression = sp.factor(C.extract((1, 2, 3), (0, 1, 2)).det())
    assert sp.expand(compression + 8 * (p - 1) * (p - q) * (q - 1) * F) == 0

    triples = tuple(itertools.combinations(range(4), 3))
    divisor = sp.Poly(F, p, q, t, u)
    compound_remainders = []
    for rows in triples:
        for columns in triples:
            minor = sp.Poly(C.extract(rows, columns).det(), p, q, t, u)
            _, remainder = sp.div(minor, divisor)
            compound_remainders.append(remainder)
    assert all(remainder.is_zero for remainder in compound_remainders)

    determinant = sp.factor(C.det())
    expected_determinant = -16 * p * q * (p - 1) * (p - q) * (q - 1) * F**2
    assert sp.expand(determinant - expected_determinant) == 0

    KJ_minors = (
        sp.factor(C.extract((1, 2), (1, 2)).det()),
        sp.factor(C.extract((1, 3), (1, 2)).det()),
        sp.factor(C.extract((2, 3), (1, 2)).det()),
    )
    expected_KJ = (
        -4 * q**2 * (p - 1) * (p * t + 1) * (p * u + 1),
        -4 * p**2 * (q - 1) * (q * t + 1) * (q * u + 1),
        4 * (p - q) * (p * q * t + 1) * (p * q * u + 1),
    )
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(KJ_minors, expected_KJ)
    )

    result = {
        "legal_gauge": "Borel preserving the pure kernel line",
        "center": "y=(1,1,1,1), x=(0,1,p,q)",
        "synchronizer_dimension": 2,
        "common_compound_factor": "F",
        "compound_entries_divisible": len(compound_remainders),
        "determinant": "-16*p*q*(p-1)*(p-q)*(q-1)*F^2",
        "rank_one_compression": "excluded by three distinct forced parameter values",
        "conclusion": "Borel-generic finite-partner flat chart is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
