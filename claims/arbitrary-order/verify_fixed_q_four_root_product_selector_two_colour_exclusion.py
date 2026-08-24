"""Primary replay of the surviving finite GLD66 identities.

GLD66's graph-side exclusion was withdrawn on 2026-08-24 because it inherits
GLD65's invalid root-companion/full-coefficient bridge.  This focused replay
checks the response-anchor identity and conditional finite linear algebra; it
does not prove that a legal product selector supplies the assumed cross-Gram
form.
"""

from __future__ import annotations

from itertools import combinations
from math import prod

from sympy import Symbol, expand

ROOTS = tuple(f"r{i}" for i in range(4))
OUTSIDE = ("q0", "q1", "u", "v")
PORTS = tuple(range(4))
COLOURS = tuple(range(3))
SELECTED = (0, 1)
EDGES = tuple(combinations(PORTS, 2))
MATCHINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for rest in perfect_matchings(remaining):
            yield (edge(first, second),) + rest


ALL_VERTICES = ROOTS + OUTSIDE
WEIGHTS = {
    edge(left, right): Symbol(f"w_{left}_{right}")
    for left, right in combinations(ALL_VERTICES, 2)
}


def matching_polynomial(vertices, *, forbid_outside_edges=False):
    outside = {vertex for vertex in vertices if vertex not in ROOTS}
    return sum(
        prod(WEIGHTS[pair] for pair in matching)
        for matching in perfect_matchings(vertices)
        if not forbid_outside_edges
        or not any(pair[0] in outside and pair[1] in outside for pair in matching)
    )


def check_response_anchor_and_cross_gram_identities():
    """Check the generic six- and eight-vertex matching decompositions."""

    root_hafnian = matching_polynomial(ROOTS)

    six = ROOTS + ("q0", "q1")
    response_anchor = matching_polynomial(six, forbid_outside_edges=True)
    assert (
        expand(
            matching_polynomial(six)
            - WEIGHTS[edge("q0", "q1")] * root_hafnian
            - response_anchor
        )
        == 0
    )
    assert len(tuple(perfect_matchings(six))) == 15
    assert len(tuple(perfect_matchings(six))) - 3 == 12

    full = matching_polynomial(ALL_VERTICES)
    root_bijection = matching_polynomial(ALL_VERTICES, forbid_outside_edges=True)
    outside_compound = sum(
        WEIGHTS[edge(*first)] * WEIGHTS[edge(*second)]
        for first, second in (
            (("q0", "q1"), ("u", "v")),
            (("q0", "u"), ("q1", "v")),
            (("q0", "v"), ("q1", "u")),
        )
    )
    pair_sum = 0
    for left, right in combinations(OUTSIDE, 2):
        complement = tuple(vertex for vertex in OUTSIDE if vertex not in (left, right))
        pair_sum += WEIGHTS[edge(left, right)] * matching_polynomial(ROOTS + complement)
    assert (
        expand(full - (pair_sum - root_hafnian * outside_compound + root_bijection))
        == 0
    )

    counts = {degree: 0 for degree in (0, 1, 2)}
    for matching in perfect_matchings(ALL_VERTICES):
        degree = sum(pair[0] in OUTSIDE and pair[1] in OUTSIDE for pair in matching)
        counts[degree] += 1
    assert counts == {0: 24, 1: 72, 2: 9}
    return 12, counts


def bit(mask, pair, colour):
    return bool(mask & (1 << (3 * EDGES.index(pair) + colour)))


def support(mask, pair):
    return {colour for colour in COLOURS if bit(mask, pair, colour)}


def mixed_coefficients_zero(mask):
    return all(
        not (bit(mask, first, colour) and bit(mask, second, other))
        for first, second in MATCHINGS
        for colour in COLOURS
        for other in COLOURS
        if colour != other
    )


def pure_colour_active(mask, colour):
    return any(
        bit(mask, first, colour) and bit(mask, second, colour)
        for first, second in MATCHINGS
    )


def no_zero_edge_assignment(mask):
    assignment = []
    for first, second in MATCHINGS:
        left = support(mask, first)
        right = support(mask, second)
        assert left and right
        common = left & right
        assert len(left) == len(right) == len(common) == 1
        assignment.append(next(iter(common)))
    return tuple(assignment)


