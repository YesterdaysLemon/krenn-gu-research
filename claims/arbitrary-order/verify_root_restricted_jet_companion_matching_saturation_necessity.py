"""Verify restricted-jet companion matching saturation necessity exactly."""

from __future__ import annotations

import json
from functools import cache
from itertools import product
from math import gcd

import sympy as sp

Edge = tuple[int, int]
Row = tuple[int, int, int]


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def canonical(row: Row) -> Row:
    divisor = 0
    for value in row:
        divisor = gcd(divisor, abs(value))
    answer = tuple(value // divisor for value in row)
    first = next(value for value in answer if value)
    if first < 0:
        answer = tuple(-value for value in answer)
    return answer  # type: ignore[return-value]


def kernel_basis(row: Row) -> tuple[Row, Row]:
    pivot = next(index for index, value in enumerate(row) if value)
    basis = []
    for free in range(3):
        if free == pivot:
            continue
        vector = [0, 0, 0]
        vector[free] = row[pivot]
        vector[pivot] = -row[free]
        basis.append(tuple(vector))
    return basis[0], basis[1]  # type: ignore[return-value]


def axis_type(row: Row) -> int | None:
    occupied = [index for index, value in enumerate(row) if value]
    return occupied[0] if len(occupied) == 1 else None


def product_map_zero(rows: tuple[Row, ...]) -> bool:
    bases = tuple(kernel_basis(row) for row in rows)
    for choices in product(*bases):
        word = tuple(sp.prod(choice[coordinate] for choice in choices) for coordinate in range(3))
        if word != (0, 0, 0):
            return False
    return True


def zero_product_audit() -> dict[str, int]:
    vectors = sorted(
        {
            canonical(row)
            for row in product(range(-2, 3), repeat=3)
            if row != (0, 0, 0) and sum(row) != 0
        }
    )
    samples = []
    axes = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    samples.append(axes)
    for vector in vectors:
        samples.append((axes[0], axes[1], vector))
        samples.append((axes[0], vector))
    checked = 0
    zero = 0
    for rows in samples:
        actual = product_map_zero(rows)
        expected = {axis_type(row) for row in rows} >= {0, 1, 2}
        if actual != expected:
            raise AssertionError((rows, actual, expected))
        checked += 1
        zero += int(actual)
    return {"samples": checked, "zero_products": zero, "projective_covectors": len(vectors)}


def matching_saturation_audit() -> dict[str, int]:
    matchings_checked = 0
    subset_checks = 0
    for order in range(2, 11, 2):
        vertices = tuple(range(order))
        matchings = perfect_matchings(vertices)
        for matching in matchings:
            matched_edges = {tuple(sorted(edge)) for edge in matching}
            for mask in range(1, 1 << min(order, 6)):
                varied = {index for index in range(min(order, 6)) if mask & (1 << index)}
                incident = {edge for edge in matched_edges if edge[0] in varied or edge[1] in varied}
                saturated = {endpoint for edge in incident for endpoint in edge} >= varied
                if not saturated:
                    raise AssertionError((order, matching, varied, incident))
                subset_checks += 1
            matchings_checked += 1
    return {"perfect_matchings": matchings_checked, "varied_subset_checks": subset_checks, "maximum_vertices": 10}


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "zero_product_axis_criterion": zero_product_audit(),
                "termwise_matching_saturation": matching_saturation_audit(),
                "saturating_matching_sufficient": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
