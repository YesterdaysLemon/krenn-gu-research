#!/usr/bin/env python3
"""Independent exact audit of the component toric boundary fan."""

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
PRIMARY = HERE / "verify_p4_pure_rank_two_component_toric_boundary.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
    third: tuple[int, int, int],
) -> int:
    return (
        first[0] * (second[1] * third[2] - second[2] * third[1])
        - first[1] * (second[0] * third[2] - second[2] * third[0])
        + first[2] * (second[0] * third[1] - second[1] * third[0])
    )


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


def main() -> None:
    configurations = (
        {
            "02": (1, 0, 0),
            "03": (1, 1, 0),
            "12": (0, 0, 0),
            "13": (0, 1, 0),
        },
        {
            "01": (0, 0, -1),
            "03": (1, 1, 0),
            "12": (0, 0, 0),
            "23": (1, 1, 1),
        },
        {
            "02": (0, -1, 0),
            "03": (0, 0, 0),
            "23": (0, 0, 1),
        },
    )
    points = tuple(sorted({
        tuple(
            first[index] + second[index] + third[index]
            for index in range(3)
        )
        for first in configurations[0].values()
        for second in configurations[1].values()
        for third in configurations[2].values()
    }))

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
    supporting_normals = set()
    for normal in expected_normals:
        values = [dot(normal, point) for point in points]
        maximum = max(values)
        face = tuple(
            point for point, value in zip(points, values, strict=True)
            if value == maximum
        )
        assert len(face) >= 3
        origin = face[0]
        differences = [
            subtract(point, origin) for point in face[1:]
        ]
        face_rank_at_least_two = any(
            determinant(first, second, normal) != 0
            for first, second in itertools.combinations(differences, 2)
        )
        assert face_rank_at_least_two
        supporting_normals.add(normal)

    # Independently find every primitive supporting-plane normal from
    # triples of lattice points.
    reconstructed = set()
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
        reconstructed.add(tuple(entry // divisor for entry in normal))
    assert reconstructed == supporting_normals

    deletion_coordinates = (
        {"12", "13", "23"},
        {"02", "03", "23"},
        {"01", "03", "13"},
        {"01", "02", "12"},
    )
    all_rank_count = 0
    gate_count = 0
    for normal in expected_normals:
        if normal == (-1, 0, 0):
            continue
        supports = []
        for configuration in configurations:
            values = {
                label: dot(normal, exponent)
                for label, exponent in configuration.items()
            }
            maximum = max(values.values())
            supports.append({
                label for label, value in values.items()
                if value == maximum
            })
        for distinguished in range(4):
            if all(
                support & deletion_coordinates[distinguished]
                for support in supports
            ):
                all_rank_count += 1
            else:
                gate_count += 1
    assert (gate_count, all_rank_count) == (21, 23)

    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": "supporting-plane reconstruction",
        "minkowski_lattice_points": len(points),
        "reconstructed_facets": len(reconstructed),
        "gate_excluded_pairs": gate_count,
        "all_rank_pairs": all_rank_count,
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
        REPO_ROOT / "tmp" / "p4_pure_rank_two_component_toric_boundary_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
