#!/usr/bin/env python3
"""Independent finite-field incidence audit for the triangle obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_TRIANGLE_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(rows, prime: int) -> int:
    if not rows:
        return 0
    matrix = [[value % prime for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime
            for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(
                    matrix[row],
                    matrix[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def rref_subspaces(prime: int):
    for pivots in itertools.combinations(range(5), 3):
        free_positions = tuple(
            (row, column)
            for column in range(5)
            if column not in pivots
            for row, pivot in enumerate(pivots)
            if pivot < column
        )
        for values in itertools.product(
            range(prime),
            repeat=len(free_positions),
        ):
            rows = [[0] * 5 for _ in range(3)]
            for row, pivot in enumerate(pivots):
                rows[row][pivot] = 1
            for (row, column), value in zip(
                free_positions,
                values,
                strict=True,
            ):
                rows[row][column] = value
            yield tuple(tuple(row) for row in rows)


def contains(rows, vector, prime: int) -> bool:
    return rank_mod(rows + (vector,), prime) == 3


def restrict(rows, basis, prime: int):
    return tuple(
        tuple(
            sum(
                left * right
                for left, right in zip(row, vector, strict=True)
            )
            % prime
            for vector in basis
        )
        for row in rows
    )


def restriction_rank(rows, basis, prime: int) -> int:
    return rank_mod(restrict(rows, basis, prime), prime)


def row_basis(rows, prime: int):
    accepted = []
    for row in rows:
        if rank_mod(tuple(accepted) + (row,), prime) > len(accepted):
            accepted.append(row)
    return tuple(accepted)


def plane_normal_support(rows, basis, prime: int):
    restricted = row_basis(restrict(rows, basis, prime), prime)
    assert len(restricted) == 2
    first, second = restricted
    normal = (
        (first[1] * second[2] - first[2] * second[1]) % prime,
        (first[2] * second[0] - first[0] * second[2]) % prime,
        (first[0] * second[1] - first[1] * second[0]) % prime,
    )
    assert any(normal)
    return tuple(index for index, value in enumerate(normal) if value)


def audit_prime(prime: int) -> dict:
    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = (1, 1, 0, 0, 0)
    h0 = (1, -1, 0, 0, 0)
    u1 = (0, 0, 1, 1, 0)
    h1 = (0, 0, 1, -1, 0)
    h2 = e[4]
    j02 = (u0, e[2], e[3])
    j12 = (e[0], e[1], u1)
    j01 = (u0, h1, h2)
    j10 = (h0, u1, h2)

    spaces = tuple(rref_subspaces(prime))
    exact_a = tuple(
        rows
        for rows in spaces
        if contains(rows, h0, prime)
        and contains(rows, h1, prime)
        and not contains(rows, h2, prime)
    )
    full_a = tuple(
        rows
        for rows in exact_a
        if restriction_rank(rows, j02, prime) == 2
        and restriction_rank(rows, j12, prime) == 2
        and plane_normal_support(rows, j02, prime) == (0, 1, 2)
        and plane_normal_support(rows, j12, prime) == (0, 1, 2)
    )
    assert full_a

    exact_c = tuple(
        rows
        for rows in spaces
        if contains(rows, h1, prime)
        and contains(rows, h2, prime)
        and not contains(rows, h0, prime)
    )
    full_c02 = tuple(
        rows
        for rows in exact_c
        if restriction_rank(rows, j02, prime) == 2
        and plane_normal_support(rows, j02, prime) == (0, 1, 2)
    )
    assert full_c02
    assert all(
        restriction_rank(rows, j01, prime) == 3
        for rows in full_c02
    )

    exact_b = tuple(
        rows
        for rows in spaces
        if contains(rows, h0, prime)
        and contains(rows, h2, prime)
        and not contains(rows, h1, prime)
    )
    full_b12 = tuple(
        rows
        for rows in exact_b
        if restriction_rank(rows, j12, prime) == 2
        and plane_normal_support(rows, j12, prime) == (0, 1, 2)
    )
    assert full_b12
    assert all(
        restriction_rank(rows, j10, prime) == 3
        for rows in full_b12
    )

    exact_d = tuple(
        rows
        for rows in spaces
        if not contains(rows, h0, prime)
        and not contains(rows, h1, prime)
        and not contains(rows, h2, prime)
    )
    assert exact_d
    assert all(
        restriction_rank(rows, j01, prime) >= 2
        and restriction_rank(rows, j10, prime) >= 2
        for rows in exact_d
    )

    exact_d_h2 = tuple(
        rows
        for rows in spaces
        if contains(rows, h2, prime)
        and not contains(rows, h0, prime)
        and not contains(rows, h1, prime)
    )
    assert exact_d_h2
    assert all(
        restriction_rank(rows, j02, prime) == 2
        and restriction_rank(rows, j12, prime) == 2
        and restriction_rank(rows, j01, prime) >= 2
        and restriction_rank(rows, j10, prime) >= 2
        for rows in exact_d_h2
    )

    exact_d_h0 = tuple(
        rows
        for rows in spaces
        if contains(rows, h0, prime)
        and not contains(rows, h1, prime)
        and not contains(rows, h2, prime)
    )
    assert exact_d_h0
    d_h0_q01_rank_one = tuple(
        rows
        for rows in exact_d_h0
        if restriction_rank(rows, j01, prime) == 1
    )
    assert d_h0_q01_rank_one
    assert all(
        restriction_rank(rows, j10, prime) >= 2
        and restriction_rank(rows, j02, prime) == 2
        and restriction_rank(rows, j12, prime) >= 2
        for rows in exact_d_h0
    )
    d_h0_q01_with_j12_rank_two = tuple(
        rows
        for rows in d_h0_q01_rank_one
        if restriction_rank(rows, j12, prime) == 2
    )
    assert d_h0_q01_with_j12_rank_two
    assert all(
        plane_normal_support(rows, j02, prime) == (0,)
        for rows in d_h0_q01_with_j12_rank_two
    )
    assert all(
        not (
            restriction_rank(rows, j12, prime) == 2
            and plane_normal_support(rows, j02, prime) == (0, 1, 2)
        )
        for rows in d_h0_q01_rank_one
    )

    b01_rank_one = tuple(
        rows
        for rows in exact_b
        if restriction_rank(rows, j01, prime) == 1
    )
    c10_rank_one = tuple(
        rows
        for rows in exact_c
        if restriction_rank(rows, j10, prime) == 1
    )
    assert len(b01_rank_one) == len(c10_rank_one) == 1
    assert contains(b01_rank_one[0], u1, prime)
    assert contains(c10_rank_one[0], u0, prime)

    c01_rank_two = tuple(
        rows
        for rows in exact_c
        if restriction_rank(rows, j01, prime) == 2
    )
    b10_rank_two = tuple(
        rows
        for rows in exact_b
        if restriction_rank(rows, j10, prime) == 2
    )
    assert c01_rank_two and b10_rank_two
    assert all(
        plane_normal_support(rows, j01, prime) == (0,)
        for rows in c01_rank_two
    )
    assert all(
        plane_normal_support(rows, j10, prime) == (1,)
        for rows in b10_rank_two
    )

    return {
        "prime": prime,
        "rank_three_row_spaces": len(spaces),
        "exact_A_spaces": len(exact_a),
        "full_support_A_spaces": len(full_a),
        "full_support_C02_spaces": len(full_c02),
        "full_support_B12_spaces": len(full_b12),
        "exact_D_spaces": len(exact_d),
        "exact_D_h2_spaces": len(exact_d_h2),
        "exact_D_h0_spaces": len(exact_d_h0),
        "D_h0_Q01_rank_one_spaces": len(d_h0_q01_rank_one),
        "D_h0_Q01_with_J12_rank_two_spaces": len(
            d_h0_q01_with_j12_rank_two
        ),
        "C02_forced_J01_rank": 3,
        "B12_forced_J10_rank": 3,
        "D_minimum_cross_rank": 2,
        "D_h2_direct_residual_ranks": [2, 2],
        "D_h2_minimum_cross_rank": 2,
        "D_h0_rank_one_forces_Q02_support_one": True,
        "chirality_II_B_J01_rank_one_spaces": len(b01_rank_one),
        "chirality_II_C_J10_rank_one_spaces": len(c10_rank_one),
        "chirality_II_C_J01_support_one_spaces": len(c01_rank_two),
        "chirality_II_B_J10_support_one_spaces": len(b10_rank_two),
    }


def main() -> None:
    output = {
        "audited": True,
        "finite_fields": [audit_prime(prime) for prime in (3, 5)],
        "common_support_implications_checked": ["C02->J01", "B12->J10"],
        "exact_triangle_excluded": True,
        "distinguished_singleton_triangle_cover_excluded": True,
        "majority_singleton_triangle_cover_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "independent finite-field incidence audit",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_triangle_obstruction_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
