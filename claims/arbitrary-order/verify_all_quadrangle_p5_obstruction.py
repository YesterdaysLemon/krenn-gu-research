#!/usr/bin/env python3
"""Primary verifier for the all-quadrangle P_5 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "ALL_QUADRANGLE_P5_OBSTRUCTION.md"
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


def cross(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def choose_four_with_common_colour(
    missing_colours: tuple[int, ...],
) -> tuple[tuple[int, ...], int]:
    for discarded in range(5):
        retained = tuple(index for index in range(5) if index != discarded)
        for colour in range(3):
            if all(missing_colours[index] != colour for index in retained):
                return retained, colour
    raise AssertionError("the five-colour pigeonhole lemma failed")


def main() -> None:
    pair_supports = []
    missing_colours = []
    for singleton_colour in range(3):
        rows = QUADRANGLE + (COORDINATES[singleton_colour],)
        for left, right in itertools.combinations(range(5), 2):
            annihilator = cross(rows[left], rows[right])
            support = tuple(
                colour
                for colour, value in enumerate(annihilator)
                if value != 0
            )
            assert len(support) == 2
            pair_supports.append(support)
            missing_colours.append(
                next(colour for colour in range(3) if colour not in support)
            )
    assert len(pair_supports) == 30
    assert set(missing_colours) == {0, 1, 2}

    lists_checked = 0
    for colour_list in itertools.product(range(3), repeat=5):
        lists_checked += 1
        retained, colour = choose_four_with_common_colour(colour_list)
        assert len(retained) == 4
        assert all(colour_list[index] != colour for index in retained)
    assert lists_checked == 3**5

    # Four selected modes all vanish in the same source pair {0,1}.
    # Every source permutation assigns at least one of those four modes
    # to 0 or 1, so all 120 permanent terms vanish.
    selected_modes = {0, 1, 2, 3}
    forbidden_sources = {0, 1}
    assignments_checked = 0
    surviving_assignments = 0
    for permutation in itertools.permutations(range(5)):
        assignments_checked += 1
        survives = all(
            permutation[mode] not in forbidden_sources
            for mode in selected_modes
        )
        surviving_assignments += int(survives)
    assert assignments_checked == 120
    assert surviving_assignments == 0

    output = {
        "verified": True,
        "field": "C",
        "standard_quadrangle_local_types": 3,
        "row_pair_annihilators_checked": len(pair_supports),
        "annihilator_support_sizes": sorted(
            {len(support) for support in pair_supports}
        ),
        "missing_colour_lists_checked": lists_checked,
        "permanent_assignments_checked": assignments_checked,
        "surviving_permanent_assignments": surviving_assignments,
        "consequence": (
            "a hypothetical P5-to-Delta3 restriction cannot have "
            "five quadrangle-type local maps"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "all_quadrangle_p5_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
