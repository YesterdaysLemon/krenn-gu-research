#!/usr/bin/env python3
"""Independent crossed-coordinate audit of the apolar-triangle normal form."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))
PERMUTATION = (1, 0, 3, 2)


def permanent_dp(rows: list[sp.Matrix]) -> sp.Expr:
    layer: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_layer: dict[int, sp.Expr] = {}
        for mask, value in layer.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_layer[new_mask] = next_layer.get(new_mask, 0) + value * row[column]
        layer = next_layer
    return sp.expand(layer[15])


def squarefree_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    entries = []
    for i in range(4):
        for j in range(i + 1, 4):
            entries.append(sp.expand(left[i] * right[j] + left[j] * right[i]))
    return sp.Matrix(entries)


def main() -> None:
    p, q = sp.symbols("P Q")
    original_planes = [
        (sp.Matrix((1, 0, p, 1 + p)), sp.Matrix((0, 1, q, 1 + q))),
        (sp.Matrix((1, 1, 1, 1)), sp.Matrix((0, 0, 1, 1))),
        (sp.Matrix((1, 0, 1, 0)), sp.Matrix((1, -1, 1, 1))),
        (sp.Matrix((0, 0, 1, -1)), sp.Matrix((1, 0, -1, 0))),
    ]
    planes = [
        (left[list(PERMUTATION), :], right[list(PERMUTATION), :])
        for left, right in original_planes
    ]
    tensor = {
        bits: sp.factor(
            permanent_dp([planes[mode][bits[mode]] for mode in range(4)])
        )
        for bits in BITS
    }
    assert tensor[(0, 1, 1, 1)] == -2 * p
    assert tensor[(1, 1, 1, 1)] == -2 * q
    assert sum(value != 0 for value in tensor.values()) == 2

    ranks = []
    relation_ranks = []
    sample = {p: 1, q: 2}
    for i, j in itertools.combinations(range(4), 2):
        matrix = sp.Matrix.hstack(
            *(
                squarefree_product(planes[i][row_i], planes[j][row_j])
                for row_i in range(2)
                for row_j in range(2)
            )
        ).subs(sample)
        ranks.append(matrix.rank())
        if matrix.rank() == 3:
            relation_ranks.append(sp.Matrix(2, 2, list(matrix.nullspace()[0])).rank())
    assert ranks == [4, 4, 4, 3, 3, 3]
    assert relation_ranks == [2, 1, 1]

    # The two degree-three covectors are independently reconstructed by DP.
    def triple_dp(rows: list[sp.Matrix]) -> sp.Matrix:
        entries = []
        for missing in range(4):
            columns = [column for column in range(4) if column != missing]
            relabeled = [sp.Matrix([row[column] for column in columns]) for row in rows]
            entries.append(
                sp.expand(
                    sum(
                        relabeled[0][perm[0]] * relabeled[1][perm[1]] * relabeled[2][perm[2]]
                        for perm in itertools.permutations(range(3))
                    )
                )
            )
        return sp.Matrix(entries)

    kernel = triple_dp([original_planes[mode][0] for mode in (1, 2, 3)])
    active = triple_dp([original_planes[mode][1] for mode in (1, 2, 3)])
    assert kernel == sp.Matrix((-1, -1, -1, 1))
    assert active == sp.Matrix((1, 1, -1, -1))

    result = {
        "audit_source_order": [1, 0, 3, 2],
        "independent_permanent": "subset dynamic programming",
        "pair_profile_at_p1_q2": ranks,
        "relation_ranks": relation_ranks,
        "restricted_coefficients": {"0111": "-2*P", "1111": "-2*Q"},
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
