"""Replay the order-14 C4+C4+C6 certificate excluding orbit 3."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_quiet(arguments: list[str]) -> None:
    subprocess.run(arguments, check=True, stdout=subprocess.DEVNULL)


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
        "--orbit2-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "global_combined_v3_plus_orbit2_augmentation.json"
        ),
    )
    parser.add_argument(
        "--connectivity-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_global_combined_"
            "v3_plus_orbit2_kappa3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--connectivity-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_global_combined_"
            "v3_plus_orbit2_kappa3_augmentation_verified.json"
        ),
    )
    parser.add_argument(
        "--orbit3-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_global_combined_"
            "v3_plus_orbit2_kappa3_plus_orbit3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit3_kissat.drat"
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
            "tmp/fourteen_vertex_c4_c4_c6_orbit3_final_verified.json"
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
    orbit2 = json.loads(
        args.orbit2_augmentation.read_text(encoding="utf-8")
    )
    connectivity = json.loads(
        args.connectivity_augmentation.read_text(encoding="utf-8")
    )
    connectivity_audit = json.loads(
        args.connectivity_audit.read_text(encoding="utf-8")
    )
    orbit3 = json.loads(
        args.orbit3_augmentation.read_text(encoding="utf-8")
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
        or orbit2.get("status")
        != "minimum_activity_rules_augmented"
        or Path(orbit2["base_cnf"]).resolve()
        != Path(minimum["output_cnf"]).resolve()
        or connectivity.get("status")
        != "three_vertex_connectivity_condition_augmented"
        or Path(connectivity["base_cnf"]).resolve()
        != Path(orbit2["output_cnf"]).resolve()
        or connectivity_audit.get("verified") is not True
        or connectivity_audit.get("status")
        != "three_vertex_connectivity_augmentation_reconstructed"
        or connectivity_audit.get("augmentation_sha256")
        != sha256(args.connectivity_augmentation)
        or orbit3.get("status")
        != "minimum_activity_rules_augmented"
        or Path(orbit3["base_cnf"]).resolve()
        != Path(connectivity["output_cnf"]).resolve()
    ):
        raise AssertionError("C4+C4+C6 orbit-3 chain changed")

    rich_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
        "rich_reconstruction_recheck.json"
    )
    run_quiet(
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
        ]
    )
    rich_audit = json.loads(
        rich_recheck.read_text(encoding="utf-8")
    )
    if (
        rich_audit.get("verified") is not True
        or Path(rich_audit["final_cnf"]).resolve()
        != Path(rich["output_cnf"]).resolve()
        or rich_audit["final_cnf_sha256"]
        != rich["output_cnf_sha256"]
    ):
        raise AssertionError("rich certificate reconstruction changed")

    minimum_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
        "minimum_reconstruction_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.minimum_augmentation),
            "--output",
            str(minimum_recheck),
        ]
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

    orbit2_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
        "orbit2_augmentation_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.orbit2_augmentation),
            "--output",
            str(orbit2_recheck),
        ]
    )
    orbit2_audit = json.loads(
        orbit2_recheck.read_text(encoding="utf-8")
    )
    if (
        orbit2_audit.get("verified") is not True
        or orbit2_audit.get("certificates_replayed") != 168
        or orbit2_audit.get("new_transport_clauses") != 3712
        or orbit2_audit.get("sat") is not True
    ):
        raise AssertionError("orbit-2 augmentation changed")

    connectivity_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
        "connectivity_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "three_connectivity_augmentation.py",
            str(args.connectivity_augmentation),
            "--output",
            str(connectivity_recheck),
        ]
    )
    connectivity_rebuilt = json.loads(
        connectivity_recheck.read_text(encoding="utf-8")
    )
    if (
        connectivity_rebuilt.get("verified") is not True
        or connectivity_rebuilt.get("partition") != [4, 4, 6]
        or connectivity_rebuilt.get("first_factor_orbits") != 93
        or connectivity_rebuilt.get("new_quotient_cut_clauses")
        != 2576
        or connectivity_rebuilt.get("sat") is not True
    ):
        raise AssertionError("connectivity reconstruction changed")

    orbit3_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
        "augmentation_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.orbit3_augmentation),
            "--output",
            str(orbit3_recheck),
        ]
    )
    orbit3_audit = json.loads(
        orbit3_recheck.read_text(encoding="utf-8")
    )
    if (
        orbit3_audit.get("verified") is not True
        or orbit3_audit.get("certificates_replayed") != 272
        or orbit3_audit.get("new_transport_clauses") != 5856
        or orbit3_audit.get("sat") is not True
    ):
        raise AssertionError("orbit-3 augmentation changed")

    global_cnf = Path(orbit3["output_cnf"])
    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [235]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the global CNF plus selector 235"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
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
            "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_orbit3_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    drat = json.loads(drat_output.read_text(encoding="utf-8"))
    if drat.get("verified") is not True:
        raise AssertionError("orbit-3 DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C4+C4+C6_first_factor_orbit_3_excluded",
        "scope": (
            "order-14 equality architecture with full factor C4+C4+C6 "
            "and pinned first singleton factor orbit 3"
        ),
        "rich_certificates_replayed": 17,
        "minimum_certificates_replayed": 2357,
        "orbit2_certificates_replayed": 168,
        "connectivity_quotient_cut_clauses": 2576,
        "orbit3_certificates_replayed": 272,
        "orbit3_new_transport_clauses": 5856,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "excluded_first_factor_orbit": 3,
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
