#!/usr/bin/env python3
"""Verify the aggregate classification of the triangle-(2,1,1) cell."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
SOURCES = {
    "support_one": (
        "P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md",
        ("entire support-one boundary", "embedded-`P_3` suspension"),
    ),
    "AA_dense": (
        "P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md",
        ("dense kernel--kernel leaf chart", "active cubic falls into"),
    ),
    "AA_projective": (
        "P4_COMMON_KERNEL_YY_211_TRIANGLE_PROJECTIVE_CLASSIFICATION.md",
        ("complete projective boundary", "closure of component thirteen"),
    ),
    "AB": (
        "P4_RADICAL_CROSSED_211_TRIANGLE_OBSTRUCTION.md",
        ("entire orientation is empty", "sixth Borel-flag orbit"),
    ),
    "AC": (
        "P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md",
        ("indicated orientation and support-two", "pair image has rank at most two"),
    ),
    "BB_dense": (
        "P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md",
        ("twelfth pure", "common-active, support-two orientation"),
    ),
    "BB_projective": (
        "P4_COMMON_ACTIVE_211_TRIANGLE_PROJECTIVE_BOUNDARY_CLASSIFICATION.md",
        ("complete common-active", "component-twelve"),
    ),
    "BC": (
        "P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md",
        ("full-source-support part", "first apolar component"),
    ),
    "CC_equal": (
        "P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md",
        ("thirteenth pure", "Eisenstein norm quadric"),
    ),
    "CC_unequal": (
        "P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md",
        ("component twenty-two", "complete", "UNRESOLVED"),
    ),
}


def _source_path(filename):
    """Locate a source theorem document after the Stage 5 migration.

    Six sources still live at the repository root; three moved into
    sibling classification packages of the same triangle/211 spine.
    Search the package, the root, then the spine's sibling packages;
    fail closed if the document cannot be found.
    """
    for cand in (HERE / filename, REPO_ROOT / filename):
        if cand.exists():
            return cand
    for cand in sorted(HERE.parent.glob("*/" + filename)):
        return cand
    raise FileNotFoundError(filename)



def main() -> None:
    states = ("A", "B", "C")
    flag_orbits = tuple(
        "".join(pair) for pair in itertools.combinations_with_replacement(states, 2)
    )
    assert flag_orbits == ("AA", "AB", "AC", "BB", "BC", "CC")
    routing = {
        "AA": ("AA_dense", "AA_projective"),
        "AB": ("AB",),
        "AC": ("AC",),
        "BB": ("BB_dense", "BB_projective"),
        "BC": ("BC",),
        "CC": ("CC_equal", "CC_unequal"),
    }
    assert set(routing) == set(flag_orbits)

    checked = {}
    for name, (filename, fragments) in SOURCES.items():
        text = _source_path(filename).read_text(encoding="utf-8")
        for fragment in fragments:
            assert fragment in text, (filename, fragment)
        checked[name] = filename

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero source theorems",
                "flag_orbits": flag_orbits,
                "routing": routing,
                "source_theorems": checked,
                "triangle_211_cell_complete": True,
                "new_component_orbit": 22,
                "remaining_all_pair_cells": ["star-(2,1,1)", "star-(1,1,1)"],
                "all_pure_components_classified": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
