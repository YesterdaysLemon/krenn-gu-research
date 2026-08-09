#!/usr/bin/env python3
"""Independent combinatorial/F_5 audit of the P4 exceptional-graph reduction."""

from __future__ import annotations

import itertools
import json


PRIME = 5
VERTICES = tuple(range(4))
EDGES = tuple(itertools.combinations(VERTICES, 2))
MATCHINGS = (
    frozenset(((0, 1), (2, 3))),
    frozenset(((0, 2), (1, 3))),
    frozenset(((0, 3), (1, 2))),
)


def degrees(edges):
    result = [0] * 4
    for left, right in edges:
        result[left] += 1
        result[right] += 1
    return tuple(sorted(result, reverse=True))


def matrix_rank(a, b, c):
    if not (a or b or c):
        return 0
    return 2 if b * c % PRIME else 1


def main():
    blockers = []
    minimal = []
    edge_set = frozenset(EDGES)
    for size in range(7):
        for subset_tuple in itertools.combinations(EDGES, size):
            subset = frozenset(subset_tuple)
            if not all(subset & matching for matching in MATCHINGS):
                continue
            blockers.append(subset)
            if not any(
                proper < subset and all(proper & matching for matching in MATCHINGS)
                for proper in blockers
            ):
                minimal.append(subset)
    minimal_set = set(minimal)
    assert len(minimal_set) == 8
    assert {degrees(subset) for subset in minimal_set} == {
        (3, 1, 1, 1),
        (2, 2, 2, 0),
    }
    assert all(len(subset) == 3 for subset in minimal_set)
    assert all(subset <= edge_set for subset in minimal_set)

    rank_counts = {1: 0, 2: 0}
    for a, b, c in itertools.product(range(PRIME), repeat=3):
        rank = matrix_rank(a, b, c)
        if rank == 0:
            continue
        rank_counts[rank] += 1
        if rank == 1:
            assert b == 0 or c == 0
        else:
            assert b != 0 and c != 0
    assert sum(rank_counts.values()) == PRIME**3 - 1

    relation_label_words = tuple(itertools.product((1, 2), repeat=3))
    coarse_counts = {sum(label == 2 for label in word) for word in relation_label_words}
    assert coarse_counts == {0, 1, 2, 3}
    print(
        json.dumps(
            {
                "status": "verified",
                "field": "F_5",
                "matching_blockers": len(set(blockers)),
                "minimal_blockers": len(minimal_set),
                "minimal_degree_sequences": [
                    list(value) for value in sorted({degrees(s) for s in minimal_set})
                ],
                "nonzero_marked_relation_matrices": sum(rank_counts.values()),
                "relation_rank_counts": {str(key): value for key, value in rank_counts.items()},
                "coarse_relation_rank_counts": sorted(coarse_counts),
                "role": "independent corroboration of the constant-size combinatorics",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
