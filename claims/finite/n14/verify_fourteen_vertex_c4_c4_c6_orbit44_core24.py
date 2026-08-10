"""Verify the minimized orbit-44 extension theorem end to end.

The discovery run added 6,912 symmetry images.  Only 24 of those clauses
are needed: under selector 44, the predecessor CNF has exactly 24 factor
assignments, and each assignment is forbidden by one of the 24 clauses.
This verifier freshly reconstructs that exact boundary, byte-replays the
24-clause DIMACS append, audits all 93 selectors, checks exact selector
conditioning, binds the Kissat proof, and normally performs a fresh
forward DRAT replay.
"""

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

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



SELECTOR_ZERO = 232
ORBIT = 44
SELECTOR = SELECTOR_ZERO + ORBIT
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
EXPECTED_FINAL_SHA256 = (
    "5bea81cd27ae21111f9466c7088694fd3732e1ecae718f0229ef3e08a934cd2b"
)
EXPECTED_CONDITIONED_SHA256 = (
    "d1b390a66aee3d748bd12799850fd3a153df8b45872a33f30c2a8f49072a4739"
)
EXPECTED_PROOF_SHA256 = (
    "26ec2bbc5100d11a4e8b3cc181189c78643ba1563e68688f67869a7c12ba7c0b"
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


def dimacs_header(line: bytes) -> tuple[int, int]:
    fields = line.split()
    if len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise AssertionError("unexpected DIMACS header")
    return int(fields[2]), int(fields[3])


def verify_exact_conditioning(
    source: Path,
    conditioned: Path,
) -> None:
    """Check that conditioned is source plus the exact selector unit."""
    with source.open("rb") as left, conditioned.open("rb") as right:
        source_header = left.readline()
        conditioned_header = right.readline()
        variables, source_clauses = dimacs_header(source_header)
        conditioned_variables, conditioned_clauses = dimacs_header(
            conditioned_header
        )
        if (
            conditioned_variables != variables
            or conditioned_clauses != source_clauses + 1
        ):
            raise AssertionError("conditioned DIMACS header changed")
        while True:
            source_line = left.readline()
            if not source_line:
                break
            if right.readline() != source_line:
                raise AssertionError("conditioned DIMACS body changed")
        selector_line = right.readline()
        if selector_line.rstrip(b"\r\n") != f"{SELECTOR} 0".encode():
            raise AssertionError("selector unit changed")
        if right.read(1):
            raise AssertionError("extra data after selector unit")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_models_verified.json"
        ),
    )
    parser.add_argument(
        "--materialization",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_materialization.json"
        ),
    )
    parser.add_argument(
        "--materialization-verifier",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_materialization_verified.json"
        ),
    )
    parser.add_argument(
        "--orbit-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_all93_orbit_audit.json"
        ),
    )
    parser.add_argument(
        "--conditioning",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_conditioning.json"
        ),
    )
    parser.add_argument(
        "--kissat",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_kissat.json"
        ),
    )
    parser.add_argument(
        "--drat",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_drat_trim.json"
        ),
    )
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=Path("tmp/drat-trim/drat-trim"),
    )
    parser.add_argument(
        "--skip-fresh-drat-replay",
        action="store_true",
        help=(
            "check the stored forward replay instead of launching the "
            "normally required redundant fresh replay"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_final_verified.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()

    stored_models = read_json(args.models)
    fresh_models_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
        "core24_models_fresh_recheck.json"
    )
    run(
        [
            sys.executable,
            str(HERE / "verify_fourteen_vertex_c4_c4_c6_orbit44_core24_models.py"),
            "--output",
            str(fresh_models_path),
        ]
    )
    fresh_models = read_json(fresh_models_path)
    if (
        fresh_models.get("verified") is not True
        or without_elapsed(fresh_models) != without_elapsed(stored_models)
        or fresh_models.get("base_cnf_sha256") != EXPECTED_BASE_SHA256
        or int(fresh_models.get("enumerated_factor_models", -1)) != 24
        or fresh_models.get("support_source_memberships") != [8, 16]
        or fresh_models.get("exact_model_clause_set_match") is not True
    ):
        raise AssertionError("fresh exact-24 model reconstruction changed")

    stored_materialization = read_json(
        args.materialization_verifier
    )
    fresh_materialization_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
        "core24_materialization_fresh_recheck.json"
    )
    run(
        [
            sys.executable,
            str(HERE / "verify_materialized_dimacs_clause_subset.py"),
            str(args.materialization),
            "--output",
            str(fresh_materialization_path),
        ]
    )
    fresh_materialization = read_json(fresh_materialization_path)
    if (
        fresh_materialization.get("verified") is not True
        or without_elapsed(fresh_materialization)
        != without_elapsed(stored_materialization)
        or fresh_materialization.get("source_membership_counts")
        != [8, 16]
        or int(fresh_materialization.get("appended_clauses", -1)) != 24
        or fresh_materialization.get("output_cnf_sha256")
        != EXPECTED_FINAL_SHA256
    ):
        raise AssertionError("fresh 24-clause materialization changed")
    final_cnf = Path(fresh_materialization["output_cnf"])

    formula = CNF(from_file=str(final_cnf))
    if formula.nv != 324 or len(formula.clauses) != 4_716_133:
        raise AssertionError("minimized CNF dimensions changed")
    with Solver(
        name="cadical195", bootstrap_with=formula.clauses
    ) as solver:
        sat_orbits = [
            orbit
            for orbit in range(93)
            if solver.solve(assumptions=[SELECTOR_ZERO + orbit])
        ]
    if sat_orbits != SURVIVING_ORBITS:
        raise AssertionError("fresh all-93 selector frontier changed")
    stored_audit = read_json(args.orbit_audit)
    if (
        stored_audit.get("cnf_sha256") != EXPECTED_FINAL_SHA256
        or stored_audit.get("selected_orbits") != list(range(93))
        or stored_audit.get("sat_orbits") != SURVIVING_ORBITS
        or stored_audit.get("unsat_orbits") != EXCLUDED_ORBITS
    ):
        raise AssertionError("stored all-93 selector audit changed")
    formula = None

    conditioning = read_json(args.conditioning)
    conditioned = Path(conditioning["output_cnf"])
    if (
        conditioning.get("input_cnf_sha256")
        != EXPECTED_FINAL_SHA256
        or conditioning.get("selector_clause") != [SELECTOR]
        or conditioning.get("output_cnf_sha256")
        != EXPECTED_CONDITIONED_SHA256
        or sha256(conditioned) != EXPECTED_CONDITIONED_SHA256
    ):
        raise AssertionError("conditioning manifest changed")
    verify_exact_conditioning(final_cnf, conditioned)

    kissat = read_json(args.kissat)
    proof = Path(kissat["proof"])
    if (
        kissat.get("status") != "UNSAT"
        or int(kissat.get("returncode", -1)) != 20
        or kissat.get("cnf_sha256") != EXPECTED_CONDITIONED_SHA256
        or kissat.get("proof_sha256") != EXPECTED_PROOF_SHA256
        or sha256(proof) != EXPECTED_PROOF_SHA256
        or int(kissat.get("proof_bytes", -1)) != proof.stat().st_size
    ):
        raise AssertionError("Kissat proof manifest changed")
    stored_drat = read_json(args.drat)
    if (
        stored_drat.get("verified") is not True
        or stored_drat.get("forward") is not True
        or stored_drat.get("cnf_sha256")
        != EXPECTED_CONDITIONED_SHA256
        or stored_drat.get("proof_sha256") != EXPECTED_PROOF_SHA256
    ):
        raise AssertionError("stored forward DRAT replay changed")

    fresh_drat_path = None
    if not args.skip_fresh_drat_replay:
        fresh_drat_path = Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_drat_trim_fresh_recheck.json"
        )
        run(
            [
                sys.executable,
                str(REPO_ROOT / "tools" / "generate" / "run_drat_trim.py"),
                "--drat-trim",
                str(args.drat_trim),
                "--cnf",
                str(conditioned),
                "--proof",
                str(proof),
                "--stdout",
                "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
                "core24_drat_trim_fresh_recheck.stdout.log",
                "--stderr",
                "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
                "core24_drat_trim_fresh_recheck.stderr.log",
                "--output",
                str(fresh_drat_path),
                "--forward",
            ]
        )
        fresh_drat = read_json(fresh_drat_path)
        if (
            fresh_drat.get("verified") is not True
            or fresh_drat.get("forward") is not True
            or fresh_drat.get("cnf_sha256")
            != EXPECTED_CONDITIONED_SHA256
            or fresh_drat.get("proof_sha256")
            != EXPECTED_PROOF_SHA256
        ):
            raise AssertionError("fresh forward DRAT replay failed")

    payload = {
        "verified": True,
        "status": "c4_c4_c6_orbit44_core24_final_verified",
        "scope": (
            "fresh exact enumeration of all 24 predecessor models, "
            "verbatim binding to independently verified algebraic "
            "support clauses, byte-identical 24-clause DIMACS replay, "
            "all 93 selector decisions, exact conditioning, Kissat "
            "proof binding, stored forward DRAT verification, and "
            + (
                "a redundant fresh forward DRAT replay"
                if fresh_drat_path is not None
                else "no redundant fresh replay in this invocation"
            )
        ),
        "model_reconstruction": str(fresh_models_path),
        "model_reconstruction_sha256": sha256(fresh_models_path),
        "materialization_reconstruction": str(
            fresh_materialization_path
        ),
        "materialization_reconstruction_sha256": sha256(
            fresh_materialization_path
        ),
        "predecessor_cnf": fresh_models["base_cnf"],
        "predecessor_cnf_sha256": EXPECTED_BASE_SHA256,
        "final_cnf": str(final_cnf),
        "final_cnf_sha256": EXPECTED_FINAL_SHA256,
        "final_cnf_variables": 324,
        "final_cnf_clauses": 4_716_133,
        "exact_predecessor_models": 24,
        "appended_verified_clauses": 24,
        "newly_excluded_orbit": ORBIT,
        "excluded_orbits": EXCLUDED_ORBITS,
        "excluded_orbit_count": len(EXCLUDED_ORBITS),
        "surviving_orbits": SURVIVING_ORBITS,
        "surviving_orbit_count": len(SURVIVING_ORBITS),
        "conditioned_cnf": str(conditioned),
        "conditioned_cnf_sha256": EXPECTED_CONDITIONED_SHA256,
        "proof": str(proof),
        "proof_bytes": proof.stat().st_size,
        "proof_sha256": EXPECTED_PROOF_SHA256,
        "stored_drat_replay": str(args.drat),
        "stored_drat_replay_sha256": sha256(args.drat),
        "fresh_drat_replay": (
            str(fresh_drat_path)
            if fresh_drat_path is not None
            else None
        ),
        "fresh_drat_replay_sha256": (
            sha256(fresh_drat_path)
            if fresh_drat_path is not None
            else None
        ),
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
