#!/usr/bin/env python3
"""Independent weighted audit of the four-root/six-blocker transfer."""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "FOUR_ROOT_SIX_BLOCKER_ARBITRARY_ORDER_KERNEL_SUPPORT_OBSTRUCTION.md"


def weight(left: int, right: int, salt: int) -> Fraction:
    first, second = sorted((left, right))
    return Fraction((first + 2) * (second + 5) + salt, salt + 3)


def hafnian(vertices: tuple[int, ...], matrix) -> Fraction:
    @lru_cache(None)
    def recurse(active: tuple[int, ...]) -> Fraction:
        if not active:
            return Fraction(1)
        first = active[0]
        total = Fraction(0)
        for index in range(1, len(active)):
            second = active[index]
            remaining = active[1:index] + active[index + 1 :]
            total += matrix[first][second] * recurse(remaining)
        return total

    return recurse(vertices)


def permanent(matrix) -> Fraction:
    size = len(matrix)
    return sum(
        math.prod(matrix[row][permutation[row]] for row in range(size))
        for permutation in itertools.permutations(range(size))
    )


def weighted_case(residual_size: int, salt: int) -> dict[str, object]:
    roots = tuple(range(4))
    blockers = tuple(range(4, 10))
    residual = tuple(range(10, 10 + residual_size))
    size = 10 + residual_size
    values = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for left in range(size):
        for right in range(left + 1, size):
            root_forbidden = (left in roots or right in roots) and not (
                (left in roots and right in blockers)
                or (right in roots and left in blockers)
            )
            entry = Fraction(0) if root_forbidden else weight(left, right, salt)
            values[left][right] = values[right][left] = entry
    matrix = tuple(tuple(row) for row in values)

    full = hafnian(tuple(range(size)), matrix)
    cofactor = Fraction(0)
    for unused in itertools.combinations(blockers, 2):
        used = tuple(blocker for blocker in blockers if blocker not in unused)
        root_blocker = tuple(
            tuple(matrix[root][blocker] for blocker in used) for root in roots
        )
        cofactor += permanent(root_blocker) * hafnian((*residual, *unused), matrix)
    assert full == cofactor

    root_vectors = (
        (Fraction(2), Fraction(3), Fraction(5)),
        (Fraction(7), Fraction(11), Fraction(13)),
        (Fraction(17), Fraction(19), Fraction(23)),
        (Fraction(29), Fraction(31), Fraction(37)),
    )
    residual_vectors = tuple(
        tuple(Fraction(41 + 7 * index + colour) for colour in range(3))
        for index in range(residual_size)
    )
    diagonal = tuple(
        math.prod(vector[colour] for vector in root_vectors)
        * math.prod(vector[colour] for vector in residual_vectors)
        for colour in range(3)
    )
    assert all(diagonal)
    return {
        "residual_vertices": residual_size,
        "full_hafnian": str(full),
        "cofactor_sum": str(cofactor),
        "diagonal_coefficients": [str(value) for value in diagonal],
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    normalized = " ".join(theorem.split())
    assert "No finite-field inference is used" in normalized
    assert "at most two such modes: UNKNOWN" in theorem

    cases = tuple(
        weighted_case(residual_size, salt)
        for residual_size, salt in ((0, 2), (2, 5), (4, 7))
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent rational weighted-hafnian reconstruction",
                "field": "rational characteristic zero",
                "weighted_cases": cases,
                "arbitrary_order_claim_from_written_bijection": True,
                "full_local_to_global_reduction_complete": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
