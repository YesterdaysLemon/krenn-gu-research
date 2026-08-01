#!/usr/bin/env python3
"""Independent endpoint-orientation audit of the boundary multidegrees."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

VERTICES = tuple(range(5))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def orientation_count(
    boundary_vertex: int, omitted_edge: tuple[int, int]
) -> int:
    remaining = tuple(edge for edge in EDGES if edge != omitted_edge)
    target = tuple(1 if vertex == boundary_vertex else 2 for vertex in VERTICES)
    count = 0
    for choices in itertools.product((0, 1), repeat=len(remaining)):
        indegrees = [0] * len(VERTICES)
        for edge, choice in zip(remaining, choices, strict=True):
            indegrees[edge[choice]] += 1
        if tuple(indegrees) == target:
            count += 1
    return count


def full_intersection_count() -> int:
    count = 0
    for choices in itertools.product((0, 1), repeat=len(EDGES)):
        indegrees = [0] * len(VERTICES)
        for edge, choice in zip(EDGES, choices, strict=True):
            indegrees[edge[choice]] += 1
        if tuple(indegrees) == (2,) * 5:
            count += 1
    return count


def main() -> None:
    profiles: dict[tuple[bool, int], int] = {}
    audited_cases = 0
    for boundary_vertex in VERTICES:
        for edge in EDGES:
            incident = boundary_vertex in edge
            count = orientation_count(boundary_vertex, edge)
            expected = 12 if incident else 10
            if count != expected:
                raise AssertionError(
                    f"orientation count failed at boundary {boundary_vertex}, edge {edge}"
                )
            profiles[(incident, count)] = profiles.get((incident, count), 0) + 1
            audited_cases += 1

    if profiles != {(True, 12): 20, (False, 10): 30}:
        raise AssertionError(f"unexpected incidence profile: {profiles}")
    if full_intersection_count() != 24:
        raise AssertionError("independent five-root degree is not 24")

    coefficient_dimension = 10 * (9 - 1)
    boundary_dimension = (2 - 1) + 4 * (3 - 1)
    incidence_fibre_dimension = 10 * (8 - 1)
    incidence_dimension = boundary_dimension + incidence_fibre_dimension
    if (coefficient_dimension, boundary_dimension, incidence_dimension) != (80, 9, 79):
        raise AssertionError("incidence dimension calculation failed")

    payload = {
        "status": "audited",
        "method": "independent exhaustive endpoint orientations",
        "orientation_assignments_per_boundary_edge": 2**9,
        "audited_boundary_edge_cases": audited_cases,
        "incident_cases": profiles[(True, 12)],
        "nonincident_cases": profiles[(False, 10)],
        "incident_degree": 12,
        "nonincident_degree": 10,
        "total_degree": 4 * 12 + 6 * 10,
        "boundary_resultants": 5 * 3,
        "coefficient_space_dimension": coefficient_dimension,
        "boundary_incidence_dimension": incidence_dimension,
        "five_root_degree": 24,
    }
    output = Path("tmp", "five_root_torus_resultant_dichotomy_audited.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
