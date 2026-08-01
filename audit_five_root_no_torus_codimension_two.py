#!/usr/bin/env python3
"""Independent orientation-DP audit of the no-torus codimension theorem."""

from __future__ import annotations

import functools
import itertools
import json
from pathlib import Path

VERTICES = tuple(range(5))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def endpoint_assignment_count(
    edges: tuple[tuple[int, int], ...], target: tuple[int, ...]
) -> int:
    @functools.lru_cache(None)
    def count(index: int, remaining: tuple[int, ...]) -> int:
        if index == len(edges):
            return int(all(value == 0 for value in remaining))
        left, right = edges[index]
        total = 0
        for endpoint in (left, right):
            if remaining[endpoint] == 0:
                continue
            updated = list(remaining)
            updated[endpoint] -= 1
            total += count(index + 1, tuple(updated))
        return total

    return count(0, target)


def audit_boundary_degrees() -> dict[str, int]:
    profile: dict[str, int] = {}
    for boundary_vertex in VERTICES:
        target = tuple(1 if vertex == boundary_vertex else 2 for vertex in VERTICES)
        for omitted in EDGES:
            remaining = tuple(edge for edge in EDGES if edge != omitted)
            degree = endpoint_assignment_count(remaining, target)
            expected = 12 if boundary_vertex in omitted else 10
            if degree != expected:
                raise AssertionError(
                    f"independent degree failed at {boundary_vertex}, {omitted}: {degree}"
                )
            key = f"{'incident' if boundary_vertex in omitted else 'nonincident'}_{degree}"
            profile[key] = profile.get(key, 0) + 1
    return profile


def audit_second_root_dimensions() -> list[dict[str, int]]:
    records = []
    for shared in range(5):
        coincident = shared * (shared - 1) // 2
        if shared == 0:
            moving = 9
        else:
            moving = 2 * (5 - shared)
        total = 60 + coincident + moving
        if total >= 70:
            raise AssertionError("second boundary incidence reaches fixed-root dimension")
        records.append(
            {
                "shared_vertices": shared,
                "coincident_edge_evaluations": coincident,
                "moving_boundary_dimension_upper_bound": moving,
                "incidence_dimension": total,
            }
        )
    return records


def audit_torus_strata() -> list[dict[str, int]]:
    records = []
    for shared in range(5):
        coincident = shared * (shared - 1) // 2
        moving = 2 * (5 - shared)
        total = 60 + coincident + moving
        records.append(
            {
                "shared_vertices": shared,
                "coincident_edge_evaluations": coincident,
                "moving_torus_dimension": moving,
                "incidence_dimension": total,
            }
        )
    main = [record for record in records if record["incidence_dimension"] == 70]
    if len(main) != 1 or main[0]["shared_vertices"] != 0:
        raise AssertionError("independent torus-stratum audit found the wrong main stratum")
    return records


def main() -> None:
    full_degree = endpoint_assignment_count(EDGES, (2, 2, 2, 2, 2))
    if full_degree != 24:
        raise AssertionError("independent regular-orientation count failed")

    boundary_profile = audit_boundary_degrees()
    if boundary_profile != {"incident_12": 20, "nonincident_10": 30}:
        raise AssertionError(f"unexpected boundary profile: {boundary_profile}")

    dimension_records = audit_second_root_dimensions()
    torus_records = audit_torus_strata()

    boundary_count = 5 * 3
    repeated_load = (full_degree + boundary_count - 1) // boundary_count
    if repeated_load != 2:
        raise AssertionError("24 boundary roots do not force a repeated hyperplane")

    coefficient_dimension = 10 * (9 - 1)
    divisor_dimension = coefficient_dimension - 1
    proper_divisor_subset_dimension = divisor_dimension - 1
    if proper_divisor_subset_dimension != 78:
        raise AssertionError("codimension-two envelope dimension is wrong")

    affine_dimension = 10 * 9
    scaling_dimension = 10
    lifted_exception_dimension = proper_divisor_subset_dimension + scaling_dimension
    zero_block_dimension = affine_dimension - 9
    affine_exception_dimension = max(lifted_exception_dimension, zero_block_dimension)
    if affine_dimension - affine_exception_dimension != 2:
        raise AssertionError("affine exceptional envelope is not codimension at least two")

    payload = {
        "status": "audited",
        "method": "endpoint-orientation DP and independent incidence arithmetic",
        "five_root_degree": full_degree,
        "boundary_resultants": boundary_count,
        "pigeonhole_repeated_load": repeated_load,
        "boundary_degree_profile": boundary_profile,
        "second_boundary_incidence": dimension_records,
        "second_torus_incidence": torus_records,
        "coefficient_space_dimension": coefficient_dimension,
        "resultant_divisor_dimension": divisor_dimension,
        "proper_exception_dimension_at_most": proper_divisor_subset_dimension,
        "codimension_at_least": coefficient_dimension - proper_divisor_subset_dimension,
        "affine_coefficient_space_dimension": affine_dimension,
        "scaling_torus_dimension": scaling_dimension,
        "affine_lift_dimension_at_most": lifted_exception_dimension,
        "zero_block_union_dimension": zero_block_dimension,
        "zero_block_codimension": affine_dimension - zero_block_dimension,
        "affine_exception_codimension_at_least": (
            affine_dimension - affine_exception_dimension
        ),
        "algebraic_geometry_proof_in_markdown": True,
        "global_conjecture_resolved": False,
    }
    output = Path("tmp", "five_root_no_torus_codimension_two_audited.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
