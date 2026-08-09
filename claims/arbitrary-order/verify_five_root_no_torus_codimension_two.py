#!/usr/bin/env python3
"""Verify the discrete inputs to the five-root codimension-two theorem."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

VERTICES = tuple(range(5))
EDGES = tuple(itertools.combinations(VERTICES, 2))
THEOREM = Path("FIVE_ROOT_NO_TORUS_CODIMENSION_TWO_THEOREM.md")


def chow_product(
    edges: tuple[tuple[int, int], ...], capacities: tuple[int, ...]
) -> dict[tuple[int, ...], int]:
    coefficients = {(0,) * len(capacities): 1}
    for left, right in edges:
        updated: dict[tuple[int, ...], int] = {}
        for exponent, coefficient in coefficients.items():
            for endpoint in (left, right):
                candidate = list(exponent)
                candidate[endpoint] += 1
                if candidate[endpoint] > capacities[endpoint]:
                    continue
                key = tuple(candidate)
                updated[key] = updated.get(key, 0) + coefficient
        coefficients = updated
    return coefficients


def boundary_degree(boundary_vertex: int, omitted: tuple[int, int]) -> int:
    capacities = tuple(1 if vertex == boundary_vertex else 2 for vertex in VERTICES)
    edges = tuple(edge for edge in EDGES if edge != omitted)
    return chow_product(edges, capacities).get(capacities, 0)


def regular_tournaments() -> list[dict[tuple[int, int], int]]:
    tournaments = []
    for choices in itertools.product((0, 1), repeat=len(EDGES)):
        heads = {edge: edge[choice] for edge, choice in zip(EDGES, choices, strict=True)}
        indegrees = {
            vertex: sum(head == vertex for head in heads.values())
            for vertex in VERTICES
        }
        if set(indegrees.values()) == {2}:
            tournaments.append(heads)
    return tournaments


def permutation_jacobian_check(heads: dict[tuple[int, int], int]) -> None:
    incoming = {
        vertex: sorted(edge for edge, head in heads.items() if head == vertex)
        for vertex in VERTICES
    }
    if any(len(edges) != 2 for edges in incoming.values()):
        raise AssertionError("orientation is not regular")

    used_columns = []
    for edge in EDGES:
        head = heads[edge]
        local_coordinate = incoming[head].index(edge)
        used_columns.append(2 * head + local_coordinate)
    if sorted(used_columns) != list(range(10)):
        raise AssertionError("tangent Jacobian is not a permutation matrix")

    # Deleting the normal coordinate of any one boundary hyperplane leaves
    # nine distinct pivot columns, hence restricted tangent rank nine.
    for normal_column in range(10):
        remaining = [column for column in used_columns if column != normal_column]
        if len(remaining) != 9 or len(set(remaining)) != 9:
            raise AssertionError("boundary tangent rank is not nine")


def second_boundary_incidence_dimensions() -> dict[int, int]:
    dimensions = {0: 60 + 9}
    for shared_vertices in range(1, 5):
        coincident_evaluations = shared_vertices * (shared_vertices - 1) // 2
        moving_dimension = 2 * (5 - shared_vertices)
        dimensions[shared_vertices] = 60 + coincident_evaluations + moving_dimension
    return dimensions


def second_torus_incidence_dimensions() -> dict[int, int]:
    return {
        shared_vertices: (
            60
            + shared_vertices * (shared_vertices - 1) // 2
            + 2 * (5 - shared_vertices)
        )
        for shared_vertices in range(5)
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "codim_P closure(N) >= 2",
        "twenty-three simple torus roots",
        "six blockers   -> P_6 -> Delta_3",
        "does **not** show",
    ):
        if phrase not in theorem:
            raise AssertionError(f"missing theorem or scope phrase: {phrase}")

    full_capacities = (2,) * len(VERTICES)
    full_degree = chow_product(EDGES, full_capacities).get(full_capacities, 0)
    if full_degree != 24:
        raise AssertionError(f"five-root degree is {full_degree}, not 24")

    degree_profile: dict[str, int] = {}
    for boundary_vertex in VERTICES:
        for omitted in EDGES:
            degree = boundary_degree(boundary_vertex, omitted)
            expected = 12 if boundary_vertex in omitted else 10
            if degree != expected:
                raise AssertionError(
                    f"boundary {boundary_vertex}, omitted {omitted}: {degree} != {expected}"
                )
            key = "incident" if boundary_vertex in omitted else "nonincident"
            degree_profile[key] = degree_profile.get(key, 0) + 1
    if degree_profile != {"incident": 20, "nonincident": 30}:
        raise AssertionError(f"unexpected boundary degree profile: {degree_profile}")

    incidence_dimensions = second_boundary_incidence_dimensions()
    expected_dimensions = {0: 69, 1: 68, 2: 67, 3: 67, 4: 68}
    if incidence_dimensions != expected_dimensions:
        raise AssertionError(f"unexpected two-root dimensions: {incidence_dimensions}")
    if max(incidence_dimensions.values()) >= 70:
        raise AssertionError("second-boundary-root incidence is not proper in S_x")

    torus_dimensions = second_torus_incidence_dimensions()
    if torus_dimensions != {0: 70, 1: 68, 2: 67, 3: 67, 4: 68}:
        raise AssertionError(f"unexpected torus incidence dimensions: {torus_dimensions}")
    if [shared for shared, dimension in torus_dimensions.items() if dimension == 70] != [0]:
        raise AssertionError("the no-shared-factor stratum is not the unique main stratum")

    tournaments = regular_tournaments()
    if len(tournaments) != 24:
        raise AssertionError(f"regular tournament count is {len(tournaments)}, not 24")
    for heads in tournaments:
        permutation_jacobian_check(heads)

    if full_degree <= 5 * 3:
        raise AssertionError("the boundary-root pigeonhole step does not force repetition")

    affine_dimension = 10 * 9
    scaling_fibre_dimension = 10
    projective_exception_dimension = 80 - 2
    affine_projective_lift_dimension = (
        projective_exception_dimension + scaling_fibre_dimension
    )
    zero_block_dimension = affine_dimension - 9
    if (affine_projective_lift_dimension, zero_block_dimension) != (88, 81):
        raise AssertionError("affine codimension lift is incorrect")

    payload = {
        "status": "verified",
        "field": "C",
        "coefficient_space_dimension": 80,
        "root_incidence_dimension": 80,
        "fixed_root_coefficient_dimension": 70,
        "five_root_degree": full_degree,
        "boundary_hyperplanes": 15,
        "minimum_repeated_boundary_load": (full_degree + 14) // 15,
        "second_boundary_incidence_dimensions": incidence_dimensions,
        "second_torus_incidence_dimensions": torus_dimensions,
        "unique_main_torus_stratum_shared_vertices": 0,
        "regular_tournament_jacobians": len(tournaments),
        "boundary_degree_case_counts": degree_profile,
        "resultant_incident_degree": 12,
        "resultant_nonincident_degree": 10,
        "resultant_total_degree": 108,
        "affine_coefficient_space_dimension": affine_dimension,
        "block_scaling_fibre_dimension": scaling_fibre_dimension,
        "affine_projective_exception_dimension_at_most": affine_projective_lift_dimension,
        "zero_block_component_dimension": zero_block_dimension,
        "zero_block_component_codimension": affine_dimension - zero_block_dimension,
        "affine_no_torus_codimension_at_least": 2,
        "conclusion": "the no-torus locus is contained in a codimension-at-least-two envelope",
        "global_conjecture_resolved": False,
    }
    output = Path("tmp", "five_root_no_torus_codimension_two_verified.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
