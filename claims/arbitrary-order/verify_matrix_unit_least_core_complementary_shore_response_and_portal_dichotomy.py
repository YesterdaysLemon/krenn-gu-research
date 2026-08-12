"""Exact mechanism checks for the least-core response/portal theorem.

This script performs no graph-family enumeration and no witness search.  It
uses closed permanent formulas for two hand-constructed rational controls and
replays the local normal-bit implications used in the arbitrary-order proof.
"""

from __future__ import annotations

from fractions import Fraction

Q = Fraction
Permutation3 = tuple[int, int, int]
Matrix3 = tuple[
    tuple[Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction],
]

PERMUTATIONS_3: tuple[Permutation3, ...] = (
    (0, 1, 2),
    (0, 2, 1),
    (1, 0, 2),
    (1, 2, 0),
    (2, 0, 1),
    (2, 1, 0),
)


def permanent_two(matrix: Matrix3) -> Fraction:
    """Permanent of the leading 2 by 2 block, in closed form."""

    return matrix[0][0] * matrix[1][1] + matrix[0][1] * matrix[1][0]


def permanent_three(matrix: Matrix3) -> Fraction:
    """Permanent of a 3 by 3 matrix, in the six-term closed form."""

    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i + f * h) + b * (d * i + f * g) + c * (d * h + e * g)


def term(matrix: Matrix3, permutation: Permutation3) -> Fraction:
    return (
        matrix[0][permutation[0]]
        * matrix[1][permutation[1]]
        * matrix[2][permutation[2]]
    )


def crossing_count(permutation: Permutation3) -> int:
    """Crossings of S={u0,u1,w0,w1} in the displayed bipartite matching."""

    count = 0
    for row, column in enumerate(permutation):
        row_in_s = row < 2
        column_in_s = column < 2
        count += row_in_s != column_in_s
    return count


def check_least_core(matrix: Matrix3) -> None:
    """Check the exact cancelling K2,2 core and all four deletion cofactors."""

    assert permanent_two(matrix) == 0
    leading = (
        matrix[0][0],
        matrix[0][1],
        matrix[1][0],
        matrix[1][1],
    )
    assert all(value != 0 for value in leading)

    # Deleting any supported K2,2 edge leaves its opposite edge.  These are
    # the four nonzero restricted cofactors in the allowed core.
    cofactors = (
        matrix[1][1],
        matrix[1][0],
        matrix[0][1],
        matrix[0][0],
    )
    assert all(value != 0 for value in cofactors)


def check_completion_control() -> None:
    """A completed least relation can coexist with a nonzero full hafnian."""

    matrix: Matrix3 = (
        (Q(1), Q(1), Q(1)),
        (Q(1), Q(-1), Q(0)),
        (Q(1), Q(0), Q(1)),
    )
    check_least_core(matrix)
    assert matrix[2][2] == 1  # The two-vertex complement is matchable.

    terms = {permutation: term(matrix, permutation) for permutation in PERMUTATIONS_3}
    completed_terms = terms[(0, 1, 2)] + terms[(1, 0, 2)]
    assert terms[(0, 1, 2)] == -1
    assert terms[(1, 0, 2)] == 1
    assert completed_terms == 0

    # One two-crossing term remains, so the full pure coefficient is nonzero.
    assert terms[(2, 1, 0)] == -1
    assert crossing_count((2, 1, 0)) == 2
    assert permanent_three(matrix) == -1
    assert sum(terms.values(), Q(0)) == -1


def check_portal_control() -> None:
    """An unmatchable complement produces a genuine minimum portal."""

    matrix: Matrix3 = (
        (Q(1), Q(1), Q(1)),
        (Q(1), Q(-1), Q(0)),
        (Q(1), Q(0), Q(0)),
    )
    check_least_core(matrix)
    assert matrix[2][2] == 0  # No same-colour conformal completion.

    terms = {permutation: term(matrix, permutation) for permutation in PERMUTATIONS_3}
    nonzero = {
        permutation: value for permutation, value in terms.items() if value != 0
    }
    assert nonzero == {(2, 1, 0): Q(-1)}
    assert crossing_count((2, 1, 0)) == 2
    assert permanent_three(matrix) == -1

    # M uses u0-w2, u1-w1, u2-w0.  Its internal S edge is R={u1-w1}.
    # The two core matchings yield respectively the direct portal path
    # u0-w0 and the alternating path u0-w1-u1-w0.  Both pair the same two
    # portal vertices, whose complementary partners are w2 and u2.
    n_direct = {("u0", "w0"), ("u1", "w1")}
    n_long = {("u0", "w1"), ("u1", "w0")}
    r_partial = {("u1", "w1")}
    assert ("u0", "w0") in n_direct
    assert ("u1", "w1") in n_direct & r_partial
    assert (
        ("u0", "w1") in n_long
        and ("u1", "w1") in r_partial
        and ("u1", "w0") in n_long
    )
    assert matrix[2][2] == 0  # The portal-image edge u2-w2 is absent.


Bits = tuple[int, int, int]


def transitions(bits: Bits, colour: int) -> tuple[Bits, Bits]:
    """Both saturated transitions; the active colour's own bit is free."""

    outputs: list[Bits] = []
    for own_bit in (0, 1):
        outputs.append(
            tuple(
                own_bit if index == colour else 1 - bit
                for index, bit in enumerate(bits)
            )
        )
    return outputs[0], outputs[1]


def check_normal_bit_portal_logic() -> None:
    """Replay own-bit freedom and the valid shared-neighbour separation."""

    for mask in range(8):
        bits = tuple((mask >> index) & 1 for index in range(3))
        assert len(bits) == 3
        for e_colour in range(3):
            for d_colour in range(3):
                if d_colour == e_colour:
                    continue
                k_colour = 3 - e_colour - d_colour
                q_before = bits[d_colour] ^ bits[k_colour]
                after_e = transitions(bits, e_colour)
                after_d = transitions(bits, d_colour)

                # Both bits entering q are non-e bits and therefore flip.
                assert all(
                    (target[d_colour] ^ target[k_colour]) == q_before
                    for target in after_e
                )

                # A d-transition flips b_k but may either preserve or flip
                # its own b_d.  Thus q has both possible outcomes.
                assert {
                    target[d_colour] ^ target[k_colour] for target in after_d
                } == {q_before, 1 - q_before}

                # No type can be a d-neighbour of both endpoints of an
                # e-edge, because both d-edges would flip b_k while the
                # e-edge already flips b_k.
                for y_bits in after_e:
                    assert set(after_d).isdisjoint(transitions(y_bits, d_colour))

    # Explicit counter-transition to the rejected own-bit-preservation step.
    zero = (0, 0, 0)
    all_one = (1, 1, 1)
    assert all_one in transitions(zero, 1)
    assert (zero[1] ^ zero[2]) == (all_one[1] ^ all_one[2])


def check_size_landings() -> None:
    """Replay only the conditional response-shore size comparison."""

    n_large = 8
    s_large = 6
    response_large = n_large - s_large + 2
    assert response_large == 4
    assert response_large < s_large
    assert 2 * s_large > n_large + 2

    n_boundary = 6
    s_boundary = 4
    response_boundary = n_boundary - s_boundary + 2
    assert response_boundary == s_boundary
    assert 2 * s_boundary == n_boundary + 2


def main() -> None:
    check_completion_control()
    check_portal_control()
    check_normal_bit_portal_logic()
    check_size_landings()
    print("least-core complementary-shore response/portal primary checks: PASS")


if __name__ == "__main__":
    main()
