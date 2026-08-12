"""Independent no-import audit of the least-core response/portal mechanisms.

The audit does not import repository code or the primary verifier.  It uses a
hollow-symmetric hafnian recursion, direct support matching checks, and an
integer-mask implementation of the normal-type transitions.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache

Q = Fraction
Edge = tuple[int, int]


def symmetric_from_bipartite(block: tuple[tuple[int, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    order = 2 * len(block)
    matrix = [[Q(0) for _ in range(order)] for _ in range(order)]
    offset = len(block)
    for row, values in enumerate(block):
        for column, value in enumerate(values):
            matrix[row][offset + column] = Q(value)
            matrix[offset + column][row] = Q(value)
    return tuple(tuple(row) for row in matrix)


def hafnian(
    matrix: tuple[tuple[Fraction, ...], ...], vertices: tuple[int, ...]
) -> Fraction:
    @cache
    def recurse(active: tuple[int, ...]) -> Fraction:
        if not active:
            return Q(1)
        first = active[0]
        total = Q(0)
        for position in range(1, len(active)):
            second = active[position]
            rest = active[1:position] + active[position + 1 :]
            total += matrix[first][second] * recurse(rest)
        return total

    return recurse(vertices)


def canonical(edge: Edge) -> Edge:
    return tuple(sorted(edge))


def is_support_matching(
    matrix: tuple[tuple[Fraction, ...], ...],
    vertices: set[int],
    edges: set[Edge],
) -> bool:
    used: set[int] = set()
    for raw_edge in edges:
        left, right = canonical(raw_edge)
        if left not in vertices or right not in vertices:
            return False
        if left in used or right in used or matrix[left][right] == 0:
            return False
        used.update((left, right))
    return used == vertices


def crossing_count(edges: set[Edge], shore: set[int]) -> int:
    return sum((left in shore) != (right in shore) for left, right in edges)


def matching_weight(
    matrix: tuple[tuple[Fraction, ...], ...], edges: set[Edge]
) -> Fraction:
    result = Q(1)
    for left, right in edges:
        result *= matrix[left][right]
    return result


def check_control(block: tuple[tuple[int, ...], ...], complement_matchable: bool) -> None:
    matrix = symmetric_from_bipartite(block)
    all_vertices = tuple(range(6))
    s_vertices = (0, 1, 3, 4)
    c_vertices = (2, 5)

    assert hafnian(matrix, s_vertices) == 0
    assert hafnian(matrix, all_vertices) == -1
    assert (hafnian(matrix, c_vertices) != 0) is complement_matchable

    # Every leading K2,2 edge has a nonzero deletion cofactor on S.
    for left in (0, 1):
        for right in (3, 4):
            assert matrix[left][right] != 0
            remainder = tuple(v for v in s_vertices if v not in (left, right))
            assert hafnian(matrix, remainder) != 0


def check_completion() -> None:
    block = ((1, 1, 1), (1, -1, 0), (1, 0, 1))
    matrix = symmetric_from_bipartite(block)
    check_control(block, complement_matchable=True)

    complement = {(2, 5)}
    core_a = {(0, 3), (1, 4)}
    core_b = {(0, 4), (1, 3)}
    assert is_support_matching(matrix, set(range(6)), core_a | complement)
    assert is_support_matching(matrix, set(range(6)), core_b | complement)
    assert (
        matching_weight(matrix, core_a | complement)
        + matching_weight(matrix, core_b | complement)
        == 0
    )


def check_portal() -> None:
    block = ((1, 1, 1), (1, -1, 0), (1, 0, 0))
    matrix = symmetric_from_bipartite(block)
    check_control(block, complement_matchable=False)

    s_vertices = {0, 1, 3, 4}
    full_matching = {(0, 5), (1, 4), (2, 3)}
    assert is_support_matching(matrix, set(range(6)), full_matching)
    assert crossing_count(full_matching, s_vertices) == 2

    # A zero-crossing matching would have to use the absent complement edge.
    assert matrix[2][5] == 0

    r_partial = {(1, 4)}
    direct_core = {(0, 3), (1, 4)}
    long_core = {(0, 4), (1, 3)}
    assert direct_core ^ r_partial == {(0, 3)}
    assert long_core ^ r_partial == {(0, 4), (1, 3), (1, 4)}

    # Both alternating paths pair portal endpoints 0 and 3.  Their crossing
    # partners are 5 and 2, whose internal support edge is absent.
    assert matrix[2][5] == 0


def bit(mask: int, colour: int) -> int:
    return (mask >> colour) & 1


def transitions(mask: int, colour: int) -> frozenset[int]:
    """Allowed targets after flipping non-colour bits and freeing own bit."""

    other_bits_flipped = mask ^ (0b111 ^ (1 << colour))
    own_bit_cleared = other_bits_flipped & ~(1 << colour)
    return frozenset((own_bit_cleared, own_bit_cleared | (1 << colour)))


def check_bit_implications() -> None:
    for mask in range(8):
        for e_colour in range(3):
            for d_colour in range(3):
                if e_colour == d_colour:
                    continue
                k_colour = 3 - e_colour - d_colour
                q_before = bit(mask, d_colour) ^ bit(mask, k_colour)
                e_targets = transitions(mask, e_colour)
                d_targets = transitions(mask, d_colour)

                assert all(
                    bit(target, d_colour) ^ bit(target, k_colour) == q_before
                    for target in e_targets
                )
                assert {
                    bit(target, d_colour) ^ bit(target, k_colour)
                    for target in d_targets
                } == {q_before, 1 - q_before}

                for y_mask in e_targets:
                    assert d_targets.isdisjoint(transitions(y_mask, d_colour))

    assert 0b111 in transitions(0b000, 1)
    assert (bit(0b000, 1) ^ bit(0b000, 2)) == (
        bit(0b111, 1) ^ bit(0b111, 2)
    )


def main() -> None:
    check_completion()
    check_portal()
    check_bit_implications()
    print("least-core complementary-shore response/portal independent audit: PASS")


if __name__ == "__main__":
    main()
