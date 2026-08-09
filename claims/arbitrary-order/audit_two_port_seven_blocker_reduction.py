#!/usr/bin/env python3
"""Finite combinatorial audit of the two-port seven-blocker reduction."""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "verify_two_port_seven_blocker_reduction.py"
THEOREM = ROOT / "TWO_PORT_SEVEN_BLOCKER_REDUCTION.md"


def matching_count(adjacency: tuple[tuple[bool, ...], ...]) -> int:
    size = len(adjacency)

    @lru_cache(None)
    def count(mask: int) -> int:
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        total = 0
        partners = rest
        while partners:
            bit = partners & -partners
            second = bit.bit_length() - 1
            if adjacency[first][second]:
                total += count(rest ^ bit)
            partners ^= bit
        return total

    return count((1 << size) - 1)


def seven_blocker_adjacency() -> tuple[tuple[bool, ...], ...]:
    roots = set(range(5))
    matrix = [[False] * 12 for _ in range(12)]
    for left in range(12):
        for right in range(left + 1, 12):
            allowed = not (left in roots and right in roots)
            matrix[left][right] = matrix[right][left] = allowed
    return tuple(tuple(row) for row in matrix)


def surplus_adjacency(
    roots_count: int, surplus: int, residual: int
) -> tuple[tuple[bool, ...], ...]:
    roots = set(range(roots_count))
    blockers_end = 2 * roots_count + surplus
    residual_vertices = set(range(blockers_end, blockers_end + residual))
    size = blockers_end + residual
    matrix = [[False] * size for _ in range(size)]
    for left in range(size):
        for right in range(left + 1, size):
            root_root = left in roots and right in roots
            root_residual = (left in roots and right in residual_vertices) or (
                right in roots and left in residual_vertices
            )
            matrix[left][right] = matrix[right][left] = not (
                root_root or root_residual
            )
    return tuple(tuple(row) for row in matrix)


def odd_double_factorial(value: int) -> int:
    return math.prod(range(value, 0, -2)) if value > 0 else 1


def audit_surplus_case(roots: int, surplus: int, residual: int) -> dict[str, int]:
    count = matching_count(surplus_adjacency(roots, surplus, residual))
    expected = (
        math.comb(roots + surplus, surplus)
        * math.factorial(roots)
        * odd_double_factorial(surplus + residual - 1)
    )
    assert count == expected
    return {
        "roots": roots,
        "surplus": surplus,
        "residual": residual,
        "surviving_matchings": count,
    }


def main() -> None:
    primary = PRIMARY.read_text(encoding="utf-8")
    theorem = THEOREM.read_text(encoding="utf-8")
    for fragment in (
        '"residual_cofactor_degree": 2',
        '"p6_extracted": False',
        '"global_conjecture_resolved": False',
    ):
        assert fragment in primary
    for fragment in (
        "genuine two-port tensor",
        "three overlapping pure `P_5` restrictions",
        "UNRESOLVED",
    ):
        assert fragment in theorem

    count = matching_count(seven_blocker_adjacency())
    assert count == 21 * 120
    general_cases = [
        audit_surplus_case(*case)
        for case in ((2, 0, 2), (2, 1, 3), (2, 2, 2), (2, 3, 1), (3, 3, 1))
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "audit_field": "finite combinatorics only",
                "five_root_seven_blocker_survivors": count,
                "unused_pairs": 21,
                "bijections_per_pair": 120,
                "general_surplus_cases": general_cases,
                "characteristic_zero_proof_replaced_by_audit": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