def check_support_cover():
    valid = []
    zero_edge = []
    no_zero_edge = []
    for mask in range(1 << (3 * len(EDGES))):
        if not mixed_coefficients_zero(mask):
            continue
        if not all(pure_colour_active(mask, colour) for colour in SELECTED):
            continue
        valid.append(mask)
        if any(not support(mask, pair) for pair in EDGES):
            zero_edge.append(mask)
        else:
            no_zero_edge.append(mask)

    assignments = tuple(no_zero_edge_assignment(mask) for mask in no_zero_edge)
    expected = tuple(
        assignment
        for assignment in __import__("itertools").product(COLOURS, repeat=3)
        if set(SELECTED) <= set(assignment)
    )
    assert len(no_zero_edge) == len(set(assignments)) == 12
    assert set(assignments) == set(expected)
    assert len(valid) == len(zero_edge) + len(no_zero_edge)
    return len(valid), len(zero_edge), assignments


def matching_index(left, right):
    named = edge(left, right)
    return next(index for index, matching in enumerate(MATCHINGS) if named in matching)


def assigned_colour(assignment, left, right):
    return assignment[matching_index(left, right)]


def prescribed_pairing(assignment, left, right):
    port_left, colour_left = left
    port_right, colour_right = right
    assert port_left != port_right
    return (
        colour_left
        == colour_right
        == assigned_colour(assignment, port_left, port_right)
    )


def check_dimension_certificates(assignments):
    third_colour_kernel = 0
    proportional_kernel = 0
    for assignment in assignments:
        for base in PORTS:
            # The selected-colour subspace E_base has dimension two.  The
            # pairing map against it has rank two, witnessed by the matching
            # partners for colours 0 and 1.  Hence its kernel in W has
            # dimension at most one.
            for colour in SELECTED:
                partner = next(
                    vertex
                    for vertex in PORTS
                    if vertex != base
                    and assigned_colour(assignment, base, vertex) == colour
                )
                assert prescribed_pairing(assignment, (base, colour), (partner, colour))
                other = SELECTED[1 - SELECTED.index(colour)]
                assert not prescribed_pairing(
                    assignment, (base, other), (partner, colour)
                )

            third_neighbours = [
                vertex
                for vertex in PORTS
                if vertex != base and assigned_colour(assignment, base, vertex) == 2
            ]
            if third_neighbours:
                assert len(third_neighbours) == 1
                vertex = third_neighbours[0]
                # Both independent selected-colour vectors at this vertex
                # lie in a kernel of dimension at most one.
                assert all(
                    not prescribed_pairing(
                        assignment, (base, base_colour), (vertex, vertex_colour)
                    )
                    for base_colour in SELECTED
                    for vertex_colour in SELECTED
                )
                third_colour_kernel += 1
                continue

            kernel_vectors = []
            for vertex in PORTS:
                if vertex == base:
                    continue
                edge_colour = assigned_colour(assignment, base, vertex)
                assert edge_colour in SELECTED
                off_colour = SELECTED[1 - SELECTED.index(edge_colour)]
                vector = (vertex, off_colour)
                assert all(
                    not prescribed_pairing(assignment, (base, colour), vector)
                    for colour in SELECTED
                )
                kernel_vectors.append(vector)

            pairings = [
                prescribed_pairing(assignment, left, right)
                for left, right in combinations(kernel_vectors, 2)
            ]
            # Three nonzero vectors in one line must have either all zero or
            # all nonzero mutual pairings.  The matching assignment gives a
            # mixture, so the one-dimensional kernel is impossible.
            assert any(pairings) and not all(pairings)
            proportional_kernel += 1

    assert third_colour_kernel == proportional_kernel == 24
    return third_colour_kernel, proportional_kernel


def main():
    response_terms, matching_counts = check_response_anchor_and_cross_gram_identities()
    valid, zero_edge, assignments = check_support_cover()
    third, proportional = check_dimension_certificates(assignments)
    print("GLD66 surviving finite-identity replay: PASS")
    print("  response-anchor root-only terms:", response_terms)
    print("  eight-vertex outside-edge strata:", matching_counts)
    print("  exact two-active-colour support masks:", valid)
    print("  zero-edge masks (dimension contradiction):", zero_edge)
    print("  no-zero-edge matching assignments:", len(assignments))
    print("  third-colour kernel certificates:", third)
    print("  proportional-kernel certificates:", proportional)
    print(
        "  scope: conditional support/kernel identities; graph-side exclusion withdrawn"
    )
    print("  global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
