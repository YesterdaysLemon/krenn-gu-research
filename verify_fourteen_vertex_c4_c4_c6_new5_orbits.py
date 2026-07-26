"""Replay the C4+C4+C6 certificate excluding five additional orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF

NEW_UNSAT_ORBITS = [0, 1, 4, 12, 35]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rich-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "global_rich_combined_v1_augmentation.json"
        ),
    )
    parser.add_argument(
        "--minimum-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "global_combined_v3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "new5_orbits_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_new5_orbits_kissat.drat"
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
            "new5_orbits_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    rich = json.loads(
        args.rich_augmentation.read_text(encoding="utf-8")
    )
    minimum = json.loads(
        args.minimum_augmentation.read_text(encoding="utf-8")
    )
    if (
        rich.get("status")
        != "verified_hard_certificate_no_goods_appended"
        or len(rich["certificate_records"]) != 17
        or rich["new_no_goods"] != 136
        or minimum.get("status")
        != "minimum_activity_rules_augmented"
        or Path(minimum["base_cnf"]).resolve()
        != Path(rich["output_cnf"]).resolve()
    ):
        raise AssertionError("C4+C4+C6 augmentation chain changed")

    rich_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_new5_"
        "rich_reconstruction_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            "verify_fourteen_vertex_c4_c4_c6_rule_cnf.py",
            "tmp/fourteen_vertex_c4_c4_c6_"
            "rule_sat_shared_base31_simple.json",
            "--augmentation",
            "tmp/fourteen_vertex_c4_c4_c6_"
            "rule_sat_shared_base31_hard_augmentation.json",
            "--augmentation",
            "tmp/fourteen_vertex_c4_c4_c6_"
            "rule_sat_shared_base31_hard_core12_augmentation.json",
            "--augmentation",
            str(args.rich_augmentation),
            "--output",
            str(rich_recheck),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    rich_audit = json.loads(rich_recheck.read_text(encoding="utf-8"))
    if (
        rich_audit.get("verified") is not True
        or Path(rich_audit["final_cnf"]).resolve()
        != Path(rich["output_cnf"]).resolve()
        or rich_audit["final_cnf_sha256"]
        != rich["output_cnf_sha256"]
    ):
        raise AssertionError("rich certificate reconstruction changed")

    minimum_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_new5_"
        "minimum_reconstruction_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.minimum_augmentation),
            "--output",
            str(minimum_recheck),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    minimum_audit = json.loads(
        minimum_recheck.read_text(encoding="utf-8")
    )
    if (
        minimum_audit.get("verified") is not True
        or minimum_audit.get("certificates_replayed") != 2357
        or minimum_audit.get("new_transport_clauses") != 93410
        or minimum_audit.get("sat") is not True
    ):
        raise AssertionError("minimum certificate reconstruction changed")

    global_cnf = Path(minimum["output_cnf"])
    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in NEW_UNSAT_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the global CNF plus five selectors"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c4_c4_c6_new5_"
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
            "tmp/fourteen_vertex_c4_c4_c6_new5_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_new5_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    drat = json.loads(drat_output.read_text(encoding="utf-8"))
    if drat.get("verified") is not True:
        raise AssertionError("DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C4+C4+C6_five_additional_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C4+C4+C6 "
            "and a pinned first singleton factor in orbits 0,1,4,12,35"
        ),
        "rich_certificates_replayed": 17,
        "minimum_certificates_replayed": 2357,
        "new_transport_clauses": 93410,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "excluded_first_factor_orbits": NEW_UNSAT_ORBITS,
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
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
