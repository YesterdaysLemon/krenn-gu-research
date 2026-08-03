"""Verify the all-pair binary incidence-quotient coherence classification.

This checks five symbolic local normal forms and two fixed sharp models.  It
does not enumerate graphs, words, alignments, supports, or parameters.
"""

from itertools import combinations

import sympy as sp

ZERO = sp.zeros(2, 1)
E0 = sp.Matrix((1, 0))
E1 = sp.Matrix((0, 1))

TYPES = {
    "0": (ZERO, ZERO),
    "X": (E0, ZERO),
    "Y": (ZERO, E0),
    "B": (E0, 2 * E0),
    "G": (E0, E1),
}


def pair_rank(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> int:
    x_left, y_left = left
    x_right, y_right = right
    return sp.Matrix.hstack(
        sp.kronecker_product(x_left, x_right),
        sp.kronecker_product(y_left, y_right),
    ).rank()


def main() -> None:
    expected_compatible = {
        (left, right)
        for left in TYPES
        for right in TYPES
        if not (
            (left == "G" and right in {"B", "G"})
            or (right == "G" and left in {"B", "G"})
        )
    }
    actual_compatible = {
        (left, right)
        for left, left_vectors in TYPES.items()
        for right, right_vectors in TYPES.items()
        if pair_rank(left_vectors, right_vectors) <= 1
    }
    assert actual_compatible == expected_compatible

    # Branch I: seven arbitrary nonzero common-line ratios.
    common_line_model = [
        (sp.Matrix((1,)), sp.Matrix((ratio,))) for ratio in range(1, 8)
    ]
    assert all(
        pair_rank(common_line_model[left], common_line_model[right]) == 1
        for left, right in combinations(range(7), 2)
    )

    # Branch II: one genuine plane, followed by alternating pure-axis types.
    one_plane_model = [TYPES["G"]] + [
        TYPES["X"] if index % 2 else TYPES["Y"] for index in range(1, 7)
    ]
    assert all(
        pair_rank(one_plane_model[left], one_plane_model[right]) <= 1
        for left, right in combinations(range(7), 2)
    )
    assert pair_rank(TYPES["G"], TYPES["B"]) == 2
    assert pair_rank(TYPES["G"], TYPES["G"]) == 2

    # Kernel/rank translation: representative quotient maps on E=K^2.
    quotient_maps = {
        "0": sp.zeros(2),
        "X": sp.Matrix(((1, 0), (0, 0))),
        "Y": sp.Matrix(((0, 1), (0, 0))),
        "B": sp.Matrix(((1, 2), (0, 0))),
        "G": sp.eye(2),
    }
    assert all(
        quotient_maps[name].rank() <= 1 for name in ("0", "X", "Y", "B")
    )
    assert quotient_maps["G"].rank() == 2
    assert quotient_maps["X"] * E1 == ZERO
    assert quotient_maps["Y"] * E0 == ZERO

    print("five intrinsic binary quotient types: CLASSIFIED")
    print("all-pair rule: G compatible exactly with 0/X/Y")
    print("global dichotomy: all ranks <=1, or one G plus only 0/X/Y")
    print("both seven-mode sharp models: VERIFIED")
    print("graph_search=0 word_search=0 alignment_search=0")


if __name__ == "__main__":
    main()
