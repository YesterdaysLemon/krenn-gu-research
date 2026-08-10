"""Exact checks for the bridge-word synchronization sharpness boundary.

The six-vertex construction is a bounded countermechanism to a proof route,
not a Krenn--Gu witness and not a graph-family search.
"""

from __future__ import annotations

from collections import defaultdict
from functools import cache
from itertools import combinations, permutations

Edge = tuple[int, int]
Unit = tuple[int, int, int]
Matching = tuple[Edge, ...]

U1, U2, V1, V2, X, Y = range(6)
VERTEX_COUNT = 6
A, B, THIRD = 0, 1, 2
U_SHORE = {U1, U2, X, Y}
V_SHORE = {V1, V2}


def edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def put(
    units: dict[Edge, Unit],
    left: int,
    right: int,
    left_colour: int,
    right_colour: int,
    weight: int,
) -> None:
    if left < right:
        units[(left, right)] = (left_colour, right_colour, weight)
    else:
        units[(right, left)] = (right_colour, left_colour, weight)


def gadget() -> dict[Edge, Unit]:
    units: dict[Edge, Unit] = {}
    flag_weights = {
        U1: (1, 1),
        U2: (-1, 1),
        X: (1, -1),
        Y: (1, 1),
    }
    for u_vertex in sorted(U_SHORE):
        for row, v_vertex in enumerate((V1, V2)):
            put(
                units,
                u_vertex,
                v_vertex,
                A,
                B,
                flag_weights[u_vertex][row],
            )

    put(units, V1, V2, A, A, 1)
    put(units, U1, U2, B, B, 1)
    put(units, X, Y, B, B, 1)
    put(units, U1, X, B, B, 1)
    put(units, U2, Y, B, B, -1)
    put(units, U1, Y, A, A, 1)
    put(units, U2, X, A, A, -1)
    return units


def pure_active_relay_gadget() -> dict[Edge, Unit]:
    """Return the complete pure-active relay in zero-based vertex labels."""

    units: dict[Edge, Unit] = {}
    pure_matchings = {
        A: ((2, 3), (0, 4), (1, 5)),
        B: ((0, 1), (2, 5), (3, 4)),
        THIRD: ((4, 5), (0, 3), (1, 2)),
    }
    for colour, matching in pure_matchings.items():
        for left, right in matching:
            put(units, left, right, colour, colour, 1)

    put(units, 0, 2, A, B, 1)
    put(units, 1, 3, A, B, 1)
    put(units, 0, 5, A, THIRD, -1)
    put(units, 2, 4, B, THIRD, 1)
    put(units, 1, 4, B, A, 1)
    put(units, 3, 5, THIRD, A, 1)
    return units


def oriented_unit(units: dict[Edge, Unit], left: int, right: int) -> Unit:
    first_colour, second_colour, weight = units[edge(left, right)]
    if left < right:
        return first_colour, second_colour, weight
    return second_colour, first_colour, weight


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield (edge(first, partner),) + tail


def matching_term(
    units: dict[Edge, Unit], matching: Matching
) -> tuple[tuple[int, ...], int]:
    word = [-1] * VERTEX_COUNT
    weight = 1
    for left, right in matching:
        left_colour, right_colour, edge_weight = units[(left, right)]
        word[left] = left_colour
        word[right] = right_colour
        weight *= edge_weight
    return tuple(word), weight


def tensor(units: dict[Edge, Unit]) -> dict[tuple[int, ...], int]:
    result: dict[tuple[int, ...], int] = defaultdict(int)
    for matching in perfect_matchings(tuple(range(VERTEX_COUNT))):
        word, weight = matching_term(units, matching)
        result[word] += weight
    return {word: weight for word, weight in result.items() if weight}


def coefficient(
    units: dict[Edge, Unit], assignment: tuple[int, ...]
) -> tuple[int, list[tuple[Matching, int]]]:
    terms: list[tuple[Matching, int]] = []
    for matching in perfect_matchings(tuple(range(VERTEX_COUNT))):
        word, weight = matching_term(units, matching)
        if word == assignment:
            terms.append((matching, weight))
    return sum(weight for _, weight in terms), terms


def haf_colour(units: dict[Edge, Unit], vertices: frozenset[int], colour: int) -> int:
    @cache
    def recurse(state: tuple[int, ...]) -> int:
        if not state:
            return 1
        first = state[0]
        total = 0
        for index in range(1, len(state)):
            partner = state[index]
            left_colour, right_colour, weight = oriented_unit(units, first, partner)
            if left_colour == right_colour == colour:
                remainder = state[1:index] + state[index + 1 :]
                total += weight * recurse(remainder)
        return total

    return recurse(tuple(sorted(vertices)))


def nonrigid_set(units: dict[Edge, Unit], colour: int) -> set[int]:
    result: set[int] = set()
    for tail in range(VERTEX_COUNT):
        for head in range(VERTEX_COUNT):
            if tail == head:
                continue
            local, remote, _ = oriented_unit(units, tail, head)
            if local != colour and remote == colour:
                result.add(tail)
    return result


