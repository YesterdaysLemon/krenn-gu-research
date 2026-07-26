"""Replay the C4+C4+C6 certificate excluding first-factor orbit 5."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF


BASE_V3_SHA256 = (
    "5c798fdb3a7e5b16aeebbab7670e57dd"
    "cc6838cf461bf747da98fd9a5453facc"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v4_orbit5_augmentation.json"
        ),
    )
    parser.add_argument(
        "--augmentation-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v4_orbit5_augmentation_verified.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit5_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit5_kissat.drat"
        ),
    )
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=Path("tmp/drat-trim/drat-trim"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit5_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    augmentation = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    stored_audit = json.loads(
        args.augmentation_audit.read_text(encoding="utf-8")
    )
    base_cnf = Path(augmentation["base_cnf"])
    global_cnf = Path(augmentation["output_cnf"])
    prerequisite = augmentation["three_connectivity_prerequisite"]
    prerequisite_manifest = Path(prerequisite["augmentation"])
    prerequisite_audit = Path(prerequisite["audit"])
    if (
        augmentation.get("status")
        != "minimum_activity_rules_augmented"
        or augmentation.get("partition") != [4, 4, 6]
        or augmentation.get("certificates_replayed") != 96
        or augmentation.get("new_transport_clauses") != 4720
        or sha256(base_cnf) != BASE_V3_SHA256
        or augmentation.get("base_cnf_sha256") != BASE_V3_SHA256
        or stored_audit.get("verified") is not True
        or stored_audit.get("augmentation_sha256")
        != sha256(args.augmentation)
        or prerequisite.get("base_extension_clauses") != 5856
        or sha256(prerequisite_manifest)
        != prerequisite["augmentation_sha256"]
        or sha256(prerequisite_audit)
        != prerequisite["audit_sha256"]
    ):
        raise AssertionError("orbit-5 augmentation chain changed")

    recheck_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit5_"
        "augmentation_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.augmentation),
            "--output",
            str(recheck_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    recheck = json.loads(recheck_path.read_text(encoding="utf-8"))
    if (
        recheck.get("verified") is not True
        or recheck.get("certificates_replayed") != 96
        or recheck.get("new_transport_clauses") != 4720
        or recheck.get("sat") is not True
    ):
        raise AssertionError("orbit-5 augmentation replay changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [237]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the global CNF plus selector 237"
        )

    drat_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit5_"
        "final_drat_trim_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            "run_drat_trim.py",
            "--drat-trim",
            str(args.drat_trim),
            "--cnf",
            str(args.conditioned_cnf),
            "--proof",
            str(args.proof),
            "--stdout",
            "tmp/fourteen_vertex_c4_c4_c6_orbit5_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_orbit5_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_path),
            "--forward",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    drat = json.loads(drat_path.read_text(encoding="utf-8"))
    if drat.get("verified") is not True:
        raise AssertionError("orbit-5 DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C4+C4+C6_first_factor_orbit_5_excluded",
        "scope": (
            "order-14 equality architecture with full factor C4+C4+C6, "
            "skeleton vertex connectivity at least 3, and pinned first "
            "singleton factor orbit 5"
        ),
        "minimal_counterexample_relevance": (
            "a minimal Krenn-Gu counterexample must be 4-connected "
            "(Chandran-Gajjala-Illickan, arXiv:2407.00303)"
        ),
        "base_v3_cnf": str(base_cnf),
        "base_v3_cnf_sha256": sha256(base_cnf),
        "orbit5_certificates_replayed": 96,
        "orbit5_new_transport_clauses": 4720,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "excluded_first_factor_orbit": 5,
        "selector_clause": selector_clause,
        "conditioned_cnf": str(args.conditioned_cnf),
        "conditioned_cnf_sha256": sha256(args.conditioned_cnf),
        "conditioned_cnf_clauses": len(conditioned_formula.clauses),
        "proof": str(args.proof),
        "proof_sha256": sha256(args.proof),
        "proof_bytes": args.proof.stat().st_size,
        "drat_trim_verified": True,
        "elapsed_seconds": time.perf_counter() - started,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
