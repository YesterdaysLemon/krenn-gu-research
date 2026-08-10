#!/usr/bin/env python3
"""Replay the refuted overstrong embedded-P3 weighted-H22 closure argument."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md"
GENERIC = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
RANK_TWO = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
RANK_ONE = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md"
P4_BOUNDARY = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def permanent3(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def normalized_coefficients() -> dict[tuple[int, ...], sp.Expr]:
    cap_c, cap_a, cap_b = sp.symbols("C A B")
    planes = (
        ((-cap_a, cap_c, 0), (-cap_b, 0, cap_c)),
        ((cap_a, cap_c, 0), (cap_b, 0, cap_c)),
        ((cap_a, cap_c, 0), (-cap_b, 0, cap_c)),
    )
    coefficients = {
        word: sp.factor(
            permanent3(tuple(planes[mode][word[mode]] for mode in range(3)))
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
    return coefficients


def support_one_certificate() -> dict[str, bool]:
    result = {}
    for normal_coordinate in range(3):
        plane_coordinates = tuple(
            coordinate for coordinate in range(3) if coordinate != normal_coordinate
        )
        basis = tuple(
            tuple(sp.Integer(index == coordinate) for index in range(3))
            for coordinate in plane_coordinates
        )
        tensor = {
            word: permanent3(tuple(basis[word[mode]] for mode in range(3)))
            for word in WORDS3
        }
        assert all(value == 0 for value in tensor.values())
        result[str(1 << normal_coordinate)] = True
    assert set(result) == {"1", "2", "4"}
    return result


def nonzero_chart_cover() -> dict[str, dict[str, object]]:
    result = {}
    for mask in range(1, 8):
        support = tuple(
            coordinate for coordinate in range(3) if mask & (1 << coordinate)
        )
        if len(support) < 2:
            continue
        common_slot, nonzero_b_slot = support[:2]
        remaining_slot = next(
            coordinate
            for coordinate in range(3)
            if coordinate not in (common_slot, nonzero_b_slot)
        )
        source_order = (common_slot, remaining_slot, nonzero_b_slot)
        assert len(set(source_order)) == 3
        assert mask & (1 << source_order[0])
        assert mask & (1 << source_order[2])
        result[str(mask)] = {
            "source_order_CAB": list(source_order),
            "C_prime_nonzero": True,
            "B_prime_nonzero": True,
        }
    assert set(result) == {"3", "5", "6", "7"}
    return result


def perfect_matching_orbit() -> dict[str, object]:
    standard = frozenset((frozenset((0, 1)), frozenset((2, 3))))
    images = set()
    witnesses = {}
    for permutation in itertools.permutations(range(4)):
        image = frozenset(
            frozenset(permutation[index] for index in pair) for pair in standard
        )
        canonical = tuple(sorted(tuple(sorted(pair)) for pair in image))
        images.add(canonical)
        witnesses.setdefault(str(canonical), list(permutation))
    expected = {
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    }
    assert images == expected
    return {
        "orbit_size": len(images),
        "perfect_matchings": [list(map(list, matching)) for matching in sorted(images)],
        "witness_permutations": witnesses,
        "weighted_H22_source_pairing_transitive": True,
    }


def main() -> None:
    coefficients = normalized_coefficients()
    zero_points = support_one_certificate()
    chart_cover = nonzero_chart_cover()
    matching_orbit = perfect_matching_orbit()
    report = {
        "status": "pass",
        "claim_label": "REFUTED",
        "role": "proof_b",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "scope": "refutation of a full projective H22 closure inference from the projective-normal chart cover alone",
        "inputs": {
            GENERIC.name: sha256(GENERIC),
            RANK_TWO.name: sha256(RANK_TWO),
            RANK_ONE.name: sha256(RANK_ONE),
            P4_BOUNDARY.name: sha256(P4_BOUNDARY),
        },
        "method": "homogeneous sign-rectangle coefficients, exact support cover, and source-perfect-matching transport",
        "command": 'uv run --with sympy python claims/p5/h22/embedded-p3/verify_p5_h22_embedded_p3_component_projective_closure.py',
        "outputs": {THEOREM.name: sha256(THEOREM)},
        "limitations": "normal-base transport subclaims verified, but free mode-zero-plane normalization boundary remains uncovered; full projective H22 target UNKNOWN",
        "homogeneous_nonzero_coefficients": {
            "100": str(coefficients[(1, 0, 0)]),
            "101": str(coefficients[(1, 0, 1)]),
        },
        "support_one_zero_restrictions": zero_points,
        "nonzero_projective_support_chart_cover": chart_cover,
        "weighted_source_pairing_orbit": matching_orbit,
        "projective_normal_base_chart_transport_verified": True,
        "dependency_cover_complete": False,
        "missing_dependency": "weighted-H22 analogue of the embedded-P3 free-mode-zero-plane r=0 normalization boundary",
        "whole_projective_embedded_P3_H22_fibre_empty": "UNKNOWN",
        "finite_field_computation_used_as_proof": False,
        "fresh_independent_verifier_complete": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
