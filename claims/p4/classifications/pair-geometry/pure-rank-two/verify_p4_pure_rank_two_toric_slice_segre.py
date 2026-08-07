#!/usr/bin/env python3
"""Verify Segre intersections on every toric base orbit."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md"
TORIC = ROOT / "P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md"
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(*vectors: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(sum(vector[index] for vector in vectors) for index in range(3))


def subtract(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> tuple[int, int, int]:
    return tuple(left[index] - right[index] for index in range(3))


def cross(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> tuple[int, int, int]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def dot(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> int:
    return sum(
        first * second
        for first, second in zip(left, right, strict=True)
    )


def affine_rank(points: frozenset[tuple[int, int, int]]) -> int:
    values = tuple(points)
    if len(values) <= 1:
        return 0
    return sp.Matrix([
        subtract(point, values[0]) for point in values[1:]
    ]).rank()


def plane_from_pluecker(
    values: dict[str, int],
) -> sp.Matrix:
    skew = sp.zeros(4)
    for label, value in values.items():
        left, right = map(int, label)
        skew[left, right] = value
        skew[right, left] = -value
    columns = skew.columnspace()
    assert len(columns) == 2
    return sp.Matrix.hstack(*columns).T


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def slice_map(planes: tuple[sp.Matrix, sp.Matrix, sp.Matrix]) -> sp.Matrix:
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(
                permanent((
                    basis,
                    tuple(planes[0][bits[0], :]),
                    tuple(planes[1][bits[1], :]),
                    tuple(planes[2][bits[2], :]),
                ))
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def segre_equations(
    basis: sp.Matrix,
) -> tuple[tuple[sp.Symbol, ...], tuple[sp.Expr, ...]]:
    variables = sp.symbols(f"z0:{basis.cols}")
    tensor = basis * sp.Matrix(variables)
    equations = []
    for mode in range(3):
        flattening = sp.zeros(2, 4)
        for bits in itertools.product((0, 1), repeat=3):
            index = bits[0] * 4 + bits[1] * 2 + bits[2]
            column = 0
            for other in range(3):
                if other != mode:
                    column = 2 * column + bits[other]
            flattening[bits[mode], column] = tensor[index]
        for left, right in itertools.combinations(range(4), 2):
            equation = sp.factor(
                flattening[0, left] * flattening[1, right]
                - flattening[0, right] * flattening[1, left]
            )
            if equation != 0 and equation not in equations:
                equations.append(equation)
    return variables, tuple(equations)


def classify_slice(matrix: sp.Matrix) -> tuple[str, int, str]:
    columns = matrix.columnspace()
    rank = len(columns)
    if rank == 0:
        return "zero", 0, "0"
    basis = sp.Matrix.hstack(*columns)
    variables, equations = segre_equations(basis)
    if rank == 1:
        if not equations:
            return "pure-line", rank, "0"
        return "disjoint", rank, str(sp.factor(equations[0]))
    assert rank == 2
    if not equations:
        return "contained", rank, "0"
    common = equations[0]
    for equation in equations[1:]:
        common = sp.gcd(common, equation)
    common = sp.factor(common)
    factors = sp.factor_list(common)[1]
    if len(factors) == 1 and factors[0][1] == 2:
        return "tangent", rank, str(common)
    degree = sum(
        sp.Poly(factor, variables).total_degree() * multiplicity
        for factor, multiplicity in factors
    )
    assert degree == 2
    return "secant", rank, str(common)


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
        add(first[0], second[0], third[0])
        for first in configurations[0].values()
        for second in configurations[1].values()
        for third in configurations[2].values()
    }))
    facets: dict[
        tuple[int, int, int],
        frozenset[tuple[int, int, int]],
    ] = {}
    for first, second, third in itertools.combinations(points, 3):
        normal = cross(
            subtract(second, first),
            subtract(third, first),
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
        offset = dot(normal, first)
        facets[normal] = frozenset(
            point for point in points if dot(normal, point) == offset
        )

    faces: dict[
        int,
        set[frozenset[tuple[int, int, int]]],
    ] = {
        2: set(facets.values()),
        1: set(),
        0: set(),
    }
    for first, second in itertools.combinations(facets.values(), 2):
        intersection = first & second
        if intersection and affine_rank(intersection) == 1:
            faces[1].add(frozenset(intersection))
    for point in points:
        incident = [
            normal for normal, face in facets.items() if point in face
        ]
        if sp.Matrix(incident).rank() == 3:
            faces[0].add(frozenset((point,)))
    assert {dimension: len(values) for dimension, values in faces.items()} == {
        2: 12,
        1: 26,
        0: 16,
    }

    deletion_coordinates = (
        {"12", "13", "23"},
        {"02", "03", "23"},
        {"01", "03", "13"},
        {"01", "02", "12"},
    )
    records = []
    for dimension in (2, 1, 0):
        for face in faces[dimension]:
            incident = tuple(sorted(
                normal
                for normal, facet in facets.items()
                if face <= facet
            ))
            weight = tuple(
                sum(normal[index] for normal in incident)
                for index in range(3)
            )
            supports = []
            planes = []
            for configuration in configurations:
                pairings = {
                    label: dot(weight, exponent)
                    for label, (exponent, _coefficient)
                    in configuration.items()
                }
                maximum = max(pairings.values())
                values = {
                    label: configuration[label][1]
                    for label, pairing in pairings.items()
                    if pairing == maximum
                }
                supports.append(tuple(values))
                planes.append(plane_from_pluecker(values))
            slice_type, rank, equation = classify_slice(
                slice_map(tuple(planes))
            )
            all_rank = tuple(
                distinguished
                for distinguished in range(4)
                if all(
                    set(support) & deletion_coordinates[distinguished]
                    for support in supports
                )
            )
            records.append({
                "dimension": dimension,
                "incident_normals": incident,
                "supports": tuple(supports),
                "slice_rank": rank,
                "slice_type": slice_type,
                "equation": equation,
                "all_rank": all_rank,
            })

    counts = {}
    for record in records:
        key = (
            record["dimension"],
            record["slice_type"],
            record["slice_rank"],
        )
        counts[key] = counts.get(key, 0) + 1
    assert counts == {
        (2, "disjoint", 1): 6,
        (2, "secant", 2): 5,
        (2, "tangent", 2): 1,
        (1, "disjoint", 1): 22,
        (1, "secant", 2): 4,
        (0, "disjoint", 1): 15,
        (0, "zero", 0): 1,
    }

    capable_edges = tuple(sorted(
        (
            record["incident_normals"],
            record["all_rank"],
        )
        for record in records
        if record["dimension"] == 1
        and record["slice_type"] == "secant"
    ))
    expected_edges = tuple(sorted((
        (((-1, 0, 0), (-1, 1, 0)), (0, 2)),
        (((-1, 0, 0), (0, 0, -1)), (2, 3)),
        (((-1, 1, 0), (0, 1, 0)), (0, 2)),
        (((0, 0, -1), (1, 0, -1)), (2, 3)),
    )))
    assert capable_edges == expected_edges

    genuine_capable_divisors = [
        record
        for record in records
        if record["dimension"] == 2
        and record["slice_type"] in ("secant", "tangent")
        and record["incident_normals"] != ((-1, 0, 0),)
    ]
    assert len(genuine_capable_divisors) == 5
    divisor_pairs = sum(
        len(record["all_rank"]) for record in genuine_capable_divisors
    )
    edge_pairs = sum(
        len(all_rank) for _normals, all_rank in capable_edges
    )
    assert (divisor_pairs, edge_pairs, divisor_pairs + edge_pairs) == (
        13, 8, 21
    )

    output = {
        "verified": True,
        "field": "C",
        "method": "toric face lattice and exact Segre minors",
        "toric_orbits": {
            "divisors": len(faces[2]),
            "edges": len(faces[1]),
            "vertices": len(faces[0]),
        },
        "slice_types": {
            f"dimension_{dimension}_{kind}_rank_{rank}": count
            for (dimension, kind, rank), count in sorted(counts.items())
        },
        "genuine_segre_capable_divisors": 5,
        "segre_capable_edges": 4,
        "segre_capable_vertices": 0,
        "remaining_divisor_orientation_pairs": divisor_pairs,
        "remaining_edge_orientation_pairs": edge_pairs,
        "remaining_toric_orbit_orientation_pairs": (
            divisor_pairs + edge_pairs
        ),
        "capable_edges": [
            {
                "normals": [list(normal) for normal in normals],
                "all_rank": list(all_rank),
            }
            for normals, all_rank in capable_edges
        ],
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "dependency": {
            TORIC.name: sha256(TORIC),
        },
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_pure_rank_two_toric_slice_segre_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
