#!/usr/bin/env python3
"""Independent hafnian and kernel audit of odd-residual port extraction."""

from __future__ import annotations

import itertools
import json
from functools import cache


def deterministic_weight(left: int, right: int, salt: int) -> int:
    if left > right:
        left, right = right, left
    return (left + 2) * (right + 3) + salt * (left + right + 1)


def matching_sum(vertices: tuple[int, ...], weight) -> int:
    @cache
    def recurse(current: tuple[int, ...]) -> int:
        if not current:
            return 1
        first = current[0]
        total = 0
        for index in range(1, len(current)):
            second = current[index]
            remaining = current[1:index] + current[index + 1 :]
            total += weight(first, second) * recurse(remaining)
        return total

    return recurse(vertices)


def permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    size = len(matrix)
    table = {0: 1}
    for row in range(size):
        updated: dict[int, int] = {}
        for mask, coefficient in table.items():
            for column in range(size):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    updated[target] = (
                        updated.get(target, 0)
                        + coefficient * matrix[row][column]
                    )
        table = updated
    return table[(1 << size) - 1]


def audit_case(r: int, q_size: int, salt: int) -> dict[str, object]:
    roots = tuple(range(r))
    blockers = tuple(range(r, 2 * r + 1))
    residual = tuple(range(2 * r + 1, 2 * r + 1 + q_size))
    root_set = frozenset(roots)
    blocker_set = frozenset(blockers)

    def restricted_weight(left: int, right: int) -> int:
        if left in root_set and right not in blocker_set:
            return 0
        if right in root_set and left not in blocker_set:
            return 0
        return deterministic_weight(left, right, salt)

    full_value = matching_sum(roots + blockers + residual, restricted_weight)
    matrix_rows: list[tuple[int, ...]] = []
    for root in roots:
        matrix_rows.append(
            tuple(restricted_weight(root, blocker) for blocker in blockers)
        )
    matrix_rows.append(
        tuple(
            matching_sum((blocker, *residual), restricted_weight)
            for blocker in blockers
        )
    )
    port_value = permanent(tuple(matrix_rows))
    assert full_value == port_value
    assert full_value != 0
    return {
        "roots": r,
        "blockers": r + 1,
        "residual_vertices": q_size,
        "salt": salt,
        "full_hafnian_value": str(full_value),
        "port_permanent_value": str(port_value),
    }


def span_mod_5(generators: tuple[tuple[int, int, int], ...]) -> frozenset[tuple[int, int, int]]:
    output = set()
    for coefficients in itertools.product(range(5), repeat=len(generators)):
        output.add(
            tuple(
                sum(
                    coefficient * generator[coordinate]
                    for coefficient, generator in zip(
                        coefficients, generators, strict=True
                    )
                )
                % 5
                for coordinate in range(3)
            )
        )
    return frozenset(output)


def audit_kernel_torus() -> dict[str, int]:
    vectors = tuple(itertools.product(range(5), repeat=3))
    nonzero = tuple(vector for vector in vectors if vector != (0, 0, 0))
    subspaces = {span_mod_5((vector,)) for vector in nonzero}
    subspaces.update(
        span_mod_5((left, right))
        for left in nonzero
        for right in nonzero
    )
    subspaces.add(frozenset(vectors))
    checked = 0
    for subspace in subspaces:
        contained_in_coordinate_plane = any(
            all(vector[colour] == 0 for vector in subspace)
            for colour in range(3)
        )
        if contained_in_coordinate_plane:
            continue
        assert any(all(coordinate != 0 for coordinate in vector) for vector in subspace)
        checked += 1
    return {
        "field_order": 5,
        "distinct_nonzero_subspaces": len(subspaces),
        "subspaces_not_in_coordinate_hyperplane": checked,
    }


def main() -> None:
    cases = tuple(
        audit_case(r, q_size, salt)
        for r, q_size in ((2, 3), (3, 1), (4, 3), (5, 5))
        for salt in (1, 7)
    )
    print(
        json.dumps(
            {
                "status": "audited",
                "method": (
                    "independent weighted hafnian recurrence versus permanent "
                    "subset recurrence"
                ),
                "cases": cases,
                "kernel_torus_audit": audit_kernel_torus(),
                "all_numeric_port_identities_nonzero": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
