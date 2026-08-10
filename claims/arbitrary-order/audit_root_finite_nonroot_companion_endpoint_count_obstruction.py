"""Independent no-import audit of the nonroot endpoint-count obstruction."""

from __future__ import annotations

import json
from itertools import product
from math import gcd

Row = tuple[int, int, int]


def primitive(row: Row) -> Row:
    common = 0
    for value in row:
        common = gcd(common, abs(value))
    answer = tuple(value // common for value in row)
    leading = next(value for value in answer if value)
    if leading < 0:
        answer = tuple(-value for value in answer)
    return answer  # type: ignore[return-value]


def null_basis(row: Row) -> tuple[Row, Row]:
    pivot = max(range(3), key=lambda index: abs(row[index]))
    answer = []
    for free in range(3):
        if free == pivot:
            continue
        vector = [0, 0, 0]
        vector[free] = row[pivot]
        vector[pivot] = -row[free]
        answer.append(tuple(vector))
    return answer[0], answer[1]  # type: ignore[return-value]


def zero_coordinate_on_kernel(row: Row, coordinate: int) -> bool:
    return all(vector[coordinate] == 0 for vector in null_basis(row))


def main() -> None:
    rows = {
        primitive(row)
        for row in product(range(-3, 4), repeat=3)
        if row != (0, 0, 0) and sum(row) != 0
    }
    kernel_checks = 0
    for row in rows:
        for coordinate in range(3):
            expected = row[coordinate] != 0 and sum(value != 0 for value in row) == 1
            if zero_coordinate_on_kernel(row, coordinate) != expected:
                raise AssertionError((row, coordinate, expected))
            kernel_checks += 1

    count_checks = 0
    extremal_examples = 0
    for roots in range(2, 61):
        for endpoints in range(roots):
            minimum_axis_count = roots - endpoints
            feasible = 3 * minimum_axis_count <= roots
            predicted = 3 * endpoints >= 2 * roots
            if feasible != predicted:
                raise AssertionError((roots, endpoints))
            if feasible:
                n0 = minimum_axis_count
                n1 = minimum_axis_count
                n2 = roots - n0 - n1
                counts = (n0, n1, n2)
                if min(counts) < minimum_axis_count:
                    raise AssertionError((roots, endpoints, counts))
                # Avoiding an axis type leaves at most t roots, so no
                # (t+1)-subset can omit that type.
                if any(roots - count > endpoints for count in counts):
                    raise AssertionError((roots, endpoints, counts))
                extremal_examples += 1
            count_checks += 1

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent integer kernels and counting; no sympy or repository imports",
                "projective_covectors": len(rows),
                "kernel_coordinate_checks": kernel_checks,
                "root_endpoint_count_checks": count_checks,
                "extremal_axis_examples": extremal_examples,
                "maximum_roots": 60,
                "bounded_checks_are_theorem_evidence": False,
                "root_root_channels_excluded": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
