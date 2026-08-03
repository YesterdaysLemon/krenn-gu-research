"""Verify the nonprojective root-pair fan tomography theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

PAIRS = tuple(combinations(range(4), 2))


def fan_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            sp.kronecker_product(left[:, first], right[:, second])
            + sp.kronecker_product(left[:, second], right[:, first])
            for first, second in PAIRS
        )
    )


def hollow(face: sp.Matrix) -> sp.Matrix:
    result = sp.zeros(4)
    for index, (first, second) in enumerate(PAIRS):
        result[first, second] = result[second, first] = face[index]
    return result


def complement_permutation() -> sp.Matrix:
    result = sp.zeros(6)
    universe = frozenset(range(4))
    for port_index, pair in enumerate(PAIRS):
        complement = tuple(sorted(universe.difference(pair)))
        face_index = PAIRS.index(complement)
        result[port_index, face_index] = 1
    return result


def main() -> None:
    left = sp.Matrix(2, 4, sp.symbols("a0:8"))
    right = sp.Matrix(2, 4, sp.symbols("b0:8"))
    face = sp.Matrix(sp.symbols("c0:6"))
    fan = fan_matrix(left, right)
    sandwich = left * hollow(face) * right.T
    difference = fan * face - sp.Matrix(list(sandwich))
    assert all(sp.expand(entry) == 0 for entry in difference)

    left_one = sp.Matrix(((1, 0, 1, 0), (0, 1, 0, 1)))
    right_one = sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0)))
    fan_one = fan_matrix(left_one, right_one)
    expected_one = sp.Matrix(
        (
            (0, 1, 1, 0, 0, 1),
            (1, 1, 0, 1, 0, 0),
            (1, 0, 1, 0, 1, 0),
            (0, 0, 0, 1, 1, 1),
        )
    )
    assert fan_one == expected_one
    assert fan_one.rank() == 4
    null_one = sp.Matrix((0, 1, -1, -1, 1, 0))
    null_two = sp.Matrix((1, 0, -1, -1, 0, 1))
    assert fan_one * null_one == sp.zeros(4, 1)
    assert fan_one * null_two == sp.zeros(4, 1)
    assert sp.Matrix.hstack(null_one, null_two).rank() == 2
    assert len(fan_one.nullspace()) == 2

    left_two = sp.Matrix(((1, 0, 1, 1), (0, 1, 1, 2)))
    right_two = sp.Matrix(((1, 0, 1, 2), (0, 1, 2, 1)))
    fan_two = fan_matrix(left_two, right_two)
    expected_two = sp.Matrix(
        (
            (0, 2, 3, 0, 0, 3),
            (1, 2, 1, 1, 1, 3),
            (1, 1, 2, 1, 2, 4),
            (0, 0, 0, 3, 3, 5),
        )
    )
    assert fan_two == expected_two
    assert fan_two.rank() == 4
    stacked = fan_one.col_join(fan_two)
    assert stacked.rank() == 6
    assert stacked[list(range(6)), :].det() == 4
    assert stacked.nullspace() == []

    complement = complement_permutation()
    assert complement * complement == sp.eye(6)
    observed = fan_one * complement * face
    for invisible in (null_one, null_two):
        deformed = face + complement * invisible
        assert fan_one * complement * deformed == observed
        assert fan_two * complement * deformed != fan_two * complement * face

    projective_zero = fan_matrix(sp.zeros(2, 4), right_one)
    assert projective_zero == sp.zeros(4, 6)

    print("PASS: symbolic hollow sandwich Kc=vec(A X(c) B^T)")
    print("PASS: one polarized fan has sharp rank four and defect two")
    print("PASS: two explicit fan defects are transverse with stacked rank six")
    print("PASS: complement-face invisible deformations and projective zero fan")
    print("SCOPE: legal co-occurrence and nuisance-column separation remain UNKNOWN")
    print("searches=0")


if __name__ == "__main__":
    main()
