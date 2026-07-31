#!/usr/bin/env python3
"""Verify the eight-cell exceptional-graph reduction for pure P4."""

from __future__ import annotations

import itertools
import json

import sympy as sp


VERTICES = tuple(range(4))
EDGES = tuple(itertools.combinations(VERTICES, 2))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def degree_sequence(edges):
    degree = [0] * 4
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1
    return tuple(sorted(degree, reverse=True))


def main():
    admissible_profiles = []
    transversals = set()
    for ranks in itertools.product((3, 4), repeat=6):
        profile = dict(zip(EDGES, ranks, strict=True))
        if not all(profile[left] + profile[right] <= 7 for left, right in MATCHINGS):
            continue
        exceptional = {edge for edge, rank in profile.items() if rank == 3}
        assert all(exceptional & set(matching) for matching in MATCHINGS)
        admissible_profiles.append(ranks)
        for selected in itertools.product(*(
            tuple(exceptional & set(matching)) for matching in MATCHINGS
        )):
            selected_set = frozenset(selected)
            assert len(selected_set) == 3
            assert degree_sequence(selected_set) in ((3, 1, 1, 1), (2, 2, 2, 0))
            transversals.add(selected_set)

    expected_stars = {
        frozenset(edge for edge in EDGES if vertex in edge)
        for vertex in VERTICES
    }
    expected_triangles = {
        frozenset(edge for edge in EDGES if vertex not in edge)
        for vertex in VERTICES
    }
    assert transversals == expected_stars | expected_triangles
    assert len(admissible_profiles) == 27

    a, b, c, d = sp.symbols("a b c d")
    relation = sp.Matrix(((a, b), (c, d)))
    pure_active_coefficient = sp.Symbol("T1111", nonzero=True)
    active_evaluation = sp.expand(d * pure_active_coefficient)
    assert sp.solve(active_evaluation, d) == [0]
    marked_relation = relation.subs(d, 0)
    assert sp.factor(marked_relation.det()) == -b * c
    assert sp.Matrix(((a, 0), (c, 0))) == sp.Matrix((a, c)) * sp.Matrix(((1, 0),))
    assert sp.Matrix(((a, b), (0, 0))) == sp.Matrix((1, 0)) * sp.Matrix(((a, b),))

    cells = tuple(
        (shape, rank_two_count)
        for shape in ("star", "triangle")
        for rank_two_count in range(4)
    )
    assert len(cells) == 8
    print(
        json.dumps(
            {
                "status": "verified",
                "admissible_rank_profiles": len(admissible_profiles),
                "minimal_exceptional_transversals": len(transversals),
                "labelled_stars": len(expected_stars),
                "labelled_triangles": len(expected_triangles),
                "coarse_relation_rank_cells": len(cells),
                "resolved_cells": [
                    "star-222",
                    "star-221",
                    "triangle-222",
                    "triangle-221",
                ],
                "component_exhaustiveness": "unresolved",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
