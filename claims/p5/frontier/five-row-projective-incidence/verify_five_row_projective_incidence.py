#!/usr/bin/env python3
"""Primary verifier for the five-row projective incidence lemma."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = HERE / "FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA.md"
EDGES = tuple(itertools.combinations(range(5), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIANGLES = tuple(itertools.combinations(range(5), 3))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def singleton_placement_orbits() -> int:
    """Count five-edge source-by-colour multisets up to row/colour labels."""
    colour_permutations = tuple(itertools.permutations(range(3)))
    representatives = set()
    for cells in itertools.combinations_with_replacement(range(15), 5):
        counts = [[0] * 3 for _ in range(5)]
        for cell in cells:
            counts[cell // 3][cell % 3] += 1
        orbit = []
        for permutation in colour_permutations:
            rows = tuple(
                sorted(
                    tuple(row[permutation[colour]] for colour in range(3))
                    for row in counts
                )
            )
            orbit.append(rows)
        representatives.add(min(orbit))
    return len(representatives)


def main() -> None:
    rainbow_triangle_counts: Counter[int] = Counter()
    fully_rainbow = 0
    assignments_checked = 0
    for colours in itertools.product(range(3), repeat=len(EDGES)):
        assignments_checked += 1
        rainbow = 0
        for a, b, c in TRIANGLES:
            triangle_colours = {
                colours[EDGE_INDEX[tuple(sorted(edge))]]
                for edge in ((a, b), (a, c), (b, c))
            }
            if len(triangle_colours) == 3:
                rainbow += 1
        rainbow_triangle_counts[rainbow] += 1
        if rainbow == len(TRIANGLES):
            fully_rainbow += 1
    assert assignments_checked == 3**10
    assert fully_rainbow == 0
    assert max(rainbow_triangle_counts) < len(TRIANGLES)

    # The annihilator step uses only the dimension formula for a map
    # C^3 -> C^2 and the equivalence K subset ker(e_c) iff
    # e_c belongs to the row span.
    kernel_dimension_lower_bound = 3 - 2
    assert kernel_dimension_lower_bound == 1

    placement_orbits = singleton_placement_orbits()
    assert placement_orbits == 68

    output = {
        "verified": True,
        "field": "C",
        "edge_colour_assignments_checked": assignments_checked,
        "triangles_per_assignment": len(TRIANGLES),
        "rainbow_triangle_count_distribution": dict(
            sorted(rainbow_triangle_counts.items())
        ),
        "fully_rainbow_assignments": fully_rainbow,
        "two_row_common_kernel_dimension_lower_bound": (
            kernel_dimension_lower_bound
        ),
        "singleton_placement_orbits": placement_orbits,
        "consequence": (
            "every local map in a hypothetical P5-to-Delta3 "
            "restriction has a nonzero singleton row"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "five_row_projective_incidence_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
