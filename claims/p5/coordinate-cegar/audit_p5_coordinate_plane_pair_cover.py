#!/usr/bin/env python3
"""Independent F_7 audit of the P_5 coordinate-plane pair cover."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIME = 7
ZERO = (0, 0, 0)
COORDINATES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    reduced = tuple(value % PRIME for value in vector)
    if not any(reduced):
        return ZERO
    first = next(value for value in reduced if value)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in reduced)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right)) % PRIME


def cross(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return canonical(
        (
            left[1] * right[2] - left[2] * right[1],
            left[2] * right[0] - left[0] * right[2],
            left[0] * right[1] - left[1] * right[0],
        )
    )


def coordinate_plane_pair_count(
    rows: tuple[tuple[int, int, int], ...],
) -> int:
    return sum(
        sum(value != 0 for value in cross(rows[left], rows[right])) == 1
        for left, right in itertools.combinations(range(5), 2)
    )


def main() -> None:
    projective_points = tuple(
        sorted(
            {
                canonical(vector)
                for vector in itertools.product(range(PRIME), repeat=3)
                if any(vector)
            }
        )
    )
    assert len(projective_points) == PRIME**2 + PRIME + 1
    projective_lines = projective_points

    line_configurations = 0
    axial_configurations = 0
    generic_configurations = 0
    pair_count_distribution: Counter[int] = Counter()
    generic_maximum = 0
    for singleton in COORDINATES:
        for line in projective_lines:
            points_on_line = tuple(
                point for point in projective_points if dot(line, point) == 0
            )
            if singleton in points_on_line:
                continue
            coordinate_points = tuple(
                point for point in COORDINATES if point in points_on_line
            )
            if not coordinate_points:
                continue
            noncoordinates = tuple(
                point
                for point in points_on_line
                if point not in COORDINATES
            )
            for chosen in itertools.combinations(noncoordinates, 4):
                rows = chosen + (singleton,)
                pair_count = coordinate_plane_pair_count(rows)
                pair_count_distribution[pair_count] += 1
                line_configurations += 1
                if len(coordinate_points) == 2:
                    axial_configurations += 1
                    assert pair_count == 6
                else:
                    generic_configurations += 1
                    generic_maximum = max(generic_maximum, pair_count)
                    assert pair_count <= 1

    assert axial_configurations == 3 * 15
    assert generic_configurations == 3 * 12 * 35
    assert line_configurations == axial_configurations + generic_configurations
    assert generic_maximum == 1

    # Independent incidence-budget replay.
    local_non_axial_maximum = 1
    modes = 5
    required_pairs = 10
    assert modes * local_non_axial_maximum < required_pairs

    primary = ROOT / "tmp" / "p5_coordinate_plane_pair_cover_verified.json"
    output = {
        "verified": True,
        "finite_field": f"F_{PRIME}",
        "projective_points_and_lines": len(projective_points),
        "line_configurations_checked": line_configurations,
        "axial_line_configurations": axial_configurations,
        "generic_line_configurations": generic_configurations,
        "coordinate_plane_pair_count_distribution": dict(
            sorted(pair_count_distribution.items())
        ),
        "generic_line_maximum_pair_count": generic_maximum,
        "five_mode_non_axial_pair_budget": (
            modes * local_non_axial_maximum
        ),
        "required_pair_cover": required_pairs,
        "primary_artifact": primary.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(primary),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_coordinate_plane_pair_cover_audited.json"
    )
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
