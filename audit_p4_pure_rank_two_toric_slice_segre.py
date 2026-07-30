#!/usr/bin/env python3
"""Independent finite-field audit of all toric slice-Segre types."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md"
PRIMARY = ROOT / "verify_p4_pure_rank_two_toric_slice_segre.py"
PRIME = 5


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subtract(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> tuple[int, int, int]:
    return tuple(left[index] - right[index] for index in range(3))


def dot(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> int:
    return sum(
        first * second
        for first, second in zip(left, right, strict=True)
    )


def rank_mod(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    work = [[entry % PRIME for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, PRIME)
        work[rank] = [
            entry * inverse % PRIME for entry in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (left - scale * right) % PRIME
                    for left, right in zip(
                        work[row], work[rank], strict=True
                    )
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def permanent(rows: tuple[tuple[int, ...], ...]) -> int:
    return sum(
        math.prod(rows[row][permutation[row]] for row in range(4))
        for permutation in itertools.permutations(range(4))
    ) % PRIME


def plane_from_pluecker(values: dict[str, int]) -> list[list[int]]:
    skew = [[0] * 4 for _ in range(4)]
    for label, value in values.items():
        left, right = map(int, label)
        skew[left][right] = value % PRIME
        skew[right][left] = -value % PRIME
    independent = []
    for column in zip(*skew, strict=True):
        candidate = independent + [list(column)]
        if rank_mod(candidate) > len(independent):
            independent.append(list(column))
        if len(independent) == 2:
            break
    assert len(independent) == 2
    return independent


def slice_columns(
    planes: tuple[list[list[int]], ...],
) -> list[list[int]]:
    matrix = []
    for bits in itertools.product((0, 1), repeat=3):
        row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            row.append(
                permanent((
                    basis,
                    tuple(planes[0][bits[0]]),
                    tuple(planes[1][bits[1]]),
                    tuple(planes[2][bits[2]]),
                ))
            )
        matrix.append(row)
    columns = [list(column) for column in zip(*matrix, strict=True)]
    basis = []
    for column in columns:
        if rank_mod(basis + [column]) > len(basis):
            basis.append(column)
    return basis


def is_pure(tensor: list[int]) -> bool:
    if not any(tensor):
        return False
    for mode in range(3):
        flattening = [[0] * 4 for _ in range(2)]
        for bits in itertools.product((0, 1), repeat=3):
            index = bits[0] * 4 + bits[1] * 2 + bits[2]
            column = 0
            for other in range(3):
                if other != mode:
                    column = 2 * column + bits[other]
            flattening[bits[mode]][column] = tensor[index]
        if rank_mod(flattening) != 1:
            return False
    return True


def projective_vectors(dimension: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        (0,) * first + (1,) + tail
        for first in range(dimension)
        for tail in itertools.product(
            range(PRIME), repeat=dimension - first - 1
        )
    )


def main() -> None:
    configurations = (
        {
            "02": ((1, 0, 0), 1),
            "03": ((1, 1, 0), 1),
            "12": ((0, 0, 0), 1),
            "13": ((0, 1, 0), 1),
        },
        {
            "01": ((0, 0, -1), 1),
            "03": ((1, 1, 0), 1),
            "12": ((0, 0, 0), 1),
            "23": ((1, 1, 1), -1),
        },
        {
            "02": ((0, -1, 0), -1),
            "03": ((0, 0, 0), 1),
            "23": ((0, 0, 1), 1),
        },
    )
    points = tuple(sorted({
        tuple(
            first[0][index] + second[0][index] + third[0][index]
            for index in range(3)
        )
        for first in configurations[0].values()
        for second in configurations[1].values()
        for third in configurations[2].values()
    }))
    facets = {}
    for first, second, third in itertools.combinations(points, 3):
        u = subtract(second, first)
        v = subtract(third, first)
        normal = (
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
        )
        if normal == (0, 0, 0):
            continue
        relative = [
            dot(normal, subtract(point, first))
            for point in points
        ]
        if not (
            all(value >= 0 for value in relative)
            or all(value <= 0 for value in relative)
        ):
            continue
        if all(value >= 0 for value in relative):
            normal = tuple(-entry for entry in normal)
        divisor = math.gcd(*(abs(entry) for entry in normal if entry))
        normal = tuple(entry // divisor for entry in normal)
        maximum = max(dot(normal, point) for point in points)
        facets[normal] = frozenset(
            point for point in points if dot(normal, point) == maximum
        )

    edges = set()
    for first, second in itertools.combinations(facets.values(), 2):
        intersection = first & second
        if len(intersection) < 2:
            continue
        values = tuple(intersection)
        if rank_mod([
            list(subtract(point, values[0]))
            for point in values[1:]
        ]) == 1:
            edges.add(frozenset(intersection))
    vertices = {
        frozenset((point,))
        for point in points
        if rank_mod([
            list(normal)
            for normal, face in facets.items()
            if point in face
        ]) == 3
    }
    faces = {2: set(facets.values()), 1: edges, 0: vertices}
    assert {key: len(value) for key, value in faces.items()} == {
        2: 12, 1: 26, 0: 16
    }

    type_counts = {}
    pure_direction_counts = {}
    for dimension, dimension_faces in faces.items():
        for face in dimension_faces:
            incident = [
                normal for normal, facet in facets.items()
                if face <= facet
            ]
            weight = tuple(
                sum(normal[index] for normal in incident)
                for index in range(3)
            )
            planes = []
            for configuration in configurations:
                maximum = max(
                    dot(weight, exponent)
                    for exponent, _coefficient in configuration.values()
                )
                values = {
                    label: coefficient
                    for label, (exponent, coefficient)
                    in configuration.items()
                    if dot(weight, exponent) == maximum
                }
                planes.append(plane_from_pluecker(values))
            basis = slice_columns(tuple(planes))
            projective = projective_vectors(len(basis)) if basis else ()
            pure_count = 0
            for coefficients in projective:
                tensor = [
                    sum(
                        coefficients[index] * basis[index][coordinate]
                        for index in range(len(basis))
                    ) % PRIME
                    for coordinate in range(8)
                ]
                if is_pure(tensor):
                    pure_count += 1
            key = (dimension, len(basis), pure_count)
            type_counts[key] = type_counts.get(key, 0) + 1
            pure_direction_counts[pure_count] = (
                pure_direction_counts.get(pure_count, 0) + 1
            )

    assert type_counts == {
        (2, 1, 0): 6,
        (2, 2, 1): 1,
        (2, 2, 2): 5,
        (1, 1, 0): 22,
        (1, 2, 2): 4,
        (0, 1, 0): 15,
        (0, 0, 0): 1,
    }

    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "finite_field": "F_5",
        "method": "projective pure-direction count",
        "toric_orbits": {
            "divisors": len(faces[2]),
            "edges": len(faces[1]),
            "vertices": len(faces[0]),
        },
        "type_counts": {
            str(key): value for key, value in sorted(type_counts.items())
        },
        "pure_direction_histogram": {
            str(key): value
            for key, value in sorted(pure_direction_counts.items())
        },
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_pure_rank_two_toric_slice_segre_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
