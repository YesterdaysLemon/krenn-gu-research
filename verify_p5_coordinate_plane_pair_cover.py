#!/usr/bin/env python3
"""Primary verifier for the P_5 coordinate-plane pair-cover theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COORDINATE_PLANE_PAIR_COVER.md"
ACTIVE_MASKS = (0b001, 0b010, 0b100, 0b011, 0b101, 0b110)
COORDINATES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
QUADRANGLE = (
    (1, 1, 1),
    (-1, 1, 1),
    (1, -1, 1),
    (1, 1, -1),
    (0, 0, 1),
)
AXIAL_LINE = (
    (1, 1, 0),
    (1, 2, 0),
    (1, 3, 0),
    (1, 4, 0),
    (0, 0, 1),
)
GENERIC_LINE = (
    (0, 1, 1),
    (1, 1, 1),
    (2, 1, 1),
    (3, 1, 1),
    (0, 0, 1),
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


def coordinate_plane_pairs(
    rows: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, int], ...]:
    result = []
    for left, right in itertools.combinations(range(5), 2):
        kernel = cross(rows[left], rows[right])
        if sum(value != 0 for value in kernel) == 1:
            result.append((left, right))
    return tuple(result)


def main() -> None:
    active_tuples_checked = 0
    admissible_tuples = 0
    without_singleton = 0
    for active_sets in itertools.product(ACTIVE_MASKS, repeat=5):
        active_tuples_checked += 1
        colour_counts = tuple(
            sum(bool(mask & (1 << colour)) for mask in active_sets)
            for colour in range(3)
        )
        if max(colour_counts) >= 4:
            continue
        admissible_tuples += 1
        has_singleton = any(mask.bit_count() == 1 for mask in active_sets)
        without_singleton += int(not has_singleton)
        assert has_singleton
    assert active_tuples_checked == 6**5
    assert without_singleton == 0

    pair_counts = {
        "quadrangle": len(coordinate_plane_pairs(QUADRANGLE)),
        "axial_line": len(coordinate_plane_pairs(AXIAL_LINE)),
        "generic_line_maximal_example": len(
            coordinate_plane_pairs(GENERIC_LINE)
        ),
    }
    assert pair_counts == {
        "quadrangle": 0,
        "axial_line": 6,
        "generic_line_maximal_example": 1,
    }

    selected_modes = {0, 1, 2, 3}
    forbidden_sources = {0, 1}
    assignments_checked = 0
    surviving_assignments = 0
    for permutation in itertools.permutations(range(5)):
        assignments_checked += 1
        surviving_assignments += int(
            all(
                permutation[mode] not in forbidden_sources
                for mode in selected_modes
            )
        )
    assert assignments_checked == 120
    assert surviving_assignments == 0

    output = {
        "verified": True,
        "field": "C",
        "active_set_tuples_checked": active_tuples_checked,
        "tuples_surviving_four_mode_obstruction": admissible_tuples,
        "surviving_tuples_without_singleton_active_set": without_singleton,
        "local_coordinate_plane_pair_counts": pair_counts,
        "permanent_assignments_checked": assignments_checked,
        "surviving_permanent_assignments": surviving_assignments,
        "forced_source_pair_cover_size": 10,
        "consequence": (
            "some local map has at least two coordinate rows or "
            "has axial 4+1 support"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_coordinate_plane_pair_cover_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
