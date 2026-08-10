#!/usr/bin/env python3
"""Independent finite-field audit of the alternating-gate obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md"


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


def slice_matrix(mode, row_pairs, prime):
    matrix = []
    for word in itertools.product((0, 1), repeat=3):
        row = []
        for coordinate in range(4):
            rows = []
            other_index = 0
            for index in range(4):
                if index == mode:
                    rows.append(
                        tuple(
                            int(entry == coordinate)
                            for entry in range(4)
                        )
                    )
                else:
                    rows.append(row_pairs[index][word[other_index]])
                    other_index += 1
            row.append(permanent_dynamic(rows, prime))
        matrix.append(row)
    return matrix


def projective_lines(prime):
    return [(1, value) for value in range(prime)] + [(0, 1)]


def contraction_support(directions, prime):
    # P5 is the sum of all assignments of five distinct coordinates.
    remaining_degree = 5 - len(directions)
    coefficients = {}
    for remaining in itertools.combinations(range(5), remaining_degree):
        contracted = tuple(
            coordinate for coordinate in range(5)
            if coordinate not in remaining
        )
        value = 0
        for assignment in itertools.permutations(contracted):
            product = 1
            for row, coordinate in zip(
                directions,
                assignment,
                strict=True,
            ):
                product *= row[coordinate]
            value += product
        value %= prime
        if value:
            coefficients[remaining] = value
    return coefficients


def audit_prime(prime):
    e2 = (0, 0, 1, 0)
    e3 = (0, 0, 0, 1)
    transverse_points = 0
    for p, q in projective_lines(prime):
        for r, t in projective_lines(prime):
            lam = (p * t + q * r) % prime
            delta = (p * t - q * r) % prime
            if not lam or not delta:
                continue
            x2, x3, y2, y3 = 1, 2 % prime, 3 % prime, 4 % prime
            row_pairs = (
                (e2, e3),
                ((p, q, x2, x3), e2),
                (e3, (r, -t, y2, y3)),
                (
                    (
                        delta * r,
                        delta * t,
                        lam * y2,
                        lam * y3,
                    ),
                    (
                        delta * p,
                        -delta * q,
                        -lam * x2,
                        -lam * x3,
                    ),
                ),
            )
            ranks = [
                rank_mod(slice_matrix(mode, row_pairs, prime), prime)
                for mode in (1, 2, 3)
            ]
            assert ranks == [4, 4, 4]
            transverse_points += 1

    tangent_points = 0
    for p, q in projective_lines(prime):
        if not p or not q:
            continue
        row_pairs = (
            (e2, e3),
            ((p, q, 0, 0), e2),
            (e3, (p, -q, 0, 0)),
            (
                (p, q, 1, 2 % prime),
                (p, -q, 3 % prime, 4 % prime),
            ),
        )
        matrices = [
            slice_matrix(mode, row_pairs, prime)
            for mode in (1, 2, 3)
        ]
        assert [
            rank_mod(matrix, prime) for matrix in matrices
        ] == [4, 4, 2]
        assert all(row[2:] == [0, 0] for row in matrices[2])
        assert rank_mod(
            [row[:2] for row in matrices[2]],
            prime,
        ) == 2
        assert (-2 * p * q) % prime
        tangent_points += 1

    b, c = 2 % prime, 3 % prime
    n = (0, 0, 0, c, b)
    double_support = contraction_support((n, n), prime)
    triple_support = contraction_support((n, n, n), prime)
    assert double_support == {
        (0, 1, 2): 2 * b * c % prime
    }
    assert triple_support == {}

    return {
        "prime": prime,
        "transverse_projective_points": transverse_points,
        "transverse_slice_ranks": [4, 4, 4],
        "tangent_projective_points": tangent_points,
        "tangent_slice_ranks": [4, 4, 2],
        "double_normal_support": ["012"],
        "triple_normal_support": [],
    }


def main() -> None:
    output = {
        "audited": True,
        "method": (
            "independent dynamic permanents, modular row reduction, "
            "and squarefree contraction support"
        ),
        "finite_field_audits": [
            audit_prime(prime) for prime in (5, 7)
        ],
        "ambient_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "two_cross_marked_boundary_excluded": True,
        "one_cross_normal_incidence_retained": True,
        "adjacent_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "generic adjacent alternating-gate lift",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_alternating_gate_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
