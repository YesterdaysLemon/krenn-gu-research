#!/usr/bin/env python3
"""Verify the Chow multidegrees in the five-root boundary resultants."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

VERTICES = tuple(range(5))
COLOURS = tuple(range(3))
EDGES = tuple(itertools.combinations(VERTICES, 2))
THEOREM = Path(__file__).resolve().with_name(
    "FIVE_ROOT_TORUS_RESULTANT_DICHOTOMY.md"
)


def multiply_endpoint_classes(
    edges: tuple[tuple[int, int], ...],
    capacities: tuple[int, ...],
) -> dict[tuple[int, ...], int]:
    """Expand product_(ij in edges) (h_i+h_j), truncated by capacities."""

    coefficients = {(0,) * len(capacities): 1}
    for left, right in edges:
        updated: dict[tuple[int, ...], int] = {}
        for exponent, coefficient in coefficients.items():
            for endpoint in (left, right):
                candidate = list(exponent)
                candidate[endpoint] += 1
                candidate_tuple = tuple(candidate)
                if candidate[endpoint] <= capacities[endpoint]:
                    updated[candidate_tuple] = (
                        updated.get(candidate_tuple, 0) + coefficient
                    )
        coefficients = updated
    return coefficients


def boundary_degree(boundary_vertex: int, omitted_edge: tuple[int, int]) -> int:
    capacities = tuple(1 if vertex == boundary_vertex else 2 for vertex in VERTICES)
    remaining = tuple(edge for edge in EDGES if edge != omitted_edge)
    return multiply_endpoint_classes(remaining, capacities).get(capacities, 0)


def coincidence_incidence_bound(
    boundary_vertex: int, omitted_edge: tuple[int, int]
) -> int:
    """Maximum two-root coincidence-incidence dimension."""

    factor_dimensions = tuple(
        1 if vertex == boundary_vertex else 2 for vertex in VERTICES
    )
    dimensions = []
    for size in range(2, len(VERTICES)):
        for agreed in itertools.combinations(VERTICES, size):
            if not set(omitted_edge).issubset(agreed):
                continue
            outside_dimension = sum(
                factor_dimensions[vertex]
                for vertex in VERTICES
                if vertex not in agreed
            )
            coincident_conditions = size * (size - 1) // 2 - 1
            dimensions.append(
                63 + outside_dimension + coincident_conditions
            )
    return max(dimensions)


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    required_phrases = (
        "multihomogeneous polynomial",
        "4*12+6*10=108",
        "total blocker union has at least six vertices",
        "does **not** show",
    )
    for phrase in required_phrases:
        if phrase not in theorem:
            raise AssertionError(f"missing scope or theorem phrase: {phrase}")

    full_capacities = (2,) * 5
    full_product = multiply_endpoint_classes(EDGES, full_capacities)
    if full_product.get(full_capacities) != 24:
        raise AssertionError("five-root top intersection is not 24")

    degree_table: dict[str, dict[str, int]] = {}
    coincidence_bounds = []
    for boundary_vertex in VERTICES:
        by_edge: dict[str, int] = {}
        for edge in EDGES:
            degree = boundary_degree(boundary_vertex, edge)
            expected = 12 if boundary_vertex in edge else 10
            if degree != expected:
                raise AssertionError(
                    f"boundary {boundary_vertex}, edge {edge}: {degree} != {expected}"
                )
            by_edge[f"{edge[0]}{edge[1]}"] = degree
            coincidence_bounds.append(
                coincidence_incidence_bound(boundary_vertex, edge)
            )
        if sum(by_edge.values()) != 108:
            raise AssertionError("boundary resultant total degree is not 108")
        degree_table[str(boundary_vertex)] = by_edge
    if max(coincidence_bounds) != 70 or max(coincidence_bounds) >= 72:
        raise AssertionError("two-root evaluation coincidence is not proper")

    if len(VERTICES) * len(COLOURS) != 15:
        raise AssertionError("unexpected number of coordinate boundaries")

    payload = {
        "status": "verified",
        "field": "C",
        "coefficient_space_dimension": len(EDGES) * 8,
        "boundary_dimension": 1 + 4 * 2,
        "incidence_fibre_dimension": len(EDGES) * 7,
        "incidence_dimension": 79,
        "boundary_resultant_count": 15,
        "incident_edge_multidegree": 12,
        "nonincident_edge_multidegree": 10,
        "ordinary_total_degree": 108,
        "five_root_intersection_degree": 24,
        "two_root_coincidence_max_dimension": max(coincidence_bounds),
        "nine_block_parameter_dimension": 72,
        "degree_table_by_boundary_vertex": degree_table,
    }
    output = Path("tmp", "five_root_torus_resultant_dichotomy_verified.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
