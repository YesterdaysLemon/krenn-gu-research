#!/usr/bin/env python3
"""Verify the toric boundary fan and H31 gate reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md"
CHART_BOUNDARY = (
    REPO_ROOT
    / "claims/p5/h31/component-chart-boundary/P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md"
)
FIBER_BOUNDARY = REPO_ROOT / "P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md"
GATE = (
    REPO_ROOT / "claims" / "p5" / "h31" / "secondary-gate-exclusion"
    / "P5_H31_SECONDARY_GATE_EXCLUSION.md"
)


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


def primitive(
    vector: tuple[int, int, int],
) -> tuple[int, int, int]:
    divisor = math.gcd(*(abs(entry) for entry in vector if entry))
    return tuple(entry // divisor for entry in vector)


def main() -> None:
    configurations = {
        1: {
            "02": (1, 0, 0),
            "03": (1, 1, 0),
            "12": (0, 0, 0),
            "13": (0, 1, 0),
        },
        2: {
            "01": (0, 0, -1),
            "03": (1, 1, 0),
            "12": (0, 0, 0),
            "23": (1, 1, 1),
        },
        3: {
            "02": (0, -1, 0),
            "03": (0, 0, 0),
            "23": (0, 0, 1),
        },
    }
    points = tuple(sorted({
        add(first, second, third)
        for first in configurations[1].values()
        for second in configurations[2].values()
        for third in configurations[3].values()
    }))
    assert len(points) == 28

    facets: dict[
        tuple[tuple[int, int, int], int],
        tuple[tuple[int, int, int], ...],
    ] = {}
    for first, second, third in itertools.combinations(points, 3):
        normal = cross(
            subtract(second, first),
            subtract(third, first),
        )
        if normal == (0, 0, 0):
            continue
        values = [
            dot(normal, subtract(point, first))
            for point in points
        ]
        if not (
            all(value >= 0 for value in values)
            or all(value <= 0 for value in values)
        ):
            continue
        if all(value >= 0 for value in values):
            normal = tuple(-entry for entry in normal)
        normal = primitive(normal)
        offset = dot(normal, first)
        face = tuple(
            point for point in points if dot(normal, point) == offset
        )
        facets[(normal, offset)] = face

    expected_normals = (
        (-1, 0, 0),
        (-1, 0, 1),
        (-1, 1, 0),
        (0, -1, 0),
        (0, -1, 1),
        (0, 0, -1),
        (0, 0, 1),
        (0, 1, -1),
        (0, 1, 0),
        (1, -1, 0),
        (1, 0, -1),
        (1, 0, 0),
    )
    assert tuple(sorted(normal for normal, _offset in facets)) == (
        expected_normals
    )
    assert len(facets) == 12

    expected_supports = {
        (-1, 0, 0): (("12", "13"), ("01", "12"), ("02", "03", "23")),
        (-1, 0, 1): (("12", "13"), ("12", "23"), ("23",)),
        (-1, 1, 0): (("13",), ("01", "03", "12", "23"), ("03", "23")),
        (0, -1, 0): (("02", "12"), ("01", "12"), ("02",)),
        (0, -1, 1): (("02", "12"), ("12", "23"), ("02", "23")),
        (0, 0, -1): (("02", "03", "12", "13"), ("01",), ("02", "03")),
        (0, 0, 1): (("02", "03", "12", "13"), ("23",), ("23",)),
        (0, 1, -1): (("03", "13"), ("01", "03"), ("03",)),
        (0, 1, 0): (("03", "13"), ("03", "23"), ("03", "23")),
        (1, -1, 0): (("02",), ("01", "03", "12", "23"), ("02",)),
        (1, 0, -1): (("02", "03"), ("01", "03"), ("02", "03")),
        (1, 0, 0): (("02", "03"), ("03", "23"), ("02", "03", "23")),
    }
    supports = {}
    for normal in expected_normals:
        plane_supports = []
        for plane in (1, 2, 3):
            values = {
                label: dot(normal, exponent)
                for label, exponent in configurations[plane].items()
            }
            maximum = max(values.values())
            plane_supports.append(
                tuple(
                    label
                    for label, value in values.items()
                    if value == maximum
                )
            )
        supports[normal] = tuple(plane_supports)
    assert supports == expected_supports

    deletion_coordinates = {
        0: {"12", "13", "23"},
        1: {"02", "03", "23"},
        2: {"01", "03", "13"},
        3: {"01", "02", "12"},
    }
    expected_all_rank = {
        (-1, 0, 0): (0, 2, 3),
        (-1, 0, 1): (0,),
        (-1, 1, 0): (0, 2),
        (0, -1, 0): (3,),
        (0, -1, 1): (0, 1, 3),
        (0, 0, -1): (2, 3),
        (0, 0, 1): (0, 1),
        (0, 1, -1): (1, 2),
        (0, 1, 0): (0, 1, 2),
        (1, -1, 0): (1, 3),
        (1, 0, -1): (1, 2, 3),
        (1, 0, 0): (1, 2),
    }
    all_rank = {}
    for normal, plane_supports in supports.items():
        all_rank[normal] = tuple(
            distinguished
            for distinguished in range(4)
            if all(
                set(support) & deletion_coordinates[distinguished]
                for support in plane_supports
            )
        )
    assert all_rank == expected_all_rank

    genuine_normals = tuple(
        normal for normal in expected_normals if normal != (-1, 0, 0)
    )
    genuine_pairs = len(genuine_normals) * 4
    remaining_pairs = sum(
        len(all_rank[normal]) for normal in genuine_normals
    )
    gate_pairs = genuine_pairs - remaining_pairs
    assert (genuine_pairs, gate_pairs, remaining_pairs) == (44, 21, 23)

    output = {
        "verified": True,
        "method": "exact Minkowski-sum normal fan",
        "minkowski_lattice_points": len(points),
        "toric_facets": len(facets),
        "facet_normals": [list(normal) for normal in expected_normals],
        "internal_E_zero_normal": [-1, 0, 0],
        "genuine_base_boundary_divisors": len(genuine_normals),
        "divisor_orientation_pairs": genuine_pairs,
        "gate_excluded_pairs": gate_pairs,
        "all_rank_pairs": remaining_pairs,
        "all_rank_orientations": {
            str(normal): list(values)
            for normal, values in all_rank.items()
            if normal != (-1, 0, 0)
        },
        "ambient_local_maps_enumerated": 0,
        "Grassmannians_enumerated": 0,
        "dependencies": {
            CHART_BOUNDARY.name: sha256(CHART_BOUNDARY),
            FIBER_BOUNDARY.name: sha256(FIBER_BOUNDARY),
            GATE.name: sha256(GATE),
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
        REPO_ROOT / "tmp" / "p4_pure_rank_two_component_toric_boundary_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
