#!/usr/bin/env python3
"""Independent exact audit for the crossed (2,1,1) support theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def multiply_degree_one(left: tuple[int, ...], right: tuple[int, ...]) -> sp.Matrix:
    entries = []
    for i, j in itertools.combinations(range(4), 2):
        entries.append(left[i] * right[j] + left[j] * right[i])
    return sp.Matrix(entries)


def subset_permanent(rows: list[tuple[int, ...]]) -> int:
    table: dict[int, int] = {0: 1}
    for row in rows:
        nxt: dict[int, int] = {}
        for mask, value in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    new_mask = mask | (1 << column)
                    nxt[new_mask] = nxt.get(new_mask, 0) + value * entry
        table = nxt
    return table[(1 << 4) - 1]


def transform(row: tuple[int, ...]) -> tuple[int, ...]:
    # Unrelated source order (2,0,3,1) and unequal diagonal scaling.
    order = (2, 0, 3, 1)
    scales = (2, 3, 5, 7)
    return tuple(scales[index] * row[order[index]] for index in range(4))


def main() -> None:
    p, q = 1, 2
    raw_planes = (
        ((1, 0, p, 1 + p), (0, 1, q, 1 + q)),
        ((1, 1, 1, 1), (0, 0, 1, 1)),
        ((1, 0, 1, 0), (1, -1, 1, 1)),
        ((0, 0, 1, -1), (1, 0, -1, 0)),
    )
    planes = tuple(tuple(transform(row) for row in plane) for plane in raw_planes)

    coefficients = {
        bits: subset_permanent([planes[mode][bits[mode]] for mode in range(4)])
        for bits in itertools.product(range(2), repeat=4)
    }
    support = {bits: value for bits, value in coefficients.items() if value != 0}
    assert set(support) == {(0, 1, 1, 1), (1, 1, 1, 1)}

    pair_matrices: dict[tuple[int, int], sp.Matrix] = {}
    for i, j in itertools.combinations(range(4), 2):
        pair_matrices[(i, j)] = sp.Matrix.hstack(
            *(
                multiply_degree_one(planes[i][left], planes[j][right])
                for left, right in itertools.product(range(2), repeat=2)
            )
        )

    assert [pair_matrices[edge].rank() for edge in ((1, 2), (1, 3), (2, 3))] == [3, 3, 3]
    relation_ranks = []
    for edge in ((1, 2), (1, 3), (2, 3)):
        kernel = pair_matrices[edge].nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, list(kernel[0])).rank())
    assert relation_ranks == [2, 1, 1]

    # Independent block determinant replay of the disjoint anchor step.
    u0, u1, up0, up1, v0, v1, vp0, vp1 = sp.symbols(
        "u0 u1 up0 up1 v0 v1 vp0 vp1"
    )
    u = sp.Matrix((u0, u1))
    up = sp.Matrix((up0, up1))
    v = sp.Matrix((v0, v1))
    vp = sp.Matrix((vp0, vp1))
    observed = u * vp.T + up * v.T
    exterior = sp.Matrix.hstack(u, up).det() * sp.Matrix.hstack(vp, v).det()
    assert sp.factor(observed.det() - exterior) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "permuted and diagonally scaled source coordinates",
                "pure_support": {str(bits): value for bits, value in support.items()},
                "triangle_pair_ranks": [3, 3, 3],
                "relation_ranks": relation_ranks,
                "permanent": "subset dynamic programming",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
