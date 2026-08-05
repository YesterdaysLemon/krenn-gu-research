"""Independent no-import audit for the mixed second-jet rank theorem."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import product
from math import gcd

Vector = tuple[Fraction, Fraction, Fraction]


def canonical(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    common = 0
    for value in vector:
        common = gcd(common, abs(value))
    answer = tuple(value // common for value in vector)
    for value in answer:
        if value:
            if value < 0:
                answer = tuple(-entry for entry in answer)
            return answer  # type: ignore[return-value]
    raise AssertionError("zero vector")


def null_rows(row: tuple[int, int, int]) -> list[Vector]:
    pivot = max(range(3), key=lambda index: abs(row[index]))
    answer: list[Vector] = []
    for free in range(3):
        if free == pivot:
            continue
        vector = [Fraction(0), Fraction(0), Fraction(0)]
        vector[free] = Fraction(1)
        vector[pivot] = Fraction(-row[free], row[pivot])
        answer.append(tuple(vector))  # type: ignore[arg-type]
    return answer


def rank_of_product(row_a: tuple[int, int, int], row_b: tuple[int, int, int]) -> int:
    columns: list[tuple[Fraction, Fraction]] = []
    for left in null_rows(row_a):
        for right in null_rows(row_b):
            word = [left[index] * right[index] for index in range(3)]
            columns.append((word[0] - word[2], word[1] - word[2]))
    nonzero = [column for column in columns if column != (0, 0)]
    if not nonzero:
        return 0
    anchor = nonzero[0]
    if all(anchor[0] * column[1] == anchor[1] * column[0] for column in nonzero[1:]):
        return 1
    return 2


def predicted_rank_one(row_a: tuple[int, int, int], row_b: tuple[int, int, int]) -> bool:
    for coordinate in range(3):
        if row_a[coordinate] != 0 or row_b[coordinate] != 0:
            continue
        other = [index for index in range(3) if index != coordinate]
        if row_a[other[0]] * row_b[other[0]] == row_a[other[1]] * row_b[other[1]]:
            return True
    return False


def main() -> None:
    vectors = {
        canonical(vector)
        for vector in product(range(-3, 4), repeat=3)
        if vector != (0, 0, 0) and sum(vector) != 0
    }
    rank_counts = {1: 0, 2: 0}
    checked = 0
    permutation_checks = 0
    permutations = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    for row_a in vectors:
        for row_b in vectors:
            rank = rank_of_product(row_a, row_b)
            assert rank in (1, 2)
            assert (rank == 1) == predicted_rank_one(row_a, row_b)
            rank_counts[rank] += 1
            checked += 1
            for permutation in permutations:
                permuted_a = tuple(row_a[index] for index in permutation)
                permuted_b = tuple(row_b[index] for index in permutation)
                assert rank_of_product(permuted_a, permuted_b) == rank
                assert predicted_rank_one(permuted_a, permuted_b) == (rank == 1)
                permutation_checks += 1

    print(
        json.dumps(
            {
                "status": "audit_pass",
                "implementation": "independent fractions; no sympy or repository imports",
                "projective_covectors": len(vectors),
                "checked_pairs": checked,
                "permutation_checks": permutation_checks,
                "rank_counts": rank_counts,
                "rank_one_criterion_verified": True,
                "cofactor_realizability_proved": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
