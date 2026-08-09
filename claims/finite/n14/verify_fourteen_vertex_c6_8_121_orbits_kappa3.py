"""Replay the order-14 C6+C8 certificate excluding 121 kappa>=3 orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF


UNSAT_ORBITS = [
    *range(0, 8),
    *range(100, 145),
    *range(171, 174),
    179,
    182,
    185,
    *range(187, 190),
    *range(200, 219),
    *range(220, 226),
    227,
    232,
    233,
    238,
    247,
    269,
    *range(300, 328),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_quiet(arguments: list[str]) -> None:
    subprocess.run(arguments, check=True, stdout=subprocess.DEVNULL)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--connectivity-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v19_kappa3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--orbit7-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v20_orbit7_targeted_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_121_orbits_"
            "v20_kappa3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_121_orbits_"
            "v20_kappa3_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_121_orbits_"
            "kappa3_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    predecessor_output = Path(
        "tmp/fourteen_vertex_c6_8_121_orbits_"
        "predecessor_v18_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_c6_8_119_orbits.py",
            "--output",
            str(predecessor_output),
        ]
    )
    predecessor = read_json(predecessor_output)
    predecessor_cnf = Path(str(predecessor["global_cnf"]))
    if (
        predecessor.get("verified") is not True
        or predecessor_cnf
        != Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v18_orbit6_one_extra.cnf"
        )
        or predecessor.get("global_cnf_sha256")
        != "5162bd3a83a0f730f2860059d39731ae"
        "439fe8dc085be3498339ba1c843ce300"
    ):
        raise AssertionError("v18 rule-base reconstruction changed")

    connectivity = read_json(args.connectivity_augmentation)
    kappa3_cnf = Path(str(connectivity["output_cnf"]))
    if (
        connectivity.get("status")
        != "three_vertex_connectivity_condition_augmented"
        or connectivity.get("partition") != [6, 8]
        or Path(str(connectivity["base_cnf"])).resolve()
        != predecessor_cnf.resolve()
        or connectivity.get("base_cnf_sha256")
        != sha256(predecessor_cnf)
        or connectivity.get("new_quotient_cut_clauses") != 1947
        or connectivity.get("output_cnf_sha256") != sha256(kappa3_cnf)
    ):
        raise AssertionError("explicit kappa>=3 augmentation changed")

    connectivity_output = Path(
        "tmp/fourteen_vertex_c6_8_121_orbits_"
        "kappa3_augmentation_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "three_connectivity_augmentation.py",
            str(args.connectivity_augmentation),
            "--output",
            str(connectivity_output),
        ]
    )
    connectivity_audit = read_json(connectivity_output)
    if (
        connectivity_audit.get("verified") is not True
        or connectivity_audit.get("status")
        != "three_vertex_connectivity_augmentation_reconstructed"
        or connectivity_audit.get("new_quotient_cut_clauses") != 1947
        or connectivity_audit.get("sat") is not True
    ):
        raise AssertionError("explicit kappa>=3 replay changed")

    orbit7 = read_json(args.orbit7_augmentation)
    global_cnf = Path(str(orbit7["output_cnf"]))
    prerequisite = orbit7.get("three_connectivity_prerequisite")
    if not isinstance(prerequisite, dict):
        raise AssertionError("orbit-7 connectivity prerequisite missing")
    if (
        orbit7.get("status") != "minimum_activity_rules_augmented"
        or orbit7.get("partition") != [6, 8]
        or Path(str(orbit7["base_cnf"])).resolve()
        != kappa3_cnf.resolve()
        or orbit7.get("base_cnf_sha256") != sha256(kappa3_cnf)
        or Path(str(prerequisite["augmentation"])).resolve()
        != args.connectivity_augmentation.resolve()
        or prerequisite.get("augmentation_sha256")
        != sha256(args.connectivity_augmentation)
        or orbit7.get("certificates_replayed") != 184
        or orbit7.get("new_transport_clauses") != 292
        or orbit7.get("output_cnf_sha256") != sha256(global_cnf)
    ):
        raise AssertionError("orbit-7 augmentation chain changed")

    orbit7_output = Path(
        "tmp/fourteen_vertex_c6_8_121_orbits_"
        "orbit7_augmentation_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.orbit7_augmentation),
            "--output",
            str(orbit7_output),
        ]
    )
    orbit7_audit = read_json(orbit7_output)
    if (
        orbit7_audit.get("verified") is not True
        or orbit7_audit.get("status")
        != "minimum_activity_augmentation_reconstructed"
        or orbit7_audit.get("certificates_replayed") != 184
        or orbit7_audit.get("new_transport_clauses") != 292
        or orbit7_audit.get("sat") is not True
    ):
        raise AssertionError("orbit-7 augmentation replay changed")

    orbit_output = Path(
        "tmp/fourteen_vertex_c6_8_121_orbits_"
        "final_orbit_audit_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "audit_fourteen_vertex_c4_c4_c6_rule_sat_orbits.py",
            "--cnf",
            str(global_cnf),
            "--selector-zero",
            "232",
            "--orbit-offset",
            "0",
            "--orbits",
            "328",
            "--output",
            str(orbit_output),
        ]
    )
    orbit_audit = read_json(orbit_output)
    expected_sat = [
        orbit for orbit in range(328) if orbit not in UNSAT_ORBITS
    ]
    if (
        orbit_audit["unsat_orbits"] != UNSAT_ORBITS
        or orbit_audit["sat_orbits"] != expected_sat
    ):
        raise AssertionError("fresh 121-orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in UNSAT_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not global CNF plus the 121 selectors"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c6_8_121_orbits_"
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
            "tmp/fourteen_vertex_c6_8_121_orbits_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c6_8_121_orbits_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    drat = read_json(drat_output)
    if drat.get("verified") is not True:
        raise AssertionError("121-orbit DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C6+C8_kappa3_121_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C6+C8, "
            "skeleton vertex connectivity at least 3, and a pinned "
            "first singleton factor in the listed 121 orbits"
        ),
        "minimal_counterexample_relevance": (
            "a minimal Krenn-Gu counterexample must be 4-connected "
            "(Chandran-Gajjala-Illickan, arXiv:2407.00303)"
        ),
        "v18_rule_base_reconstructed": True,
        "connectivity_clauses_replayed": 1947,
        "orbit7_certificates_replayed": 184,
        "orbit7_new_transport_clauses": 292,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "sat_first_factor_orbits": len(expected_sat),
        "unsat_first_factor_orbits": UNSAT_ORBITS,
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
