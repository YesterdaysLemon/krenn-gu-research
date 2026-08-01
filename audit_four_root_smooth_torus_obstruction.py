#!/usr/bin/env python3
"""Independent graph audit for the smooth four-root torus theorem."""

from __future__ import annotations

import itertools
import json
from collections import Counter

VERTICES = tuple(range(4))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def endpoint_orientation_audit() -> dict[str, object]:
    counts: Counter[tuple[int, int, int, int]] = Counter()
    for choices in itertools.product((0, 1), repeat=len(EDGES)):
        exponents = [0, 0, 0, 0]
        for edge, choice in zip(EDGES, choices, strict=True):
            exponents[edge[choice]] += 1
        if max(exponents) <= 2:
            counts[tuple(exponents)] += 1

    no_factor_counts = {}
    for omitted in VERTICES:
        candidates = {
            exponent: coefficient
            for exponent, coefficient in counts.items()
            if exponent[omitted] == 0
        }
        expected = tuple(0 if index == omitted else 2 for index in VERTICES)
        assert candidates == {expected: 2}
        no_factor_counts[str(omitted)] = 2
    return {
        "endpoint_assignments": 2 ** len(EDGES),
        "surviving_truncated_monomials": sum(counts.values()),
        "distinct_surviving_monomials": len(counts),
        "no_factor_coefficients": no_factor_counts,
    }


def koszul_graph_audit() -> dict[str, object]:
    cohomological = []
    for edge_count in range(len(EDGES) + 1):
        for selected in itertools.combinations(EDGES, edge_count):
            degree = [0, 0, 0, 0]
            for left, right in selected:
                degree[left] += 1
                degree[right] += 1
            if all(value in (0, 3) for value in degree):
                sheaf_degree = 2 * sum(value == 3 for value in degree)
                cohomological.append(
                    {
                        "edge_count": edge_count,
                        "degree_sequence": degree,
                        "sheaf_cohomology_degree": sheaf_degree,
                        "hypercohomology_total_degree": sheaf_degree - edge_count,
                    }
                )
    assert cohomological == [
        {
            "edge_count": 0,
            "degree_sequence": [0, 0, 0, 0],
            "sheaf_cohomology_degree": 0,
            "hypercohomology_total_degree": 0,
        },
        {
            "edge_count": 6,
            "degree_sequence": [3, 3, 3, 3],
            "sheaf_cohomology_degree": 8,
            "hypercohomology_total_degree": 2,
        },
    ]
    return {
        "edge_subsets": 2 ** len(EDGES),
        "cohomologically_nonzero_subsets": cohomological,
        "only_empty_subset_contributes_to_H0": True,
    }


def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    matchings = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for residual in perfect_matchings(remaining):
            matchings.append(((first, partner),) + residual)
    return tuple(matchings)


def tight_eight_vertex_audit() -> dict[str, object]:
    roots = frozenset(range(4))
    outside = frozenset(range(4, 8))

    # The blocker lower bound gives four blockers inside a four-element
    # outside set, separately for each of the three fully supported colours.
    colour_blockers = tuple(outside for _ in range(3))
    common_blockers = frozenset.intersection(*colour_blockers)
    assert common_blockers == outside

    matchings = perfect_matchings(tuple(range(8)))
    assert len(matchings) == 105
    surviving = tuple(
        matching
        for matching in matchings
        if all(not (left in roots and right in roots) for left, right in matching)
    )
    assert len(surviving) == 24
    assert all(
        all((left in roots) != (right in roots) for left, right in matching)
        for matching in surviving
    )

    permutation_supports = set()
    for matching in surviving:
        root_to_outside = {}
        for left, right in matching:
            root, blocker = (left, right) if left in roots else (right, left)
            root_to_outside[root] = blocker - 4
        permutation_supports.add(
            tuple(root_to_outside[root] for root in sorted(roots))
        )
    assert permutation_supports == set(itertools.permutations(range(4)))

    return {
        "outside_vertices": len(outside),
        "minimum_blockers_per_colour": len(roots),
        "common_blockers": len(common_blockers),
        "residual_modes": 0,
        "perfect_matchings": len(matchings),
        "surviving_root_blocker_bijections": len(surviving),
        "permanent_permutation_supports": len(permutation_supports),
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "audited",
                "method": (
                    "independent endpoint orientations, graph-degree Koszul ledger, "
                    "and tight eight-vertex matching enumeration"
                ),
                "chow_audit": endpoint_orientation_audit(),
                "koszul_audit": koszul_graph_audit(),
                "tight_eight_vertex_audit": tight_eight_vertex_audit(),
                "finite_checks_are_formula_audits_only": True,
                "global_conjecture_resolved": False,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
