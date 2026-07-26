"""Replay the order-14 C6+C8 certificate excluding 108 first orbits."""

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
    *range(0, 5),
    *range(100, 144),
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v7_"
            "augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_108_orbits_"
            "conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_108_orbits_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_108_orbits_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    augmentation = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    global_cnf = Path(augmentation["output_cnf"])

    reconstruction_output = Path(
        "tmp/fourteen_vertex_c6_8_108_orbits_"
        "final_reconstruction_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(args.augmentation),
            "--output",
            str(reconstruction_output),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    reconstruction = json.loads(
        reconstruction_output.read_text(encoding="utf-8")
    )
    if (
        reconstruction.get("verified") is not True
        or reconstruction.get("certificates_replayed") != 2019
        or reconstruction.get("new_transport_clauses") != 36080
        or reconstruction.get("sat") is not True
    ):
        raise AssertionError("fresh global reconstruction changed")

    orbit_output = Path(
        "tmp/fourteen_vertex_c6_8_108_orbits_"
        "final_orbit_audit_recheck.json"
    )
    subprocess.run(
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
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    orbit_audit = json.loads(
        orbit_output.read_text(encoding="utf-8")
    )
    expected_sat = [
        orbit for orbit in range(328) if orbit not in UNSAT_ORBITS
    ]
    if (
        orbit_audit["unsat_orbits"] != UNSAT_ORBITS
        or orbit_audit["sat_orbits"] != expected_sat
    ):
        raise AssertionError("fresh orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in UNSAT_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not global CNF plus the 108 selectors"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c6_8_108_orbits_"
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
            "tmp/fourteen_vertex_c6_8_108_orbits_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c6_8_108_orbits_"
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
        "status": "C6+C8_108_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C6+C8 "
            "and a pinned first singleton factor in the listed 108 orbits"
        ),
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "certificates_replayed": 2019,
        "new_transport_clauses": 36080,
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
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
