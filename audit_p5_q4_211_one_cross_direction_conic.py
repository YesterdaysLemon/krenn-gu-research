#!/usr/bin/env python3
"""Independent finite-field audit of the direction-conic reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md"


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
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    next_states.get(new_mask, 0) + coefficient * value
                ) % prime
        states = next_states
    return states[(1 << len(rows)) - 1]


def rank_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
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
        for row in range(len(rows)):
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
        pivot_row += 1
    return pivot_row


def projective_lines(prime):
    return [(1, value) for value in range(prime)] + [(0, 1)]


def proportional(left, right, prime):
    return all(
        (
            left[index] * right[(index + 1) % 2]
            - left[(index + 1) % 2] * right[index]
        ) % prime == 0
        for index in range(2)
    )


def audit_prime(prime):
    a, b, c = 2 % prime, 3 % prime, 4 % prime
    inv2 = pow(2, -1, prime)
    matrix = [
        [a * inv2 % prime, 0, 1],
        [0, -a * inv2 % prime, 0],
        [1, 0, 0],
    ]
    assert rank_mod(matrix, prime) == 3

    q_solutions = []
    p_solutions = []
    for first in projective_lines(prime):
        for second in projective_lines(prime):
            A, B = first
            C, D = second
            normal_value = (
                2
                * (A * b + B * c)
                * (C * b + D * c)
            ) % prime
            if (-2 * b * A * C) % prime == 0 and normal_value == 0:
                q_solutions.append((first, second))
            if (-2 * c * B * D) % prime == 0 and normal_value == 0:
                p_solutions.append((first, second))

    u1 = (1, 0)
    u2 = (0, 1)
    m = (1, -b * pow(c, -1, prime) % prime)
    expected_q = {
        (u2, m),
        (m, u2),
    }
    expected_p = {
        (u1, m),
        (m, u1),
    }
    assert set(q_solutions) == expected_q
    assert set(p_solutions) == expected_p
    return {
        "prime": prime,
        "conic_rank": 3,
        "ordered_direction_pairs_checked": (prime + 1) ** 2,
        "q_solution_pairs": len(q_solutions),
        "p_solution_pairs": len(p_solutions),
    }


def main() -> None:
    output = {
        "audited": True,
        "method": (
            "independent modular conic rank and projective "
            "direction-pair checks"
        ),
        "finite_field_audits": [
            audit_prime(prime) for prime in (5, 7)
        ],
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "q_direction_lines": ["C*u2", "C*(c*u1-b*u2)"],
        "p_direction_lines": ["C*u1", "C*(c*u1-b*u2)"],
        "free_polar_core_retained": False,
        "remaining_gate_count": 4,
        "one_cross_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "one-cross direction conic",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_direction_conic_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
