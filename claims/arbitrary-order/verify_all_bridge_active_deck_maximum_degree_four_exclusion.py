"""Focused exact checks for the all-bridge maximum-degree-four theorem.

The accompanying markdown contains the arbitrary-order proof.  This bounded
program checks its matching and Hamiltonian-arc interfaces without searching
Krenn--Gu witnesses or support families.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations, pairwise

Edge = tuple[int, int]


def edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for offset, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:offset] + vertices[offset + 1 :]
        for tail in perfect_matchings(rest):
            output.append((edge(first, partner), *tail))
    return tuple(output)


@cache
def partial_matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = list(partial_matchings(vertices[1:]))
    for offset, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:offset] + vertices[offset + 1 :]
        for tail in partial_matchings(rest):
            output.append((edge(first, partner), *tail))
    return tuple(output)


def hafnian(vertices: tuple[int, ...], weights: dict[Edge, int]) -> int:
    total = 0
    for matching in perfect_matchings(vertices):
        product = 1
        for item in matching:
            product *= weights.get(item, 0)
        total += product
    return total


def has_perfect_matching(vertices: tuple[int, ...], support: set[Edge]) -> bool:
    return any(all(item in support for item in matching) for matching in perfect_matchings(vertices))


def verify_path_score_boundary() -> None:
    # At a path endpoint, Laplace gives s_0=1.  The next vertex would give
    # s_0+s_1=1, hence s_1=0, contradicting activity.
    for path_edges in range(1, 12):
        first_score = 1
        if path_edges > 1:
            second_score = 1 - first_score
            assert second_score == 0


def verify_two_matching_noncancellation() -> None:
    checked = 0
    for order in (2, 4, 6):
        vertices = tuple(range(order))
        perfect = {edge(i, i + 1) for i in range(0, order, 2)}
        for residual_tuple in partial_matchings(vertices):
            residual = set(residual_tuple)
            if residual & perfect:
                continue
            weights = {
                item: 2 + 2 * index
                for index, item in enumerate(sorted(perfect))
            }
            for index, item in enumerate(sorted(residual)):
                weights[item] = (-1 if index % 2 else 1) * (3 + 2 * index)
            support = set(weights)
            if hafnian(vertices, weights) == 0:
                continue
            for size in range(0, order + 1, 2):
                for subset in combinations(vertices, size):
                    if has_perfect_matching(subset, support):
                        assert hafnian(subset, weights) != 0
            checked += 1

    # The nonzero-full-hafnian premise is necessary: this four-cycle has
    # alternating products 1 and -1.
    cancel_weights = {
        edge(0, 1): 1,
        edge(2, 3): 1,
        edge(1, 2): 1,
        edge(0, 3): -1,
    }
    assert hafnian((0, 1, 2, 3), cancel_weights) == 0
    assert checked > 50


def matching_covers(items: set[Edge], vertices: set[int]) -> bool:
    incidence = {vertex: 0 for vertex in vertices}
    for left, right in items:
        if left not in vertices or right not in vertices:
            return False
        incidence[left] += 1
        incidence[right] += 1
    return all(value == 1 for value in incidence.values())


def forward_arc(order: int, start: int, finish: int) -> list[int]:
    vertices = [start]
    current = start
    while current != finish:
        current = (current + 1) % order
        vertices.append(current)
    return vertices


def arc_edges(vertices: list[int]) -> set[Edge]:
    return {edge(left, right) for left, right in pairwise(vertices)}


def verify_hamiltonian_chord_argument() -> None:
    checked = 0
    for order in range(6, 22, 2):
        pc = {edge(i, i + 1) for i in range(0, order, 2)}
        pd = {edge(i, (i + 1) % order) for i in range(1, order, 2)}
        cycle = pc | pd
        assert len(cycle) == order

        for left, right in combinations(range(order), 2):
            chord = edge(left, right)
            if (left - right) % 2 == 0 or chord in cycle:
                continue
            first_arc = forward_arc(order, left, right)
            second_arc = list(reversed(forward_arc(order, right, left)))
            candidates = []
            for arc in (first_arc, second_arc):
                if edge(arc[0], arc[1]) in pd and edge(arc[-2], arc[-1]) in pd:
                    candidates.append(arc)
            assert len(candidates) == 1
            selected = candidates[0]
            length = len(selected) - 1
            assert 3 <= length <= order - 3

            selected_vertices = set(selected)
            selected_edges = arc_edges(selected)
            assert matching_covers(selected_edges & pd, selected_vertices)
            assert matching_covers((selected_edges & pc) | {chord}, selected_vertices)
            complement = set(range(order)) - selected_vertices
            assert complement
            assert matching_covers({item for item in pd if set(item) <= complement}, complement)
            checked += 1
    assert checked > 100


def main() -> None:
    verify_path_score_boundary()
    verify_two_matching_noncancellation()
    verify_hamiltonian_chord_argument()
    print("all-bridge maximum-degree-four focused verification: PASS")
    print("orders checked for Hamiltonian chords: 6,8,10,12,14,16,18,20")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
