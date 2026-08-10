"""Verify the zero/one-endpoint full-root jet axis necessity exactly."""

from __future__ import annotations

import json
from functools import cache
from itertools import product
from math import gcd

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


def axis_type(row: Row) -> int | None:
    support = [index for index, value in enumerate(row) if value]
    return support[0] if len(support) == 1 else None


def full_jet_rank(rows: tuple[Row, ...]) -> int:
    bases = tuple(kernel_basis(row) for row in rows)
    forms = []
    for coordinate in range(3):
        forms.append(
            [
                sp.prod(vector[coordinate] for vector in basis_choice)
                for basis_choice in product(*bases)
            ]
        )
    return int(sp.Matrix(forms).rank())


@cache
def internal_matchings(vertices: tuple[int, ...]) -> int:
    if not vertices:
        return 1
    if len(vertices) % 2:
        return 0
    total = 0
    for position in range(1, len(vertices)):
        total += internal_matchings(vertices[1:position] + vertices[position + 1 :])
    return total


def endpoint_parity_audit() -> dict[str, int]:
    cases = 0
    largest_count = 0
    for root_count in range(2, 13):
        roots = tuple(range(root_count))
        without_endpoint = internal_matchings(roots)
        with_endpoint = sum(
            internal_matchings(roots[:position] + roots[position + 1 :])
            for position in range(root_count)
        )
        expected_without = internal_matchings(roots) if root_count % 2 == 0 else 0
        expected_with = 0 if root_count % 2 == 0 else root_count * internal_matchings(roots[1:])
        if without_endpoint != expected_without or with_endpoint != expected_with:
            raise AssertionError((root_count, without_endpoint, with_endpoint))
        if bool(without_endpoint) == bool(with_endpoint):
            raise AssertionError((root_count, "endpoint-use parity is not unique"))
        largest_count = max(largest_count, without_endpoint, with_endpoint)
        cases += 1
    return {"root_counts": cases, "maximum_roots": 12, "largest_matching_count": largest_count}


def rank_audit() -> dict[str, object]:
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
            axis_types = {
                axis
                for row in sample
                if (axis := axis_type(row)) is not None
            }
            predicted_rank_at_most_one = len(axis_types) >= 2
            if (rank <= 1) != predicted_rank_at_most_one:
                raise AssertionError((sample, rank, axis_types))
            rank_histogram[rank] += 1
            checked += 1
        counts[root_count] = checked

    balanced = ((1, 1, 0),) * 5
    if full_jet_rank(balanced) <= 1:
        raise AssertionError("uniform balanced five-root jet unexpectedly has rank at most one")
    return {
        "projective_covectors": len(rows),
        "tuple_counts": counts,
        "rank_histogram": rank_histogram,
        "uniform_balanced_five_root_rank": full_jet_rank(balanced),
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "full_jet_rank": rank_audit(),
                "endpoint_parity": endpoint_parity_audit(),
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
