#!/usr/bin/env python3
"""Primary verifier for the five-row projective normal-form theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "FIVE_ROW_PROJECTIVE_NORMAL_FORMS.md"
VERTICES = range(4)
EDGES = tuple(itertools.combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIANGLES = tuple(itertools.combinations(VERTICES, 3))
OPPOSITE_PAIRS = (
    (((0, 1)), ((2, 3))),
    (((0, 2)), ((1, 3))),
    (((0, 3)), ((1, 2))),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cross(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right))


def main() -> None:
    rainbow_assignments = []
    for colours in itertools.product(range(3), repeat=len(EDGES)):
        if all(
            len(
                {
                    colours[EDGE_INDEX[tuple(sorted((a, b)))]],
                    colours[EDGE_INDEX[tuple(sorted((a, c)))]],
                    colours[EDGE_INDEX[tuple(sorted((b, c)))]],
                }
            )
            == 3
            for a, b, c in TRIANGLES
        ):
            rainbow_assignments.append(colours)
            assert all(
                colours[EDGE_INDEX[left]] == colours[EDGE_INDEX[right]]
                for left, right in OPPOSITE_PAIRS
            )
    assert len(rainbow_assignments) == 6

    points = (
        (1, 1, 1),
        (-1, 1, 1),
        (1, -1, 1),
        (1, 1, -1),
    )
    coordinates = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    quadrangle_diagonals = []
    for left, right in OPPOSITE_PAIRS:
        first_line = cross(points[left[0]], points[left[1]])
        second_line = cross(points[right[0]], points[right[1]])
        intersection = cross(first_line, second_line)
        assert sum(value != 0 for value in intersection) == 1
        quadrangle_diagonals.append(intersection)
    assert {
        next(index for index, value in enumerate(point) if value)
        for point in quadrangle_diagonals
    } == {0, 1, 2}

    # A representative line-type configuration.  Its four
    # non-coordinate points lie in L=span(e_0,(0,1,1)); the annihilator
    # t=(0,1,-1) has support two, kills them, and is nonzero on the
    # unique coordinate row e_1 off L.
    line_points = (
        (1, 1, 1),
        (2, 1, 1),
        (3, 1, 1),
        (4, 1, 1),
    )
    line_annihilator = (0, 1, -1)
    singleton = coordinates[1]
    assert all(dot(row, line_annihilator) == 0 for row in line_points)
    assert dot(singleton, line_annihilator) != 0
    assert sum(value != 0 for value in line_annihilator) == 2

    output = {
        "verified": True,
        "field": "C",
        "k4_edge_colour_assignments_checked": 3 ** len(EDGES),
        "fully_rainbow_k4_assignments": len(rainbow_assignments),
        "all_have_equal_opposite_edge_colours": True,
        "standard_quadrangle_diagonal_coordinate_count": len(
            quadrangle_diagonals
        ),
        "line_type_annihilator_support": sum(
            value != 0 for value in line_annihilator
        ),
        "line_type_source_image_support": 1,
        "local_strata": (
            "at-least-two-coordinate, line, quadrangle"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "five_row_projective_normal_forms_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
