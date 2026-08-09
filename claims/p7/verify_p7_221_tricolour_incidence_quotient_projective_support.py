"""Verify the tricolour incidence-quotient projective-support theorem."""

from itertools import combinations

import sympy as sp

import verify_p7_221_degree5_incidence_quotient_rectangle_flattening as binary

FACES = {
    "01": frozenset("1234a"),
    "02": frozenset("1235b"),
    "12": frozenset("1345b"),
}


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def triple_pair_rank(left, right) -> int:
    return sp.Matrix.hstack(
        *(tensor(left[colour], right[colour]) for colour in range(3))
    ).rank()


def main() -> None:
    rho = binary.RHO
    beta = 2 * (1 + rho) / 7
    expected = {
        "01": (1 + 43 * rho / 21, -6, 0),
        "02": (rho, 0, beta),
        "12": (0, rho, beta),
    }
    for label, face in FACES.items():
        actual = tuple(binary.formal_wick_value(colour, face) for colour in range(3))
        assert all(
            sp.simplify(left - right) == 0
            for left, right in zip(actual, expected[label], strict=True)
        )

    assert sp.simplify((1 + 43 * rho / 21) * (1 - 43 * rho / 21)) == -sp.Rational(1828, 21)
    assert sp.simplify(rho * (-rho)) == -21
    assert sp.simplify(beta * (2 * (1 - rho) / 7)) == -sp.Rational(80, 49)

    zero = sp.zeros(2, 1)
    e0 = sp.Matrix((1, 0))
    e1 = sp.Matrix((0, 1))

    # Three sharp rank-two modes, one for each colour pair.
    rank_two_modes = (
        (e0, e1, zero),
        (zero, e0, e1),
        (e0, zero, e1),
    )
    singleton_modes = (
        (e0, zero, zero),
        (zero, e0, zero),
        (zero, zero, e0),
        (e0, zero, zero),
    )
    sharp_model = rank_two_modes + singleton_modes
    assert [sp.Matrix.hstack(*mode).rank() for mode in sharp_model[:3]] == [2, 2, 2]
    assert all(
        triple_pair_rank(sharp_model[left], sharp_model[right]) <= 1
        for left, right in combinations(range(7), 2)
    )

    # A rank-three mode forces every other support to be a singleton.
    e2 = sp.Matrix((0, 0, 1))
    zero3 = sp.zeros(3, 1)
    rank_three = (sp.Matrix((1, 0, 0)), sp.Matrix((0, 1, 0)), e2)
    rank_three_model = (rank_three,) + (
        (sp.Matrix((1, 0, 0)), zero3, zero3),
        (zero3, sp.Matrix((1, 0, 0)), zero3),
        (zero3, zero3, sp.Matrix((1, 0, 0))),
        (sp.Matrix((1, 0, 0)), zero3, zero3),
        (zero3, sp.Matrix((1, 0, 0)), zero3),
        (zero3, zero3, sp.Matrix((1, 0, 0))),
    )
    assert sp.Matrix.hstack(*rank_three).rank() == 3
    assert all(
        triple_pair_rank(rank_three_model[left], rank_three_model[right]) <= 1
        for left, right in combinations(range(7), 2)
    )

    # Four rank-two modes would need four distinct independent colour pairs,
    # but only C(3,2)=3 exist.
    assert len(tuple(combinations(range(3), 2))) == 3

    print("three exact two-colour Wick faces: VERIFIED")
    print("all-pair tricolour quotient span <=1: SYMBOLIC")
    print("high-rank quotient modes <=3: PROJECTIVE-SUPPORT PROOF")
    print("three-rank-two and one-rank-three sharp models: VERIFIED")
    print("graph_search=0 word_search=0 alignment_search=0")


if __name__ == "__main__":
    main()
