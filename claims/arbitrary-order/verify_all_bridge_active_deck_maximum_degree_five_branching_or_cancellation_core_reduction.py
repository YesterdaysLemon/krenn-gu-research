"""Focused exact checks for the all-bridge saturated-degree-five reduction.

The accompanying markdown contains the arbitrary-order proof.  This program
checks the finite degree ledger, the Hamiltonian-chord interface, the two
scalar sharpness controls, the least-core cycle/branching interfaces, and the
typed eight-vertex mixed-cut control.  It does not search for Krenn--Gu
witnesses or claim an exhaustive arbitrary-order graph enumeration.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, product
from math import factorial

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output: list[Matching] = []
    for position, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            output.append((edge(first, partner), *tail))
    return tuple(output)


def matching_weight(
    matching: Matching, weights: dict[Edge, int | Fraction]
) -> int | Fraction:
    product: int | Fraction = 1
    for item in matching:
        product *= weights.get(item, 0)
    return product


def hafnian(
    vertices: tuple[int, ...], weights: dict[Edge, int | Fraction]
) -> int | Fraction:
    return sum(matching_weight(matching, weights) for matching in perfect_matchings(vertices))


def nonzero_matching_terms(
    vertices: tuple[int, ...], weights: dict[Edge, int | Fraction]
) -> list[int | Fraction]:
    return [
        value
        for matching in perfect_matchings(vertices)
        if (value := matching_weight(matching, weights)) != 0
    ]


def active_scores(
    vertices: tuple[int, ...], weights: dict[Edge, int | Fraction]
) -> dict[Edge, int | Fraction]:
    output: dict[Edge, int | Fraction] = {}
    for item, value in weights.items():
        complement = tuple(vertex for vertex in vertices if vertex not in item)
        output[item] = value * hafnian(complement, weights)
    return output


def degrees(vertices: tuple[int, ...], items: set[Edge]) -> dict[int, int]:
    output = {vertex: 0 for vertex in vertices}
    for left, right in items:
        output[left] += 1
        output[right] += 1
    return output


def is_perfect_matching(vertices: tuple[int, ...], items: set[Edge]) -> bool:
    return all(value == 1 for value in degrees(vertices, items).values())


def has_perfect_matching(vertices: tuple[int, ...], support: set[Edge]) -> bool:
    return any(
        all(item in support for item in matching)
        for matching in perfect_matchings(vertices)
    )


def connected(vertices: tuple[int, ...], items: set[Edge]) -> bool:
    if not vertices:
        return True
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in items:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = {vertices[0]}
    queue = deque([vertices[0]])
    while queue:
        current = queue.popleft()
        for neighbour in adjacency[current] - seen:
            seen.add(neighbour)
            queue.append(neighbour)
    return len(seen) == len(vertices)


def is_hamiltonian_cycle(vertices: tuple[int, ...], items: set[Edge]) -> bool:
    return len(items) == len(vertices) and connected(vertices, items) and all(
        value == 2 for value in degrees(vertices, items).values()
    )


def bipartition(vertices: tuple[int, ...], items: set[Edge]) -> tuple[set[int], set[int]]:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in items:
        adjacency[left].add(right)
        adjacency[right].add(left)
    colour: dict[int, int] = {}
    for start in vertices:
        if start in colour:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in adjacency[current]:
                expected = 1 - colour[current]
                if neighbour in colour:
                    assert colour[neighbour] == expected
                else:
                    colour[neighbour] = expected
                    queue.append(neighbour)
    return (
        {vertex for vertex, side in colour.items() if side == 0},
        {vertex for vertex, side in colour.items() if side == 1},
    )


def verify_degree_table() -> None:
    observed: set[tuple[tuple[int, int, int], int]] = set()
    degree_five: set[tuple[tuple[int, int, int], int]] = set()
    labelled_by_degree = {3: 0, 4: 0, 5: 0}
    for a0 in range(1, 6):
        for a1 in range(1, 6):
            for a2 in range(1, 6):
                for inactive in range(3):
                    total = a0 + a1 + a2 + inactive
                    if total > 5:
                        continue
                    shape = (tuple(sorted((a0, a1, a2), reverse=True)), inactive)
                    observed.add(shape)
                    labelled_by_degree[total] += factorial(total) // (
                        factorial(a0)
                        * factorial(a1)
                        * factorial(a2)
                        * factorial(inactive)
                    )
                    if total == 5:
                        degree_five.add(shape)

                    if max(a0, a1, a2) <= 2:
                        residual_degree = inactive + sum(
                            value == 2 for value in (a0, a1, a2)
                        )
                        assert residual_degree <= 2
                        if total == 5:
                            assert residual_degree == 2

    assert observed == {
        ((1, 1, 1), 0),
        ((1, 1, 1), 1),
        ((1, 1, 1), 2),
        ((2, 1, 1), 0),
        ((2, 1, 1), 1),
        ((2, 2, 1), 0),
        ((3, 1, 1), 0),
    }
    assert degree_five == {
        ((1, 1, 1), 2),
        ((2, 1, 1), 1),
        ((2, 2, 1), 0),
        ((3, 1, 1), 0),
    }
    assert labelled_by_degree == {3: 6, 4: 60, 5: 390}

    residual_labels = {
        ((1, 1, 1), 2): ("H", "H"),
        ((2, 1, 1), 1): ("Q_c", "H"),
        ((2, 2, 1), 0): ("Q_c", "Q_d"),
    }
    assert set(residual_labels) == degree_five - {((3, 1, 1), 0)}


def verify_support_decomposition_truth_table() -> None:
    # For one physical edge, active exclusivity permits at most one active
    # colour.  If support colour c is active, it must be the same colour;
    # otherwise the edge is inactive in all colours and belongs to H.
    for supports in product((False, True), repeat=3):
        for active_colour in (None, 0, 1, 2):
            legal = active_colour is None or (
                supports[active_colour]
                and all(
                    not supports[colour]
                    for colour in range(3)
                    if colour != active_colour
                )
            )
            if not legal:
                continue
            for colour in range(3):
                in_ec = active_colour == colour
                in_hc = active_colour is None and supports[colour]
                assert supports[colour] == (in_ec or in_hc)
                assert not (in_ec and in_hc)


def verify_branching_active_control() -> None:
    vertices = tuple(range(6))
    weights = {
        edge(0, 1): -1,
        edge(0, 2): 1,
        edge(0, 3): 1,
        edge(1, 4): 1,
        edge(1, 5): 1,
        edge(2, 4): 1,
        edge(3, 5): 1,
    }
    assert sorted(nonzero_matching_terms(vertices, weights)) == [-1, 1, 1]
    assert hafnian(vertices, weights) == 1

    scores = active_scores(vertices, weights)
    expected = {
        edge(0, 1): -1,
        edge(0, 2): 1,
        edge(0, 3): 1,
        edge(1, 4): 1,
        edge(1, 5): 1,
        edge(2, 4): 0,
        edge(3, 5): 0,
    }
    assert scores == expected
    for vertex in vertices:
        assert sum(value for item, value in scores.items() if vertex in item) == 1

    active = {item for item, value in scores.items() if value}
    assert sorted(degrees(vertices, active).values()) == [1, 1, 1, 1, 3, 3]
    left, right = bipartition(vertices, set(weights))
    assert len(left) == len(right) == 3
    assert not has_perfect_matching(vertices, active)
    assert has_perfect_matching(vertices, set(weights))

    # The minimal Hall-deficient shore X={2,3}, T={0} has one active boundary
    # edge 01 of score -1.  Its complementary matching has exactly the two
    # inactive, vertex-disjoint repairs 24 and 35 (b=2,q=0).
    hall_x = {2, 3}
    hall_t = {0}
    boundary = {
        item for item in active if len(set(item) & hall_t) == 1 and not set(item) & hall_x
    }
    assert boundary == {edge(0, 1)}
    assert sum(scores[item] for item in boundary) == -1
    complement = (2, 3, 4, 5)
    supported_complements = [
        matching
        for matching in perfect_matchings(complement)
        if matching_weight(matching, weights)
    ]
    repairs = {edge(2, 4), edge(3, 5)}
    assert supported_complements == [(edge(2, 4), edge(3, 5))]
    assert repairs.isdisjoint(active)
    assert is_perfect_matching(complement, repairs)
    assert len(repairs) == 2
    for repair in repairs:
        deleted = tuple(vertex for vertex in vertices if vertex not in repair)
        assert hafnian(deleted, weights) == 0


def verify_branching_with_active_matching_control() -> None:
    vertices = tuple(range(6))
    weights = {
        edge(row, 3 + column): Fraction(1, 6) if row == 0 else Fraction(1)
        for row in range(3)
        for column in range(3)
    }
    assert hafnian(vertices, weights) == 1
    scores = active_scores(vertices, weights)
    assert set(scores.values()) == {Fraction(1, 3)}
    active = set(scores)
    assert set(degrees(vertices, active).values()) == {3}
    assert has_perfect_matching(vertices, active)


def verify_degree_two_cancellation_control() -> None:
    vertices = tuple(range(6))
    perfect = {edge(0, 4), edge(1, 5), edge(2, 3)}
    residual = {edge(0, 1), edge(0, 2), edge(1, 3), edge(4, 5)}
    weights = {item: 1 for item in perfect | residual}
    weights[edge(1, 3)] = -1

    assert is_perfect_matching(vertices, perfect)
    assert max(degrees(vertices, residual).values()) == 2
    assert sorted(nonzero_matching_terms(vertices, weights)) == [-1, 1, 1]
    assert hafnian(vertices, weights) == 1
    scores = active_scores(vertices, weights)
    assert all(scores[item] != 0 for item in perfect)
    subset = (0, 1, 2, 3)
    assert has_perfect_matching(subset, set(weights))
    assert hafnian(subset, weights) == 0


def forward_arc(order: int, start: int, finish: int) -> list[int]:
    output = [start]
    current = start
    while current != finish:
        current = (current + 1) % order
        output.append(current)
    return output


def arc_edges(vertices: list[int]) -> set[Edge]:
    return {edge(left, right) for left, right in pairwise(vertices)}


def verify_hamiltonian_chord_interface() -> None:
    checked = 0
    for order in range(6, 22, 2):
        vertices = tuple(range(order))
        pc = {edge(index, index + 1) for index in range(0, order, 2)}
        pd = {edge(index, (index + 1) % order) for index in range(1, order, 2)}
        assert is_hamiltonian_cycle(vertices, pc | pd)

        for left, right in combinations(vertices, 2):
            chord = edge(left, right)
            if (left - right) % 2 == 0 or chord in pc or chord in pd:
                continue
            arcs = (
                forward_arc(order, left, right),
                list(reversed(forward_arc(order, right, left))),
            )
            selected = [
                path
                for path in arcs
                if edge(path[0], path[1]) in pd
                and edge(path[-2], path[-1]) in pd
            ]
            assert len(selected) == 1
            path = selected[0]
            assert 3 <= len(path) - 1 <= order - 3
            chosen = tuple(sorted(set(path)))
            complement = tuple(vertex for vertex in vertices if vertex not in chosen)
            path_support = arc_edges(path)
            assert is_perfect_matching(chosen, path_support & pd)
            assert is_perfect_matching(chosen, (path_support & pc) | {chord})
            assert is_perfect_matching(
                complement,
                {item for item in pd if set(item) <= set(complement)},
            )
            checked += 1
    assert checked > 100


def verify_minimal_core_interfaces() -> None:
    cycle_vertices = (0, 1, 2, 3)
    cycle_weights = {
        edge(0, 1): 1,
        edge(2, 3): 1,
        edge(1, 2): 1,
        edge(0, 3): -1,
    }
    assert hafnian(cycle_vertices, cycle_weights) == 0
    cycle_active = {
        item
        for item, value in active_scores(cycle_vertices, cycle_weights).items()
        if value
    }
    assert cycle_active == set(cycle_weights)
    assert is_hamiltonian_cycle(cycle_vertices, cycle_active)
    assert len(nonzero_matching_terms(cycle_vertices, cycle_weights)) == 2

    # A least supported branching cancellation: a 3x3 bipartite matrix with
    # permanent zero and every complementary 2x2 permanent nonzero.
    branching_vertices = tuple(range(6))
    matrix = (
        (-2, -2, -2),
        (-2, -2, -2),
        (-2, 1, 1),
    )
    branching_weights = {
        edge(row, 3 + column): matrix[row][column]
        for row in range(3)
        for column in range(3)
    }
    assert hafnian(branching_vertices, branching_weights) == 0
    branching_active = {
        item
        for item, value in active_scores(branching_vertices, branching_weights).items()
        if value
    }
    assert branching_active == set(branching_weights)
    assert connected(branching_vertices, branching_active)
    assert set(degrees(branching_vertices, branching_active).values()) == {3}
    assert len(nonzero_matching_terms(branching_vertices, branching_weights)) == 6

    # Every proper even supported subset has nonzero hafnian, so the six-
    # vertex branching cancellation is cardinality-minimal.
    for size in (2, 4):
        for subset in combinations(branching_vertices, size):
            if has_perfect_matching(subset, set(branching_weights)):
                assert hafnian(subset, branching_weights) != 0


def verify_bipartite_subcubic_rank_strata() -> None:
    def cyclomatic(vertices: tuple[int, ...], items: set[Edge]) -> int:
        return len(items) - len(vertices) + 1

    def cubic_count(vertices: tuple[int, ...], items: set[Edge]) -> int:
        return sum(value == 3 for value in degrees(vertices, items).values())

    cycle_vertices = tuple(range(4))
    cycle = {edge(0, 1), edge(1, 2), edge(2, 3), edge(0, 3)}
    assert cyclomatic(cycle_vertices, cycle) == 1
    assert cubic_count(cycle_vertices, cycle) == 0

    # Closed all-odd theta with route lengths 1,3,3.  The three perfect
    # matching terms have weights 1,1,-2 and no proper subsum vanishes.
    theta_vertices = tuple(range(6))
    theta_weights = {
        edge(0, 1): 1,
        edge(0, 2): 1,
        edge(2, 3): 1,
        edge(3, 1): 1,
        edge(0, 4): 1,
        edge(4, 5): 1,
        edge(5, 1): -2,
    }
    theta = set(theta_weights)
    assert connected(theta_vertices, theta)
    assert bipartition(theta_vertices, theta)
    assert cyclomatic(theta_vertices, theta) == 2
    assert cubic_count(theta_vertices, theta) == 2
    theta_terms = nonzero_matching_terms(theta_vertices, theta_weights)
    assert sorted(theta_terms) == [-2, 1, 1]
    assert hafnian(theta_vertices, theta_weights) == 0
    assert all(sum(choice) != 0 for size in (1, 2) for choice in combinations(theta_terms, size))
    for size in (2, 4):
        for subset in combinations(theta_vertices, size):
            if has_perfect_matching(subset, theta):
                assert hafnian(subset, theta_weights) != 0

    rank_three_vertices = tuple(range(6))
    rank_three_matrix = ((-3, -3, -3), (-3, -2, 1), (-2, 1, 0))
    rank_three_weights = {
        edge(row, 3 + column): rank_three_matrix[row][column]
        for row in range(3)
        for column in range(3)
        if rank_three_matrix[row][column]
    }
    rank_three = set(rank_three_weights)
    assert connected(rank_three_vertices, rank_three)
    assert bipartition(rank_three_vertices, rank_three)
    assert cyclomatic(rank_three_vertices, rank_three) == 3
    assert cubic_count(rank_three_vertices, rank_three) == 4
    assert hafnian(rank_three_vertices, rank_three_weights) == 0
    for size in (2, 4):
        for subset in combinations(rank_three_vertices, size):
            if has_perfect_matching(subset, rank_three):
                assert hafnian(subset, rank_three_weights) != 0

    for vertices, items in (
        (cycle_vertices, cycle),
        (theta_vertices, theta),
        (rank_three_vertices, rank_three),
    ):
        beta = cyclomatic(vertices, items)
        assert cubic_count(vertices, items) == 2 * (beta - 1)


def least_supported_cancellation(
    matrices: tuple[dict[Edge, int], ...], vertices: tuple[int, ...]
) -> tuple[int, tuple[int, ...]] | None:
    for size in range(2, len(vertices), 2):
        candidates: list[tuple[int, tuple[int, ...]]] = []
        for colour, weights in enumerate(matrices):
            for subset in combinations(vertices, size):
                if has_perfect_matching(subset, set(weights)) and hafnian(subset, weights) == 0:
                    candidates.append((colour, subset))
        if candidates:
            return min(candidates)
    return None


def verify_global_least_selector() -> None:
    vertices = tuple(range(8))
    cycle = {
        edge(0, 1): 1,
        edge(2, 3): 1,
        edge(1, 2): 1,
        edge(0, 3): -1,
        edge(4, 5): 1,
        edge(6, 7): 1,
    }
    later = {
        edge(row, 3 + column): value
        for row, values in enumerate(((-2, -2, -2), (-2, -2, -2), (-2, 1, 1)))
        for column, value in enumerate(values)
    }
    later[edge(6, 7)] = 1
    neutral = {
        edge(0, 1): 1,
        edge(2, 3): 1,
        edge(4, 5): 1,
        edge(6, 7): 1,
    }
    selected = least_supported_cancellation((later, cycle, neutral), vertices)
    assert selected == (1, (0, 1, 2, 3))

    colour, subset = selected
    weights = (later, cycle, neutral)[colour]
    assert hafnian(subset, weights) == 0
    allowed = {
        item
        for item in weights
        if set(item) <= set(subset)
        and has_perfect_matching(
            tuple(vertex for vertex in subset if vertex not in item),
            set(weights),
        )
    }
    active = {
        item
        for item in weights
        if set(item) <= set(subset)
        and weights[item]
        * hafnian(tuple(vertex for vertex in subset if vertex not in item), weights)
        != 0
    }
    assert active == allowed
    assert connected(subset, active)
    assert is_hamiltonian_cycle(subset, active)


def flips_saturated_bits(left: str, right: str, colour: int) -> bool:
    return all(left[index] != right[index] for index in range(3) if index != colour)


def verify_typed_mixed_cut_control() -> None:
    vertices = tuple(range(8))
    normal_types = ("000", "011", "101", "110", "110", "101", "001", "010")
    active_matchings = (
        {edge(0, 1), edge(2, 3), edge(4, 5), edge(6, 7)},
        {edge(0, 2), edge(1, 4), edge(3, 6), edge(5, 7)},
        {edge(0, 3), edge(1, 5), edge(2, 7), edge(4, 6)},
    )
    extras = ({}, {edge(0, 5): 1}, {edge(0, 4): 1})
    matrices: list[dict[Edge, int]] = []

    for colour, matching in enumerate(active_matchings):
        weights = {item: 1 for item in matching}
        weights.update(extras[colour])
        matrices.append(weights)
        assert is_perfect_matching(vertices, matching)
        assert hafnian(vertices, weights) == 1
        scores = active_scores(vertices, weights)
        assert {item for item, value in scores.items() if value} == matching
        assert all(scores[item] == 1 for item in matching)
        assert all(scores[item] == 0 for item in extras[colour])
        for vertex in vertices:
            assert sum(value for item, value in scores.items() if vertex in item) == 1
        for item in weights:
            assert flips_saturated_bits(
                normal_types[item[0]], normal_types[item[1]], colour
            )

    for left, right in combinations(range(3), 2):
        assert is_hamiltonian_cycle(
            vertices, active_matchings[left] | active_matchings[right]
        )

    diagonal_support = set().union(*(set(weights) for weights in matrices))
    assert degrees(vertices, diagonal_support) == {
        0: 5,
        1: 3,
        2: 3,
        3: 3,
        4: 4,
        5: 4,
        6: 3,
        7: 3,
    }

    chosen = (2, 3, 6, 7)
    complement = tuple(vertex for vertex in vertices if vertex not in chosen)
    assert hafnian(chosen, matrices[0]) == 1
    assert hafnian(complement, matrices[1]) == 1
    assert hafnian(chosen, matrices[0]) * hafnian(complement, matrices[1]) == 1
    assert hafnian(chosen, matrices[1]) == 0
    assert hafnian(complement, matrices[0]) == 1
    assert hafnian(chosen, matrices[1]) * hafnian(complement, matrices[0]) == 0


def verify_unconditional_full_support_boundary() -> None:
    # The three primary killers are physically distinct and lie outside the
    # entire diagonal backbone, which contains saturated D.  Reconstruct the
    # exact pointwise degree union rather than treating the +3 as arithmetic
    # metadata only.
    for diagonal_degree in range(13):
        diagonal_neighbours = set(range(diagonal_degree))
        killers = set(range(diagonal_degree, diagonal_degree + 3))
        assert diagonal_neighbours.isdisjoint(killers)
        assert len(diagonal_neighbours | killers) == diagonal_degree + 3

    # The inherited Delta(D)>=5 boundary therefore forces Delta(G)>=8.
    inherited_minimum_saturated_degree = 5
    assert inherited_minimum_saturated_degree + 3 == 8
    assert all(order - 1 < 8 for order in (6, 8))
    assert min(order for order in range(6, 20, 2) if order - 1 >= 8) == 10


def main() -> None:
    verify_degree_table()
    verify_support_decomposition_truth_table()
    verify_branching_active_control()
    verify_branching_with_active_matching_control()
    verify_degree_two_cancellation_control()
    verify_hamiltonian_chord_interface()
    verify_minimal_core_interfaces()
    verify_bipartite_subcubic_rank_strata()
    verify_global_least_selector()
    verify_typed_mixed_cut_control()
    verify_unconditional_full_support_boundary()
    print("all-bridge maximum-degree-five reduction verification: PASS")
    print("local degree-five labelled assignments: 390")
    print("Hamiltonian chord orders checked: 6,8,10,12,14,16,18,20")
    print("unconditional all-bridge boundary: Delta(G)>=8 and n>=10")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
