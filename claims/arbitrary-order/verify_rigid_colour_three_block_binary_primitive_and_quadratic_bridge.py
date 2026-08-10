"""Focused exact checks for the rigid-colour three-block theorem.

The arbitrary-order convolution and bridge proofs are written in the owning
note.  This script audits their finite combinatorics and sharp examples.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from math import comb


def matchings(vertices: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not vertices:
        return [()]
    u = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            answer.append(((u, v),) + tail)
    return answer


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def sparse_matchings(n: int, support: set[tuple[int, int]]):
    def rec(vertices: tuple[int, ...]):
        if not vertices:
            return [()]
        u = vertices[0]
        answer = []
        for index in range(1, len(vertices)):
            v = vertices[index]
            if edge(u, v) not in support:
                continue
            rest = vertices[1:index] + vertices[index + 1 :]
            for tail in rec(rest):
                answer.append((edge(u, v),) + tail)
        return answer

    return rec(tuple(range(n)))


def check_convolution_multiplicity() -> None:
    for n in (4, 6, 8):
        vertices = tuple(range(n))
        full = {frozenset(matching) for matching in matchings(vertices)}
        m = n // 2
        for k in range(m + 1):
            counts: Counter[frozenset[tuple[int, int]]] = Counter()
            for subset in combinations(vertices, 2 * k):
                left_vertices = tuple(subset)
                right_vertices = tuple(v for v in vertices if v not in subset)
                for left in matchings(left_vertices):
                    for right in matchings(right_vertices):
                        counts[frozenset(left + right)] += 1
            assert set(counts) == full
            assert set(counts.values()) == {comb(m, k)}


BLOCKS = ((0, 1), (2, 3), (4, 5))


def block_of(vertex: int) -> int:
    return vertex // 2


def cell_edge(matching, first: int, second: int):
    for u, v in matching:
        if {block_of(u), block_of(v)} == {first, second}:
            return edge(u, v)
    raise AssertionError("missing cell edge")


def assignment(matching, block: int, neighbour: int) -> int:
    u, v = cell_edge(matching, block, neighbour)
    return u if block_of(u) == block else v


def block_types(first, second):
    types = []
    for block in range(3):
        neighbours = [other for other in range(3) if other != block]
        agreements = [
            assignment(first, block, other) == assignment(second, block, other)
            for other in neighbours
        ]
        assert agreements[0] == agreements[1]
        types.append("S" if agreements[0] else "D")
    return tuple(types)


def oriented_labels(labels, u, v):
    a, b, weight = labels[edge(u, v)]
    return (a, b, weight) if u < v else (b, a, weight)


def coefficient(labels, word):
    total = 0
    active = 0
    for matching in matchings(tuple(range(len(word)))):
        weight = 1
        for u, v in matching:
            if edge(u, v) not in labels:
                weight = 0
                break
            a, b, scalar = oriented_labels(labels, u, v)
            if (word[u], word[v]) != (a, b):
                weight = 0
                break
            weight *= scalar
        if weight:
            total += weight
            active += 1
    return total, active


def add_oriented(labels, u, v, left, right, weight):
    key = edge(u, v)
    if u < v:
        record = (left, right, weight)
    else:
        record = (right, left, weight)
    assert key not in labels
    labels[key] = record


def completed_six_system(pure_a, pure_b):
    labels = {}
    assert set(pure_a).isdisjoint(pure_b)
    for u, v in pure_a:
        add_oriented(labels, u, v, 0, 0, 1)
    for u, v in pure_b:
        add_oriented(labels, u, v, 1, 1, 1)
    types = block_types(pure_a, pure_b)
    for first, second in combinations(range(3), 2):
        ea = cell_edge(pure_a, first, second)
        eb = cell_edge(pure_b, first, second)
        if types[first] == types[second] == "D":
            xa = ea[0] if block_of(ea[0]) == first else ea[1]
            ya = ea[1] if block_of(ea[1]) == second else ea[0]
            xb = eb[0] if block_of(eb[0]) == first else eb[1]
            yb = eb[1] if block_of(eb[1]) == second else eb[0]
            add_oriented(labels, xa, yb, 0, 1, 1)
            add_oriented(labels, xb, ya, 1, 0, -1)
    return labels, types


def check_order_six_classification() -> None:
    tripartite = {
        edge(u, v)
        for first, second in combinations(range(3), 2)
        for u in BLOCKS[first]
        for v in BLOCKS[second]
    }
    pure_matchings = sparse_matchings(6, tripartite)
    checked = 0
    type_counts = Counter()
    for pure_a in pure_matchings:
        for pure_b in pure_matchings:
            if not set(pure_a).isdisjoint(pure_b):
                continue
            labels, types = completed_six_system(pure_a, pure_b)
            assert types.count("S") <= 1
            type_counts[types.count("S")] += 1
            checked += 1
            values = {}
            for word in product(range(2), repeat=6):
                value, active = coefficient(labels, word)
                if value:
                    values[word] = (value, active)
            assert values[(0,) * 6][0] == 1
            assert values[(1,) * 6][0] == 1
            forbidden = {word: item for word, item in values.items() if len(set(word)) > 1}
            expected = 6 if "S" not in types else 2
            assert len(forbidden) == expected
            assert all(active == 1 and value != 0 for value, active in forbidden.values())
    assert checked > 0 and set(type_counts) == {0, 1}


def check_order_four_boundary() -> None:
    matchings_four = matchings((0, 1, 2, 3))
    labels = {}
    for colour, matching in enumerate(matchings_four):
        for u, v in matching:
            add_oriented(labels, u, v, colour, colour, 1)
    assert len(labels) == 6
    values = {word: coefficient(labels, word)[0] for word in product(range(3), repeat=4)}
    assert {word: value for word, value in values.items() if value} == {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 1,
        (2, 2, 2, 2): 1,
    }


def shift_matching(m: int, shift: int):
    return tuple(edge(i, m + (i + shift) % m) for i in range(m))


def matching_word(matching, colours):
    word = [None] * (2 * (len(matching)))
    for current in matching:
        colour = colours[current]
        for vertex in current:
            word[vertex] = colour
    return tuple(word)


def check_shift_boundaries() -> None:
    for m in (3, 5, 7):
        selected = [shift_matching(m, shift) for shift in range(3)]
        assert all(set(selected[i]).isdisjoint(selected[j]) for i, j in combinations(range(3), 2))
        for i, j in combinations(range(3), 2):
            pair_support = set(selected[i]) | set(selected[j])
            assert set(sparse_matchings(2 * m, pair_support)) == {selected[i], selected[j]}

        binary_support = set(selected[1]) | set(selected[2])
        assert set(sparse_matchings(2 * m, binary_support)) == {selected[1], selected[2]}

        colours = {
            current: colour
            for colour, matching in enumerate(selected)
            for current in matching
        }
        all_support = set().union(*map(set, selected))
        mixed = []
        for current in sparse_matchings(2 * m, all_support):
            word = matching_word(current, colours)
            if len(set(word)) > 1:
                mixed.append((current, word))
        assert mixed
        current, _ = mixed[0]
        z_edges = set(current) & set(selected[0])
        assert z_edges and z_edges != set(current)
        deleted = {vertex for current_edge in z_edges for vertex in current_edge}
        remaining = tuple(vertex for vertex in range(2 * m) if vertex not in deleted)
        induced_support = {
            current_edge
            for current_edge in binary_support
            if all(vertex in remaining for vertex in current_edge)
        }
        # Reconstruct directly on the surviving vertices.
        def rem_rec(vertices, support=induced_support):
            if not vertices:
                return [()]
            u = vertices[0]
            answer = []
            for index in range(1, len(vertices)):
                v = vertices[index]
                if edge(u, v) not in support:
                    continue
                for tail in rem_rec(vertices[1:index] + vertices[index + 1 :]):
                    answer.append((edge(u, v),) + tail)
            return answer

        assert len(rem_rec(remaining)) == 1


def main() -> None:
    check_convolution_multiplicity()
    check_order_six_classification()
    check_order_four_boundary()
    check_shift_boundaries()
    print("rigid-colour three-block/quadratic-bridge focused checks: PASS")
    print("scope: bounded combinatorial audits; arbitrary-order proof is written")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
