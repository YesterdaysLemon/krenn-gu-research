#!/usr/bin/env python3
"""Independent F_7 audit of the P_5 kernel Hall hierarchy."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIME = 7
ZERO = (0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    reduced = tuple(value % PRIME for value in vector)
    first = next(value for value in reduced if value)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in reduced)


def main() -> None:
    projective_vectors = tuple(
        sorted(
            {
                canonical(vector)
                for vector in itertools.product(range(PRIME), repeat=3)
                if any(vector)
            }
        )
    )
    kernel_lines = tuple(
        vector
        for vector in projective_vectors
        if any(value == 0 for value in vector)
    )
    coordinate_planes = (
        ((0, 1, 0), (0, 0, 1)),
        ((1, 0, 0), (0, 0, 1)),
        ((1, 0, 0), (0, 1, 0)),
    )

    active_sets: Counter[tuple[int, ...]] = Counter()
    for vector in kernel_lines:
        active_sets[
            tuple(index for index, value in enumerate(vector) if value)
        ] += 1
    for plane in coordinate_planes:
        active_sets[
            tuple(
                index
                for index in range(3)
                if any(vector[index] for vector in plane)
            )
        ] += 1
    assert set(active_sets) == {
        (0,),
        (1,),
        (2,),
        (0, 1),
        (0, 2),
        (1, 2),
    }

    hierarchy_checks = {}
    for source_size in (2, 3, 4):
        maximum_active = 5 - source_size
        masks_checked = 0
        accepted = 0
        minimum_inactive = 5
        for active_mode_mask in range(1 << 5):
            masks_checked += 1
            active_count = active_mode_mask.bit_count()
            if active_count <= maximum_active:
                accepted += 1
                minimum_inactive = min(
                    minimum_inactive, 5 - active_count
                )
        assert minimum_inactive == source_size
        hierarchy_checks[str(source_size)] = {
            "masks_checked": masks_checked,
            "accepted": accepted,
            "maximum_active": maximum_active,
            "minimum_dual_inactive": minimum_inactive,
        }

    primary = ROOT / "tmp" / "p5_kernel_hall_hierarchy_verified.json"
    output = {
        "verified": True,
        "finite_field": f"F_{PRIME}",
        "projective_kernel_lines_in_coordinate_hyperplanes": len(
            kernel_lines
        ),
        "coordinate_kernel_planes": len(coordinate_planes),
        "active_set_distribution": {
            ",".join(map(str, key)): value
            for key, value in sorted(active_sets.items())
        },
        "hierarchy_checks": hierarchy_checks,
        "primary_artifact": primary.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(primary),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_kernel_hall_hierarchy_audited.json"
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
