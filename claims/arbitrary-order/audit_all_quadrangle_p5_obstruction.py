#!/usr/bin/env python3
"""Independent F_7 audit of the all-quadrangle P_5 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIME = 7
COORDINATES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
QUADRANGLE = (
    (1, 1, 1),
    (-1, 1, 1),
    (1, -1, 1),
    (1, 1, -1),
)


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


def main() -> None:
    local_types = []
    for singleton_source in range(5):
        remaining_sources = tuple(
            source for source in range(5) if source != singleton_source
        )
        for singleton_colour in range(3):
            for order in itertools.permutations(range(4)):
                rows: list[tuple[int, int, int] | None] = [None] * 5
                rows[singleton_source] = COORDINATES[singleton_colour]
                for source, vertex in zip(remaining_sources, order):
                    rows[source] = QUADRANGLE[vertex]
                local_types.append(tuple(rows))
    assert len(local_types) == 5 * 3 * math.factorial(4)

    pair_checks = 0
    missing_distribution: Counter[int] = Counter()
    for rows in local_types:
        for left, right in itertools.combinations(range(5), 2):
            annihilator = cross(rows[left], rows[right])
            support = tuple(value != 0 for value in annihilator)
            assert sum(support) == 2
            missing_distribution[
                next(index for index, present in enumerate(support) if not present)
            ] += 1
            pair_checks += 1
    assert pair_checks == 3600
    assert len(set(missing_distribution.values())) == 1

    selections_checked = 0
    for missing in itertools.product(range(3), repeat=5):
        found = False
        for retained in itertools.combinations(range(5), 4):
            for colour in range(3):
                if all(missing[index] != colour for index in retained):
                    found = True
        assert found
        selections_checked += 1
    assert selections_checked == 243

    primary = ROOT / "tmp" / "all_quadrangle_p5_obstruction_verified.json"
    output = {
        "verified": True,
        "finite_field": f"F_{PRIME}",
        "labelled_quadrangle_local_types": len(local_types),
        "row_pair_annihilators_checked": pair_checks,
        "missing_colour_distribution": dict(
            sorted(missing_distribution.items())
        ),
        "missing_colour_lists_checked": selections_checked,
        "selection_failures": 0,
        "primary_artifact": primary.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(primary),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "all_quadrangle_p5_obstruction_audited.json"
    )
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
