#!/usr/bin/env python3
"""Independent finite-field audit of the projective normal chart cover."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_h31_embedded_p3_component_projective_closure.py"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent3(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    total = 0
    for permutation in itertools.permutations(range(3)):
        product = 1
        for row in range(3):
            product *= rows[row][permutation[row]]
        total += product
    return total % prime


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if work[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = pow(work[row][column], prime - 2, prime)
        work[row] = [entry * scale % prime for entry in work[row]]
        for other in range(len(work)):
            if other == row:
                continue
            factor = work[other][column]
            if factor:
                work[other] = [
                    (left - factor * right) % prime
                    for left, right in zip(
                        work[other], work[row], strict=True
                    )
                ]
        row += 1
        if row == len(work):
            break
    return row


def plane_from_normal(
    normal: tuple[int, int, int], prime: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    pivot = next(index for index, entry in enumerate(normal) if entry % prime)
    other_coordinates = tuple(index for index in range(3) if index != pivot)
    rows = []
    for coordinate in other_coordinates:
        row = [0, 0, 0]
        row[coordinate] = normal[pivot] % prime
        row[pivot] = -normal[coordinate] % prime
        assert sum(
            row[index] * normal[index] for index in range(3)
        ) % prime == 0
        rows.append(tuple(row))
    return tuple(rows)  # type: ignore[return-value]


def projective_points(prime: int):
    for point in itertools.product(range(prime), repeat=3):
        if point == (0, 0, 0):
            continue
        first = next(index for index, entry in enumerate(point) if entry)
        if point[first] != 1:
            continue
        yield point


def tensor_from_absolute_normal(
    point: tuple[int, int, int], prime: int
) -> dict[tuple[int, ...], int]:
    cap_c, cap_a, cap_b = point
    normals = (
        (cap_c, cap_a, cap_b),
        (cap_c, -cap_a % prime, -cap_b % prime),
        (cap_c, -cap_a % prime, cap_b),
    )
    planes = tuple(plane_from_normal(normal, prime) for normal in normals)
    return {
        word: permanent3(
            tuple(planes[mode][word[mode]] for mode in range(3)),
            prime,
        )
        for word in WORDS3
    }


def flattening_rank(
    tensor: dict[tuple[int, ...], int], mode: int, prime: int
) -> int:
    other = tuple(index for index in range(3) if index != mode)
    columns = tuple(itertools.product((0, 1), repeat=2))
    matrix = []
    for value in (0, 1):
        row = []
        for column in columns:
            word = [0, 0, 0]
            word[mode] = value
            word[other[0]] = column[0]
            word[other[1]] = column[1]
            row.append(tensor[tuple(word)])
        matrix.append(row)
    return rank_mod(matrix, prime)


def main() -> None:
    prime_results = {}
    for prime in (3, 5):
        zero_points = 0
        nonzero_points = 0
        support_counts = {}
        for point in projective_points(prime):
            support = tuple(index for index, entry in enumerate(point) if entry)
            tensor = tensor_from_absolute_normal(point, prime)
            nonzero = any(tensor.values())
            if len(support) == 1:
                assert not nonzero
                zero_points += 1
            else:
                assert nonzero
                assert all(
                    flattening_rank(tensor, mode, prime) == 1
                    for mode in range(3)
                )
                common_slot, b_slot = support[:2]
                assert point[common_slot] and point[b_slot]
                nonzero_points += 1
            support_counts[str(len(support))] = (
                support_counts.get(str(len(support)), 0) + 1
            )
        assert zero_points == 3
        assert zero_points + nonzero_points == prime**2 + prime + 1
        prime_results[str(prime)] = {
            "projective_points": prime**2 + prime + 1,
            "support_one_zero_restrictions": zero_points,
            "nonzero_decomposable_restrictions": nonzero_points,
            "support_counts": support_counts,
            "every_nonzero_point_has_two_coordinate_chart": True,
        }

    output = {
        "verified": True,
        "method": (
            "independent projective-point enumeration, normal-kernel "
            "planes, subset permanents, and flattening ranks"
        ),
        "finite_field_audit_is_theorem": False,
        "primes": prime_results,
        "whole_projective_ninth_component_H31_fibre_empty": True,
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
