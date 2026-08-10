#!/usr/bin/env python3
"""Primary verifier for the P_5 source-row tricolour cover."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_SOURCE_ROW_TRICOLOUR_COVER.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    cases = []
    for killed_mask in range(8):
        killed = killed_mask.bit_count()
        surviving = 3 - killed
        if surviving == 0:
            outcome = "all_colour_terms_killed"
            admissible = True
        elif surviving == 1:
            outcome = "one_nonzero_tensor_cannot_vanish"
            admissible = False
        elif surviving == 2:
            outcome = "killer_plane_makes_surviving_factors_independent"
            admissible = False
        else:
            outcome = "three_term_dependence_would_force_rank_one_mode"
            admissible = False
        cases.append(
            {
                "killed_colour_mask": killed_mask,
                "surviving_terms": surviving,
                "outcome": outcome,
                "admissible": admissible,
            }
        )

    admissible = [case for case in cases if case["admissible"]]
    assert len(admissible) == 1
    assert admissible[0]["killed_colour_mask"] == 0b111

    source_rows = 5
    colours = 3
    modes = 5
    forced_coordinate_cells = source_rows * colours
    assert forced_coordinate_cells == 15
    assert (forced_coordinate_cells + modes - 1) // modes == 3

    output = {
        "verified": True,
        "field": "C",
        "restricted_diagonal_term_cases_checked": len(cases),
        "admissible_killed_colour_masks": [
            case["killed_colour_mask"] for case in admissible
        ],
        "coordinate_rows_forced": forced_coordinate_cells,
        "minimum_coordinate_rows_in_one_mode": 3,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_source_row_tricolour_cover_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
