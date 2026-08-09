#!/usr/bin/env python3
"""Verify the common-kernel YX factorisation obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


MASKS2 = (3, 5, 9, 6, 10, 12)


def product(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> sp.Matrix:
    values: list[sp.Expr] = []
    for mask in MASKS2:
        indices = [index for index in range(4) if mask & (1 << index)]
        i, j = indices
        values.append(sp.expand(left[i] * right[j] + left[j] * right[i]))
    return sp.Matrix(values)


def main() -> None:
    b0, b1, d0, d1, s2, s3, t2, t3, lam = sp.symbols(
        "b0 b1 d0 d1 s2 s3 t2 t3 lambda", nonzero=True
    )
    a = (1, 1, 0, 0)
    b = (b0, b1, s2, s3)
    d = (d0, d1, t2, t3)
    coefficients = product(b, d)
    expected = sp.Matrix(
        [b0 * d1 + b1 * d0, b0 * t2 + d0 * s2,
         b0 * t3 + d0 * s3, b1 * t2 + d1 * s2,
         b1 * t3 + d1 * s3, s2 * t3 + s3 * t2]
    )
    assert coefficients == expected

    delta = b0 * d1 - b1 * d0
    for s, t, e0, e1 in (
        (s2, t2, expected[1], expected[3]),
        (s3, t3, expected[2], expected[4]),
    ):
        assert sp.expand(d1 * e0 - d0 * e1 - delta * t) == 0
        assert sp.expand(b1 * e0 - b0 * e1 + delta * s) == 0

    # Delta=0 and b0*d1+b1*d0=2 give the reflection factorisation.
    B = (b0, b1, 0, 0)
    s = (0, 0, s2, s3)
    reflected_b = tuple(B[index] + s[index] for index in range(4))
    reflected_d = tuple(lam * (B[index] - s[index]) for index in range(4))
    reflected_product = product(reflected_b, reflected_d)
    assert reflected_product == sp.Matrix(
        [2 * lam * b0 * b1, 0, 0, 0, 0, -2 * lam * s2 * s3]
    )

    # The second pair relation is an identity before imposing the two scalar
    # equations lambda*b0*b1=1 and s2*s3=0.
    second_relation = (
        product(a, reflected_d) / lam
        + product(a, reflected_b)
        - (b0 + b1) * product(a, a)
    )
    assert all(sp.factor(entry) == 0 for entry in second_relation)

    # On either coordinate-ray chart, every 3x3 pair-image minor vanishes.
    for ray in ({s3: 0}, {s2: 0}):
        pair_image = sp.Matrix.hstack(
            product(a, reflected_d),
            product(a, a),
            product(reflected_b, reflected_d),
            product(reflected_b, a),
        ).subs(ray)
        for rows in itertools.combinations(range(6), 3):
            for columns in itertools.combinations(range(4), 3):
                assert sp.factor(pair_image.extract(rows, columns).det()) == 0

    # In the Delta!=0 branch (8) forces s=t=0; the image is one-dimensional.
    rigid_image = sp.Matrix.hstack(
        product(a, (d0, d1, 0, 0)),
        product(a, a),
        product((b0, b1, 0, 0), (d0, d1, 0, 0)),
        product((b0, b1, 0, 0), a),
    )
    assert rigid_image.rank() == 1

    print(
        json.dumps(
            {
                "status": "pass",
                "orientation": "common-kernel YX (2,1,1) triangle",
                "factorisation": "b*d=a^2",
                "branches": {
                    "Delta_nonzero": "pair-image rank 1",
                    "Delta_zero": "reflection factorisation and pair-image rank <=2",
                },
                "second_relation": "lambda^-1*a*d+a*b-(b0+b1)*a^2=0",
                "rank_three_pair": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
