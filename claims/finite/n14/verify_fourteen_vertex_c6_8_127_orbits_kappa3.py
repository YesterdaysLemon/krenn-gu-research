"""Replay the order-14 C6+C8 certificate excluding 127 kappa>=3 orbits."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from pysat.formula import CNF

from verify_fourteen_vertex_c6_8_126_orbits_kappa3 import (
    read_json,
    run_quiet,
    sha256,
)


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

UNSAT_ORBITS = [
    *range(0, 14),
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbit13-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v26_orbit13_targeted_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_127_orbits_"
            "v26_kappa3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_127_orbits_"
            "v26_kappa3_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_127_orbits_"
            "kappa3_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    predecessor_output = Path(
        "tmp/fourteen_vertex_c6_8_127_orbits_"
        "predecessor_126_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_c6_8_126_orbits_kappa3.py",
            "--output",
            str(predecessor_output),
        ]
    )
    predecessor = read_json(predecessor_output)
    predecessor_cnf = Path(str(predecessor["global_cnf"]))
    if (
        predecessor.get("verified") is not True
        or predecessor.get("status")
        != "C6+C8_kappa3_126_first_factor_orbits_excluded"
        or predecessor_cnf
        != Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v25_orbit12_targeted.cnf"
        )
        or predecessor.get("global_cnf_sha256")
        != "cad473ce07b2b77de2485b27deea93cc9"
        "b17d5630b045179339c3625a12942b7"
    ):
        raise AssertionError("126-orbit predecessor reconstruction changed")

    augmentation = read_json(args.orbit13_augmentation)
    global_cnf = Path(str(augmentation["output_cnf"]))
    prerequisite = augmentation.get("three_connectivity_prerequisite")
    if not isinstance(prerequisite, dict):
        raise AssertionError("orbit-13 connectivity prerequisite missing")
    connectivity = Path(str(prerequisite["augmentation"]))
    if (
        augmentation.get("status") != "minimum_activity_rules_augmented"
        or augmentation.get("partition") != [6, 8]
        or Path(str(augmentation["base_cnf"])).resolve()
        != predecessor_cnf.resolve()
        or augmentation.get("base_cnf_sha256") != sha256(predecessor_cnf)
        or prerequisite.get("augmentation_sha256") != sha256(connectivity)
        or prerequisite.get("base_extension_clauses") != 3244
        or augmentation.get("certificates_replayed") != 56
        or augmentation.get("new_transport_clauses") != 212
        or augmentation.get("output_cnf_sha256") != sha256(global_cnf)
        or augmentation.get("output_cnf_variables") != 559
        or augmentation.get("output_cnf_clauses") != 130066
    ):
        raise AssertionError("orbit-13 augmentation changed")

    augmentation_recheck = Path(
        "tmp/fourteen_vertex_c6_8_127_orbits_"
        "orbit13_augmentation_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            str(REPO_ROOT / "claims" / "finite" / "n14" / "verify_fourteen_vertex_two_even_cycle_minimum_activity_augmentation.py"),
            str(args.orbit13_augmentation),
            "--output",
            str(augmentation_recheck),
        ]
    )
    replay = read_json(augmentation_recheck)
    if (
        replay.get("verified") is not True
        or replay.get("status")
        != "minimum_activity_augmentation_reconstructed"
        or replay.get("certificates_replayed") != 56
        or replay.get("new_transport_clauses") != 212
        or replay.get("output_cnf_variables") != 559
        or replay.get("output_cnf_clauses") != 130066
        or replay.get("sat") is not True
    ):
        raise AssertionError("orbit-13 augmentation replay changed")

    orbit_output = Path(
        "tmp/fourteen_vertex_c6_8_127_orbits_"
        "orbit_audit_recheck.json"
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
        raise AssertionError("fresh 127-orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in UNSAT_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not global CNF plus the 127 selectors"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c6_8_127_orbits_"
        "final_drat_trim_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "generate" / "run_drat_trim.py"),
            "--drat-trim",
            str(args.drat_trim),
            "--cnf",
            str(args.conditioned_cnf),
            "--proof",
            str(args.proof),
            "--stdout",
            "tmp/fourteen_vertex_c6_8_127_orbits_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c6_8_127_orbits_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    if read_json(drat_output).get("verified") is not True:
        raise AssertionError("127-orbit DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C6+C8_kappa3_127_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C6+C8, "
            "skeleton vertex connectivity at least 3, and a pinned "
            "first singleton factor in the listed 127 orbits"
        ),
        "minimal_counterexample_relevance": (
            "the sparse-graph reduction leaves the 4-connected branch "
            "and a degree-three escape case"
        ),
        "predecessor_126_replayed": True,
        "orbit13_certificates_replayed": 56,
        "orbit13_new_transport_clauses": 212,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "sat_first_factor_orbits": 328 - len(UNSAT_ORBITS),
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
