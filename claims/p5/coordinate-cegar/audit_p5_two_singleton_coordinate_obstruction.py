#!/usr/bin/env python3
"""Independent catalogue audit of the P5 two-singleton theorem."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

import audit_p5_pair_signature_catalogue_coverage as COVERAGE


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md"
COORDINATE_MASKS = (1, 2, 4)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def singleton_axes(supports: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        colour
        for colour in range(3)
        if sum(bool(mask & (1 << colour)) for mask in supports) == 1
    )


def unique_source(supports: tuple[int, ...], colour: int) -> int:
    sources = tuple(
        source
        for source, mask in enumerate(supports)
        if mask & (1 << colour)
    )
    if len(sources) != 1:
        raise AssertionError("target coordinate is not singleton-supported")
    return sources[0]


def coordinate_profile(supports: tuple[int, ...]) -> tuple[int, ...]:
    colours = tuple(
        mask.bit_length() - 1
        for mask in supports
        if mask in COORDINATE_MASKS
    )
    return tuple(
        sorted(Counter(colours).values(), reverse=True)
    )


def support_count_profile(supports: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            (
                sum(bool(mask & (1 << colour)) for mask in supports)
                for colour in range(3)
            ),
            reverse=True,
        )
    )


def main() -> None:
    catalogue = COVERAGE.catalogue_pair_patterns()
    selected = []
    family_counts = Counter()
    for supports, incidences in catalogue:
        axes = singleton_axes(supports)
        if len(axes) < 2:
            continue
        sources = tuple(unique_source(supports, colour) for colour in axes)
        if len(set(sources)) != len(sources):
            raise AssertionError("singleton target axes share a source row")
        selected.append((supports, incidences))
        family_counts[
            (
                sum(mask in COORDINATE_MASKS for mask in supports),
                coordinate_profile(supports),
                support_count_profile(supports),
            )
        ] += 1

    expected = {
        (4, (2, 1, 1), (2, 1, 1)): 180,
        (4, (3, 1), (4, 1, 1)): 120,
        (5, (3, 1, 1), (3, 1, 1)): 60,
    }
    assert len(catalogue) == 6495
    assert len(selected) == 360
    assert dict(family_counts) == expected

    output = {
        "audited": True,
        "finite_field": "F_5",
        "scope": "catalogue census only; theorem is over C",
        "catalogue_pair_signatures": len(catalogue),
        "two_singleton_signatures": len(selected),
        "unique_source_rows_always_distinct": True,
        "family_counts": [
            {
                "coordinate_rows": key[0],
                "coordinate_multiplicity": list(key[1]),
                "target_support_counts": list(key[2]),
                "count": count,
            }
            for key, count in sorted(family_counts.items())
        ],
        "two_singleton_local_map_possible": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_two_singleton_obstruction_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
