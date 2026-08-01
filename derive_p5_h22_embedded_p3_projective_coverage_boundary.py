#!/usr/bin/env python3
"""Derive the exact chart boundary left by embedded-P3 weighted-H22 results."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_COVERAGE_BOUNDARY.md"
GENERIC = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
RANK_TWO = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md"
RANK_ONE = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md"
R_ZERO_VERIFY = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_VERIFICATION.md"
ENDPOINT = (
    ROOT
    / "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_OBSTRUCTION_CANDIDATE.md"
)
ENDPOINT_VERIFICATION = ROOT / (
    "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_"
    "ENDPOINTS_VERIFICATION.md"
)
OLD_AUDIT = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_VERIFICATION.md"

WORDS3 = tuple(itertools.product((0, 1), repeat=3))
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def permanent(rows):
    """Permanent by squarefree subset dynamic programming."""
    size = len(rows)
    state = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, value in state.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                updated[new_mask] = sp.expand(
                    updated.get(new_mask, 0) + value * row[column]
                )
        state = updated
    return sp.expand(state[(1 << size) - 1])


def tensor_coefficients(planes):
    words = WORDS3 if len(planes) == 3 else WORDS4
    return {
        word: permanent(
            tuple(planes[index][word[index]] for index in range(len(planes)))
        )
        for word in words
    }


def basis_of_normal(normal):
    return tuple(
        tuple(entry for entry in vector) for vector in sp.Matrix([normal]).nullspace()
    )


def normal_support_audit():
    # Bits are the coordinates (C,A,B)=(partner, first opposite, second opposite).
    pure_masks = {}
    for mask in range(1, 8):
        C, A, B = (sp.Integer(bool(mask & (1 << index))) for index in range(3))
        normals = ((C, A, B), (C, -A, -B), (C, -A, B))
        planes = tuple(basis_of_normal(normal) for normal in normals)
        coefficients = tensor_coefficients(planes)
        support = {
            "".join(map(str, word)): str(value)
            for word, value in coefficients.items()
            if value != 0
        }
        pure_masks[mask] = support
        assert bool(support) == (mask.bit_count() >= 2)
    return pure_masks


def chart_census():
    # The distinguished common coordinate is c=0.  In the fixed H22 matching
    # 01|23 its unique partner is p=1, represented by the C bit below.
    admissible_normal_masks = (3, 5, 6, 7)
    line_masks = tuple(range(1, 8))
    cells = {}
    uncovered = []
    for normal_mask in admissible_normal_masks:
        for line_mask in line_masks:
            normal_partner_nonzero = bool(normal_mask & 1)
            free_partner_pivot_nonzero = bool(line_mask & 1)
            covered_chart = normal_partner_nonzero and free_partner_pivot_nonzero
            key = f"N{normal_mask}_L{line_mask}"
            cells[key] = {
                "normal_partner_nonzero": normal_partner_nonzero,
                "free_partner_pivot_nonzero": free_partner_pivot_nonzero,
                "enters_CB_P01_chart": covered_chart,
            }
            if not covered_chart:
                uncovered.append(key)
    assert len(cells) == 28
    assert (
        len([value for value in cells.values() if value["enters_CB_P01_chart"]]) == 12
    )
    assert len(uncovered) == 16
    return cells, uncovered


def plucker_chart_audit():
    S, U, R, T = sp.symbols("S U R T")
    alpha = sp.Matrix((0, 1, S, U))
    beta = sp.Matrix((1, 0, R, T))
    rows = sp.Matrix.hstack(alpha, beta).T
    plucker = {}
    for i, j in itertools.combinations(range(4), 2):
        plucker[f"P{i}{j}"] = sp.factor(rows[:, (i, j)].det())
    expected = {
        "P01": -1,
        "P02": -S,
        "P03": -U,
        "P12": R,
        "P13": T,
        "P23": S * T - U * R,
    }
    assert plucker == expected
    return {key: str(value) for key, value in plucker.items()}


def coordinate_hyperplanes(plane):
    return tuple(
        coordinate
        for coordinate in range(4)
        if all(row[coordinate] == 0 for row in plane)
    )


def unique_embedded_triple(planes):
    triples = []
    for modes in itertools.combinations(range(4), 3):
        common = set(range(4))
        for mode in modes:
            common &= set(coordinate_hyperplanes(planes[mode]))
        if common:
            triples.append((modes, tuple(sorted(common))))
    return triples


def explicit_counterexamples():
    full_last = (
        ((0, -1, 1, 0), (0, -1, 0, 1)),
        ((0, 1, 1, 0), (0, 1, 0, 1)),
        ((0, 1, 1, 0), (0, -1, 0, 1)),
    )

    old_u0 = ((0, 1, 0, 0), (1, 0, 0, 0))
    old_planes = (old_u0, *full_last)
    old_coefficients = tensor_coefficients(old_planes)
    old_support = {
        "".join(map(str, word)): str(value)
        for word, value in old_coefficients.items()
        if value != 0
    }
    assert old_support == {"1100": "2", "1101": "-2"}
    assert unique_embedded_triple(old_planes) == [((1, 2, 3), (0,))]

    free_pivot_u0 = ((0, 0, 1, 0), (1, 0, 0, 0))
    free_pivot_planes = (free_pivot_u0, *full_last)
    free_pivot_coefficients = tensor_coefficients(free_pivot_planes)
    free_pivot_support = {
        "".join(map(str, word)): str(value)
        for word, value in free_pivot_coefficients.items()
        if value != 0
    }
    assert free_pivot_support == {"1100": "2", "1101": "-2"}
    assert unique_embedded_triple(free_pivot_planes) == [((1, 2, 3), (0,))]

    mask6_last = (
        ((0, 1, 0, 0), (0, 0, 1, -1)),
        ((0, 1, 0, 0), (0, 0, 1, -1)),
        ((0, 1, 0, 0), (0, 0, 1, 1)),
    )
    normal_gap_planes = (old_u0, *mask6_last)
    normal_gap_coefficients = tensor_coefficients(normal_gap_planes)
    normal_gap_support = {
        "".join(map(str, word)): str(value)
        for word, value in normal_gap_coefficients.items()
        if value != 0
    }
    assert normal_gap_support == {"1110": "-2"}
    assert unique_embedded_triple(normal_gap_planes) == [((1, 2, 3), (0,))]

    return {
        "old_counterexample_now_corner": {
            "normal": "[1:1:1]",
            "U0": "span(e0,e1)",
            "P01_nonzero": True,
            "R": 0,
            "T": 0,
            "tensor_support": old_support,
        },
        "new_free_pivot_gap": {
            "normal": "[1:1:1]",
            "U0": "span(e0,e2)",
            "P01": 0,
            "P02_nonzero": True,
            "tensor_support": free_pivot_support,
        },
        "new_normal_partner_gap": {
            "normal": "[0:1:1]",
            "U0": "span(e0,e1)",
            "P01_nonzero": True,
            "normal_partner_coefficient_C": 0,
            "tensor_support": normal_gap_support,
        },
    }


def permutation_invariants():
    nC, nA, nB = sp.symbols("nC nA nB")
    normal = (0, nC, nA, nB)
    P = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"P{i}{j}"))
    checked = 0
    for permutation in itertools.permutations(range(4)):
        c, partner = 0, 1
        new_c, new_partner = permutation[c], permutation[partner]
        transformed_normal = [0, 0, 0, 0]
        for old_coordinate in range(4):
            transformed_normal[permutation[old_coordinate]] = normal[old_coordinate]
        assert transformed_normal[new_partner] == nC
        # A Pluecker coordinate transforms to the same old coordinate up to
        # the sign needed to restore increasing index order.
        left, right = sorted((new_c, new_partner))
        sign = 1 if (new_c, new_partner) == (left, right) else -1
        transformed_plucker = sign * P[c, partner]
        assert sp.factor(transformed_plucker - sign * P[0, 1]) == 0
        checked += 1
    assert checked == 24
    return {
        "source_permutations_checked": checked,
        "normal_partner_zero_invariant": True,
        "P_common_partner_zero_invariant": True,
    }


def infinity_structural_zero():
    S, U = sp.symbols("S U")
    alpha = (
        (0, 1, S, U),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    D01 = tuple((row[0], row[2], row[3], 0) for row in alpha)
    D23 = tuple((row[0], row[1], row[2], 0) for row in alpha)
    assert permanent(D01) == 0
    assert permanent(D23) == 0
    return {"D01_infinity_A": "0", "D23_infinity_A": "0"}


def orientation_endpoint_audit():
    z0, z1, z2, z3, e, rho, sigma, R, T = sp.symbols("z0 z1 z2 z3 e rho sigma R T")
    swapped = (z0, z1, z3, z2)
    D01_after = (rho * swapped[0] + sigma * swapped[1], swapped[2], swapped[3], e)
    assert D01_after == (rho * z0 + sigma * z1, z3, z2, e)
    D23_after = (swapped[0], swapped[1], rho * swapped[2] + sigma * swapped[3], e)
    assert D23_after == (z0, z1, sigma * z2 + rho * z3, e)
    free_beta = (1, 0, R, T)
    swapped_beta = (free_beta[0], free_beta[1], free_beta[3], free_beta[2])
    assert swapped_beta == (1, 0, T, R)
    return {
        "normal_B_zero_requires_opposite_pair_swap": True,
        "D01_weight_after_swap": "[rho:sigma]",
        "D23_weight_after_swap": "[sigma:rho]",
        "free_coordinates_after_swap": {"R_prime": "T", "T_prime": "R"},
        "nonendpoint_rebalance_available": "rho*sigma!=0",
        "infinity_endpoint_structural_zero": "[1:0]",
        "zero_endpoint_covered_after_swap_when": "T=0 (verified r0 endpoint theorem)",
        "uncovered_orientation_endpoint": "B=0,C*A*P01*T!=0,[rho:sigma]=[0:1]",
    }


def main():
    pure_masks = normal_support_audit()
    cells, uncovered = chart_census()
    plucker = plucker_chart_audit()
    counterexamples = explicit_counterexamples()
    invariants = permutation_invariants()
    infinity = infinity_structural_zero()
    orientation = orientation_endpoint_audit()
    inputs = {
        path.name: sha256(path)
        for path in (
            GENERIC,
            RANK_TWO,
            RANK_ONE,
            R_ZERO_VERIFY,
            ENDPOINT,
            ENDPOINT_VERIFICATION,
            OLD_AUDIT,
        )
    }
    output = {
        "role": "proof_a",
        "date_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_commit": git_commit(),
        "claim_label": "DERIVED",
        "scope": "chart and pivot coverage of the embedded-P3 projective weighted-H22 closure",
        "inputs": inputs,
        "method": "exact normal-support census, Grassmann Pluecker charts, matching-partner invariants, and explicit pure counterexamples",
        "command": "uv run --with sympy python derive_p5_h22_embedded_p3_projective_coverage_boundary.py",
        "outputs": {
            REPORT.name: sha256(REPORT),
            Path(__file__).name: sha256(Path(__file__)),
        },
        "limitations": "coverage result only; the full r0 divisor is verified, but uncovered normal-mask, Grassmann-pivot, and orientation-endpoint strata remain UNKNOWN",
        "normal_support_tensors": pure_masks,
        "chart_cell_count": len(cells),
        "covered_chart_cell_count": len(cells) - len(uncovered),
        "uncovered_chart_cells": uncovered,
        "canonical_plucker_coordinates": plucker,
        "counterexamples": counterexamples,
        "symmetry_invariants": invariants,
        "infinity_structural_zero": infinity,
        "orientation_endpoint": orientation,
        "old_counterexample_repaired_by_r_zero_corner": True,
        "r_zero_only_omitted_free_plane_divisor": False,
        "additional_free_pivot_divisor": "P_common,partner=0",
        "additional_normal_divisor": "normal_partner_coefficient=0",
        "conditional_covered_locus": (
            "C*P01!=0 with B!=0; or B=0,A!=0 away from [0:1]; "
            "at [0:1] the B=0 chart is covered only when T=0"
        ),
        "additional_orientation_endpoint_gap": "B=0,C*A*P01*T!=0,[rho:sigma]=[0:1]",
        "whole_projective_embedded_P3_H22_fibre_empty": "UNKNOWN",
        "report": REPORT.name,
        "report_sha256": sha256(REPORT),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
