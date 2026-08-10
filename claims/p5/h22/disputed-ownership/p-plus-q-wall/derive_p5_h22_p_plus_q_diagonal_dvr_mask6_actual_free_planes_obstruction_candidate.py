#!/usr/bin/env python3
"""Exact obstruction on the actual diagonal-DVR mask-6 free-plane atlas.

The calculation stays in the wall coordinates (e,A,B,C), preserves the
standard 01|23 matching and its shared homogeneous weight, and imports no
discovery or verification code.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
CERTIFICATE = ROOT / (
    "p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_"
    "certificate.json"
)
REPORT = ROOT / (
    "P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_"
    "OBSTRUCTION_CANDIDATE.md"
)
LEDGER = ROOT / "p5_h22_p_plus_q_diagonal_dvr_coverage.json"
P4_WALL = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H22_DEFINITION = REPO_ROOT / "claims/p5/h22/embedded-p3/P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
VERIFICATION_REPORT = ROOT / (
    "P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_"
    "INDEPENDENT_VERIFICATION.md"
)
INDEPENDENT_VERIFIER = (
    ROOT
    / "audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py"
)

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
EXPECTED_UNKNOWN = {
    "finite_generic_negative_y_embedded_p3",
    "finite_half_centre_negative_y_embedded_p3",
    "infinity_lower_pair_embedded_p3",
}


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


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def original_wall_bases(c1, c2, xi, upsilon):
    """Return the exact wall orientation with active word 1110."""
    e = (1, 0, 0, 0)
    lower = (0, c1, -c2, 0)
    upper = (0, c1, c2, 0)
    free = (xi, upsilon * c1, upsilon * c2, 1)
    alpha = (lower, e, e, e)
    beta = (free, lower, lower, upper)
    return alpha, beta


def standard_marking_bases(c1, c2, xi, upsilon, markings):
    """Swap the U3 basis internally, then mark beta_i -> beta_i+h_i alpha_i."""
    original_alpha, original_beta = original_wall_bases(c1, c2, xi, upsilon)
    alpha = original_alpha[:3] + (original_beta[3],)
    unmarked_beta = original_beta[:3] + (original_alpha[3],)
    beta = tuple(
        tuple(
            sp.expand(unmarked_beta[i][j] + markings[i] * alpha[i][j])
            for j in range(4)
        )
        for i in range(4)
    )
    return alpha, beta


def tensor_coefficients(alpha, beta):
    return {
        word: permanent4(
            tuple(beta[i] if word[i] else alpha[i] for i in range(4))
        )
        for word in WORDS4
    }


def project(row, extension, direction, rho, sigma):
    if direction == "D01":
        return (rho * row[0] + sigma * row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], rho * row[2] + sigma * row[3], extension)
    raise ValueError(direction)


def all_alpha_data(alpha, extensions, direction, rho, sigma):
    rows = tuple(
        project(alpha[i], extensions[i], direction, rho, sigma) for i in range(4)
    )
    diagonal = permanent4(rows)
    cofactors = tuple(
        permanent3(tuple(rows[j][:3] for j in range(4) if j != i))
        for i in range(4)
    )
    assert sp.expand(diagonal - sum(extensions[i] * cofactors[i] for i in range(4))) == 0
    return rows, sp.expand(diagonal), tuple(sp.factor(value) for value in cofactors)


def verify_ledger_and_certificate():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    unknown = {
        entry["id"] for entry in ledger["strata"] if entry["h22_status"] == "UNKNOWN"
    }
    assert unknown == EXPECTED_UNKNOWN
    by_id = {entry["id"]: entry for entry in ledger["strata"]}
    assert all(by_id[key]["normal_support_mask"] == 6 for key in EXPECTED_UNKNOWN)

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["claim_label"] == "VERIFIED"
    assert {entry["id"] for entry in certificate["actual_families"]} == EXPECTED_UNKNOWN
    for family in certificate["actual_families"]:
        flags = family["flags"]
        assert len(flags) == 4
        assert {(entry["first"], entry["second"]) for entry in flags} == {
            (0, 0), (1, 0), (0, 1), (1, 1)
        }
    assert certificate["certificate"]["homogeneous_weight_coverage"] == [
        "[0:1]", "[1:0]", "rho*sigma!=0"
    ]
    return ledger, certificate


def main():
    ledger, certificate = verify_ledger_and_certificate()
    c1, c2, xi, upsilon, rho, sigma = sp.symbols(
        "c1 c2 xi upsilon rho sigma"
    )
    markings = sp.symbols("h0:4")
    extensions = sp.symbols("x0:4")

    original_alpha, original_beta = original_wall_bases(c1, c2, xi, upsilon)
    original_coefficients = tensor_coefficients(original_alpha, original_beta)
    assert {
        word: sp.factor(value)
        for word, value in original_coefficients.items()
        if value != 0
    } == {(1, 1, 1, 0): -2 * c1 * c2}

    alpha, beta = standard_marking_bases(c1, c2, xi, upsilon, markings)
    marked_coefficients = tensor_coefficients(alpha, beta)
    assert {
        word: sp.factor(value)
        for word, value in marked_coefficients.items()
        if value != 0
    } == {(1, 1, 1, 1): -2 * c1 * c2}

    d01_rows, d01_diagonal, d01_cofactors = all_alpha_data(
        alpha, extensions, "D01", rho, sigma
    )
    d23_rows, d23_diagonal, d23_cofactors = all_alpha_data(
        alpha, extensions, "D23", rho, sigma
    )
    assert d01_diagonal == 0
    assert d23_diagonal == 0
    assert d01_cofactors == (0, 0, 0, 0)
    assert d23_cofactors == (0, 0, 0, 0)

    # D01 has a literal zero C target column on all transverse alpha rows.
    assert all(row[2] == 0 for row in d01_rows)
    # At the rho=0 endpoint D23 has a literal zero merged target column.
    assert all(sp.expand(row[2].subs(rho, 0)) == 0 for row in d23_rows)
    # The other endpoint and the open torus are included by the same identity.
    assert d23_diagonal.subs({rho: 1, sigma: 0}) == 0
    assert d23_diagonal.subs({rho: 1, sigma: 1}) == 0

    result = {
        "status": "pass",
        "role": "construction",
        "claim_label": "VERIFIED",
        "git_commit": git_commit(),
        "scope": certificate["scope"],
        "inputs": {
            LEDGER.name: sha256(LEDGER),
            P4_WALL.name: sha256(P4_WALL),
            H22_DEFINITION.name: sha256(H22_DEFINITION),
            VERIFICATION_REPORT.name: sha256(VERIFICATION_REPORT),
            INDEPENDENT_VERIFIER.name: sha256(INDEPENDENT_VERIFIER),
        },
        "method": certificate["method"],
        "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            CERTIFICATE.name: sha256(CERTIFICATE),
            REPORT.name: sha256(REPORT),
        },
        "ledger_unknown_strata": sorted(EXPECTED_UNKNOWN),
        "actual_family_flag_counts": {
            entry["id"]: len(entry["flags"])
            for entry in certificate["actual_families"]
        },
        "original_pure_support": {"1110": str(-2 * c1 * c2)},
        "standard_marking_pure_support": {"1111": str(-2 * c1 * c2)},
        "D01_all_alpha_cofactors": [str(value) for value in d01_cofactors],
        "D23_all_alpha_cofactors": [str(value) for value in d23_cofactors],
        "D01_all_alpha_diagonal": str(d01_diagonal),
        "D23_all_alpha_diagonal": str(d23_diagonal),
        "both_weighted_directions_never_binary": True,
        "actual_mask6_strata_obstructed": True,
        "finite_field_computation_used": False,
        "broad_grid_used": False,
        "projective_transport_used": False,
        "independent_verifier_complete": True,
        "limitations": certificate["limitations"],
        "ledger_sha256": sha256(LEDGER),
        "ledger_claim_label_before_this_candidate": ledger["claim_label"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
