#!/usr/bin/env python3
"""Independent no-import audit of nonzero-cross maximal-overlap port freedom."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction

import sympy as sp

Vector = tuple[Fraction, Fraction, Fraction]


def vector(*entries: int | Fraction) -> Vector:
    return tuple(Fraction(entry) for entry in entries)  # type: ignore[return-value]


def linear(*terms: tuple[int, Vector]) -> Vector:
    return tuple(
        sum(Fraction(scale) * item[index] for scale, item in terms)
        for index in range(3)
    )  # type: ignore[return-value]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum(a * b for a, b in zip(left, right))


def root_rows() -> tuple[tuple[Vector, ...], ...]:
    e0, e1, e2 = vector(1, 0, 0), vector(0, 1, 0), vector(0, 0, 1)
    exceptional0 = (
        e1,
        e2,
        linear((1, e1), (1, e2)),
        linear((1, e1), (2, e2)),
        linear((1, e1), (-1, e2)),
        e0,
    )
    exceptional1 = (
        e0,
        e2,
        linear((1, e0), (1, e2)),
        linear((1, e0), (2, e2)),
        linear((1, e0), (-1, e2)),
        e1,
    )
    exceptional2 = (
        e0,
        e1,
        linear((1, e0), (1, e1)),
        linear((1, e0), (2, e1)),
        linear((1, e0), (-1, e1)),
        e2,
    )
    full = (
        e0,
        e1,
        e2,
        vector(1, 1, 1),
        vector(1, 2, 3),
        vector(3, 2, 1),
    )
    return (exceptional0, exceptional1, exceptional2, full, full, full)


def span_profile(rows: tuple[Vector, ...]) -> int:
    matrix = sp.Matrix(rows)
    rank = matrix.rank()
    mask = 0
    for colour in range(3):
        coordinate = [0, 0, 0]
        coordinate[colour] = 1
        if matrix.col_join(sp.Matrix([coordinate])).rank() == rank:
            mask |= 1 << colour
    return mask


def subset_permanent(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    states = {0: Fraction(1)}
    for column in range(6):
        next_states: dict[int, Fraction] = {}
        for mask, value in states.items():
            for row in range(6):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = next_states.get(new_mask, Fraction(0)) + (
                    value * matrix[row][column]
                )
        states = next_states
    return states.get(63, Fraction(0))


def contraction(modes: tuple[tuple[Vector, ...], ...]) -> tuple[Fraction, ...]:
    values = []
    for word in itertools.product(range(3), repeat=6):
        matrix = tuple(
            tuple(modes[mode][row][word[mode]] for mode in range(6)) for row in range(6)
        )
        values.append(subset_permanent(matrix))
    return tuple(values)


def outer(left: Vector, right: Vector) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(a * b for b in right) for a in left)


def add_blocks(
    left: tuple[tuple[Fraction, ...], ...],
    right: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(3))
        for row in range(3)
    )


def evaluate(first: Vector, block: tuple[tuple[Fraction, ...], ...]) -> Vector:
    return tuple(
        sum(first[row] * block[row][column] for row in range(3)) for column in range(3)
    )  # type: ignore[return-value]


def main() -> None:
    roots = root_rows()
    port_b = tuple(
        vector(*row)
        for row in (
            (1, 1, 0),
            (0, 1, 1),
            (1, 0, 1),
            (2, 1, 1),
            (1, 3, 1),
            (1, 1, 4),
        )
    )
    port_a = tuple(
        vector(*row)
        for row in (
            (0, 1, 2),
            (2, 0, 1),
            (1, 2, 0),
            (1, 1, 2),
            (2, 1, 1),
            (1, 2, 1),
        )
    )

    left_profiles = tuple(span_profile(mode[:5]) for mode in roots)
    right_profiles = tuple(span_profile((*mode[:4], mode[5])) for mode in roots)
    assert left_profiles == (6, 5, 3, 7, 7, 7)
    assert right_profiles == (7, 7, 7, 7, 7, 7)

    left_modes = tuple((*mode[:5], port_b[index]) for index, mode in enumerate(roots))
    right_modes = tuple(
        (*mode[:4], mode[5], port_a[index]) for index, mode in enumerate(roots)
    )
    assert all(sp.Matrix(mode).rank() == 3 for mode in (*left_modes, *right_modes))

    unknowns = sp.symbols("s0:36")
    common_map = sp.Matrix(6, 6, unknowns)
    equations = []
    for left, right in zip(left_modes, right_modes):
        equations.extend(common_map * sp.Matrix(left) - sp.Matrix(right))
    system, values = sp.linear_eq_to_matrix(equations, unknowns)
    assert system.rank() == 36
    assert system.row_join(values).rank() == 37

    left_tensor = contraction(left_modes)
    right_tensor = contraction(right_modes)
    assert len(left_tensor) == len(right_tensor) == 729
    assert (left_tensor[1], right_tensor[1]) == (12, 18)
    assert (left_tensor[3], right_tensor[3]) == (12, 14)
    minor = left_tensor[1] * right_tensor[3] - left_tensor[3] * right_tensor[1]
    assert minor == -48
    assert sum(value != 0 for value in left_tensor) == 476
    assert sum(value != 0 for value in right_tensor) == 476

    encoded = ";".join(
        f"{left.numerator}/{left.denominator},{right.numerator}/{right.denominator}"
        for left, right in zip(left_tensor, right_tensor)
    ).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    assert digest == "3c962e1af17fe60424aaa3cb2fbf0608079aa85c6a0d1818b33b43d08afb63c3"

    # Alternate dual sections, differing from the primary verifier by
    # annihilator multiples, independently realize all required evaluations.
    x = vector(1, 1, 1)
    z_a, z_b = vector(1, 2, 3), vector(1, 3, 2)
    h_a, h_b = vector(1, -2, 1), vector(-1, -1, 2)
    alpha_a, zeta_a = vector(3, -3, 1), vector(1, -3, 2)
    alpha_b = vector(Fraction(1, 2), Fraction(-3, 2), 2)
    zeta_b = vector(Fraction(-5, 2), Fraction(-3, 2), 4)
    for port, alpha, zeta in (
        (z_a, alpha_a, zeta_a),
        (z_b, alpha_b, zeta_b),
    ):
        assert dot(alpha, x) == 1
        assert dot(alpha, port) == 0
        assert dot(zeta, x) == 0
        assert dot(zeta, port) == 1
    assert dot(h_a, x) == dot(h_a, z_a) == 0
    assert dot(h_b, x) == dot(h_b, z_b) == 0

    cross = outer(alpha_a, alpha_b)
    assert dot(evaluate(x, cross), x) == 1
    assert dot(evaluate(x, cross), z_b) == 0
    assert dot(evaluate(z_a, cross), x) == 0

    for index, mode in enumerate(roots):
        block_a = add_blocks(outer(alpha_a, mode[4]), outer(zeta_a, port_a[index]))
        block_b = add_blocks(outer(alpha_b, mode[5]), outer(zeta_b, port_b[index]))
        assert evaluate(x, block_a) == mode[4]
        assert evaluate(z_a, block_a) == port_a[index]
        assert evaluate(x, block_b) == mode[5]
        assert evaluate(z_b, block_b) == port_b[index]
        assert any(entry != 0 for row in block_a for entry in row)
        assert any(entry != 0 for row in block_b for entry in row)

    nonblocker_a = sp.Matrix([h_a, alpha_a])
    nonblocker_b = sp.Matrix([h_b, alpha_b])
    assert nonblocker_a.rank() == nonblocker_b.rank() == 2
    assert nonblocker_a * sp.Matrix(z_a) == sp.zeros(2, 1)
    assert nonblocker_b * sp.Matrix(z_b) == sp.zeros(2, 1)
    assert span_profile((h_a, alpha_a)) == span_profile((h_b, alpha_b)) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "no-import alternate sections and subset permanents",
                "field": "characteristic zero",
                "left_profiles": left_profiles,
                "right_profiles": right_profiles,
                "target_words_checked_per_tensor": 729,
                "common_output_map_system_ranks": [36, 37],
                "coefficient_pair_sha256": digest,
                "proportionality_minor": int(minor),
                "alternate_incident_sections_realized": True,
                "global_matching_identity_realized": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
