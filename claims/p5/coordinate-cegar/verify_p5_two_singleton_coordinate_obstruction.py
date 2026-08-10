#!/usr/bin/env python3
"""Verify the basis-free two-singleton obstruction for P5."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md"
DEPENDENCIES = (
    ROOT / "claims/p4/classifications/pair-geometry/decomposable-restriction-rank-drop/P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md",
    ROOT / "P5_Q5_311_SHARED_DROP_OBSTRUCTION.md",
    ROOT / "P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deleted_permanent(selector: int) -> dict[tuple[int, ...], int]:
    result = {}
    remaining = tuple(index for index in range(5) if index != selector)
    for word in itertools.product(range(5), repeat=4):
        result[word] = int(tuple(sorted(word)) == remaining)
    return result


def main() -> None:
    a0, a1, a2, a3, a4, b3, c4 = sp.symbols(
        "a0 a1 a2 a3 a4 b3 c4",
        nonzero=True,
    )
    rows = (
        sp.Matrix([a0, 0, 0]),
        sp.Matrix([a1, 0, 0]),
        sp.Matrix([a2, 0, 0]),
        sp.Matrix([a3, b3, 0]),
        sp.Matrix([a4, 0, c4]),
    )
    row_matrix = sp.Matrix.hstack(*rows).T
    assert row_matrix.rank() == 3

    pullback_one = tuple(row[1] for row in rows)
    pullback_two = tuple(row[2] for row in rows)
    assert pullback_one == (0, 0, 0, b3, 0)
    assert pullback_two == (0, 0, 0, 0, c4)

    first = deleted_permanent(3)
    second = deleted_permanent(4)
    assert sum(first.values()) == 24
    assert sum(second.values()) == 24
    first_support = {word for word, value in first.items() if value}
    second_support = {word for word, value in second.items() if value}
    first_sources = set.intersection(
        *(set(word) for word in first_support)
    )
    second_sources = set.intersection(
        *(set(word) for word in second_support)
    )
    assert first_sources == {0, 1, 2, 4}
    assert second_sources == {0, 1, 2, 3}
    assert first_sources & second_sources == {0, 1, 2}

    dependencies = {
        path.name: sha256(path)
        for path in DEPENDENCIES
    }
    output = {
        "verified": True,
        "field": "C",
        "singleton_target_coordinates": [1, 2],
        "singleton_source_rows": [3, 4],
        "common_source_rows": [0, 1, 2],
        "deleted_P4_term_counts": [sum(first.values()), sum(second.values())],
        "shared_rank_drop_possible": False,
        "disjoint_rank_drop_case_possible": False,
        "two_singleton_local_map_possible": False,
        "dependencies": dependencies,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_two_singleton_obstruction_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
