#!/usr/bin/env python3
"""Independent DP and finite-field audit of one-nonblocker extraction."""

from __future__ import annotations

import itertools
import json
import math
from functools import lru_cache

P = 5


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


def surplus_adjacency(r: int) -> tuple[tuple[bool, ...], ...]:
    roots = set(range(r))
    marker = r
    blockers = set(range(r + 1, 2 * r + 2))
    size = 2 * r + 2
    matrix = [[False] * size for _ in range(size)]
    for left in range(size):
        for right in range(left + 1, size):
            allowed = (
                (left in roots and right in blockers)
                or (right in roots and left in blockers)
                or (left == marker and right in blockers)
                or (right == marker and left in blockers)
                or (left in blockers and right in blockers)
            )
            matrix[left][right] = matrix[right][left] = allowed
    return tuple(tuple(row) for row in matrix)


def projective_vectors() -> list[tuple[int, int, int]]:
    vectors = []
    for vector in itertools.product(range(P), repeat=3):
        if vector == (0, 0, 0):
            continue
        first = next(value for value in vector if value)
        inverse = pow(first, -1, P)
        normalized = tuple((inverse * value) % P for value in vector)
        if normalized not in vectors:
            vectors.append(normalized)
    return vectors


def span(vectors: tuple[tuple[int, int, int], ...]) -> set[tuple[int, int, int]]:
    if not vectors:
        return {(0, 0, 0)}
    result = set()
    for coefficients in itertools.product(range(P), repeat=len(vectors)):
        result.add(
            tuple(
                sum(
                    coefficient * vector[index]
                    for coefficient, vector in zip(
                        coefficients, vectors, strict=True
                    )
                )
                % P
                for index in range(3)
            )
        )
    return result


def torus_kernel_audit() -> dict:
    projective = projective_vectors()
    coordinate = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}
    subspaces = [span(())]
    subspaces.extend(span((line,)) for line in projective)
    # Every plane is the kernel of one projective normal.
    subspaces.extend(
        {
            vector
            for vector in itertools.product(range(P), repeat=3)
            if sum(left * right for left, right in zip(normal, vector, strict=True)) % P == 0
        }
        for normal in projective
    )
    unique = {frozenset(space) for space in subspaces}
    qualifying = 0
    for a_space in unique:
        if any(unit in a_space for unit in coordinate):
            continue
        kernel = {
            z
            for z in itertools.product(range(P), repeat=3)
            if all(
                sum(
                    left * right
                    for left, right in zip(a, z, strict=True)
                )
                % P
                == 0
                for a in a_space
            )
        }
        assert any(all(entry != 0 for entry in z) for z in kernel)
        qualifying += 1
    return {"subspaces": len(unique), "qualifying_nonblocker_subspaces": qualifying}


def main() -> None:
    records = []
    for r in range(2, 7):
        count = matching_count(surplus_adjacency(r))
        assert count == math.factorial(r + 1)
        records.append({"r": r, "dp_survivors": count})
    torus = torus_kernel_audit()
    print(
        json.dumps(
            {
                "audited": True,
                "matching_dp": records,
                "torus_kernel_audit": torus,
                "torus_field": "F_5",
                "formula_audit_only": True,
                "permanent_nonrestriction_proved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