def injections(domain: tuple[int, ...], codomain: tuple[int, ...]):
    if not domain:
        yield {}
        return
    for image_tuple in permutations(codomain, len(domain)):
        yield dict(zip(domain, image_tuple, strict=True))


def wick_value(
    units: dict[Edge, Unit],
    colour: int,
    other: int,
    nonrigid: set[int],
    heads: frozenset[int],
) -> int:
    ordered_heads = tuple(sorted(heads))
    total = 0
    for size in range(len(ordered_heads) + 1):
        for exposed_tuple in combinations(ordered_heads, size):
            exposed = frozenset(exposed_tuple)
            internal = heads - exposed
            if len(internal) % 2:
                continue
            core = haf_colour(units, internal, colour)
            if not core:
                continue
            for injection in injections(exposed_tuple, tuple(sorted(nonrigid))):
                flag_product = 1
                for head, tail in injection.items():
                    local, remote, weight = oriented_unit(units, tail, head)
                    if (local, remote) != (other, colour):
                        flag_product = 0
                        break
                    flag_product *= weight
                if not flag_product:
                    continue
                residue = (
                    frozenset(range(VERTEX_COUNT))
                    - heads
                    - frozenset(injection.values())
                )
                total += core * flag_product * haf_colour(units, residue, other)
    return total


def check_local_word_flips() -> None:
    square_original = (A, A, B, B)
    square_promoted = (B, B, A, A)
    assert all(
        original != promoted
        for original, promoted in zip(square_original, square_promoted, strict=True)
    )
    square_word_classes = ({0, 1}, {2, 3})
    assert square_word_classes == ({0, 1}, {2, 3})

    # Vertex order: u0,u1,v0,v2,w1,w2.
    hex_original = (0, 1, 0, 2, 1, 2)
    # Promoted pairs: u1-v2 in 0, u0-w2 in 1, v0-w1 in 2.
    hex_promoted = (1, 0, 2, 0, 2, 1)
    assert all(
        original != promoted
        for original, promoted in zip(hex_original, hex_promoted, strict=True)
    )
    preserving_pairs = {
        edge(0, 2): 0,
        edge(1, 4): 1,
        edge(3, 5): 2,
    }
    promoted_pairs = {
        edge(1, 3): 0,
        edge(0, 5): 1,
        edge(2, 4): 2,
    }
    assert preserving_pairs.keys().isdisjoint(promoted_pairs)


def check_edge_table_and_tensor() -> dict[Edge, Unit]:
    units = gadget()
    assert len(units) == VERTEX_COUNT * (VERTEX_COUNT - 1) // 2
    assert all(weight != 0 for _, _, weight in units.values())
    assert all(
        {left_colour, right_colour} <= {A, B}
        for left_colour, right_colour, _ in units.values()
    )

    matching_count = 0
    for matching in perfect_matchings(tuple(range(VERTEX_COUNT))):
        matching_count += 1
        word, _ = matching_term(units, matching)
        assert tuple(word.count(colour) % 2 for colour in range(3)) == (0, 0, 0)
    assert matching_count == 15
    assert tensor(units) == {(A,) * VERTEX_COUNT: -1}

    gauged = {
        pair: (left_colour, right_colour, -weight if U1 in pair else weight)
        for pair, (left_colour, right_colour, weight) in units.items()
    }
    assert tensor(gauged) == {(A,) * VERTEX_COUNT: 1}
    assert coefficient(units, (B,) * VERTEX_COUNT)[0] == 0
    assert coefficient(units, (THIRD,) * VERTEX_COUNT)[0] == 0
    return units


def check_separate_wordwise_cancellations(units: dict[Edge, Unit]) -> None:
    original_word = (A, A, B, B, B, B)
    normalized_word = (B, B, A, A, B, B)
    original_matching = tuple(sorted((edge(U1, V1), edge(U2, V2), edge(X, Y))))
    cross_matching = tuple(sorted((edge(U1, V2), edge(U2, V1), edge(X, Y))))
    normalized_matching = tuple(sorted((edge(U1, U2), edge(V1, V2), edge(X, Y))))
    pure_alternative = tuple(sorted((edge(U1, X), edge(U2, Y), edge(V1, V2))))

    assert matching_term(units, original_matching) == (original_word, 1)
    assert matching_term(units, cross_matching) == (original_word, -1)
    assert matching_term(units, normalized_matching) == (normalized_word, 1)
    assert matching_term(units, pure_alternative) == (normalized_word, -1)

    original_value, original_terms = coefficient(units, original_word)
    normalized_value, normalized_terms = coefficient(units, normalized_word)
    assert original_value == normalized_value == 0
    assert {term for term, _ in original_terms} == {
        original_matching,
        cross_matching,
    }
    assert {term for term, _ in normalized_terms} == {
        normalized_matching,
        pure_alternative,
    }


