#!/usr/bin/env python3
"""Verify the packaged non-unimodular P5 Laurent boundary artifacts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
BOUNDARY = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "nonunimodular_boundary"
)
CONVERTER = ROOT / "tmp" / "convert_p5_singular_to_msolve.py"
AUDITOR = ROOT / "tmp" / "audit_p5_coordinate_support_ledger.py"
LEDGER = BOUNDARY / "focused_ledger.json"

CASES = (
    {
        "indices": (4199, 1974, 272, 214, 2803),
        "pivot_determinant": 2,
        "relation_equations": 10,
        "source_sha256": (
            "c250024370e0895d7bdad363e3c1d166c6b1b47ba87a6ceff32bca8c50a8a1c9"
        ),
        "msolve_input_sha256": (
            "0a1d10b7bc71483e060a181387b84567b638045c8fd429206f6a94f4da23889c"
        ),
    },
    {
        "indices": (4199, 1974, 266, 4272, 2803),
        "pivot_determinant": -2,
        "relation_equations": 11,
        "source_sha256": (
            "ace19f72aca232e37d8b835b756b02e8b73b99fc6122fa0aba96790db4e5e462"
        ),
        "msolve_input_sha256": (
            "32d7e8bd03ac6f3f32231c758702fc41b3b9606f9cf3f730140186d1f5de4b81"
        ),
    },
    {
        "indices": (4199, 1974, 266, 232, 2803),
        "pivot_determinant": -2,
        "relation_equations": 10,
        "source_sha256": (
            "934d303c3826457aa197ff700de143c187595892496f1b8bcab333414a35ed51"
        ),
        "msolve_input_sha256": (
            "c889f9880e3cab6bddd40b6d70c0114853bb9e7ed2edae86d4438fa4f80cac60"
        ),
    },
)

UNIT_LOG_SHA256 = (
    "0974a6369609c6077c8151dd9209fd59621304c15ebdde10a065d7d1bf6c0a36"
)
MSOLVE_UNIT_SHA256 = (
    "0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490"
)
LEDGER_SHA256 = (
    "c106ccbb600ee5a44086e65d7a27191582bd2d8d91b8989bd4e4f9fd60923a2f"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_unit_log(path: Path) -> None:
    if path.read_text(encoding="utf-8").strip() != "UNIT_IDEAL":
        raise AssertionError(f"{path} is not a Singular unit-ideal log")
    if sha256(path) != UNIT_LOG_SHA256:
        raise AssertionError(f"{path} has an unexpected byte representation")


def semantic_ledger_audit() -> dict:
    env = os.environ.copy()
    dependency_path = str(ROOT / "tmp" / "python_deps")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        dependency_path + os.pathsep + existing if existing else dependency_path
    )
    completed = subprocess.run(
        [sys.executable, str(AUDITOR), str(LEDGER)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if completed.returncode:
        raise AssertionError(
            "focused ledger semantic audit failed:\n"
            + completed.stdout
            + completed.stderr
        )
    payload = json.loads(completed.stdout)
    if (
        payload.get("status") != "AUDIT_PASS"
        or payload.get("records") != 3
        or payload.get("unique_base_clauses") != 3
        or payload.get("modes") != {"singular_unit_ideal": 3}
        or payload.get("replay_scopes")
        != {"exact_recorded_mechanism": 3}
    ):
        raise AssertionError(f"unexpected focused audit payload: {payload}")
    return payload


def main() -> None:
    if sha256(LEDGER) != LEDGER_SHA256:
        raise AssertionError("focused ledger hash differs")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    records = ledger.get("learned_records", [])
    if len(records) != len(CASES):
        raise AssertionError("focused ledger does not contain three records")

    verified_cases = []
    with tempfile.TemporaryDirectory(prefix="p5-msolve-conversion-") as raw:
        temporary = Path(raw)
        for case, record in zip(CASES, records):
            indices = case["indices"]
            slug = "_".join(map(str, indices))
            slimgb_source = BOUNDARY / f"p5_signature_slimgb_{slug}.sing"
            slimgb_log = BOUNDARY / f"p5_signature_slimgb_{slug}.log"
            std_source = BOUNDARY / f"p5_signature_std_{slug}.sing"
            std_log = BOUNDARY / f"p5_signature_std_{slug}.log"
            packaged_input = BOUNDARY / f"p5_signature_slimgb_{slug}.ms"
            msolve_output = (
                BOUNDARY / f"p5_signature_slimgb_{slug}.msolve.out"
            )

            source_text = slimgb_source.read_text(encoding="utf-8")
            required_markers = (
                f"// signature source: {indices}",
                "// binomial handling: implicit saturated ideal",
                (
                    "// selected pivot determinant: "
                    f"{case['pivot_determinant']}"
                ),
                (
                    "// explicit binomial equations: "
                    f"{case['relation_equations']}"
                ),
                "z*(",
            )
            if any(marker not in source_text for marker in required_markers):
                raise AssertionError(
                    f"{slimgb_source} lacks an implicit-ideal marker"
                )
            if sha256(slimgb_source) != case["source_sha256"]:
                raise AssertionError(f"{slimgb_source} hash differs")

            std_text = std_source.read_text(encoding="utf-8")
            expected_std = source_text.replace(
                "ideal G=slimgb(I);", "ideal G=std(I);"
            )
            if expected_std != std_text:
                raise AssertionError(
                    "std and slimgb sources do not encode the same ideal"
                )
            assert_unit_log(slimgb_log)
            assert_unit_log(std_log)

            converted = temporary / f"{slug}.ms"
            conversion = subprocess.run(
                [
                    sys.executable,
                    str(CONVERTER),
                    str(slimgb_source),
                    str(converted),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if conversion.returncode:
                raise AssertionError(
                    f"msolve conversion failed: {conversion.stderr}"
                )
            if converted.read_bytes() != packaged_input.read_bytes():
                raise AssertionError(
                    f"reconverted msolve input differs for {indices}"
                )
            if sha256(packaged_input) != case["msolve_input_sha256"]:
                raise AssertionError(f"{packaged_input} hash differs")
            if (
                msolve_output.read_text(encoding="utf-8").strip() != "[-1]:"
                or sha256(msolve_output) != MSOLVE_UNIT_SHA256
            ):
                raise AssertionError(
                    f"{msolve_output} is not the packaged unit-ideal result"
                )

            certificate = record.get("certificate", {})
            if (
                tuple(certificate.get("signature_indices", ())) != indices
                or record.get("contradiction_mode") != "singular_unit_ideal"
                or len(record.get("clause", ())) != 5
                or any(literal >= 0 for literal in record["clause"])
            ):
                raise AssertionError(
                    f"focused ledger record differs for {indices}"
                )
            verified_cases.append(
                {
                    "signature_indices": indices,
                    "pivot_determinant": case["pivot_determinant"],
                    "relation_equations": case["relation_equations"],
                    "singular_algorithms": ["slimgb", "std"],
                    "msolve_result": "[-1]:",
                }
            )

    audit = semantic_ledger_audit()
    output = {
        "verified": True,
        "scope": "three reproduced non-unimodular P5 signature strata",
        "cases": verified_cases,
        "focused_ledger_sha256": LEDGER_SHA256,
        "semantic_audit": {
            "records": audit["records"],
            "unique_base_clauses": audit["unique_base_clauses"],
            "replay_scopes": audit["replay_scopes"],
        },
        "global_conjecture_resolved": False,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
