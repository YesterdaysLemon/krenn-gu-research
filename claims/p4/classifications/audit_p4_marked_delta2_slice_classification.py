#!/usr/bin/env python3
"""Independent finite-field audit of the marked Delta2 slice theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dynamic(rows, prime):
    states = {0: 1}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                next_states[next_mask] = (
                    next_states.get(next_mask, 0) + coefficient * value
                ) % prime
        states = next_states
    return states[(1 << len(rows)) - 1]


def nullspace_basis_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0])
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [
            value * inverse % prime for value in rows[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            multiple = rows[row][column]
            if multiple:
                rows[row] = [
                    (left - multiple * right) % prime
                    for left, right in zip(
                        rows[row],
                        rows[pivot_row],
                        strict=True,
                    )
                ]
        pivots.append(column)
        pivot_row += 1
    free = [column for column in range(column_count) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * column_count
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -rows[row][free_column] % prime
        basis.append(tuple(vector))
    return basis


def audit_prime(prime):
    family_points = 0
    shared_cases = 0
    omitted_cases = 0
    for A in range(1, prime):
        for B in range(prime):
            for T in range(1, prime):
                alpha = (
                    (0, 1, T, -B % prime),
                    (1, 0, 0, A),
                    (1, 0, 0, A),
                )
                beta = (
                    (1, 0, 0, -A % prime),
                    (0, 1, -T % prime, B),
                    (B, A, -A * T % prime, 0),
                )
                coefficients = {}
                for word in itertools.product((0, 1), repeat=4):
                    first = (0, 0, 1, 0) if word[0] == 0 else (0, 0, 0, 1)
                    rows = [first] + [
                        alpha[index] if word[index + 1] == 0 else beta[index]
                        for index in range(3)
                    ]
                    coefficients[word] = permanent_dynamic(rows, prime)
                assert coefficients[(0, 0, 0, 0)] == 2 * A % prime
                assert coefficients[(1, 1, 1, 1)] == -2 * A * T % prime
                assert all(
                    value == 0
                    for word, value in coefficients.items()
                    if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
                )
                family_points += 1

            # Variable order: x1,y1,x2,y2,x3,y3.
            shared_matrix = (
                (2 * A, 0, -B, 0, -B, 0),
                (A * B, 0, -B * B, 0, 0, -B),
                (B, 0, 0, -B, 0, 0),
                (B * B, 0, 0, -B * B, 0, 0),
                (0, 2 * A, 0, 0, 0, 0),
                (0, A * B, -A * B, 0, 0, 0),
                (0, B, 0, 0, B, 0),
            )
            shared_pure = (0, B * B, 0, -A * B, 0, B)
            for vector in nullspace_basis_mod(shared_matrix, prime):
                assert sum(
                    left * right
                    for left, right in zip(shared_pure, vector, strict=True)
                ) % prime == 0
            shared_cases += 1

            omitted_matrix = (
                (0, 0, 1, 0, 1, 0),
                (A, 0, B, 0, 0, 1),
                (1, 0, 0, 1, 0, 0),
                (B, 0, 0, B, 0, 0),
                (0, A, A, 0, 0, 0),
                (0, 1, 0, 0, 1, 0),
            )
            omitted_pure = (0, B, 0, A, 0, 1)
            omitted_nullspace = nullspace_basis_mod(omitted_matrix, prime)
            assert len(omitted_nullspace) == 1
            assert sum(
                left * right
                for left, right in zip(
                    omitted_pure,
                    omitted_nullspace[0],
                    strict=True,
                )
            ) % prime != 0
            omitted_cases += 1

    return {
        "prime": prime,
        "explicit_family_points_checked": family_points,
        "shared_common_coordinate_systems": shared_cases,
        "shared_system_pure_functional_zero": True,
        "omitted_common_coordinate_systems": omitted_cases,
        "omitted_system_nullity": 1,
    }


def main() -> None:
    output = {
        "audited": True,
        "method": "dynamic-programming permanents and finite-field linear systems",
        "finite_field_audits": [audit_prime(prime) for prime in (3, 5)],
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "all_rank_two_family_retained": True,
        "marked_Delta2_boundary_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "marked P4-to-Delta2 slice compatibility",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p4_marked_delta2_slice_classification_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
