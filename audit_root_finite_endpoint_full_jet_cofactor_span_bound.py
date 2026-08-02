"""No-import audit of the finite-endpoint full-root cofactor-span theorem."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, product
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


def row_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                left - multiple * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
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
    return row_rank(forms)


def predicted_rank_at_most_two(rows: tuple[Row, ...]) -> bool:
    if any(sum(value != 0 for value in row) == 1 for row in rows):
        return True
    supports = [{index for index, value in enumerate(row) if value} for row in rows]
    return any(all(support <= set(pair) for support in supports) for pair in ((0, 1), (0, 2), (1, 2)))


def subset_count(root_count: int, endpoint_count: int) -> int:
    count = 0
    endpoints = tuple(range(endpoint_count))
    for mask in range(1 << endpoint_count):
        chosen = tuple(index for index in endpoints if mask & (1 << index))
        if len(chosen) <= root_count and len(chosen) % 2 == root_count % 2:
            count += 1
    return count


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
        if (tensor_rank(sample) <= 2) != predicted_rank_at_most_two(sample):
            raise AssertionError((sample, tensor_rank(sample)))
        pair_checks += 1

    selected = wide_rows[:: max(1, len(wide_rows) // 13)]
    triple_checks = 0
    for sample in product(selected, repeat=3):
        if (tensor_rank(sample) <= 2) != predicted_rank_at_most_two(sample):
            raise AssertionError((sample, tensor_rank(sample)))
        triple_checks += 1

    subset_checks = 0
    for root_count in range(2, 19):
        for endpoint_count in range(7):
            count = subset_count(root_count, endpoint_count)
            explicit = sum(
                1
                for used in range(min(root_count, endpoint_count) + 1)
                for _subset in combinations(range(endpoint_count), used)
                if used % 2 == root_count % 2
            )
            if count != explicit:
                raise AssertionError((root_count, endpoint_count, count, explicit))
            subset_checks += 1

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent integer kernels, rational row reduction, and bitmask endpoint subsets",
                "wide_projective_covectors": len(wide_rows),
                "pair_checks": pair_checks,
                "selected_triple_checks": triple_checks,
                "endpoint_subset_checks": subset_checks,
                "maximum_roots": 18,
                "maximum_endpoints": 6,
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
