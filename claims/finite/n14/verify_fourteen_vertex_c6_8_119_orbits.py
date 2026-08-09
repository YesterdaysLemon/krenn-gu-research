"""Replay the order-14 C6+C8 certificate excluding 119 first orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF


PREDECESSOR_UNSAT_ORBITS = [
    *range(0, 6),
    *range(100, 144),
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
UNSAT_ORBITS = sorted([*PREDECESSOR_UNSAT_ORBITS, 6])


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
        "--augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v18_"
            "orbit6_one_extra_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_119_orbits_v18_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_119_orbits_v18_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_119_orbits_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    predecessor_output = Path(
        "tmp/fourteen_vertex_c6_8_119_orbits_"
        "predecessor_118_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_c6_8_118_orbits.py",
            "--output",
            str(predecessor_output),
        ]
    )
    predecessor = json.loads(
        predecessor_output.read_text(encoding="utf-8")
    )
    if (
        predecessor.get("verified") is not True
        or predecessor.get("unsat_first_factor_orbits")
        != PREDECESSOR_UNSAT_ORBITS
    ):
        raise AssertionError("118-orbit predecessor certificate changed")

    augmentation = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    base_cnf = Path(augmentation["base_cnf"])
    global_cnf = Path(augmentation["output_cnf"])
    if (
        base_cnf.resolve()
        != Path(predecessor["global_cnf"]).resolve()
        or augmentation.get("status")
        != "verified_one_extra_cycle_rules_augmented"
        or augmentation.get("partition") != [6, 8]
        or augmentation.get("base_cnf_sha256") != sha256(base_cnf)
        or augmentation.get("output_cnf_sha256") != sha256(global_cnf)
        or len(augmentation.get("certificate_records", [])) != 38
        or augmentation.get("new_no_goods") != 152
    ):
        raise AssertionError("orbit-6 augmentation chain changed")

    augmentation_output = Path(
        "tmp/fourteen_vertex_c6_8_119_orbits_"
        "augmentation_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "one_extra_cycle_augmentation.py",
            str(args.augmentation),
            "--output",
            str(augmentation_output),
        ]
    )
    augmentation_audit = json.loads(
        augmentation_output.read_text(encoding="utf-8")
    )
    if (
        augmentation_audit.get("verified") is not True
        or augmentation_audit.get("status")
        != "one_extra_cycle_augmentation_reconstructed"
        or augmentation_audit.get("certificates_replayed") != 38
        or augmentation_audit.get("new_transport_no_goods") != 152
        or augmentation_audit.get("sat") is not True
    ):
        raise AssertionError("orbit-6 augmentation replay changed")

    orbit_output = Path(
        "tmp/fourteen_vertex_c6_8_119_orbits_"
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
        raise AssertionError("fresh 119-orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in UNSAT_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not global CNF plus the 119 selectors"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c6_8_119_orbits_"
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
            "tmp/fourteen_vertex_c6_8_119_orbits_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c6_8_119_orbits_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    drat = json.loads(drat_output.read_text(encoding="utf-8"))
    if drat.get("verified") is not True:
        raise AssertionError("119-orbit DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C6+C8_119_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C6+C8 "
            "and a pinned first singleton factor in the listed 119 orbits"
        ),
        "predecessor_118_verified": True,
        "orbit6_certificates_replayed": 38,
        "orbit6_new_transport_clauses": 152,
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
