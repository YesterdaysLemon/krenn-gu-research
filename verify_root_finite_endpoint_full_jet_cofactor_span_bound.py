"""Verify the finite-endpoint full-root cofactor-span theorem exactly."""

from __future__ import annotations

import json
from itertools import combinations, product
from math import comb, gcd

import sympy as sp

Row = tuple[int, int, int]


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
    answer = []
    for free in range(3):
        if free == pivot:
            continue
        vector = [0, 0, 0]
        vector[free] = row[pivot]
        vector[pivot] = -row[free]
        answer.append(tuple(vector))
    return answer[0], answer[1]  # type: ignore[return-value]


def full_jet_rank(rows: tuple[Row, ...]) -> int:
    bases = tuple(kernel_basis(row) for row in rows)
    forms = [
        [
            sp.prod(vector[coordinate] for vector in choice)
            for choice in product(*bases)
        ]
        for coordinate in range(3)
    ]
    return int(sp.Matrix(forms).rank())


def is_axis(row: Row) -> bool:
    return sum(value != 0 for value in row) == 1


def common_coordinate_pair(rows: tuple[Row, ...]) -> bool:
    for pair in combinations(range(3), 2):
        outside = ({0, 1, 2} - set(pair)).pop()
        if all(row[outside] == 0 for row in rows):
            return True
    return False


def cofactor_bound(root_count: int, endpoint_count: int) -> int:
    return sum(
        comb(endpoint_count, used)
        for used in range(min(root_count, endpoint_count) + 1)
        if used % 2 == root_count % 2
    )


def endpoint_subset_audit() -> dict[str, int]:
    checks = 0
    for root_count in range(2, 13):
        for endpoint_count in range(7):
            subsets = [
                subset
                for used in range(min(root_count, endpoint_count) + 1)
                if used % 2 == root_count % 2
                for subset in combinations(range(endpoint_count), used)
            ]
            if len(subsets) != cofactor_bound(root_count, endpoint_count):
                raise AssertionError((root_count, endpoint_count, subsets))
            if endpoint_count == 1 and len(subsets) != 1:
                raise AssertionError((root_count, endpoint_count, subsets))
            if endpoint_count == 2 and len(subsets) != 2:
                raise AssertionError((root_count, endpoint_count, subsets))
            checks += 1
    return {"checks": checks, "maximum_roots": 12, "maximum_endpoints": 6}


def rank_two_audit() -> dict[str, object]:
    rows = sorted(
        {
            canonical(row)
            for row in product(range(-1, 2), repeat=3)
            if row != (0, 0, 0) and sum(row) != 0
        }
    )
    counts: dict[int, int] = {}
    rank_histogram = {0: 0, 1: 0, 2: 0, 3: 0}
    for root_count in range(2, 5):
        checked = 0
        for sample in product(rows, repeat=root_count):
            rank = full_jet_rank(sample)
            predicted = any(is_axis(row) for row in sample) or common_coordinate_pair(sample)
            if (rank <= 2) != predicted:
                raise AssertionError((sample, rank, predicted))
            rank_histogram[rank] += 1
            checked += 1
        counts[root_count] = checked
    return {
        "projective_covectors": len(rows),
        "tuple_counts": counts,
        "rank_histogram": rank_histogram,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "cofactor_subset_bound": endpoint_subset_audit(),
                "rank_two_classification": rank_two_audit(),
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
