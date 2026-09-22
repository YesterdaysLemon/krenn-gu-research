#!/usr/bin/env python3
"""Exact replay of the degree-two four-crossing macro control."""

from functools import lru_cache
from itertools import product


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
LANE_WEIGHTS = (1, 1, 1, -1)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


ALL_MATCHINGS = perfect_matchings(tuple(range(8)))


def active_edges(word):
    edges = {}
    crossing_edges = set()
    for component in (0, 1):
        offset = 4 * component
        for colour, pairs in MATCHINGS.items():
            for left, right in pairs:
                u, v = offset + left, offset + right
                if word[u] == word[v] == colour:
                    edges[(u, v)] = 1

    for colour_a in range(3):
        for colour_b in range(3):
            if colour_a == colour_b:
                continue
            for port, weight in enumerate(LANE_WEIGHTS):
                edge = (port, 4 + port)
                if word[port] == colour_a and word[4 + port] == colour_b:
                    edges[edge] = weight
                    crossing_edges.add(edge)
    return edges, crossing_edges


def coefficient(word):
    edges, crossing_edges = active_edges(word)
    terms = []
    for matching in ALL_MATCHINGS:
        weight = 1
        for edge in matching:
            if edge not in edges:
                break
            weight *= edges[edge]
        else:
            crossing_count = sum(edge in crossing_edges for edge in matching)
            terms.append((matching, weight, crossing_count))
    return sum(term[1] for term in terms), terms


def main():
    assert len(ALL_MATCHINGS) == 105

    # Reconstruct the actual state support.  Each state has one same-port edge
    # to each of the two opposite colours on the other component.
    support = set()
    degree = {
        (component, port, colour): 0
        for component in (0, 1)
        for port in range(4)
        for colour in range(3)
    }
    for port in range(4):
        for colour_a in range(3):
            for colour_b in range(3):
                if colour_a == colour_b:
                    continue
                edge = ((0, port, colour_a), (1, port, colour_b))
                support.add(edge)
                degree[edge[0]] += 1
                degree[edge[1]] += 1
    assert len(support) == 24
    assert set(degree.values()) == {2}
    for component in (0, 1):
        for port in range(4):
            for colour in range(3):
                state = (component, port, colour)
                incident = [edge for edge in support if state in edge]
                assert len(incident) == 2
                assert all(edge[0][2] != edge[1][2] for edge in incident)

    for colour_a in range(3):
        for colour_b in range(3):
            word = (colour_a,) * 4 + (colour_b,) * 4
            value, terms = coefficient(word)
            target = 1 if colour_a == colour_b else 0
            assert value == target
            if colour_a != colour_b:
                assert sorted(term[2] for term in terms) == [0, 4]
                assert sorted(term[1] for term in terms) == [-1, 1]

    separator = tuple(map(int, "00000011"))
    value, terms = coefficient(separator)
    assert value == -1
    assert len(terms) == 1
    assert terms[0][2] == 2

    # Full enumeration is a replay boundary, not an exhaustive theorem.
    errors = 0
    for word in product(range(3), repeat=8):
        value, _ = coefficient(word)
        target = 1 if len(set(word)) == 1 else 0
        errors += value != target
    assert errors == 1506

    print("perfect_matchings=105 words=6561")
    print("state_crossing_degree=2")
    print("pure_macros=3 mixed_macros=6 all_targets=PASS")
    print("mixed_macro_crossing_counts=0,4")
    print("separator=00000011 coefficient=-1 unique_matching=YES")
    print("full_source_error_words=1506")
    print("FOUR_CROSS_MACRO_CONTROL_PASS")


if __name__ == "__main__":
    main()
