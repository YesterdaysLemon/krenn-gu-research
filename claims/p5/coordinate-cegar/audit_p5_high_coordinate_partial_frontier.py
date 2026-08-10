#!/usr/bin/env python3
"""Independent catalogue audit of the high-coordinate partial frontier."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/frontier")

import audit_p5_pair_signature_catalogue_coverage as COVERAGE


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md"
COORDINATE_MASKS = (1, 2, 4)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coordinate_multiplicity(supports: tuple[int, ...]) -> tuple[int, ...]:
    colours = tuple(
        mask.bit_length() - 1
        for mask in supports
        if mask in COORDINATE_MASKS
    )
    return tuple(sorted(Counter(colours).values(), reverse=True))


def target_support_counts(supports: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            (
                sum(bool(mask & (1 << colour)) for mask in supports)
                for colour in range(3)
            ),
            reverse=True,
        )
    )


def classify(supports: tuple[int, ...]) -> str | None:
    coordinate_rows = sum(mask in COORDINATE_MASKS for mask in supports)
    multiplicity = coordinate_multiplicity(supports)
    counts = target_support_counts(supports)
    if coordinate_rows == 5 and multiplicity == (3, 1, 1):
        return "q5_311"
    if coordinate_rows == 5 and multiplicity == (2, 2, 1):
        return "q5_221"
    if coordinate_rows != 4:
        return None
    partial_mask = next(
        mask for mask in supports if mask not in COORDINATE_MASKS
    )
    if multiplicity == (2, 1, 1):
        return "q4_zero" if partial_mask == 0 else "q4_partial"
    if multiplicity == (3, 1):
        if counts == (4, 1, 1):
            return "partial_31_two_singleton"
        if counts == (3, 2, 1):
            return "H31_a0"
        if counts == (4, 2, 1):
            return "H31_a_nonzero"
    if multiplicity == (2, 2):
        if counts == (3, 2, 1):
            return "H22_one_mark"
        if counts == (3, 3, 1):
            return "H22_two_marks"
    raise AssertionError(
        f"unclassified high support: {supports}, {multiplicity}, {counts}"
    )


def main() -> None:
    catalogue = COVERAGE.catalogue_pair_patterns()
    counts = Counter()
    for supports, _incidences in catalogue:
        family = classify(supports)
        if family is not None:
            counts[family] += 1

    expected = {
        "H22_one_mark": 180,
        "H22_two_marks": 90,
        "H31_a0": 120,
        "H31_a_nonzero": 120,
        "partial_31_two_singleton": 120,
        "q4_partial": 720,
        "q4_zero": 180,
        "q5_221": 90,
        "q5_311": 60,
    }
    assert len(catalogue) == 6495
    assert dict(counts) == expected
    excluded_families = {
        "partial_31_two_singleton",
        "q4_partial",
        "q4_zero",
        "q5_221",
        "q5_311",
    }
    frontier_families = {
        "H31_a0",
        "H31_a_nonzero",
        "H22_one_mark",
        "H22_two_marks",
    }
    excluded = sum(counts[family] for family in excluded_families)
    frontier = sum(counts[family] for family in frontier_families)
    assert excluded == 1170
    assert frontier == 510
    assert excluded + frontier == 1680

    output = {
        "audited": True,
        "finite_field": "F_5",
        "scope": "independent local-signature census; reduction is over C",
        "catalogue_pair_signatures": len(catalogue),
        "high_coordinate_signatures": excluded + frontier,
        "excluded_high_coordinate_signatures": excluded,
        "frontier_high_coordinate_signatures": frontier,
        "family_counts": dict(sorted(counts.items())),
        "all_high_signatures_classified": True,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_high_coordinate_partial_frontier_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
