"""Fail-closed audit of the final six-vertex certificate chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_CNF_SHA256 = (
    "154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7"
)
EXPECTED_PROOF_SHA256 = (
    "9273c872b3aa071e67b3ff176d84c50d104e212bcab38980be38de69f9ffb1d1"
)
EXPECTED_PROOF_BYTES = 86_426_936


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_json_verified(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload.get("verified"):
        raise AssertionError(f"manifest is not verified: {path}")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/six_vertex_final_audit.json"),
    )
    args = parser.parse_args()
    base = args.base.resolve()
    tmp = base / "tmp"

    cnf = (
        tmp
        / "global_candidate_pattern18_unnormalized_certified_symbreak.cnf"
    )
    cnf_hash = sha256(cnf)
    if cnf_hash != EXPECTED_CNF_SHA256:
        raise AssertionError(f"final CNF hash mismatch: {cnf_hash}")

    solver_files = [
        tmp / "global_candidate_pattern18_symbreak_cadical.json",
        tmp / "global_candidate_pattern18_symbreak_glucose.json",
        tmp / "global_candidate_pattern18_symbreak_maple.json",
        tmp
        / "global_candidate_pattern18_corrected_symbreak_cadical.json",
    ]
    solver_rows = []
    for path in solver_files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload["status"] != "UNSAT":
            raise AssertionError(f"solver did not return UNSAT: {path}")
        referenced_cnf = base / str(payload["cnf"])
        referenced_hash = sha256(referenced_cnf)
        if referenced_hash != EXPECTED_CNF_SHA256:
            raise AssertionError(
                f"solver used a different CNF: {path}"
            )
        solver_rows.append(
            {
                "solver": payload["solver"],
                "result": str(path.relative_to(base)),
                "elapsed_seconds": payload["elapsed_seconds"],
                "cnf_sha256": referenced_hash,
            }
        )

    external_log = (
        tmp / "global_candidate_pattern18_final_cadical195.log"
    )
    proof = tmp / "global_candidate_pattern18_final_cadical195.drat"
    drat_log = (
        tmp / "global_candidate_pattern18_final_drat_trim_verified.log"
    )
    external_text = external_log.read_text(encoding="utf-8")
    if "s UNSATISFIABLE" not in external_text:
        raise AssertionError("external CaDiCaL log is not UNSAT")
    drat_text = drat_log.read_text(encoding="utf-8")
    if "s VERIFIED" not in drat_text:
        raise AssertionError("drat-trim did not verify the proof")
    proof_hash = sha256(proof)
    if proof_hash != EXPECTED_PROOF_SHA256:
        raise AssertionError(f"final DRAT proof hash mismatch: {proof_hash}")
    if proof.stat().st_size != EXPECTED_PROOF_BYTES:
        raise AssertionError(
            f"final DRAT proof size mismatch: {proof.stat().st_size}"
        )

    pattern_replay = require_json_verified(
        tmp
        / "global_pattern_orbits_unnormalized_linear_verified_glucose.json"
    )
    pattern_manifest = (
        tmp / "global_pattern_orbits_unnormalized_linear_certified.json"
    )
    if pattern_replay["manifest_sha256"] != sha256(pattern_manifest):
        raise AssertionError("linear pattern manifest hash changed")
    old_pattern_manifest = json.loads(
        (
            tmp
            / "global_pattern_orbits_unnormalized_cadical_detailed.json"
        ).read_text(encoding="utf-8")
    )
    new_pattern_manifest = json.loads(
        pattern_manifest.read_text(encoding="utf-8")
    )
    old_patterns = sorted(
        tuple(tuple(map(int, neighbours)) for neighbours in row["pattern"])
        for row in old_pattern_manifest["rows"]
    )
    new_patterns = sorted(
        tuple(tuple(map(int, neighbours)) for neighbours in row["pattern"])
        for row in new_pattern_manifest["rows"]
    )
    if old_patterns != new_patterns:
        raise AssertionError("linear upgrade changed the pattern orbit set")
    prism_partition = require_json_verified(
        tmp / "prism_gauge_partition_verified.json"
    )
    m10_partition = require_json_verified(
        tmp / "m10_gauge_partition_verified.json"
    )

    k33_results = sorted(tmp.glob("k33_orbit_*.result"))
    if len(k33_results) != 48:
        raise AssertionError(
            f"expected 48 K3,3 results, found {len(k33_results)}"
        )
    if any(
        path.read_text(encoding="ascii").strip() != "UNSAT"
        for path in k33_results
    ):
        raise AssertionError("a K3,3 result is not UNSAT")
    k33_proofs = sorted(tmp.glob("k33_orbit_*.drat"))
    if len(k33_proofs) != 48 or any(
        path.stat().st_size == 0 for path in k33_proofs
    ):
        raise AssertionError("K3,3 DRAT proof set is incomplete")
    k33_audit = require_json_verified(
        tmp / "k33_drat_trim_audit.json"
    )
    if int(k33_audit["orbits"]) != 48:
        raise AssertionError("K3,3 DRAT audit count mismatch")

    result = {
        "verified": True,
        "claim": "no complex six-vertex witness with d >= 3",
        "cnf": str(cnf.relative_to(base)),
        "cnf_sha256": cnf_hash,
        "variables": 66_152,
        "clauses": 339_096,
        "solver_results": solver_rows,
        "external_solver": "cadical-1.9.5",
        "external_log": str(external_log.relative_to(base)),
        "proof": str(proof.relative_to(base)),
        "proof_sha256": proof_hash,
        "proof_bytes": proof.stat().st_size,
        "drat_trim_log": str(drat_log.relative_to(base)),
        "drat_trim_log_sha256": sha256(drat_log),
        "pattern_orbits": pattern_replay["pattern_orbits"],
        "pattern_laurent_certificates": pattern_replay[
            "laurent_certificates"
        ],
        "pattern_exact_fallbacks": pattern_replay["exact_fallbacks"],
        "prism_gauge_full": prism_partition["gauge_full"],
        "prism_gauge_deficient": prism_partition["gauge_deficient"],
        "m10_gauge_full": m10_partition["gauge_full"],
        "m10_gauge_deficient": m10_partition["gauge_deficient"],
        "k33_support_orbits": len(k33_results),
    }
    output = (
        args.output
        if args.output.is_absolute()
        else base / args.output
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {output}: verified=True "
        f"cnf_sha256={cnf_hash}"
    )


if __name__ == "__main__":
    main()
