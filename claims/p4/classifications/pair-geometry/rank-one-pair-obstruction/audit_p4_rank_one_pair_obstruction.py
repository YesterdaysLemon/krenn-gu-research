#!/usr/bin/env python3
"""Independent rational audit of the rank-one pair-image obstruction."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))


def product(left, right):
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def determinant_two(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def main() -> None:
    zero = Fraction(0)
    one = Fraction(1)
    curve_checks = 0
    slice_determinants = []

    # Use nonsymmetric rational representatives and a nontrivial source
    # permutation for every coordinate block.
    order = (2, 0, 3, 1)
    for original_p, original_q in PAIRS:
        p, q = order[original_p], order[original_q]
        left = tuple(Fraction(2) if i == p else Fraction(3) if i == q else zero for i in range(4))
        right = tuple(Fraction(2) if i == p else Fraction(-3) if i == q else zero for i in range(4))
        assert product(left, right) == (zero,) * 6

        # Coordinate-plane multiplication has matrix [[0,1],[1,0]].
        xp = tuple(one if i == p else zero for i in range(4))
        xq = tuple(one if i == q else zero for i in range(4))
        edge_index = PAIRS.index(tuple(sorted((p, q))))
        binary = [
            [product(xp, xp)[edge_index], product(xp, xq)[edge_index]],
            [product(xq, xp)[edge_index], product(xq, xq)[edge_index]],
        ]
        det = determinant_two(binary)
        assert det == -1
        slice_determinants.append(det)
        curve_checks += 1

    assert curve_checks == 6
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "source-permuted rational zero-product curves",
                "curve_checks": curve_checks,
                "binary_slice_determinants": [int(value) for value in slice_determinants],
                "rank_zero_or_one_pure_strata": "empty",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
