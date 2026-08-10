"""Verify the fixed-support rank barrier to promoting the two heralds."""

from __future__ import annotations

import json

from sympy import Matrix, symbols


def main() -> None:
    # A_i is the two-edge amplitude of the monochromatic colour-i
    # matching on vertices 1,...,4.  H_j is the weight of colour j on 56.
    a1, a2, a3, h1, h2, h3 = symbols(
        "A1 A2 A3 H1 H2 H3",
        nonzero=True,
    )
    amplitudes = (a1, a2, a3)
    heralds = (h1, h2, h3)
    coefficient_matrix = Matrix(
        [
            [amplitudes[i] * heralds[j] for j in range(3)]
            for i in range(3)
        ]
    )

    assert coefficient_matrix.rank() == 1
    assert all(
        coefficient_matrix[i, j] != 0
        for i in range(3)
        for j in range(3)
    )
    target = Matrix.eye(3)
    assert target.rank() == 3

    # The six off-diagonal entries are the unique matching coefficients
    # of (ci,ci,ci,ci,cj,cj), i != j, on the fixed promoted support.
    off_diagonal = [
        str(coefficient_matrix[i, j])
        for i in range(3)
        for j in range(3)
        if i != j
    ]
    assert len(off_diagonal) == 6

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "add arbitrary nonzero c1,c2,c3 modes only on "
                    "the herald edge 56"
                ),
                "coefficient_matrix": [
                    [str(coefficient_matrix[i, j]) for j in range(3)]
                    for i in range(3)
                ],
                "observed_rank": coefficient_matrix.rank(),
                "required_diagonal_rank": target.rank(),
                "unavoidable_nonzero_off_diagonal_coefficients": (
                    off_diagonal
                ),
                "fixed_support_promotion_possible": False,
                "global_question_1_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
