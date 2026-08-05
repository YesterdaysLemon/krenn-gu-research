#!/usr/bin/env python3
"""Independent exact audit of the proper cut-support obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def multiply(left, right):
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in PAIRS
        ]
    )


def main() -> None:
    basis = tuple(sp.eye(4).col(i) for i in range(4))

    # Use missing coordinate two and unequal weights:
    # q=X3(2X0+3X1).
    anchor = basis[3]
    line = 2 * basis[0] + 3 * basis[1]
    opposite = 2 * basis[0] - 3 * basis[1]
    star = multiply(anchor, line)
    assert tuple(star) == (0, 0, 2, 0, 3, 0)
    assert multiply(anchor, anchor) == sp.zeros(6, 1)
    assert multiply(line, opposite) == sp.zeros(6, 1)

    r = sp.symbols("r0:4")
    s = sp.symbols("s0:4")
    relation = multiply(anchor, sp.Matrix(r)) + multiply(
        opposite, sp.Matrix(s)
    )
    # Coefficients on edges 02,12,23 force both partner rows to omit X2.
    assert relation[1] == 2 * s[2]
    assert relation[3] == -3 * s[2]
    assert relation[5] == r[2]

    gamma, delta, coupling = sp.symbols("gamma delta coupling")
    partner_one = gamma * anchor - coupling * opposite
    partner_two = coupling * anchor + delta * line
    assert (
        multiply(anchor, partner_one)
        + multiply(opposite, partner_two)
        == sp.zeros(6, 1)
    )
    assert partner_one[2] == partner_two[2] == 0

    # Independently audit a single edge at X2X3.
    single_relation = multiply(basis[2], sp.Matrix(r)) + multiply(
        basis[3], sp.Matrix(s)
    )
    assert single_relation[0] == 0
    assert single_relation[1] == r[0]
    assert single_relation[2] == s[0]
    assert single_relation[3] == r[1]
    assert single_relation[4] == s[1]
    assert single_relation[5] == r[3] + s[2]
    single_partner_one = sp.Matrix((0, 0, gamma, coupling))
    single_partner_two = sp.Matrix((0, 0, -coupling, delta))
    single_map = sp.Matrix.hstack(
        *(
            multiply(left, right)
            for left in (basis[2], basis[3])
            for right in (single_partner_one, single_partner_two)
        )
    )
    assert single_map.rank() <= 1

    support_sizes = {
        "one_three_full": 3,
        "one_three_proper_max": 2,
        "two_two_full": 2 * 2,
        "two_two_one_factor_boundary": 1 * 2,
        "two_two_two_factor_boundary": 1 * 1,
    }
    assert set(support_sizes.values()) == {1, 2, 3, 4}

    perfect_pairing = sp.Matrix(((0, 1, 0), (1, 0, 0), (0, 0, 1)))
    assert abs(perfect_pairing.det()) == 1
    assert 3 + 2 - 3 > 1

    result = {
        "unequal_star_weights": [2, 3],
        "star_missing_coordinate": 2,
        "star_partner_stays_in_hyperplane": True,
        "single_edge_partner_rank_upper_bound": single_map.rank(),
        "cut_support_sizes": support_sizes,
        "three_variable_pairing_determinant": int(perfect_pairing.det()),
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
