"""No-import audit of the zero/one-endpoint full-root jet theorem."""

from __future__ import annotations

import json
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd

Row = tuple[int, int, int]


def primitive(row: Row) -> Row:
    divisor = 0
    for value in row:
        divisor = gcd(divisor, abs(value))
    answer = tuple(value // divisor for value in row)
    first = next(value for value in answer if value)
    if first < 0:
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


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    height = len(work)
    width = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                left - multiple * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def tensor_rank(rows: tuple[Row, ...]) -> int:
    bases = tuple(null_basis(row) for row in rows)
    forms: list[list[int]] = []
    for coordinate in range(3):
        values = []
        for choice in product(*bases):
            value = 1
            for vector in choice:
                value *= vector[coordinate]
            values.append(value)
        forms.append(values)
    return rational_rank(forms)


def axis(row: Row) -> int | None:
    support = [index for index, value in enumerate(row) if value]
    return support[0] if len(support) == 1 else None


@cache
def pairings(size: int) -> int:
    if size == 0:
        return 1
    if size % 2:
        return 0
    return (size - 1) * pairings(size - 2)


def main() -> None:
    wide_rows = sorted(
        {
            primitive(row)
            for row in product(range(-2, 3), repeat=3)
            if row != (0, 0, 0) and sum(row) != 0
        }
    )
    pair_checks = 0
    for sample in product(wide_rows, repeat=2):
        axis_types = {kind for row in sample if (kind := axis(row)) is not None}
        if (tensor_rank(sample) <= 1) != (len(axis_types) >= 2):
            raise AssertionError((sample, tensor_rank(sample), axis_types))
        pair_checks += 1

    selected = wide_rows[:: max(1, len(wide_rows) // 13)]
    triple_checks = 0
    for sample in product(selected, repeat=3):
        axis_types = {kind for row in sample if (kind := axis(row)) is not None}
        if (tensor_rank(sample) <= 1) != (len(axis_types) >= 2):
            raise AssertionError((sample, tensor_rank(sample), axis_types))
        triple_checks += 1

    parity_checks = 0
    for root_count in range(2, 19):
        internal = pairings(root_count)
        endpoint = root_count * pairings(root_count - 1)
        if root_count % 2 == 0:
            if not internal or endpoint:
                raise AssertionError((root_count, internal, endpoint))
        elif internal or not endpoint:
            raise AssertionError((root_count, internal, endpoint))
        parity_checks += 1

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent integer kernels, rational row reduction, and double-factorial matching recursion",
                "wide_projective_covectors": len(wide_rows),
                "pair_checks": pair_checks,
                "selected_triple_checks": triple_checks,
                "endpoint_parity_checks": parity_checks,
                "maximum_roots": 18,
                "bounded_checks_are_theorem_evidence": False,
                "root_root_tangent_edges_allowed": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
