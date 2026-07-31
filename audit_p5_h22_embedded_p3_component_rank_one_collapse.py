#!/usr/bin/env python3
"""Independent modular audit of the rank-one weighted H22 collapse."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h22_embedded_p3_component_rank_one_collapse.py"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def squarefree_top(rows, prime: int) -> int:
    size = len(rows)
    coefficients = {0: 1}
    for row in rows:
        updated: dict[int, int] = {}
        for support, coefficient in coefficients.items():
            for coordinate, entry in enumerate(row):
                bit = 1 << coordinate
                if support & bit:
                    continue
                target = support | bit
                updated[target] = (
                    updated.get(target, 0) + coefficient * entry
                ) % prime
        coefficients = updated
    return coefficients.get((1 << size) - 1, 0)


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    result = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(result[0]) if result else 0):
        selected = next(
            (
                row
                for row in range(pivot_row, len(result))
                if result[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = (
            result[selected],
            result[pivot_row],
        )
        inverse = pow(result[pivot_row][column], -1, prime)
        result[pivot_row] = [
            entry * inverse % prime for entry in result[pivot_row]
        ]
        for row in range(len(result)):
            if row == pivot_row:
                continue
            multiplier = result[row][column]
            if multiplier:
                result[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(
                        result[row], result[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == len(result):
            break
    return pivot_row


def nullspace_mod(matrix: list[list[int]], prime: int):
    result = [[entry % prime for entry in row] for row in matrix]
    pivots = []
    pivot_row = 0
    for column in range(len(result[0])):
        selected = next(
            (
                row
                for row in range(pivot_row, len(result))
                if result[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = (
            result[selected],
            result[pivot_row],
        )
        inverse = pow(result[pivot_row][column], -1, prime)
        result[pivot_row] = [
            entry * inverse % prime for entry in result[pivot_row]
        ]
        for row in range(len(result)):
            if row == pivot_row:
                continue
            multiplier = result[row][column]
            if multiplier:
                result[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(
                        result[row], result[pivot_row], strict=True
                    )
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(result):
            break
    free = [
        column
        for column in range(len(result[0]))
        if column not in pivots
    ]
    basis = []
    for free_column in free:
        vector = [0] * len(result[0])
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -result[row][free_column] % prime
        basis.append(vector)
    return basis


def projected_row_01(row, extension, slope, prime: int):
    return (
        (slope * row[0] + row[1]) % prime,
        row[2] % prime,
        row[3] % prime,
        extension % prime,
    )


def projected_row_23(row, extension, slope, prime: int):
    return (
        row[0] % prime,
        row[1] % prime,
        (slope * row[2] + row[3]) % prime,
        extension % prime,
    )


def audit_fibre(cap_s: int, prime: int):
    cap_u = 3
    slope = pow(cap_s % prime, -1, prime)
    cap_t = cap_u * slope % prime
    alpha = (
        (0, 1, cap_s, cap_u),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta = (
        (1, 0, 1, cap_t),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    marked_beta_zero = tuple(
        (
            beta[0][coordinate]
            - slope * alpha[0][coordinate]
        )
        % prime
        for coordinate in range(4)
    )
    marked_beta = (marked_beta_zero, *beta[1:])
    unwanted_words = tuple(
        word for word in WORDS3 if word != (1, 1, 1)
    )
    insertion = []
    desired_23 = []
    desired_01 = []
    for variable in range(6):
        extension = [0] * 8
        if variable < 3:
            extension[1 + variable] = 1
        else:
            extension[5 + variable - 3] = 1
        alpha_23 = tuple(
            projected_row_23(
                alpha[mode], extension[mode], slope, prime
            )
            for mode in range(4)
        )
        beta_23 = tuple(
            projected_row_23(
                marked_beta[mode],
                extension[4 + mode],
                slope,
                prime,
            )
            for mode in range(4)
        )
        insertion.append(
            [
                squarefree_top(
                    (beta_23[0],)
                    + tuple(
                        beta_23[mode + 1]
                        if word[mode]
                        else alpha_23[mode + 1]
                        for mode in range(3)
                    ),
                    prime,
                )
                for word in unwanted_words
            ]
        )
        desired_23.append(
            squarefree_top(beta_23, prime)
        )

        alpha_01 = tuple(
            projected_row_01(
                alpha[mode], extension[mode], slope, prime
            )
            for mode in range(4)
        )
        desired_01.append(squarefree_top(alpha_01, prime))

    insertion_matrix = [
        [insertion[column][row] for column in range(6)]
        for row in range(7)
    ]
    rank = rank_mod(insertion_matrix, prime)
    kernel = nullspace_mod(insertion_matrix, prime)
    assert len(kernel) == 6 - rank
    return {
        "rank": rank,
        "kernel_dimension": len(kernel),
        "kernel_kills_D23_beta_diagonal": all(
            sum(
                desired_23[index] * vector[index]
                for index in range(6)
            )
            % prime
            == 0
            for vector in kernel
        ),
        "kernel_kills_D01_alpha_diagonal": all(
            sum(
                desired_01[index] * vector[index]
                for index in range(6)
            )
            % prime
            == 0
            for vector in kernel
        ),
    }


def audit_prime(prime: int):
    generic = audit_fibre(2, prime)
    plus = audit_fibre(1, prime)
    minus = audit_fibre(-1, prime)
    assert generic["rank"] == 6
    assert plus["rank"] == 4
    assert plus["kernel_kills_D23_beta_diagonal"]
    assert minus["rank"] == 4
    assert minus["kernel_kills_D01_alpha_diagonal"]
    return {
        "S_equals_2": generic,
        "S_equals_1": plus,
        "S_equals_minus_1": minus,
    }


def main() -> None:
    audits = {str(prime): audit_prime(prime) for prime in (101, 103)}
    output = {
        "verified": True,
        "method": (
            "independent squarefree subset multiplication and "
            "modular complementary-insertion kernels"
        ),
        "primes": audits,
        "generic_complementary_insertion_rank": 6,
        "exceptional_complementary_insertion_rank": 4,
        "rank_one_projection_collapse_weighted_H22_fibre_empty": True,
        "finite_field_audit_is_theorem": False,
        "global_problem_resolved": False,
        "dependencies": {
            THEOREM.name: sha256(THEOREM),
            PRIMARY.name: sha256(PRIMARY),
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
