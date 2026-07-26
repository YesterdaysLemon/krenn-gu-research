"""Verify the orbit-44 support and DRAT extension step end to end."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from pysat.formula import CNF
from pysat.solvers import Solver


SELECTOR_ZERO = 232
SURVIVING_ORBITS = [
    9,
    10,
    11,
    13,
    14,
    15,
    16,
    22,
    36,
    37,
    38,
    39,
    40,
    41,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    54,
    55,
    57,
    63,
    68,
]
EXCLUDED_ORBITS = [
    orbit for orbit in range(93) if orbit not in SURVIVING_ORBITS
]
EXPECTED_BASE_SHA256 = (
    "e9482392e9c6568190ba6a1a4cd6c23025e7c8fd5a17fc5ff0c582cf864adb35"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str]) -> None:
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(
            "subprocess failed:\n"
            + " ".join(command)
            + "\n"
            + (result.stderr or result.stdout)
        )


def without_elapsed(payload: dict[str, object]) -> dict[str, object]:
    output = dict(payload)
    output.pop("elapsed_seconds", None)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cegar",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_"
            "orbit44_probe_cegar_support1_50.json"
        ),
    )
    parser.add_argument(
        "--orbit-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "probe_symbinomial2_orbit_audit.json"
        ),
    )
    parser.add_argument(
        "--conditioning",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_probe_"
            "symbinomial2_orbit44_conditioning.json"
        ),
    )
    parser.add_argument(
        "--kissat",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_probe_"
            "symbinomial2_orbit44_kissat.json"
        ),
    )
    parser.add_argument(
        "--drat",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_probe_"
            "symbinomial2_orbit44_drat_trim.json"
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
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "extension_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    cegar = read_json(args.cegar)
    if (
        cegar.get("status") != "symmetry_binomial_cegar_stopped"
        or int(cegar.get("certified_supports", -1)) != 2
        or int(cegar.get("new_support_no_goods", -1)) != 6912
        or cegar.get("terminal", {}).get("mode") != "selector_unsat"
        or int(cegar.get("terminal", {}).get("support", -1)) != 3
        or len(cegar.get("records", [])) != 2
        or len(cegar.get("materializations", [])) != 1
    ):
        raise AssertionError("orbit-44 CEGAR summary changed")
    base = Path(cegar["initial_cnf"])
    if sha256(base) != EXPECTED_BASE_SHA256:
        raise AssertionError("verified predecessor CNF changed")

    fresh_support_replays = []
    for record in cegar["records"]:
        analysis = Path(record["analysis"])
        stored_path = Path(record["verified_support"])
        stored = read_json(stored_path)
        fresh_path = Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            f"support{record['support']}_fresh_recheck.json"
        )
        run(
            [
                sys.executable,
                "verify_fourteen_vertex_partial_circuit_binomial_branch.py",
                str(analysis),
                "--output",
                str(fresh_path),
            ]
        )
        fresh = read_json(fresh_path)
        if (
            not fresh.get("verified")
            or without_elapsed(fresh) != without_elapsed(stored)
        ):
            raise AssertionError("fresh support replay changed")
        fresh_support_replays.append(
            {
                "support": int(record["support"]),
                "analysis": str(analysis),
                "analysis_sha256": sha256(analysis),
                "stored_verifier": str(stored_path),
                "stored_verifier_sha256": sha256(stored_path),
                "fresh_verifier": str(fresh_path),
                "fresh_verifier_sha256": sha256(fresh_path),
            }
        )

    materialization = cegar["materializations"][0]
    augmentation = Path(materialization["augmentation"])
    fresh_augmentation = Path(
        "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
        "support2_augmentation_fresh_recheck.json"
    )
    run(
        [
            sys.executable,
            "verify_fourteen_vertex_binomial_support_"
            "closure_augmentation.py",
            str(augmentation),
            "--output",
            str(fresh_augmentation),
        ]
    )
    augmentation_audit = read_json(fresh_augmentation)
    final_cnf = Path(cegar["final_cnf"])
    if (
        not augmentation_audit.get("verified")
        or augmentation_audit.get("status")
        != "binomial_support_closure_augmentation_verified"
        or int(augmentation_audit["certificate_records_checked"]) != 2
        or int(augmentation_audit["new_support_no_goods"]) != 6912
        or Path(augmentation_audit["output_cnf"]) != final_cnf
        or augmentation_audit["output_cnf_sha256"]
        != sha256(final_cnf)
        or int(augmentation_audit["output_clauses"]) != 4_723_021
    ):
        raise AssertionError("fresh augmentation replay changed")

    formula = CNF(from_file=str(final_cnf))
    rows = []
    with Solver(
        name="cadical195", bootstrap_with=formula.clauses
    ) as solver:
        for orbit in range(93):
            rows.append(
                {
                    "orbit": orbit,
                    "sat": bool(
                        solver.solve(
                            assumptions=[SELECTOR_ZERO + orbit]
                        )
                    ),
                }
            )
    sat_orbits = [row["orbit"] for row in rows if row["sat"]]
    unsat_orbits = [row["orbit"] for row in rows if not row["sat"]]
    if (
        sat_orbits != SURVIVING_ORBITS
        or unsat_orbits != EXCLUDED_ORBITS
    ):
        raise AssertionError("fresh 93-selector frontier changed")

    stored_audit = read_json(args.orbit_audit)
    former_frontier = sorted([44, *SURVIVING_ORBITS])
    if (
        stored_audit.get("cnf_sha256") != sha256(final_cnf)
        or stored_audit.get("selected_orbits") != former_frontier
        or stored_audit.get("unsat_orbits") != [44]
        or stored_audit.get("sat_orbits") != SURVIVING_ORBITS
    ):
        raise AssertionError("stored 27-selector audit changed")

    conditioning = read_json(args.conditioning)
    conditioned = Path(conditioning["output_cnf"])
    conditioned_formula = CNF(from_file=str(conditioned))
    if (
        conditioning.get("input_cnf_sha256") != sha256(final_cnf)
        or conditioning.get("selector_clause") != [SELECTOR_ZERO + 44]
        or conditioned_formula.clauses
        != [*formula.clauses, [SELECTOR_ZERO + 44]]
        or conditioning.get("output_cnf_sha256")
        != sha256(conditioned)
    ):
        raise AssertionError("conditioned DIMACS changed")
    formula = None
    conditioned_formula = None

    kissat = read_json(args.kissat)
    proof = Path(kissat["proof"])
    if (
        kissat.get("status") != "UNSAT"
        or int(kissat.get("returncode", -1)) != 20
        or kissat.get("cnf_sha256") != sha256(conditioned)
        or kissat.get("proof_sha256") != sha256(proof)
        or int(kissat.get("proof_bytes", -1)) != proof.stat().st_size
    ):
        raise AssertionError("Kissat proof manifest changed")
    stored_drat = read_json(args.drat)
    if (
        not stored_drat.get("verified")
        or not stored_drat.get("forward")
        or stored_drat.get("cnf_sha256") != sha256(conditioned)
        or stored_drat.get("proof_sha256") != sha256(proof)
    ):
        raise AssertionError("stored DRAT replay changed")

    fresh_drat_output = Path(
        "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
        "drat_trim_fresh_recheck.json"
    )
    run(
        [
            sys.executable,
            "run_drat_trim.py",
            "--drat-trim",
            str(args.drat_trim),
            "--cnf",
            str(conditioned),
            "--proof",
            str(proof),
            "--stdout",
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "drat_trim_fresh_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "drat_trim_fresh_recheck.stderr.log",
            "--output",
            str(fresh_drat_output),
            "--forward",
        ]
    )
    fresh_drat = read_json(fresh_drat_output)
    if (
        not fresh_drat.get("verified")
        or fresh_drat.get("cnf_sha256") != sha256(conditioned)
        or fresh_drat.get("proof_sha256") != sha256(proof)
    ):
        raise AssertionError("fresh DRAT replay failed")

    payload = {
        "verified": True,
        "status": "c4_c4_c6_orbit44_extension_verified",
        "scope": (
            "two fresh support-algebra replays, exact full-colour "
            "augmentation reconstruction, all 93 selector decisions, "
            "exact conditioned DIMACS, and fresh forward DRAT replay"
        ),
        "cegar": str(args.cegar),
        "cegar_sha256": sha256(args.cegar),
        "predecessor_cnf": str(base),
        "predecessor_cnf_sha256": sha256(base),
        "support_replays": fresh_support_replays,
        "fresh_augmentation_audit": str(fresh_augmentation),
        "fresh_augmentation_audit_sha256": sha256(
            fresh_augmentation
        ),
        "final_cnf": str(final_cnf),
        "final_cnf_sha256": sha256(final_cnf),
        "final_cnf_variables": 324,
        "final_cnf_clauses": 4_723_021,
        "excluded_orbits": EXCLUDED_ORBITS,
        "excluded_orbit_count": len(EXCLUDED_ORBITS),
        "surviving_orbits": SURVIVING_ORBITS,
        "surviving_orbit_count": len(SURVIVING_ORBITS),
        "newly_excluded_orbit": 44,
        "conditioned_cnf": str(conditioned),
        "conditioned_cnf_sha256": sha256(conditioned),
        "proof": str(proof),
        "proof_bytes": proof.stat().st_size,
        "proof_sha256": sha256(proof),
        "fresh_drat_replay": str(fresh_drat_output),
        "fresh_drat_replay_sha256": sha256(fresh_drat_output),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
