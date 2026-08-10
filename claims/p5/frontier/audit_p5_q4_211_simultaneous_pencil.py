#!/usr/bin/env python3
"""Independent audit of the q4_211 simultaneous-pencil reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION.md"
PRIMARY = ROOT / "tmp" / "p5_q4_211_simultaneous_pencil_verified.json"
TARGET_WORDS = tuple(itertools.product(range(3), repeat=4))
MAPS = (
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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    rows = [[entry % prime for entry in row] for row in matrix]
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
            entry * inverse % prime for entry in rows[pivot_row]
        ]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
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


def coefficient_vector(
    colours: tuple[int, ...],
    prime: int,
    maps: tuple[tuple[tuple[int, ...], ...], ...] = MAPS,
) -> list[int]:
    values = []
    for missing in range(5):
        coordinates = tuple(
            index for index in range(5) if index != missing
        )
        total = 0
        for injection in itertools.permutations(coordinates):
            term = 1
            for mode in range(4):
                term *= maps[mode][injection[mode]][colours[mode]]
            total += term
        values.append(total % prime)
    return values


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
            columns.append(source + [alpha])
        maps.append(
            tuple(
                tuple(
                    columns[column][row] % prime
                    for column in range(3)
                )
                for row in range(5)
            )
        )
    return tuple(maps)


def matrix_vector(
    matrix: list[list[int]], vector: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    return tuple(
        sum(left * right for left, right in zip(row, vector)) % prime
        for row in matrix
    )


def main() -> None:
    field_results = {}
    generator = (1, 1, 1, 1, 0)
    for prime in (5, 7):
        off_diagonal = [
            coefficient_vector(word, prime)
            for word in TARGET_WORDS
            if len(set(word)) != 1
        ]
        diagonal = [
            coefficient_vector((colour,) * 4, prime)
            for colour in range(3)
        ]
        rank = rank_mod(off_diagonal, prime)
        assert rank == 4
        assert matrix_vector(off_diagonal, generator, prime) == (0,) * 78
        diagonal_image = matrix_vector(diagonal, generator, prime)
        assert diagonal_image == (12 % prime,) * 3

        selected_words = (
            (0, 0, 0, 1),
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (1, 0, 0, 0),
        )
        selected_columns = (0, 1, 2, 4)
        minor_matrix = [
            [
                coefficient_vector(word, prime)[column]
                for column in selected_columns
            ]
            for word in selected_words
        ]
        assert rank_mod(minor_matrix, prime) == 4

        projective_kernel = []
        for vector in itertools.product(range(prime), repeat=5):
            if not any(vector):
                continue
            if matrix_vector(off_diagonal, vector, prime) != (0,) * 78:
                continue
            first = next(entry for entry in vector if entry)
            inverse = pow(first, -1, prime)
            canonical = tuple(entry * inverse % prime for entry in vector)
            if canonical not in projective_kernel:
                projective_kernel.append(canonical)
        assert projective_kernel == [generator]

        support_profiles = set()
        pencil_torus_points = 0
        for a, b, c in itertools.product(range(prime), repeat=3):
            if sum(entry != 0 for entry in (a, b, c)) < 2:
                continue
            for t0, t1, t2 in itertools.product(
                range(1, prime), repeat=3
            ):
                if (a * t0 + b * t1 + c * t2) % prime:
                    continue
                z = (0, t0, t0, t1, t2)
                assert sum(entry != 0 for entry in z) == 4
                pencil_torus_points += 1
            if a and b and c:
                boundaries = (
                    (0, 0, 0, c, -b),
                    (0, c, c, 0, -a),
                    (0, b, b, -a, 0),
                )
                support_profiles.add(
                    tuple(
                        sum(entry % prime != 0 for entry in vector)
                        for vector in boundaries
                    )
                )
        assert support_profiles == {(2, 3, 3)}
        assert pencil_torus_points > 0

        family_points = 0
        family_rank_counts = {}
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
            family_off_diagonal = [
                coefficient_vector(word, prime, maps)
                for word in TARGET_WORDS
                if len(set(word)) != 1
            ]
            family_rank = rank_mod(family_off_diagonal, prime)
            family_rank_counts[family_rank] = (
                family_rank_counts.get(family_rank, 0) + 1
            )
        assert family_rank_counts == {4: family_points}

        edge_pairs = {
            len(set(first) & set(second))
            for first in itertools.combinations(range(4), 2)
            for second in itertools.combinations(range(4), 2)
        }
        assert edge_pairs == {0, 1, 2}

        field_results[f"F_{prime}"] = {
            "off_diagonal_matrix_shape": [78, 5],
            "off_diagonal_rank": rank,
            "projective_kernel": [list(item) for item in projective_kernel],
            "diagonal_image": list(diagonal_image),
            "full_parameter_boundary_support_profile": [2, 3, 3],
            "pencil_torus_points_checked": pencil_torus_points,
            "support_four_family_points_checked": family_points,
            "support_four_family_off_diagonal_rank_counts": (
                family_rank_counts
            ),
            "minimal_two_edge_intersection_types": sorted(edge_pairs),
        }

    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    assert primary["verified"] is True
    assert primary["theorem_sha256"] == sha256(THEOREM)
    assert primary["known_support_four_off_diagonal_rank"] == 4
    assert primary["q4_required_off_diagonal_rank_upper_bound"] == 2
    assert primary["q4_211_excluded"] is False

    output = {
        "verified": True,
        "scope": "normalized q4_211 simultaneous-pencil reduction",
        "finite_fields": field_results,
        "known_support_four_family_q4_lift": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary_artifact": PRIMARY.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_simultaneous_pencil_audited.json"
    )
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
