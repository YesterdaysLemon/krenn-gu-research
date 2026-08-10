"""Replay the order-14 C6+C8 first-factor orbits 0--2 certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



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
            "tmp/fourteen_vertex_c6_8_rule_sat_low0_2_"
            "fresh_global_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_orbits0_2_"
            "fresh_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_orbits0_2_fresh_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_orbits0_2_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    augmentation = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    global_cnf = Path(augmentation["output_cnf"])

    reconstruction_output = Path(
        "tmp/fourteen_vertex_c6_8_orbits0_2_"
        "final_reconstruction_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            str(HERE / "verify_fourteen_vertex_two_even_cycle_minimum_activity_augmentation.py"),
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
        or reconstruction.get("certificates_replayed") != 400
        or reconstruction.get("new_transport_clauses") != 794
        or reconstruction.get("sat") is not True
    ):
        raise AssertionError("fresh global reconstruction changed")

    orbit_output = Path(
        "tmp/fourteen_vertex_c6_8_orbits0_2_"
        "final_orbit_audit_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            str(HERE / "audit_fourteen_vertex_c4_c4_c6_rule_sat_orbits.py"),
            "--cnf",
            str(global_cnf),
            "--first-selector",
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
    if (
        orbit_audit["unsat_orbits"] != [0, 1, 2]
        or orbit_audit["sat_orbits"] != list(range(3, 328))
    ):
        raise AssertionError("fresh orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232, 233, 234]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the global CNF plus selectors 0--2"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c6_8_orbits0_2_"
        "final_drat_trim_recheck.json"
    )
    subprocess.run(
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
            "tmp/fourteen_vertex_c6_8_orbits0_2_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c6_8_orbits0_2_"
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
        "status": "C6+C8_first_factor_orbits_0_1_2_excluded",
        "scope": (
            "order-14 equality architecture with full factor C6+C8 "
            "and pinned first singleton factor orbit 0, 1, or 2 only"
        ),
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "certificates_replayed": 400,
        "new_transport_clauses": 794,
        "sat_first_factor_orbits": 325,
        "unsat_first_factor_orbits": [0, 1, 2],
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
