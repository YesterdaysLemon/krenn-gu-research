#!/usr/bin/env python3
"""Independent DP-permanent audit of the endpoint t3=1 divisor."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp


for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])
expose_claim_package(REPO_ROOT, "claims/p5/h31/elliptic-end-genus-two-exception")

from audit_p5_h31_elliptic_end_genus_two_exception import permanent_dp
from verify_p5_h31_elliptic_end_t3_divisor import (
    ROOT,
    THEOREM,
    verify_endpoint,
)


PRIMARY = ROOT / "verify_p5_h31_elliptic_end_t3_divisor.py"
Q3_AUDIT = REPO_ROOT / 'claims/p5/h31/elliptic-end-t3-divisor-q3/audit_p5_h31_elliptic_end_t3_divisor_q3.py'
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dp_system_builder(distinguished, alpha, beta):
    extension = sp.symbols("a0:4") + sp.symbols("b0:4")
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_extended = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extension[mode],)
        for mode, row in enumerate(alpha)
    )
    beta_extended = tuple(
        tuple(row[coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode, row in enumerate(beta)
    )
    coefficients = {
        word: permanent_dp(tuple(
            beta_extended[mode] if word[mode] else alpha_extended[mode]
            for mode in range(4)
        ))
        for word in WORDS
    }
    rows = {
        word: [sp.diff(coefficients[word], variable) for variable in extension]
        for word in WORDS
    }
    mixed = sp.Matrix([
        rows[word]
        for word in WORDS
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])
    return (
        mixed,
        sp.Matrix([rows[(0, 0, 0, 0)]]),
        sp.Matrix([rows[(1, 1, 1, 1)]]),
    )


def main() -> None:
    q0 = verify_endpoint(0, 1, dp_system_builder)
    q3_completed = subprocess.run(
        [sys.executable, str(Q3_AUDIT)],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=360,
    )
    if q3_completed.returncode != 0:
        raise AssertionError(
            (
                "independent q=3 audit failed",
                q3_completed.stdout,
                q3_completed.stderr,
            )
        )
    q3 = json.loads(q3_completed.stdout)
    assert q3["audited"] is True
    assert q3["binary_survivor_on_regular_t3_divisor"] is False

    primary_completed = subprocess.run(
        [sys.executable, str(PRIMARY)],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=600,
    )
    if primary_completed.returncode != 0:
        raise AssertionError(
            (
                "primary verifier failed",
                primary_completed.stdout,
                primary_completed.stderr,
            )
        )
    primary_output = json.loads(primary_completed.stdout)
    assert primary_output["verified"] is True
    assert primary_output["whole_regular_t3_divisor_closed"] is True

    output = {
        "audited": True,
        "field": "C",
        "independent_permanent": "subset dynamic programming",
        "distinguished_coordinates": [0, 3],
        "marking_divisor": "t3=1",
        "q0": q0,
        "q3": q3,
        "whole_regular_t3_divisor_closed": True,
        "primary_replay_verified": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "q3_audit": Q3_AUDIT.name,
        "q3_audit_sha256": sha256(Q3_AUDIT),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_elliptic_end_t3_divisor_audited.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
