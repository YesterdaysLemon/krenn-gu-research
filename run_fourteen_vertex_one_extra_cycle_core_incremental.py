"""Incrementally learn verified direct one-extra cycle-core rules."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    edge_variable,
    parse_factor,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
    full_automorphisms,
)
from explore_random_even_cycle_forks import cycle_edges
from run_fourteen_vertex_two_even_cycle_rule_sat_incremental import (
    certificate_no_goods,
    minimum_condition_no_goods,
)


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
    parser.add_argument("--compiled-cnf", type=Path, required=True)
    parser.add_argument("--compiled-result", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument(
        "--cores-per-support",
        type=int,
        default=1,
        help=(
            "learn this many distinct one-extra cores from each residual "
            "support after computing its matching census once"
        ),
    )
    parser.add_argument(
        "--unit-origins-per-relation",
        type=int,
        default=1,
        help=(
            "retain this many one-extra witnesses per relation while "
            "building each residual's direct-core batch"
        ),
    )
    parser.add_argument(
        "--spread-base-equations",
        action="store_true",
        help=(
            "spread multi-core batches across the full-only equation "
            "catalogue instead of retaining only the earliest cores"
        ),
    )
    parser.add_argument(
        "--minimum-activation",
        action="store_true",
        help=(
            "independently minimize every direct core's activation "
            "premises under the necessary three-connected support scope"
        ),
    )
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.cores_per_support < 1:
        raise ValueError("--cores-per-support must be positive")
    if args.unit_origins_per_relation < 1:
        raise ValueError(
            "--unit-origins-per-relation must be positive"
        )
    started = time.perf_counter()

    compiled = json.loads(
        args.compiled_result.read_text(encoding="utf-8")
    )
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, compiled["partition"]))
    if (
        tuple(map(int, census["partition"])) != lengths
        or sum(lengths) != N
        or len(lengths) < 2
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("all-even partition changed")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    if args.orbit < 0 or args.orbit >= len(representatives):
        raise ValueError("orbit is outside the census")
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    selectors = tuple(
        3 * len(eligible_edges) + 1 + index
        for index in range(len(representatives))
    )
    actions = full_automorphisms(cycles)
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("automorphism count changed")

    base = CNF(from_file=str(args.compiled_cnf))
    known = {
        tuple(
            sorted(
                set(map(int, clause)),
                key=lambda item: (abs(item), item),
            )
        )
        for clause in base.clauses
    }
    all_new: set[tuple[int, ...]] = set()
    records = []
    terminal_status = "round_limit"
    with Solver(
        name="cadical195", bootstrap_with=base.clauses
    ) as solver:
        for iteration in range(args.rounds):
            if not solver.solve(assumptions=[selectors[args.orbit]]):
                terminal_status = "UNSAT"
                records.append(
                    {
                        "iteration": iteration,
                        "sat": False,
                        "incremental_no_goods": len(all_new),
                    }
                )
                break
            positive = {
                literal
                for literal in solver.get_model()
                if literal > 0
            }
            selected_orbits = [
                orbit
                for orbit, selector in enumerate(selectors)
                if selector in positive
            ]
            if selected_orbits != [args.orbit]:
                raise AssertionError("SAT model selector changed")
            factors = []
            for role in range(3):
                factor = tuple(
                    item
                    for edge_id, item in enumerate(eligible_edges)
                    if edge_variable(
                        role, edge_id, len(eligible_edges)
                    )
                    in positive
                )
                if len(factor) != N // 2:
                    raise AssertionError(
                        "SAT model factor is not perfect"
                    )
                factors.append(factor)
            if factors[0] != representatives[args.orbit]:
                raise AssertionError(
                    "SAT model first factor is not representative"
                )

            samples_path = Path(f"{args.prefix}_{iteration}_samples.json")
            samples = {
                "status": "SAT_rule_residual_samples",
                "partition": list(lengths),
                "source_census": str(args.census),
                "survivors": [
                    {
                        "orbit_id": args.orbit,
                        "first": [list(item) for item in factors[0]],
                        "second": [list(item) for item in factors[1]],
                        "third": [list(item) for item in factors[2]],
                    }
                ],
                "exploratory_only": True,
            }
            samples_path.parent.mkdir(parents=True, exist_ok=True)
            samples_path.write_text(
                json.dumps(samples, indent=2) + "\n",
                encoding="utf-8",
            )
            core_path = Path(f"{args.prefix}_{iteration}_core.json")
            extra_core_prefix = Path(
                f"{args.prefix}_{iteration}_core_alt"
            )
            finder_arguments = [
                sys.executable,
                str(REPO_ROOT / "tools" / "explore" / "find_fourteen_vertex_one_extra_cycle_core.py"),
                str(samples_path),
                "--survivor-index",
                "0",
                "--output",
                str(core_path),
            ]
            if args.cores_per_support > 1:
                finder_arguments.extend(
                    [
                        "--max-certificates",
                        str(args.cores_per_support),
                        "--extra-output-prefix",
                        str(extra_core_prefix),
                    ]
                )
            if args.unit_origins_per_relation > 1:
                finder_arguments.extend(
                    [
                        "--unit-origins-per-relation",
                        str(args.unit_origins_per_relation),
                    ]
                )
            if args.spread_base_equations:
                finder_arguments.append("--spread-base-equations")
            subprocess.run(
                finder_arguments,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            proof = json.loads(core_path.read_text(encoding="utf-8"))
            if proof.get("status") != "one_extra_cycle_core":
                terminal_status = "direct_core_absent"
                records.append(
                    {
                        "iteration": iteration,
                        "sat": True,
                        "core_status": proof.get("status"),
                        "samples": str(samples_path),
                        "core": str(core_path),
                        "incremental_no_goods": len(all_new),
                    }
                )
                break
            found = int(proof.get("certificates_found", 1))
            if found < 1 or found > args.cores_per_support:
                raise AssertionError("direct-core batch count changed")
            core_paths = [
                core_path,
                *[
                    Path(f"{extra_core_prefix}_{index}.json")
                    for index in range(1, found)
                ],
            ]
            support_new: set[tuple[int, ...]] = set()
            core_records = []
            for candidate_path in core_paths:
                candidate_proof = json.loads(
                    candidate_path.read_text(encoding="utf-8")
                )
                audit_path = candidate_path.with_name(
                    f"{candidate_path.stem}_verified.json"
                )
                subprocess.run(
                    [
                        sys.executable,
                        str(REPO_ROOT / "claims" / "finite" / "n14" / "verify_fourteen_vertex_one_extra_cycle_core.py"),
                        str(candidate_path),
                        "--output",
                        str(audit_path),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                audit = json.loads(
                    audit_path.read_text(encoding="utf-8")
                )
                if (
                    audit.get("verified") is not True
                    or audit.get("status")
                    != "one_extra_cycle_core_verified"
                    or audit.get("certificate_sha256")
                    != sha256(candidate_path)
                ):
                    raise AssertionError("direct core audit changed")
                certificate = candidate_proof["certificate"]
                equations = [
                    int(certificate["full_only_equation_index"]),
                    *[
                        int(row["one_extra_equation_index"])
                        for row in certificate["cycle_rows"]
                    ],
                ]
                equations = list(dict.fromkeys(equations))
                colourings = tuple(
                    tuple(
                        (equation // (3**vertex)) % 3
                        for vertex in range(N)
                    )
                    for equation in equations
                )
                minimum_path = None
                minimum_audit_path = None
                minimum_score = None
                if args.minimum_activation:
                    minimum_path = candidate_path.with_name(
                        f"{candidate_path.stem}_minimum_activity.json"
                    )
                    minimum_audit_path = candidate_path.with_name(
                        f"{candidate_path.stem}_"
                        "minimum_activity_verified.json"
                    )
                    subprocess.run(
                        [
                            sys.executable,
                            "minimize_fourteen_vertex_two_even_cycle_"
                            "certificate_activation.py",
                            str(samples_path),
                            str(candidate_path),
                            "--survivor-index",
                            "0",
                            "--three-connected-structural-feasibility",
                            "--output",
                            str(minimum_path),
                        ],
                        check=True,
                        stdout=subprocess.DEVNULL,
                    )
                    subprocess.run(
                        [
                            sys.executable,
                            "verify_fourteen_vertex_two_even_cycle_"
                            "minimum_activity_certificate.py",
                            str(minimum_path),
                            "--output",
                            str(minimum_audit_path),
                        ],
                        check=True,
                        stdout=subprocess.DEVNULL,
                    )
                    minimum = json.loads(
                        minimum_path.read_text(encoding="utf-8")
                    )
                    minimum_audit = json.loads(
                        minimum_audit_path.read_text(encoding="utf-8")
                    )
                    if (
                        minimum_audit.get("verified") is not True
                        or minimum_audit.get("status")
                        != "fourteen_vertex_minimum_activity_"
                        "certificate_verified"
                        or minimum_audit.get("certificate_sha256")
                        != sha256(minimum_path)
                    ):
                        raise AssertionError(
                            "minimum direct-core activation audit changed"
                        )
                    minimum_score = int(
                        minimum["activation_constraint_score"]
                    )
                    clauses = minimum_condition_no_goods(
                        tuple(factors),
                        minimum["activation_conditions"],
                        representative_id,
                        selectors,
                        actions,
                        eligible_edges,
                    )
                else:
                    clauses = certificate_no_goods(
                        tuple(factors),
                        colourings,
                        representative_id,
                        selectors,
                        actions,
                        eligible_edges,
                    )
                candidate_new = (
                    clauses - known - all_new - support_new
                )
                support_new.update(candidate_new)
                core_records.append(
                    {
                        "core": str(candidate_path),
                        "core_sha256": sha256(candidate_path),
                        "audit": str(audit_path),
                        "audit_sha256": sha256(audit_path),
                        "activation_equations": equations,
                        "minimum_activity": (
                            str(minimum_path) if minimum_path else None
                        ),
                        "minimum_activity_sha256": (
                            sha256(minimum_path)
                            if minimum_path
                            else None
                        ),
                        "minimum_activity_audit": (
                            str(minimum_audit_path)
                            if minimum_audit_path
                            else None
                        ),
                        "minimum_activity_audit_sha256": (
                            sha256(minimum_audit_path)
                            if minimum_audit_path
                            else None
                        ),
                        "minimum_activity_score": minimum_score,
                        "transport_clauses": len(clauses),
                        "new_no_goods": len(candidate_new),
                    }
                )
            new = support_new
            if not new:
                raise AssertionError(
                    "verified residual generated no new rule"
                )
            for clause in sorted(new):
                solver.add_clause(list(clause))
            all_new.update(new)
            first = core_records[0]
            record = {
                "iteration": iteration,
                "sat": True,
                "samples": str(samples_path),
                "samples_sha256": sha256(samples_path),
                **first,
                "core_candidates": core_records,
                "cores_replayed": len(core_records),
                "transport_clauses": sum(
                    row["transport_clauses"]
                    for row in core_records
                ),
                "new_no_goods": len(new),
                "incremental_no_goods": len(all_new),
            }
            records.append(record)
            print(json.dumps(record), flush=True)

    final = CNF()
    final.nv = base.nv
    final.clauses = [
        *[list(clause) for clause in base.clauses],
        *[list(clause) for clause in sorted(all_new)],
    ]
    final_path = Path(f"{args.prefix}_final.cnf")
    final_path.parent.mkdir(parents=True, exist_ok=True)
    final.to_file(str(final_path))
    payload = {
        "status": terminal_status,
        "partition": list(lengths),
        "orbit": args.orbit,
        "base_cnf": str(args.compiled_cnf),
        "base_cnf_sha256": sha256(args.compiled_cnf),
        "base_clauses": len(base.clauses),
        "compiled_result": str(args.compiled_result),
        "compiled_result_sha256": sha256(args.compiled_result),
        "census": str(args.census),
        "census_sha256": sha256(args.census),
        "iterations": records,
        "verified_cores": sum(
            (
                len(row["core_candidates"])
                if row.get("core_candidates")
                else bool(row.get("audit"))
            )
            for row in records
        ),
        "spread_base_equations": args.spread_base_equations,
        "incremental_no_goods": len(all_new),
        "final_cnf": str(final_path),
        "final_cnf_sha256": sha256(final_path),
        "final_clauses": len(final.clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_until_independently_reconstructed": (
            bool(all_new)
        ),
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
