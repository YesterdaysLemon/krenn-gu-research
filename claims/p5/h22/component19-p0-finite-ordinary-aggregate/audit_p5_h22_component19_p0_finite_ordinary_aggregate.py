#!/usr/bin/env python3
"""Aggregate verifier for the finite ordinary p=0 component-19 divisor."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md"

ARTIFACTS = {
    "generic_open": (
        "claims/p5/h22/component19-p0-ordinary-obstruction-open/audit_p5_h22_component19_p0_ordinary_obstruction_open.py",
        "claims/p5/h22/component19-p0-ordinary-obstruction-open/P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md",
        "q*phi*(q-phi)*(q^2-1)*(phi^2-1)*((q*phi)^2-1)!=0",
    ),
    "qphi_equals_one": (
        "claims/p5/h22/component19-p0-qphi-one-independent/audit_p5_h22_component19_p0_qphi_equals_one.py",
        "claims/p5/h22/component19-p0-qphi-one-independent/P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md",
        "q*phi=1",
    ),
    "qphi_minus_one_axes": (
        "claims/p5/h22/component19-p0-qphi-minus-one-axes/audit_p5_h22_component19_p0_qphi_minus_one_axes.py",
        "claims/p5/h22/component19-p0-qphi-minus-one-axes/P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md",
        "q*phi=-1",
    ),
    "qphi_minus_one_axis_compatibility": (
        "claims/p5/h22/component19-p0-qphi-minus-one-ternary-compatibility/audit_p5_h22_component19_p0_qphi_minus_one_ternary_compatibility.py",
        "claims/p5/h22/component19-p0-qphi-minus-one-ternary-compatibility/P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_TERNARY_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md",
        "q=-1/phi",
    ),
    "qphi_minus_one_phi_crossings": (
        "claims/p5/h22/component19-p0-qphi-minus-one-phi-endpoints/audit_p5_h22_component19_p0_qphi_minus_one_phi_endpoints.py",
        "claims/p5/h22/component19-p0-qphi-minus-one-phi-endpoints/P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_PHI_ENDPOINTS_VERIFICATION.md",
        "phi^2=1",
    ),
    "qphi_minus_one_infinity": (
        "claims/p5/h22/component19-p0-qphim1-infinity-no-import/audit_p5_h22_component19_p0_qphim1_infinity_no_import.py",
        "claims/p5/h22/component19-p0-qphim1-infinity-no-import/P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md",
        "weight-at-infinity",
    ),
    "q_endpoints": (
        "claims/p5/h22/component19-p0-q-endpoints-no-import/audit_p5_h22_component19_p0_q_endpoints_no_import.py",
        "claims/p5/h22/component19-p0-q-endpoints-no-import/P5_H22_COMPONENT19_P0_Q_ENDPOINTS_NO_IMPORT_VERIFICATION.md",
        "q=+/-1",
    ),
    "phi_endpoints": (
        "claims/p5/h22/component19-p0-phi-endpoints-no-import/audit_p5_h22_component19_p0_phi_endpoints_no_import.py",
        "claims/p5/h22/component19-p0-phi-endpoints-no-import/P5_H22_COMPONENT19_P0_PHI_ENDPOINTS_NO_IMPORT_VERIFICATION.md",
        "phi=+/-1",
    ),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit():
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def replay_verified_artifacts():
    records = {}
    for label, (script_name, report_name, scope_snippet) in ARTIFACTS.items():
        script = REPO_ROOT / script_name
        report = REPO_ROOT / report_name
        text = report.read_text(encoding="utf-8")
        assert "claim_label: VERIFIED" in text, report_name
        assert scope_snippet in text, (report_name, scope_snippet)
        started = time.perf_counter()
        completed = subprocess.run(
            (sys.executable, str(script)),
            cwd=REPO_ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=300,
            check=False,
        )
        elapsed = time.perf_counter() - started
        if completed.returncode != 0:
            raise RuntimeError(
                f"replay failed for {script_name}:\n{completed.stdout}\n{completed.stderr}"
            )
        records[label] = {
            "script": script_name,
            "script_sha256": sha256(script),
            "report": report_name,
            "report_sha256": sha256(report),
            "report_claim_label": "VERIFIED",
            "replay_returncode": 0,
            "replay_seconds": round(elapsed, 3),
        }
    return records


def exact_set_theoretic_ledger():
    q, phi, cap_x, cap_z, cap_g = sp.symbols("q phi X Z G")

    identities = {
        "qphi_one_target_identity": (
            phi * (q - phi) - (1 - phi**2) - (q * phi - 1)
        ),
        "qphi_minus_one_target_identity": (
            phi * (q - phi) + (1 + phi**2) - (q * phi + 1)
        ),
        "q_endpoint_same_sign_identity": (
            (q - phi) - q * (1 - q * phi) - phi * (q**2 - 1)
        ),
        "q_endpoint_opposite_sign_identity": (
            (q + phi) - q * (1 + q * phi) + phi * (q**2 - 1)
        ),
        "phi_endpoint_same_sign_identity": (
            (q - phi) - phi * (q * phi - 1) + q * (phi**2 - 1)
        ),
        "phi_endpoint_opposite_sign_identity": (
            (q + phi) - phi * (q * phi + 1) + q * (phi**2 - 1)
        ),
        "double_endpoint_identity": (
            (q * phi) ** 2 - 1 - phi**2 * (q**2 - 1) - (phi**2 - 1)
        ),
    }
    assert all(sp.expand(value) == 0 for value in identities.values())

    r = q - phi
    generic_m0 = (
        64
        * cap_z
        * (phi**2 - 1)
        * (2 * phi * cap_x + (phi * q + 1) * cap_z)
        * cap_g
        / r**2
    )
    off_axis_minus_one = sp.factor(generic_m0.subs(q, -1 / phi))
    expected_off_axis = (
        128
        * cap_x
        * cap_z
        * cap_g
        * phi**3
        * (phi**2 - 1)
        / (phi**2 + 1) ** 2
    )
    assert sp.cancel(off_axis_minus_one - expected_off_axis) == 0

    cases = [
        {
            "case": "generic_open",
            "condition": "(q^2-1)*(phi^2-1)*((q*phi)^2-1)!=0",
            "certificate": "generic_open",
        },
        {
            "case": "qphi_equals_one",
            "condition": "q*phi=1; target q!=phi implies phi^2!=1",
            "certificate": "qphi_equals_one",
        },
        {
            "case": "qphi_minus_one_regular_off_axis",
            "condition": (
                "q*phi=-1, phi^2!=1,-1, X*Z!=0; fixed M0 is nonzero"
            ),
            "certificate": "generic_open exact M0 identity",
        },
        {
            "case": "qphi_minus_one_regular_axes",
            "condition": (
                "q*phi=-1, phi^2!=1,-1, X*Z=0; genuine F*H!=0 excludes X=Z=0"
            ),
            "certificate": (
                "qphi_minus_one_axes plus qphi_minus_one_axis_compatibility"
            ),
        },
        {
            "case": "qphi_minus_one_phi_crossings",
            "condition": "q*phi=-1, phi^2=1; full Y=0 survivor sheet included",
            "certificate": "qphi_minus_one_phi_crossings",
        },
        {
            "case": "q_endpoints_away_from_qphi_pm_one",
            "condition": "q^2=1, (q*phi)^2!=1; then phi*(phi^2-1)!=0",
            "certificate": "q_endpoints",
        },
        {
            "case": "phi_endpoints_away_from_qphi_pm_one",
            "condition": "phi^2=1, (q*phi)^2!=1; then q*(q^2-1)!=0",
            "certificate": "phi_endpoints",
        },
    ]
    return {
        "target": "q*phi*(q-phi)!=0",
        "generic_boundary_product": "(q^2-1)*(phi^2-1)*((q*phi)^2-1)",
        "polynomial_identities_verified": list(identities),
        "qphi_minus_one_off_axis_M0": str(off_axis_minus_one),
        "cases": cases,
        "coverage_complete": True,
        "qphi_minus_one_zero_base_exclusion": (
            "phi^2=-1 implies q=-1/phi=phi, hence q=phi and is outside target"
        ),
        "double_endpoint_split": (
            "q^2=phi^2=1 forces q*phi=+/-1; +1 is q=phi zero base, "
            "-1 is the verified crossing"
        ),
        "weight_chart_coverage": {
            "finite": "all seven parameter cases above",
            "infinity_generic_and_other_exceptional_divisors": (
                "covered inside the generic, qphi=1, q-endpoint, and phi-endpoint replays"
            ),
            "infinity_qphi_minus_one": "qphi_minus_one_infinity",
            "ordinary_projective_weight_line_complete": True,
        },
    }


def main():
    replays = replay_verified_artifacts()
    ledger = exact_set_theoretic_ledger()
    script = Path(__file__).resolve()
    outputs = {script.name: sha256(script)}
    if REPORT.exists():
        outputs[REPORT.name] = sha256(REPORT)
    result = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "set-theoretic exhaustion of the complete projective weighted fibre "
            "over the ordinary nonzero all-pair-open component-19 p=0 divisor "
            "q*phi*(q-phi)!=0"
        ),
        "inputs": {
            item["report"]: item["report_sha256"] for item in replays.values()
        },
        "method": (
            "live replay of eight verified exact certificates plus an exact "
            "polynomial-identity case ledger for every exceptional intersection"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/component19-p0-finite-ordinary-aggregate/audit_p5_h22_component19_p0_finite_ordinary_aggregate.py'
        ),
        "outputs": outputs,
        "limitations": (
            "ordinary nonzero all-pair-open p=0 base only; q=phi zero base, "
            "q=0 or phi=0 lower-pair boundaries, projectivized or valuative base "
            "directions, other components, arbitrary-order reduction, and the "
            "global conjecture are not claimed"
        ),
        "replays": replays,
        "set_theoretic_ledger": ledger,
        "finite_ordinary_divisor_exhausted": True,
        "ordinary_projective_weight_fibre_exhausted": True,
        "remaining_unknown_inside_scope": None,
        "excluded_boundaries": {
            "q_equals_phi": (
                "ordinary restriction T1111=4*(q-phi) is zero; projective normal "
                "and valuative directions remain outside this aggregate"
            ),
            "q_equals_zero_or_phi_equals_zero": (
                "at least one P4 pair has rank below three; lower-pair boundary "
                "not included in the all-pair-open target"
            ),
        },
        "finite_field_computation_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
