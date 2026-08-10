"""Focused exact checks for the active-deck and cubic-diagonal theorem.

The arbitrary-order proof is the accompanying markdown argument.  This file
checks its finite algebra/combinatorics interfaces without searching graph
families or parameter values.
"""

from __future__ import annotations

from functools import cache
from itertools import permutations, product

Edge = tuple[int, int]
Matching = frozenset[Edge]


def edge(i: int, j: int) -> Edge:
    return (i, j) if i < j else (j, i)


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return (frozenset(),)
    first = vertices[0]
    output: list[Matching] = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            output.append(matching | {edge(first, partner)})
    return tuple(output)


def verify_laplace_partition() -> None:
    """Each matching occurs once in a prescribed-vertex Laplace expansion."""

    for order in (2, 4, 6, 8, 10):
        vertices = tuple(range(order))
        full = set(perfect_matchings(vertices))
        for pivot in vertices:
            expanded: list[Matching] = []
            for partner in vertices:
                if partner == pivot:
                    continue
                rest = tuple(v for v in vertices if v not in (pivot, partner))
                expanded.extend(
                    matching | {edge(pivot, partner)}
                    for matching in perfect_matchings(rest)
                )
            assert len(expanded) == len(full)
            assert len(set(expanded)) == len(full)
            assert set(expanded) == full


def cross_constraints(z: tuple[bool, ...], cofactor: tuple[bool, ...]) -> bool:
    """Boolean support form of Z_c(e) C_d(e)=0 for c != d."""

    return all(
        not (z[colour] and cofactor[other])
        for colour in range(3)
        for other in range(3)
        if colour != other
    )


def verify_active_deck_exclusivity() -> None:
    admissible = 0
    active_states = 0
    for bits in product((False, True), repeat=6):
        z = bits[:3]
        cofactor = bits[3:]
        if not cross_constraints(z, cofactor):
            continue
        admissible += 1
        active = [colour for colour in range(3) if z[colour] and cofactor[colour]]
        if active:
            active_states += 1
            assert len(active) == 1
            colour = active[0]
            for other in range(3):
                if other != colour:
                    assert not z[other]
                    assert not cofactor[other]
    assert admissible == 18
    assert active_states == 3


def verify_shared_edge_degree_count() -> None:
    """A shared selected edge plus three exclusive active edges needs degree 4."""

    physical_edges = range(4)
    shared = 0
    valid = []
    for chosen in product(physical_edges, repeat=3):
        if shared in chosen:
            continue
        if len(set(chosen)) != 3:
            continue
        valid.append(chosen)
        assert len({shared, *chosen}) == 4
    assert len(valid) == 6


def three_factorization_k33() -> tuple[dict[Edge, int], tuple[Matching, ...]]:
    left = range(3)
    matchings: list[Matching] = []
    colours: dict[Edge, int] = {}
    for colour in range(3):
        matching = frozenset(
            edge(i, 3 + ((i + colour) % 3))
            for i in left
        )
        matchings.append(matching)
        for item in matching:
            assert item not in colours
            colours[item] = colour
    assert len(colours) == 9
    return colours, tuple(matchings)


def verify_cubic_zero_layer_uniqueness() -> None:
    """The induced word selects one edge locally in a proper 3-factorization."""

    colours, factors = three_factorization_k33()
    union = set().union(*factors)
    candidates = [
        matching
        for matching in perfect_matchings(tuple(range(6)))
        if matching <= union
    ]
    assert len(candidates) == 6

    checked_nonmonochromatic = 0
    for matching in candidates:
        used_colours = {colours[item] for item in matching}
        if len(used_colours) == 1:
            continue
        checked_nonmonochromatic += 1
        vertex_colour: dict[int, int] = {}
        for i, j in matching:
            colour = colours[(i, j)]
            vertex_colour[i] = colour
            vertex_colour[j] = colour

        compatible: list[Matching] = []
        for other in candidates:
            if all(
                vertex_colour[i] == vertex_colour[j] == colours[(i, j)]
                for i, j in other
            ):
                compatible.append(other)
        assert compatible == [matching]
    assert checked_nonmonochromatic == 3


def verify_permutation_invariance() -> None:
    """The local exclusivity statement is independent of colour names."""

    base_z = (True, False, False)
    base_cofactor = (True, False, False)
    for permutation in permutations(range(3)):
        z = tuple(base_z[permutation[i]] for i in range(3))
        cofactor = tuple(base_cofactor[permutation[i]] for i in range(3))
        assert cross_constraints(z, cofactor)
        assert sum(a and b for a, b in zip(z, cofactor, strict=True)) == 1


def main() -> None:
    verify_laplace_partition()
    verify_active_deck_exclusivity()
    verify_shared_edge_degree_count()
    verify_cubic_zero_layer_uniqueness()
    verify_permutation_invariance()
    print("active-deck exclusivity and cubic-diagonal focused verification: PASS")
    print("orders checked for Laplace partition: 2,4,6,8,10")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
