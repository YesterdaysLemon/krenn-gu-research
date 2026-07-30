#!/usr/bin/env python3
"""Independent finite-field audit of the a=0 Grassmannian obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_a0_adjacent_grassmann.py"
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inv_mod(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def rref_mod(
    rows: list[list[int]] | tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[tuple[tuple[int, ...], ...], int]:
    matrix = [[entry % prime for entry in row] for row in rows]
    if not matrix:
        return tuple(), 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = inv_mod(matrix[pivot_row][column], prime)
        matrix[pivot_row] = [
            entry * inverse % prime for entry in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            multiplier = matrix[row][column] % prime
            if multiplier:
                matrix[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(
                        matrix[row],
                        matrix[pivot_row],
                        strict=True,
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    nonzero_rows = [
        tuple(row) for row in matrix if any(entry % prime for entry in row)
    ]
    return tuple(nonzero_rows), len(nonzero_rows)


def rank_mod(rows: list[list[int]], prime: int) -> int:
    return rref_mod(rows, prime)[1]


def canonical_plane(
    first: tuple[int, ...],
    second: tuple[int, ...],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    canonical, rank = rref_mod([list(first), list(second)], prime)
    if rank != 2:
        raise AssertionError("candidate rows do not span a plane")
    return canonical


def all_planes(prime: int) -> list[tuple[tuple[int, ...], ...]]:
    planes = []
    for pivots in itertools.combinations(range(4), 2):
        nonpivots = [index for index in range(4) if index not in pivots]
        variable_positions = [
            (row, column)
            for row in range(2)
            for column in nonpivots
            if column > pivots[row]
        ]
        for values in itertools.product(range(prime), repeat=len(variable_positions)):
            rows = [[0] * 4 for _ in range(2)]
            rows[0][pivots[0]] = 1
            rows[1][pivots[1]] = 1
            for (row, column), value in zip(
                variable_positions,
                values,
                strict=True,
            ):
                rows[row][column] = value
            planes.append(tuple(tuple(row) for row in rows))
    expected = (prime**2 + 1) * (prime**2 + prime + 1)
    if len(planes) != expected or len(set(planes)) != expected:
        raise AssertionError("RREF Grassmannian enumeration changed")
    return planes


def contains(
    plane: tuple[tuple[int, ...], ...],
    vector: tuple[int, ...],
    prime: int,
) -> bool:
    return rank_mod(
        [list(plane[0]), list(plane[1]), list(vector)],
        prime,
    ) == 2


def pair_contraction(
    left: tuple[int, ...],
    right: tuple[int, ...],
    prime: int,
) -> tuple[int, ...]:
    coordinates = []
    for first, second in PAIRS:
        complement = [
            index
            for index in range(4)
            if index not in (first, second)
        ]
        coordinates.append(
            (
                left[complement[0]] * right[complement[1]]
                + left[complement[1]] * right[complement[0]]
            )
            % prime
        )
    return tuple(coordinates)


def pair_image_rank(
    first: tuple[tuple[int, ...], ...],
    second: tuple[tuple[int, ...], ...],
    prime: int,
) -> int:
    return rank_mod(
        [
            list(pair_contraction(left, right, prime))
            for left in first
            for right in second
        ],
        prime,
    )


def permanent4(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    return (
        sum(
            1
            if not rows
            else _permutation_product(rows, permutation, prime)
            for permutation in itertools.permutations(range(4))
        )
        % prime
    )


def _permutation_product(
    rows: tuple[tuple[int, ...], ...],
    permutation: tuple[int, ...],
    prime: int,
) -> int:
    value = 1
    for index in range(4):
        value = value * rows[index][permutation[index]] % prime
    return value


def flattening_rank(
    rows_a: tuple[tuple[int, ...], ...],
    rows_y: tuple[tuple[int, ...], ...],
    plane_c: tuple[tuple[int, ...], ...],
    plane_d: tuple[tuple[int, ...], ...],
    prime: int,
) -> int:
    matrix = [
        [
            permanent4((row_a, row_y, row_c, row_d), prime)
            for row_c in plane_c
            for row_d in plane_d
        ]
        for row_a in rows_a
        for row_y in rows_y
    ]
    return rank_mod(matrix, prime)


def audit_prime(prime: int) -> dict[str, object]:
    h = (1, 0, 0, -1 % prime)
    u = (1, 0, 1, 0)
    n = (0, 0, 1, 1)
    m = (0, 0, 1, -1 % prime)
    u_plus = (1, 0, 0, 1)
    h_one = (1, 0, -1 % prime, 0)

    named_planes = {
        "Ph": canonical_plane(h, m, prime),
        "P": canonical_plane(h, u, prime),
        "Pu": canonical_plane(u, m, prime),
        "P0": canonical_plane(n, u_plus, prime),
    }
    if named_planes["P"] != canonical_plane(u, n, prime):
        raise AssertionError("P incidence identity failed")
    if named_planes["Pu"] != canonical_plane(u_plus, m, prime):
        raise AssertionError("Pu incidence identity failed")
    if named_planes["Ph"] != canonical_plane(h_one, m, prime):
        raise AssertionError("Ph incidence identity failed")
    if named_planes["P0"] != canonical_plane(h_one, n, prime):
        raise AssertionError("P0 incidence identity failed")

    planes = all_planes(prime)
    h_planes = [plane for plane in planes if contains(plane, h, prime)]
    u_planes = [plane for plane in planes if contains(plane, u, prime)]
    expected_line_schubert_size = prime**2 + prime + 1
    if (
        len(h_planes) != expected_line_schubert_size
        or len(u_planes) != expected_line_schubert_size
    ):
        raise AssertionError("line Schubert variety size changed")

    moving_survivors = {
        (first, second)
        for first in h_planes
        for second in u_planes
        if pair_image_rank(first, second, prime) <= 2
    }
    expected_moving = {
        (named_planes["Ph"], named_planes["P"]),
        (named_planes["Ph"], named_planes["Pu"]),
        (named_planes["P"], named_planes["Pu"]),
    }
    if moving_survivors != expected_moving:
        raise AssertionError("moving Schubert classification changed")

    fixed_survivors = {
        plane
        for plane in planes
        if pair_image_rank(named_planes["P"], plane, prime) <= 2
    }
    expected_fixed = {
        named_planes["Ph"],
        named_planes["Pu"],
        named_planes["P0"],
    }
    if fixed_survivors != expected_fixed:
        raise AssertionError("fixed-P Grassmannian classification changed")

    five_pairs = (
        ("Ph", "P"),
        ("Ph", "Pu"),
        ("P", "Ph"),
        ("P", "Pu"),
        ("P", "P0"),
    )
    kernel_checks = 0
    minimum_ay_rank = 6
    minimum_flattening_rank = 9
    for rho in range(prime):
        for sigma in range(prime):
            rows_a = (
                (-rho % prime, 1, 0, 0),
                (-1 % prime, 0, 1, 0),
                (-1 % prime, 0, 0, 1),
            )
            rows_y = (
                (-sigma % prime, 1, 0, 0),
                (-1 % prime, 0, 1, 0),
                (1, 0, 0, 1),
            )
            ay_rank = pair_image_rank(rows_a, rows_y, prime)
            minimum_ay_rank = min(minimum_ay_rank, ay_rank)
            if ay_rank < 5:
                raise AssertionError("AY pair image dropped below five")
            for first, second in five_pairs:
                flattening = flattening_rank(
                    rows_a,
                    rows_y,
                    named_planes[first],
                    named_planes[second],
                    prime,
                )
                minimum_flattening_rank = min(
                    minimum_flattening_rank,
                    flattening,
                )
                if flattening < 2:
                    raise AssertionError("candidate flattening became rank one")
                kernel_checks += 1

    # Audit the complement-pair identity on all coordinate basis rows.
    coordinate_rows = tuple(
        tuple(1 if column == row else 0 for column in range(4))
        for row in range(4)
    )
    pairing_checks = 0
    for indices in itertools.product(range(4), repeat=4):
        rows = tuple(coordinate_rows[index] for index in indices)
        left = pair_contraction(rows[0], rows[1], prime)
        right = pair_contraction(rows[2], rows[3], prime)
        paired = 0
        for index, pair in enumerate(PAIRS):
            complement = tuple(
                entry for entry in range(4) if entry not in pair
            )
            paired += left[index] * right[PAIRS.index(complement)]
        if paired % prime != permanent4(rows, prime):
            raise AssertionError("complement-pair identity changed")
        pairing_checks += 1

    return {
        "prime": prime,
        "grassmannian_planes": len(planes),
        "line_schubert_planes": expected_line_schubert_size,
        "moving_pairs_checked": len(h_planes) * len(u_planes),
        "moving_survivors": len(moving_survivors),
        "fixed_P_planes_checked": len(planes),
        "fixed_P_survivors": len(fixed_survivors),
        "kernel_parameter_flattenings_checked": kernel_checks,
        "minimum_AY_pair_image_rank": minimum_ay_rank,
        "minimum_candidate_flattening_rank": minimum_flattening_rank,
        "coordinate_pairing_checks": pairing_checks,
    }


def main() -> None:
    audits = [audit_prime(prime) for prime in (5, 7)]
    output = {
        "audited": True,
        "fields": ["F_5", "F_7"],
        "audits": audits,
        "enumerated_ambient_maps": 0,
        "adjacent_a0_excluded_over_C": True,
        "disjoint_a0_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_a0_adjacent_grassmann_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
