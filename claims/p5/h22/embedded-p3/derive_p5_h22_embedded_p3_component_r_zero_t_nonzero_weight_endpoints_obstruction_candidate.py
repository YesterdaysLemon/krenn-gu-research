#!/usr/bin/env python3
"""Exact construction replay for the two t0 != 0 homogeneous H22 endpoints.

This is deliberately standalone: it reconstructs both contractions in the
original source coordinates and imports no discovery or verification code.
"""

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
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / (
    "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_"
    "ENDPOINTS_OBSTRUCTION_CANDIDATE.md"
)
SOURCE = ROOT / "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION_CANDIDATE.md"
H31_NOTE = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md"
)
H31_VERIFIER = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/verify_p5_h31_embedded_p3_component_r_zero_boundary.py"
)
VERIFICATION_REPORT = ROOT / (
    "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_"
    "ENDPOINTS_VERIFICATION.md"
)
INDEPENDENT_VERIFIER = ROOT / (
    "audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_"
    "weight_endpoints_verifier.py"
)

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
MIXED4 = WORDS4[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


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


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(
        sum(
            rows[0][columns[p[0]]]
            * rows[1][columns[p[1]]]
            * rows[2][columns[p[2]]]
            for p in PERMUTATIONS3
        )
    )


def bases(cap_s, cap_u, t0, markings):
    """The free-plane r0=0 component bases in original coordinates."""
    alpha = (
        (0, 1, cap_s, cap_u),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    canonical_beta = (
        (1, 0, 0, t0),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    beta = tuple(
        tuple(
            sp.expand(canonical_beta[i][j] + markings[i] * alpha[i][j])
            for j in range(4)
        )
        for i in range(4)
    )
    return alpha, beta


def project(row, extension, direction):
    """Reconstruct the four endpoint maps without affine-weight division."""
    if direction == "D01_zero":       # [rho:sigma] = [0:1]
        return (row[1], row[2], row[3], extension)
    if direction == "D23_zero":       # [rho:sigma] = [0:1]
        return (row[0], row[1], row[3], extension)
    if direction == "D01_infinity":   # [rho:sigma] = [1:0]
        return (row[0], row[2], row[3], extension)
    if direction == "D23_infinity":   # [rho:sigma] = [1:0]
        return (row[0], row[1], row[2], extension)
    if direction == "delete0":
        return (row[1], row[2], row[3], extension)
    raise ValueError(direction)


def model(cap_s, cap_u, t0, markings, extensions, direction):
    alpha, beta = bases(cap_s, cap_u, t0, markings)
    alpha_rows = tuple(
        project(alpha[i], extensions[i], direction) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extensions[4 + i], direction) for i in range(4)
    )
    coefficients = {}
    for word in WORDS4:
        selected = tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        )
        # Expand the 4x4 permanent along the extension column.
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], value) for value in extensions]
            for word in MIXED4
        ]
    )
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "mixed": mixed,
        "A": coefficients[WORDS4[0]],
        "B": coefficients[WORDS4[-1]],
    }


def main():
    cap_s, cap_u, t0 = sp.symbols("S U t0")
    markings = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")

    d01_zero = model(cap_s, cap_u, t0, markings, extensions, "D01_zero")
    d23_zero = model(cap_s, cap_u, t0, markings, extensions, "D23_zero")
    d01_infinity = model(
        cap_s, cap_u, t0, markings, extensions, "D01_infinity"
    )
    d23_infinity = model(
        cap_s, cap_u, t0, markings, extensions, "D23_infinity"
    )
    deletion_zero = model(cap_s, cap_u, t0, markings, extensions, "delete0")

    # The finite endpoint D01 contraction is literally deletion zero, not just
    # equivalent after a generic change of coordinates.
    for key in ("alpha_rows", "beta_rows", "coefficients", "mixed", "A", "B"):
        assert d01_zero[key] == deletion_zero[key]

    # At [0:1], D23 retains source coordinate zero as a separate target
    # coordinate.  Every alpha has zero there, so its all-alpha permanent has
    # an identically zero target column for every marking and extension.
    assert all(row[0] == 0 for row in d23_zero["alpha_rows"])
    assert sp.expand(d23_zero["A"]) == 0

    # At [1:0], both directions retain source coordinate zero separately.
    # Hence neither direction can have the two nonzero diagonals required of
    # the genuine binary slice in a weighted-H22 pair.
    assert all(row[0] == 0 for row in d01_infinity["alpha_rows"])
    assert all(row[0] == 0 for row in d23_infinity["alpha_rows"])
    assert sp.expand(d01_infinity["A"]) == 0
    assert sp.expand(d23_infinity["A"]) == 0

    # The signed source swap used by the exact H31 theorem preserves the
    # deletion-zero direction up to this invertible target sign/swap.  There
    # is only one direction here, so no shared-weight mismatch is introduced.
    x0, x1, x2, x3, e = sp.symbols("x0 x1 x2 x3 e")
    source_swapped = (x0, x1, -x3, -x2)
    projected_after_swap = project(source_swapped, e, "delete0")
    projected_before_swap = project((x0, x1, x2, x3), e, "delete0")
    target_signed_swap = (
        projected_before_swap[0],
        -projected_before_swap[2],
        -projected_before_swap[1],
        projected_before_swap[3],
    )
    assert projected_after_swap == target_signed_swap

    payload = {
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "embedded-P3 free-plane r0=0, t0!=0 weighted-H22 fibres at "
            "[rho:sigma]=[0:1] and [1:0]"
        ),
        "inputs": {
            SOURCE.name: sha256(SOURCE),
            H31_NOTE.name: sha256(H31_NOTE),
            H31_VERIFIER.name: sha256(H31_VERIFIER),
            VERIFICATION_REPORT.name: sha256(VERIFICATION_REPORT),
            INDEPENDENT_VERIFIER.name: sha256(INDEPENDENT_VERIFIER),
        },
        "method": (
            "exact characteristic-zero reconstruction in original coordinates; "
            "structural zero-column obstructions; coefficientwise identity with "
            "the verified deletion-zero H31 model"
        ),
        "command": f"uv run --with sympy python {SCRIPT.relative_to(REPO_ROOT).as_posix()}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
        },
        "endpoint_0_1": {
            "D23_all_alpha_diagonal": str(d23_zero["A"]),
            "D01_equals_deletion_zero": True,
            "obstruction": (
                "D23 cannot be binary, so D01 would have to be binary; the "
                "exact verified direction-local H31 obstruction excludes its "
                "required local lift"
            ),
        },
        "endpoint_1_0": {
            "D01_all_alpha_diagonal": str(d01_infinity["A"]),
            "D23_all_alpha_diagonal": str(d23_infinity["A"]),
            "obstruction": "neither direction can be a genuine binary slice",
        },
        "signed_swap_deletion_zero_target_equivalence": True,
        "both_endpoint_fibres_obstructed": True,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": True,
        "limitations": (
            "VERIFIED only for the two stated endpoint fibres after a fresh "
            "no-import audit; [0:1] depends on the separately replayed exact H31 "
            "theorem; no component-exhaustiveness, arbitrary-order, prize-graph, "
            "or global Krenn-Gu conclusion"
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
