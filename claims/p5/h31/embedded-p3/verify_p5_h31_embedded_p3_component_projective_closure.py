#!/usr/bin/env python3
"""Verify projective closure of the ninth component is H31-empty."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

THEOREM = (
    HERE
    / "P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md"
)
AFFINE = (
    HERE
    / "P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md"
)
SUPPORT_TWO = (
    HERE
    / "P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md"
)
NORMALIZED = (
    HERE
    / "P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent3(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(3))
            for permutation in itertools.permutations(range(3))
        )
    )


def main() -> None:
    cap_c, cap_a, cap_b = sp.symbols("C A B")
    planes = (
        ((-cap_a, cap_c, 0), (-cap_b, 0, cap_c)),
        ((cap_a, cap_c, 0), (cap_b, 0, cap_c)),
        ((cap_a, cap_c, 0), (-cap_b, 0, cap_c)),
    )
    coefficients = {
        word: sp.factor(
            permanent3(
                tuple(planes[mode][word[mode]] for mode in range(3))
            )
        )
        for word in WORDS3
    }
    assert coefficients[(1, 0, 0)] == 2 * cap_a * cap_c**2
    assert coefficients[(1, 0, 1)] == -2 * cap_b * cap_c**2
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word not in ((1, 0, 0), (1, 0, 1))
    )

    # A common coordinate plane gives zero P3 on its triple product.
    support_one_zero = {}
    for normal_coordinate in range(3):
        plane_coordinates = tuple(
            coordinate
            for coordinate in range(3)
            if coordinate != normal_coordinate
        )
        basis = tuple(
            tuple(int(index == coordinate) for index in range(3))
            for coordinate in plane_coordinates
        )
        tensor = {
            word: permanent3(
                tuple(basis[word[mode]] for mode in range(3))
            )
            for word in WORDS3
        }
        assert all(value == 0 for value in tensor.values())
        support_one_zero[str(1 << normal_coordinate)] = True

    # Every projective support of size at least two has a chart with
    # common coordinate C' and nonzero sign parameter B'.
    chart_cover = {}
    for mask in range(1, 8):
        support = tuple(
            coordinate for coordinate in range(3) if mask & (1 << coordinate)
        )
        if len(support) == 1:
            continue
        common_slot = support[0]
        nonzero_b_slot = support[1]
        remaining_slot = next(
            (
                coordinate
                for coordinate in range(3)
                if coordinate not in (common_slot, nonzero_b_slot)
            ),
            next(
                coordinate
                for coordinate in range(3)
                if coordinate != common_slot
            ),
        )
        source_order = (common_slot, remaining_slot, nonzero_b_slot)
        assert len(set(source_order)) == 3
        assert mask & (1 << source_order[0])
        assert mask & (1 << source_order[2])
        chart_cover[str(mask)] = {
            "source_order_CAB": list(source_order),
            "C_nonzero": True,
            "B_nonzero": True,
        }
    assert len(chart_cover) == 4

    # The four nonzero supports are 011,101,110,111; the other three
    # projective coordinate points are precisely the zero restrictions.
    assert set(chart_cover) == {"3", "5", "6", "7"}
    assert set(support_one_zero) == {"1", "2", "4"}

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "homogeneous sign-rectangle normals and source-coordinate "
            "chart transport"
        ),
        "homogeneous_nonzero_coefficients": {
            "100": str(coefficients[(1, 0, 0)]),
            "101": str(coefficients[(1, 0, 1)]),
        },
        "support_one_zero_restrictions": support_one_zero,
        "nonzero_projective_support_chart_cover": chart_cover,
        "whole_projective_ninth_component_H31_fibre_empty": True,
        "ninth_component_complete_marked_H31_fibre_excluded": True,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            NORMALIZED.name: sha256(NORMALIZED),
            SUPPORT_TWO.name: sha256(SUPPORT_TWO),
            AFFINE.name: sha256(AFFINE),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
