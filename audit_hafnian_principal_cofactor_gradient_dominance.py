"""Independent no-import audit of the hafnian cofactor Hessian."""

from __future__ import annotations

import itertools
import json


def anchored_hafnian(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], int]
) -> int:
    if not vertices:
        return 1
    first = vertices[-1]
    total = 0
    for index, second in enumerate(vertices[:-1]):
        edge = tuple(sorted((first, second)))
        rest = vertices[:index] + vertices[index + 1 : -1]
        total += weights.get(edge, 0) * anchored_hafnian(rest, weights)
    return total


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                index
                for index in range(pivot_index + 1, size)
                if work[index][pivot_index] != 0
            )
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        previous = pivot
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
        for column in range(pivot_index + 1, size):
            work[pivot_index][column] = 0
    return sign * work[-1][-1]


def audit_order(pair_count: int) -> dict[str, object]:
    vertices = tuple(range(2 * pair_count))
    edges = tuple(itertools.combinations(vertices, 2))
    fixed = {(2 * i, 2 * i + 1): 1 for i in range(pair_count)}
    jacobian: list[list[int]] = []
    for left in edges:
        row = []
        for right in edges:
            if set(left) & set(right):
                row.append(0)
                continue
            removed = set(left) | set(right)
            complement = tuple(vertex for vertex in vertices if vertex not in removed)
            row.append(anchored_hafnian(complement, fixed))
        jacobian.append(row)
    determinant = bareiss_determinant(jacobian)
    expected = (-1) ** (pair_count - 1) * (pair_count - 1)
    assert determinant == expected
    return {
        "vertices": len(vertices),
        "edges": len(edges),
        "expected_swap_blocks": pair_count * (pair_count - 1),
        "determinant": determinant,
    }


def main() -> None:
    result = {
        "status": "AUDIT_PASS",
        "method": "anchored matching recurrence and fraction-free integer determinant",
        "imports_project_code": False,
        "orders": [audit_order(pair_count) for pair_count in range(2, 7)],
        "determinant_formula": "(-1)^(m-1)*(m-1)",
        "principal_cofactor_map_dominant_in_characteristic_zero": True,
        "mixed_colour_cancellation_proved": False,
        "global_conjecture_resolved": False,
        "finite_field_used": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
