"""Shared replay logic for one certified C6+C8 kappa>=3 orbit step."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from pysat.formula import CNF

from verify_fourteen_vertex_c6_8_128_orbits_kappa3 import read_json, sha256


@dataclass(frozen=True)
class Step:
    excluded_orbits: int
    new_orbit: int
    predecessor_script: str
    predecessor_status: str
    predecessor_cnf_sha256: str
    certificates: int
    new_clauses: int
    base_extension_clauses: int
    global_cnf_sha256: str
    global_cnf_clauses: int


def run_quiet(command: list[str]) -> None:
    result = subprocess.run(
        command,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"{result.stderr}"
        )


def verify_step(
    step: Step,
    *,
    augmentation_path: Path,
    conditioned_cnf: Path,
    proof: Path,
    drat_trim: Path,
    output: Path,
) -> None:
    started = time.perf_counter()
    prefix = f"tmp/fourteen_vertex_c6_8_{step.excluded_orbits}_orbits_"

    predecessor_output = Path(prefix + "predecessor_recheck.json")
    run_quiet(
        [
            sys.executable,
            step.predecessor_script,
            "--output",
            str(predecessor_output),
        ]
    )
    predecessor = read_json(predecessor_output)
    predecessor_cnf = Path(str(predecessor["global_cnf"]))
    if (
        predecessor.get("verified") is not True
        or predecessor.get("status") != step.predecessor_status
        or predecessor.get("global_cnf_sha256")
        != step.predecessor_cnf_sha256
    ):
        raise AssertionError("predecessor reconstruction changed")

    augmentation = read_json(augmentation_path)
    global_cnf = Path(str(augmentation["output_cnf"]))
    prerequisite = augmentation.get("three_connectivity_prerequisite")
    if not isinstance(prerequisite, dict):
        raise AssertionError("connectivity prerequisite missing")
    connectivity = Path(str(prerequisite["augmentation"]))
    if (
        augmentation.get("status") != "minimum_activity_rules_augmented"
        or augmentation.get("partition") != [6, 8]
        or Path(str(augmentation["base_cnf"])).resolve()
        != predecessor_cnf.resolve()
        or augmentation.get("base_cnf_sha256") != sha256(predecessor_cnf)
        or prerequisite.get("augmentation_sha256") != sha256(connectivity)
        or prerequisite.get("base_extension_clauses")
        != step.base_extension_clauses
        or augmentation.get("certificates_replayed") != step.certificates
        or augmentation.get("new_transport_clauses") != step.new_clauses
        or augmentation.get("output_cnf_sha256")
        != step.global_cnf_sha256
        or sha256(global_cnf) != step.global_cnf_sha256
        or augmentation.get("output_cnf_variables") != 559
        or augmentation.get("output_cnf_clauses")
        != step.global_cnf_clauses
    ):
        raise AssertionError("new-orbit augmentation changed")

    augmentation_recheck = Path(prefix + "augmentation_recheck.json")
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(augmentation_path),
            "--output",
            str(augmentation_recheck),
        ]
    )
    replay = read_json(augmentation_recheck)
    if (
        replay.get("verified") is not True
        or replay.get("status")
        != "minimum_activity_augmentation_reconstructed"
        or replay.get("certificates_replayed") != step.certificates
        or replay.get("new_transport_clauses") != step.new_clauses
        or replay.get("output_cnf_variables") != 559
        or replay.get("output_cnf_clauses")
        != step.global_cnf_clauses
        or replay.get("sat") is not True
    ):
        raise AssertionError("new-orbit augmentation replay changed")

    orbit_output = Path(prefix + "orbit_audit_recheck.json")
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
    unsat_orbits = list(map(int, orbit_audit["unsat_orbits"]))
    if (
        len(unsat_orbits) != step.excluded_orbits
        or step.new_orbit not in unsat_orbits
        or orbit_audit["sat_orbits"]
        != [orbit for orbit in range(328) if orbit not in unsat_orbits]
    ):
        raise AssertionError("fresh orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(conditioned_cnf))
    selector_clause = [232 + orbit for orbit in unsat_orbits]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not global CNF plus the UNSAT selectors"
        )

    drat_output = Path(prefix + "final_drat_trim_recheck.json")
    run_quiet(
        [
            sys.executable,
            "run_drat_trim.py",
            "--drat-trim",
            str(drat_trim),
            "--cnf",
            str(conditioned_cnf),
            "--proof",
            str(proof),
            "--stdout",
            prefix + "final_drat_trim_recheck.stdout.log",
            "--stderr",
            prefix + "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    if read_json(drat_output).get("verified") is not True:
        raise AssertionError("aggregate DRAT replay changed")

    payload = {
        "verified": True,
        "status": (
            f"C6+C8_kappa3_{step.excluded_orbits}_"
            "first_factor_orbits_excluded"
        ),
        "scope": (
            "order-14 equality architecture with full factor C6+C8, "
            "skeleton vertex connectivity at least 3, and a pinned first "
            f"singleton factor in the listed {step.excluded_orbits} orbits"
        ),
        "minimal_counterexample_relevance": (
            "the sparse-graph reduction leaves the 4-connected branch "
            "and a degree-three escape case"
        ),
        "predecessor_replayed": True,
        "new_orbit": step.new_orbit,
        "new_orbit_certificates_replayed": step.certificates,
        "new_orbit_transport_clauses": step.new_clauses,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "sat_first_factor_orbits": 328 - len(unsat_orbits),
        "unsat_first_factor_orbits": unsat_orbits,
        "selector_clause": selector_clause,
        "conditioned_cnf": str(conditioned_cnf),
        "conditioned_cnf_sha256": sha256(conditioned_cnf),
        "conditioned_cnf_clauses": len(conditioned_formula.clauses),
        "proof": str(proof),
        "proof_sha256": sha256(proof),
        "proof_bytes": proof.stat().st_size,
        "drat_trim_verified": True,
        "elapsed_seconds": time.perf_counter() - started,
        "global_conjecture_resolved": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
