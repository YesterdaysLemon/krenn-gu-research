#!/usr/bin/env python3
"""Tiny exact replay for the rank-two pair-kernel geometry theorem."""

from __future__ import annotations

import json

import sympy as sp


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i in range(4)
            for j in range(i + 1, 4)
        ]
    )


def multiplication_matrix(left: sp.Matrix) -> sp.Matrix:
    basis = tuple(sp.eye(4).col(index) for index in range(4))
    return sp.Matrix.hstack(*(product(left, vector) for vector in basis))


def pair_rank(u0, u1, v0, v1) -> int:
    return sp.Matrix.hstack(
        product(u0, v0),
        product(u0, v1),
        product(u1, v0),
        product(u1, v1),
    ).rank()


def main() -> None:
    e = tuple(sp.eye(4).col(index) for index in range(4))
    annihilator_ranks = {
        "support_1": multiplication_matrix(e[0]).rank(),
        "support_2": multiplication_matrix(e[0] + e[1]).rank(),
        "support_3": multiplication_matrix(e[0] + e[1] + e[2]).rank(),
        "support_4": multiplication_matrix(sum(e, sp.zeros(4, 1))).rank(),
    }
    assert annihilator_ranks == {
        "support_1": 3,
        "support_2": 3,
        "support_3": 4,
        "support_4": 4,
    }

    p, q, r, s, cap_p, cap_q, cap_r, cap_s = sp.symbols(
        "p q r s P Q R S"
    )
    tangent_two = product(
        e[0] + e[1],
        sp.Matrix((cap_p, cap_q, cap_r, cap_s)),
    ) + product(
        sp.Matrix((p, q, r, s)),
        e[0] - e[1],
    )
    assert tuple(tangent_two) == (
        cap_p + cap_q - p + q,
        cap_r + r,
        cap_s + s,
        cap_r - r,
        cap_s - s,
        0,
    )

    tangent_one = product(
        e[0],
        sp.Matrix((cap_p, cap_q, cap_r, cap_s)),
    ) + product(
        sp.Matrix((p, q, r, s)),
        e[0],
    )
    assert tuple(tangent_one) == (
        cap_q + q,
        cap_r + r,
        cap_s + s,
        0,
        0,
        0,
    )

    tangent_two_rank = pair_rank(e[0], e[1], e[0], e[1])
    tangent_one_support_one_rank = pair_rank(
        e[0],
        e[1],
        e[0],
        e[1],
    )
    tangent_one_support_two_rank = pair_rank(
        e[0],
        e[1] + e[2],
        e[0],
        e[1] + e[2],
    )
    assert tangent_two_rank == tangent_one_support_one_rank == 1
    assert tangent_one_support_two_rank == 2

    disjoint = pair_rank(
        e[0] + e[1],
        e[2] + e[3],
        e[0] - e[1],
        e[2] - e[3],
    )
    overlapping = pair_rank(
        e[0] + e[1],
        e[0] + e[2],
        e[0] - e[1],
        e[0] - e[2],
    )
    assert disjoint == overlapping == 2

    result = {
        "annihilator_dimensions": {
            key: 4 - rank for key, rank in annihilator_ranks.items()
        },
        "secant_representative_pair_ranks": {
            "2+2": disjoint,
            "1+3": overlapping,
        },
        "support_two_tangent_forces": ["r=R=0", "s=S=0"],
        "support_one_tangent_forces": [
            "q=-Q",
            "r=-R",
            "s=-S",
        ],
        "tangent_pair_ranks": {
            "two_coordinate_base": tangent_two_rank,
            "one_coordinate_base_w_support_1": tangent_one_support_one_rank,
            "one_coordinate_base_w_support_2": tangent_one_support_two_rank,
        },
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
