"""Verify the GHZ mixed second-jet quotient rank classification exactly."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import product
from math import gcd

import sympy as sp

Vector = tuple[Fraction, Fraction, Fraction]


def primitive(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    divisor = 0
    for entry in vector:
        divisor = gcd(divisor, abs(entry))
    reduced = tuple(entry // divisor for entry in vector)
    first = next(entry for entry in reduced if entry)
    if first < 0:
        reduced = tuple(-entry for entry in reduced)
    return reduced  # type: ignore[return-value]


def kernel_basis(covector: tuple[int, int, int]) -> tuple[Vector, Vector]:
    pivot = next(index for index, value in enumerate(covector) if value)
    others = [index for index in range(3) if index != pivot]
    basis = []
    for other in others:
        vector = [Fraction(0), Fraction(0), Fraction(0)]
        vector[other] = Fraction(covector[pivot])
        vector[pivot] = Fraction(-covector[other])
        basis.append(tuple(vector))
    return basis[0], basis[1]  # type: ignore[return-value]


def quotient_column(left: Vector, right: Vector) -> tuple[Fraction, Fraction]:
    value = tuple(a * b for a, b in zip(left, right, strict=True))
    return value[1] - value[0], value[2] - value[0]


def quotient_rank(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    left = kernel_basis(a)
    right = kernel_basis(b)
    columns = [quotient_column(u, v) for u in left for v in right]
    if all(column == (0, 0) for column in columns):
        return 0
    for i in range(4):
        for j in range(i + 1, 4):
            if columns[i][0] * columns[j][1] != columns[i][1] * columns[j][0]:
                return 2
    return 1


def resonant(a: tuple[int, int, int], b: tuple[int, int, int]) -> bool:
    for missing in range(3):
        if a[missing] or b[missing]:
            continue
        remaining = [index for index in range(3) if index != missing]
        if a[remaining[0]] * b[remaining[0]] == a[remaining[1]] * b[remaining[1]]:
            return True
    return False


def symbolic_minors() -> dict[str, object]:
    a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2")
    matrix = sp.Matrix(
        [
            [a0 * b0 - a1 * b1, -a1 * b2, -a2 * b1, -a2 * b2],
            [-a1 * b1, -a1 * b2, -a2 * b1, a0 * b0 - a2 * b2],
        ]
    )
    minors = [
        sp.factor(matrix[:, [i, j]].det()) for i in range(4) for j in range(i + 1, 4)
    ]
    expected = [
        -a0 * a1 * b0 * b2,
        -a0 * a2 * b0 * b1,
        a0 * b0 * (a0 * b0 - a1 * b1 - a2 * b2),
        0,
        -a0 * a1 * b0 * b2,
        -a0 * a2 * b0 * b1,
    ]
    if any(sp.expand(actual - target) != 0 for actual, target in zip(minors, expected, strict=True)):
        raise AssertionError((minors, expected))
    return {"matrix": str(matrix.tolist()), "minors": [str(value) for value in minors]}


def exhaustive_box() -> dict[str, int]:
    vectors = {
        primitive(vector)
        for vector in product(range(-2, 3), repeat=3)
        if vector != (0, 0, 0) and sum(vector) != 0
    }
    counts = {"pairs": 0, "rank_one": 0, "rank_two": 0}
    for a in vectors:
        for b in vectors:
            rank = quotient_rank(a, b)
            if rank not in (1, 2):
                raise AssertionError((a, b, rank))
            if (rank == 1) != resonant(a, b):
                raise AssertionError((a, b, rank, resonant(a, b)))
            counts["pairs"] += 1
            counts[f"rank_{'one' if rank == 1 else 'two'}"] += 1
    return counts


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "symbolic_chart": symbolic_minors(),
                "exhaustive_projective_box": exhaustive_box(),
                "rank_values": [1, 2],
                "rank_one_criterion": "exists c: a_c=b_c=0 and a_p*b_p=a_q*b_q",
                "generic_second_cofactor_classes_required": 2,
                "resonant_second_cofactor_classes_required": 1,
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
