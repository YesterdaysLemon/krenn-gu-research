#!/usr/bin/env python3
"""Independent finite-field audit of the support-four restriction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PERMUTATIONS = tuple(itertools.permutations(range(5), 4))
TARGET_TUPLES = tuple(itertools.product(range(3), repeat=4))
INTEGER_MAPS = (
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 0),
        (-1, -1, 0),
        (0, 0, -1),
    ),
    (
        (1, 1, -2),
        (-2, 1, 1),
        (1, -2, 1),
        (1, 1, 1),
        (1, 1, 1),
    ),
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 0),
        (0, -1, -1),
        (-1, 0, 0),
    ),
    (
        (-1, -1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, 1, -1),
        (0, -2, 0),
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rank_mod(matrix: object, prime: int) -> int:
    rows = [
        [int(value) % prime for value in row]
        for row in matrix
    ]
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
            if row == pivot_row or rows[row][column] == 0:
                continue
            factor = rows[row][column]
            rows[row] = [
                (left - factor * right) % prime
                for left, right in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def coefficient(
    maps: tuple[tuple[tuple[int, ...], ...], ...],
    colours: tuple[int, ...],
    prime: int,
) -> int:
    result = 0
    for injection in PERMUTATIONS:
        missing = next(
            coordinate
            for coordinate in range(5)
            if coordinate not in injection
        )
        if missing == 4:
            continue
        term = 1
        for mode in range(4):
            term *= maps[mode][injection[mode]][colours[mode]]
        result += term
    return result % prime


def family_maps(
    u: int, v: int, w: int, prime: int
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    parameters = {0: u, 2: v, 3: w}
    special_colours = {0: 2, 2: 0, 3: 1}
    distinguished_coordinate = {0: 1, 1: 2, 2: 0}
    maps = []
    for mode in range(4):
        columns = []
        for colour in range(3):
            if mode == 1:
                source = [1, 1, 1]
                source[distinguished_coordinate[colour]] = -2
                source.append(1)
                alpha = 1
            else:
                parameter = parameters[mode]
                source = [parameter] * 3
                source[distinguished_coordinate[colour]] = 1
                source.append(
                    -parameter
                    if colour == special_colours[mode]
                    else -1
                )
                alpha = (
                    parameter - 1
                    if colour == special_colours[mode]
                    else 0
                )
            columns.append(tuple((source + [alpha])))
        maps.append(
            tuple(
                tuple(columns[column][row] % prime for column in range(3))
                for row in range(5)
            )
        )
    return tuple(maps)


def main() -> None:
    field_results = {}
    for prime in (5, 7):
        integer_ranks = [
            rank_mod(matrix, prime) for matrix in INTEGER_MAPS
        ]
        assert integer_ranks == [3, 3, 3, 3]
        integer_nonzero = {
            colours: coefficient(INTEGER_MAPS, colours, prime)
            for colours in TARGET_TUPLES
            if coefficient(INTEGER_MAPS, colours, prime)
        }
        expected_value = 12 % prime
        assert integer_nonzero == {
            (0, 0, 0, 0): expected_value,
            (1, 1, 1, 1): expected_value,
            (2, 2, 2, 2): expected_value,
        }

        family_points = 0
        nonsingular_family_points = 0
        family_coefficients_checked = 0
        for u, v, w in itertools.product(range(prime), repeat=3):
            relation = (
                u * v * w
                - u * v
                - u * w
                - u
                - v * w
                - v
                - w
                - 1
            ) % prime
            if relation:
                continue
            family_points += 1
            maps = family_maps(u, v, w, prime)
            if any(rank_mod(matrix, prime) < 3 for matrix in maps):
                continue
            diagonal_value = (-12 * (u + v + w)) % prime
            if diagonal_value == 0:
                continue
            nonsingular_family_points += 1
            for colours in TARGET_TUPLES:
                actual = coefficient(maps, colours, prime)
                expected = (
                    diagonal_value if len(set(colours)) == 1 else 0
                )
                assert actual == expected
                family_coefficients_checked += 1

        field_results[f"F_{prime}"] = {
            "integer_map_ranks": integer_ranks,
            "integer_nonzero_coefficients": {
                ",".join(map(str, colours)): value
                for colours, value in integer_nonzero.items()
            },
            "family_points": family_points,
            "nonsingular_family_points": nonsingular_family_points,
            "family_coefficients_checked": family_coefficients_checked,
        }

    primary = (
        ROOT / "tmp" / "support_four_p5_contraction_restriction_verified.json"
    )
    output = {
        "verified": True,
        "finite_fields": field_results,
        "primary_artifact": primary.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(primary),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "support_four_p5_contraction_restriction_audited.json"
    )
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
