"""Replay the C4+C4+C6 certificate excluding first-factor orbit 7."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF

from verify_fourteen_vertex_c4_c4_c6_orbit6 import read_json, sha256


def run_quiet(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v4_orbit7_targeted_kappa3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit7_targeted_kappa3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit7_targeted_kappa3_kissat.drat"
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
            "orbit7_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    predecessor_output = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit7_"
        "predecessor_orbit6_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_c4_c4_c6_orbit6.py",
            "--output",
            str(predecessor_output),
        ]
    )
    predecessor = read_json(predecessor_output)
    predecessor_cnf = Path(str(predecessor["global_cnf"]))
    if (
        predecessor.get("verified") is not True
        or predecessor.get("status")
        != "C4+C4+C6_first_factor_orbit_6_excluded"
        or predecessor.get("global_cnf_sha256")
        != "2207a51d06e4a9b89d6062933c219583"
        "8295eed1c18b21da2d7727341945b318"
    ):
        raise AssertionError("orbit-6 predecessor reconstruction changed")

    augmentation = read_json(args.augmentation)
    global_cnf = Path(str(augmentation["output_cnf"]))
    prerequisite = augmentation.get("three_connectivity_prerequisite")
    if not isinstance(prerequisite, dict):
        raise AssertionError("orbit-7 connectivity prerequisite missing")
    prerequisite_manifest = Path(str(prerequisite["augmentation"]))
    prerequisite_audit = Path(str(prerequisite["audit"]))
    if (
        augmentation.get("status") != "minimum_activity_rules_augmented"
        or augmentation.get("partition") != [4, 4, 6]
        or Path(str(augmentation["base_cnf"])).resolve()
        != predecessor_cnf.resolve()
        or augmentation.get("base_cnf_sha256") != sha256(predecessor_cnf)
        or augmentation.get("certificates_replayed") != 536
        or augmentation.get("new_transport_clauses") != 13600
        or prerequisite.get("base_extension_clauses") != 5824
        or sha256(prerequisite_manifest)
        != prerequisite["augmentation_sha256"]
        or sha256(prerequisite_audit)
        != prerequisite["audit_sha256"]
        or augmentation.get("output_cnf_sha256") != sha256(global_cnf)
        or augmentation.get("output_cnf_variables") != 324
        or augmentation.get("output_cnf_clauses") != 1108529
    ):
        raise AssertionError("orbit-7 augmentation changed")

    augmentation_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit7_"
        "augmentation_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.augmentation),
            "--output",
            str(augmentation_recheck),
        ]
    )
    replay = read_json(augmentation_recheck)
    if (
        replay.get("verified") is not True
        or replay.get("status")
        != "minimum_activity_augmentation_reconstructed"
        or replay.get("certificates_replayed") != 536
        or replay.get("new_transport_clauses") != 13600
        or replay.get("output_cnf_variables") != 324
        or replay.get("output_cnf_clauses") != 1108529
        or replay.get("sat") is not True
    ):
        raise AssertionError("orbit-7 augmentation replay changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [239]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the global CNF plus selector 239"
        )

    drat_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit7_"
        "final_drat_trim_recheck.json"
    )
    run_quiet(
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
            "tmp/fourteen_vertex_c4_c4_c6_orbit7_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_orbit7_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_path),
            "--forward",
        ]
    )
    if read_json(drat_path).get("verified") is not True:
        raise AssertionError("orbit-7 DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C4+C4+C6_first_factor_orbit_7_excluded",
        "scope": (
            "order-14 equality architecture with full factor C4+C4+C6, "
            "skeleton vertex connectivity at least 3, and pinned first "
            "singleton factor orbit 7"
        ),
        "minimal_counterexample_relevance": (
            "a minimal Krenn-Gu counterexample must be 4-connected "
            "(Chandran-Gajjala-Illickan, arXiv:2407.00303)"
        ),
        "predecessor_orbit6_replayed": True,
        "orbit7_certificates_replayed": 536,
        "orbit7_new_transport_clauses": 13600,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "excluded_first_factor_orbit": 7,
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