def check_rigid_head_wick_and_cuts(units: dict[Edge, Unit]) -> None:
    expected = {
        A: V_SHORE,
        B: U_SHORE,
        THIRD: set(),
    }
    for colour, shore in expected.items():
        assert nonrigid_set(units, colour) == shore

    all_vertices = frozenset(range(VERTEX_COUNT))
    for colour, other in ((A, B), (B, A)):
        nonrigid = expected[colour]
        rigid = set(range(VERTEX_COUNT)) - nonrigid
        for size in range(1, len(rigid) + 1):
            for chosen in combinations(sorted(rigid), size):
                heads = frozenset(chosen)
                assignment = tuple(
                    colour if vertex in heads else other
                    for vertex in range(VERTEX_COUNT)
                )
                direct, _ = coefficient(units, assignment)
                assert direct == 0
                assert wick_value(units, colour, other, nonrigid, heads) == direct

        for size in range(len(rigid)):
            for chosen in combinations(sorted(rigid), size):
                heads = frozenset(chosen)
                left = frozenset(nonrigid) | heads
                right = all_vertices - left
                product = haf_colour(units, left, colour) * haf_colour(
                    units, right, other
                )
                assignment = tuple(
                    colour if vertex in left else other
                    for vertex in range(VERTEX_COUNT)
                )
                direct, _ = coefficient(units, assignment)
                assert direct == product == 0

        # The unused third-colour version vanishes termwise.
        for size in range(1, len(rigid) + 1):
            for chosen in combinations(sorted(rigid), size):
                assert (
                    wick_value(
                        units,
                        colour,
                        THIRD,
                        nonrigid,
                        frozenset(chosen),
                    )
                    == 0
                )

        for size in range(len(rigid)):
            for chosen in combinations(sorted(rigid), size):
                heads = frozenset(chosen)
                left = frozenset(nonrigid) | heads
                right = all_vertices - left
                assert (
                    haf_colour(units, left, colour) * haf_colour(units, right, THIRD)
                    == 0
                )


def check_pure_active_relay() -> None:
    units = pure_active_relay_gadget()
    vertices = frozenset(range(VERTEX_COUNT))
    assert len(units) == VERTEX_COUNT * (VERTEX_COUNT - 1) // 2
    assert all(weight != 0 for _, _, weight in units.values())

    pure_matchings = {
        A: tuple(sorted((edge(2, 3), edge(0, 4), edge(1, 5)))),
        B: tuple(sorted((edge(0, 1), edge(2, 5), edge(3, 4)))),
        THIRD: tuple(sorted((edge(4, 5), edge(0, 3), edge(1, 2)))),
    }
    for colour, pure_matching in pure_matchings.items():
        value, terms = coefficient(units, (colour,) * VERTEX_COUNT)
        assert value == 1
        assert terms == [(pure_matching, 1)]
        for left, right in pure_matching:
            assert haf_colour(units, vertices - {left, right}, colour) == 1

    # Exact near-monochromatic active-deck rows.
    for vertex in range(VERTEX_COUNT):
        for pure_colour in range(3):
            for local_colour in range(3):
                total = 0
                for partner in range(VERTEX_COUNT):
                    if partner == vertex:
                        continue
                    local, remote, weight = oriented_unit(units, vertex, partner)
                    if (local, remote) == (local_colour, pure_colour):
                        total += weight * haf_colour(
                            units,
                            vertices - {vertex, partner},
                            pure_colour,
                        )
                assert total == int(local_colour == pure_colour)

    selected_word = (A, A, B, B, THIRD, THIRD)
    selected_value, selected_terms = coefficient(units, selected_word)
    first = tuple(sorted((edge(0, 2), edge(1, 3), edge(4, 5))))
    relay = tuple(sorted((edge(0, 5), edge(1, 3), edge(2, 4))))
    assert selected_value == 0
    assert selected_terms == [(first, 1), (relay, -1)]

    diagonal_terms = []
    for matching in perfect_matchings(tuple(range(VERTEX_COUNT))):
        word, _ = matching_term(units, matching)
        if word != selected_word:
            continue
        if all(units[pair][0] == units[pair][1] for pair in matching):
            diagonal_terms.append(matching)
    assert not diagonal_terms
    assert haf_colour(units, frozenset({0, 1}), A) == 0
    assert haf_colour(units, frozenset({2, 3}), B) == 0
    assert haf_colour(units, frozenset({4, 5}), THIRD) == 1

    failure_word = (A, A, B, B, A, B)
    failure_matching = tuple(sorted((edge(0, 4), edge(1, 3), edge(2, 5))))
    failure_value, failure_terms = coefficient(units, failure_word)
    assert failure_value == 1
    assert failure_terms == [(failure_matching, 1)]


def main() -> None:
    check_local_word_flips()
    units = check_edge_table_and_tensor()
    check_separate_wordwise_cancellations(units)
    check_rigid_head_wick_and_cuts(units)
    check_pure_active_relay()
    print("matrix-unit bridge word-synchronization sharpness checks: PASS")
    print("scope: two exact n=6 countermechanisms and local word-flip conventions")
    print("maximum_torus_root_number: 1")
    print("is_krenn_gu_witness: false")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
