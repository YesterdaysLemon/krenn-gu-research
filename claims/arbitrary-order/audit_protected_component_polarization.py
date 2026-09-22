"""Independent finite audit of the protected-K4 polarization identities.

This standard-library checker reconstructs the 81 local color words directly.
It checks the 48 selector rows, 30 transversal rows, three pure rows, and the
6+12+3 connected-quartic sector decomposition.  It imports neither the
primary elimination verifier nor generated receipts and writes no files.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
import json


MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
LABEL = {
    tuple(sorted(edge)): color
    for color, matching in enumerate(MATCHINGS)
    for edge in matching
}
EDGES = tuple(sorted(LABEL))


def complement(edge):
    return tuple(vertex for vertex in range(4) if vertex not in edge)


def compatible_edges(word):
    return tuple(
        edge
        for edge in EDGES
        if word[edge[0]] == word[edge[1]] == LABEL[edge]
    )


def leg_degree(left, right):
    degree = [0, 0, 0, 0]
    for vertex in (*left, *right):
        degree[vertex] += 1
    return tuple(degree)


def verify():
    word_types = Counter()
    compatibility = Counter()
    selector_rows = 0
    transversal_rows = 0
    pure_rows = 0

    for word in product(range(3), repeat=4):
        counts = sorted(Counter(word).values(), reverse=True)
        word_types["+".join(map(str, counts))] += 1
        compatible = compatible_edges(word)
        compatibility[len(compatible)] += 1
        if len(set(word)) == 1:
            color = word[0]
            assert set(compatible) == {
                tuple(sorted(edge)) for edge in MATCHINGS[color]
            }
            pure_rows += 1
        elif compatible:
            assert len(compatible) == 1
            edge = compatible[0]
            other = complement(edge)
            assert (word[other[0]], word[other[1]]) != (LABEL[edge], LABEL[edge])
            selector_rows += 1
        else:
            transversal_rows += 1

    assert word_types == {"4": 3, "3+1": 24, "2+2": 18, "2+1+1": 36}
    assert compatibility == {2: 3, 1: 48, 0: 30}
    assert (selector_rows, transversal_rows, pure_rows) == (48, 30, 3)

    # Directly expand L4=K4/3-K2^2/18 with one token for each protected edge.
    # Squares receive -1/18.  Distinct products receive -2/18=-1/9, except
    # the three complementary pairs, which also receive +1/3 from K4.
    sectors = Counter()
    coefficients = Counter()
    cross_partition_pairs = 0
    for i, edge in enumerate(EDGES):
        coefficient = Fraction(-1, 18)
        assert sorted(leg_degree(edge, edge)) == [0, 0, 2, 2]
        sectors["repeated-edge"] += 1
        coefficients["repeated-edge", coefficient] += 1
        for other in EDGES[i + 1 :]:
            if set(edge).isdisjoint(other):
                assert LABEL[edge] == LABEL[other]
                assert tuple(sorted(other)) == tuple(sorted(complement(edge)))
                coefficient = Fraction(1, 3) - Fraction(1, 9)
                sector = "transversal-complement"
                assert leg_degree(edge, other) == (1, 1, 1, 1)
            else:
                assert LABEL[edge] != LABEL[other]
                assert len(set(edge) & set(other)) == 1
                coefficient = Fraction(-1, 9)
                sector = "repeated-overlap"
                cross_partition_pairs += 1
                assert sorted(leg_degree(edge, other)) == [0, 1, 1, 2]
            sectors[sector] += 1
            coefficients[sector, coefficient] += 1

    assert sectors == {
        "repeated-edge": 6,
        "repeated-overlap": 12,
        "transversal-complement": 3,
    }
    assert coefficients == {
        ("repeated-edge", Fraction(-1, 18)): 6,
        ("repeated-overlap", Fraction(-1, 9)): 12,
        ("transversal-complement", Fraction(2, 9)): 3,
    }
    assert cross_partition_pairs == 12

    return {
        "schema": "protected-component-polarization-audit-v1",
        "status": "verified_exact_finite_identities",
        "local_words": 81,
        "word_type_histogram": dict(word_types),
        "compatible_edge_histogram": {str(k): v for k, v in sorted(compatibility.items())},
        "selector_families": len(EDGES),
        "selector_rows": selector_rows,
        "transversal_rows": transversal_rows,
        "pure_rows": pure_rows,
        "connected_quartic_sectors": dict(sectors),
        "connected_quartic_coefficients": {
            "repeated_edge": "-1/18",
            "repeated_overlap": "-1/9",
            "transversal_complement": "2/9",
        },
        "cross_partition_repeated_leg_pairs": cross_partition_pairs,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
