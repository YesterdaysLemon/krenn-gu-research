"""Bounded symmetry-closed CEGAR for mandatory-unit support certificates.

This orchestrator accepts only supports certified by the standalone
algebra verifier and only DIMACS extensions certified by the standalone
augmentation verifier.  It stops on the first open mandatory core or
when the requested selector becomes UNSAT.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    print(f"[run] {' '.join(command)}", flush=True)
    result = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.stdout:
        print(result.stdout.rstrip(), flush=True)
    return result


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", default="4,4,6")
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--start-support", type=int, required=True)
    parser.add_argument("--maximum-support", type=int, default=40)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument(
        "--artifact-prefix",
        required=True,
        help=(
            "filename prefix below tmp, for example "
            "fourteen_vertex_c4_c4_c6_orbit9"
        ),
    )
    parser.add_argument(
        "--output-cnf-template",
        required=True,
        help="path template containing the field {support}",
    )
    parser.add_argument(
        "--incremental-solver",
        action="store_true",
        help=(
            "keep one CaDiCaL instance alive and add only independently "
            "audited extension clauses after each support"
        ),
    )
    parser.add_argument(
        "--full-support-orbit-closure",
        action="store_true",
        help=(
            "use all full-factor automorphisms and all six colour "
            "permutations instead of the pinned-factor stabilizer"
        ),
    )
    parser.add_argument(
        "--deferred-materialization",
        action="store_true",
        help=(
            "independently audit each symmetry-closed clause set "
            "immediately, but materialize and byte-replay the full DIMACS "
            "only in batches"
        ),
    )
    parser.add_argument(
        "--materialize-every",
        type=int,
        default=10,
        help="support certificates per deferred DIMACS batch",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.start_support < 1:
        raise ValueError("start support must be positive")
    if args.maximum_support < args.start_support:
        raise ValueError("maximum support precedes start support")
    if "{support}" not in args.output_cnf_template:
        raise ValueError("output CNF template lacks {support}")
    if not args.base_cnf.is_file():
        raise FileNotFoundError(args.base_cnf)
    if args.deferred_materialization and not args.incremental_solver:
        raise ValueError(
            "--deferred-materialization requires --incremental-solver"
        )
    if args.materialize_every < 1:
        raise ValueError("--materialize-every must be positive")

    started = time.perf_counter()
    current_cnf = args.base_cnf
    records: list[dict[str, object]] = []
    materializations: list[dict[str, object]] = []
    pending_verified_supports: list[Path] = []
    pending_solver_clauses: set[tuple[int, ...]] = set()
    terminal: dict[str, object] = {
        "mode": "maximum_support_reached",
        "support": args.maximum_support + 1,
    }

    formula = (
        CNF(from_file=str(args.base_cnf))
        if args.incremental_solver
        else None
    )
    solver_context = None
    if formula is not None:
        solver_context = Solver(
            name="cadical195", bootstrap_with=formula.clauses
        )
        formula = None
    solver = solver_context

    def materialize_pending(through_support: int) -> None:
        nonlocal current_cnf
        if not pending_verified_supports:
            return
        augmentation = Path(
            "tmp",
            f"{args.artifact_prefix}_symmetry_batch_through_support"
            f"{through_support}_augmentation.json",
        )
        verified_augmentation = Path(
            "tmp",
            f"{args.artifact_prefix}_symmetry_batch_through_support"
            f"{through_support}_augmentation_verified.json",
        )
        output_cnf = Path(
            args.output_cnf_template.format(support=through_support)
        )
        command = [
            sys.executable,
            "tools/generate/augment_fourteen_vertex_rule_cnf_with_"
            "binomial_support_closures.py",
            "--base-cnf",
            str(current_cnf),
        ]
        for verified_support in pending_verified_supports:
            command.extend(
                ["--verified-support", str(verified_support)]
            )
        command.extend(
            [
                (
                    "--full-support-orbit-closure"
                    if args.full_support_orbit_closure
                    else "--stabilizer-orbit-closure"
                ),
                "--output-cnf",
                str(output_cnf),
                "--output",
                str(augmentation),
                "--summary-only",
            ]
        )
        result = run(command)
        if result.returncode != 0:
            raise RuntimeError(
                "deferred support batch augmentation failed with "
                f"exit code {result.returncode}"
            )
        result = run(
            [
                sys.executable,
                "verify_fourteen_vertex_binomial_"
                "support_closure_augmentation.py",
                str(augmentation),
                "--output",
                str(verified_augmentation),
            ]
        )
        if result.returncode != 0:
            raise RuntimeError(
                "deferred support batch audit failed with "
                f"exit code {result.returncode}"
            )
        audit = read_json(verified_augmentation)
        if audit.get("verified") is not True:
            raise RuntimeError(
                "deferred support batch auditor did not certify"
            )
        augmentation_payload = read_json(augmentation)
        materializations.append(
            {
                "through_support": through_support,
                "verified_supports": len(
                    pending_verified_supports
                ),
                "augmentation": str(augmentation),
                "verified_augmentation": str(
                    verified_augmentation
                ),
                "new_support_no_goods": augmentation_payload[
                    "new_support_no_goods"
                ],
                "output_cnf": str(output_cnf),
                "output_cnf_sha256": augmentation_payload[
                    "output_cnf_sha256"
                ],
                "output_clauses": augmentation_payload[
                    "output_clauses"
                ],
            }
        )
        current_cnf = output_cnf
        pending_verified_supports.clear()
        pending_solver_clauses.clear()
        print(
            f"[materialized] through support {through_support}",
            flush=True,
        )

    try:
        for support in range(
            args.start_support, args.maximum_support + 1
        ):
            model_record = Path(
                "tmp",
                f"{args.artifact_prefix}_support{support}_"
                "incremental_sat_model.json",
            )
            partial = Path(
                "tmp",
                f"{args.artifact_prefix}_partial_minimal_circuit_"
                f"lattice_support{support}.json",
            )
            analysis = Path(
                "tmp",
                f"{args.artifact_prefix}_support{support}_"
                "mandatory_unit_binomial_closure.json",
            )
            verified_support = Path(
                "tmp",
                f"{args.artifact_prefix}_support{support}_"
                "mandatory_unit_binomial_closure_verified.json",
            )
            augmentation = Path(
                "tmp",
                f"{args.artifact_prefix}_symmetry_support{support}_"
                "augmentation.json",
            )
            verified_augmentation = Path(
                "tmp",
                f"{args.artifact_prefix}_symmetry_support{support}_"
                "augmentation_verified.json",
            )
            output_cnf = Path(
                args.output_cnf_template.format(support=support)
            )

            analyzer_command = [
                sys.executable,
                "analyze_fourteen_vertex_partial_minimal_circuit_lattice.py",
                "--cnf",
                str(current_cnf),
                "--partition",
                args.partition,
                "--orbit",
                str(args.orbit),
            ]
            if solver is not None:
                selector = 232 + args.orbit
                sat = solver.solve(assumptions=[selector])
                model = solver.get_model() if sat else None
                if not sat or model is None:
                    terminal = {
                        "mode": "selector_unsat",
                        "support": support,
                        "cnf": str(current_cnf),
                    }
                    break
                model_payload = {
                    "status": "incremental_sat_model",
                    "scope": (
                        "orchestrator model only; learned clauses are "
                        "accepted solely after the independent support "
                        "and DIMACS-extension audits"
                    ),
                    "cnf": str(current_cnf),
                    "cnf_sha256": sha256(current_cnf),
                    "selector": selector,
                    "model": model,
                }
                model_record.parent.mkdir(parents=True, exist_ok=True)
                model_record.write_text(
                    json.dumps(model_payload, indent=2) + "\n",
                    encoding="utf-8",
                )
                analyzer_command.extend(
                    ["--model-json", str(model_record)]
                )
            analyzer_command.extend(["--output", str(partial)])

            result = run(analyzer_command)
            if result.returncode != 0:
                if "requested selector is UNSAT" in result.stdout:
                    terminal = {
                        "mode": "selector_unsat",
                        "support": support,
                        "cnf": str(current_cnf),
                    }
                    break
                raise RuntimeError(
                    f"support {support} analysis failed with "
                    f"exit code {result.returncode}"
                )

            result = run(
                [
                    sys.executable,
                    "analyze_fourteen_vertex_partial_circuit_binomial_closure.py",
                    str(partial),
                    "--select-mandatory-unit-core",
                    "--output",
                    str(analysis),
                ]
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"support {support} closure failed with "
                    f"exit code {result.returncode}"
                )
            closure = read_json(analysis)
            if (
                closure.get("status") != "contradiction"
                or closure.get("support_closed") is not True
                or closure.get("selected_mandatory_unit_core") is not True
            ):
                terminal = {
                    "mode": "mandatory_unit_core_open",
                    "support": support,
                    "cnf": str(current_cnf),
                    "partial_analysis": str(partial),
                    "analysis": str(analysis),
                    "analysis_status": closure.get("status"),
                }
                break

            result = run(
                [
                    sys.executable,
                    "verify_fourteen_vertex_partial_circuit_binomial_branch.py",
                    str(analysis),
                    "--output",
                    str(verified_support),
                ]
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"support {support} verification failed with "
                    f"exit code {result.returncode}"
                )
            verified = read_json(verified_support)
            if verified.get("verified") is not True:
                raise RuntimeError(
                    f"support {support} verifier did not certify"
                )

            if args.deferred_materialization:
                clause_set = Path(
                    "tmp",
                    f"{args.artifact_prefix}_symmetry_support{support}_"
                    "clause_set.json",
                )
                verified_clause_set = Path(
                    "tmp",
                    f"{args.artifact_prefix}_symmetry_support{support}_"
                    "clause_set_verified.json",
                )
                result = run(
                    [
                        sys.executable,
                        "tools/generate/augment_fourteen_vertex_rule_cnf_with_"
                        "binomial_support_closures.py",
                        "--base-cnf",
                        str(current_cnf),
                        "--verified-support",
                        str(verified_support),
                        (
                            "--full-support-orbit-closure"
                            if args.full_support_orbit_closure
                            else "--stabilizer-orbit-closure"
                        ),
                        "--clauses-only",
                        "--output",
                        str(clause_set),
                        "--summary-only",
                    ]
                )
                if result.returncode != 0:
                    raise RuntimeError(
                        f"support {support} clause-set generation "
                        f"failed with exit code {result.returncode}"
                    )
                result = run(
                    [
                        sys.executable,
                        "verify_fourteen_vertex_binomial_"
                        "support_closure_augmentation.py",
                        str(clause_set),
                        "--output",
                        str(verified_clause_set),
                    ]
                )
                if result.returncode != 0:
                    raise RuntimeError(
                        f"support {support} clause-set audit failed "
                        f"with exit code {result.returncode}"
                    )
                clause_audit = read_json(verified_clause_set)
                if (
                    clause_audit.get("verified") is not True
                    or clause_audit.get("status")
                    != "binomial_support_no_good_clause_set_verified"
                ):
                    raise RuntimeError(
                        f"support {support} clause-set auditor did not "
                        "certify"
                    )
                clause_payload = read_json(clause_set)
                solver_insertions = 0
                if solver is not None:
                    for raw_clause in clause_payload[
                        "support_no_goods"
                    ]:
                        clause = tuple(map(int, raw_clause))
                        if clause in pending_solver_clauses:
                            continue
                        pending_solver_clauses.add(clause)
                        solver.add_clause(list(clause))
                        solver_insertions += 1
                pending_verified_supports.append(verified_support)
                records.append(
                    {
                        "support": support,
                        "partial_analysis": str(partial),
                        "analysis": str(analysis),
                        "verified_support": str(verified_support),
                        "clause_set": str(clause_set),
                        "verified_clause_set": str(
                            verified_clause_set
                        ),
                        "model_record": (
                            str(model_record)
                            if solver is not None
                            else None
                        ),
                        "selected_initial_relations": verified[
                            "selected_initial_relations"
                        ],
                        "derived_relations": verified[
                            "derived_relations_checked"
                        ],
                        "final_lattice_rank": verified[
                            "final_lattice_rank"
                        ],
                        "target_active_matchings": verified[
                            "target_active_matchings"
                        ],
                        "symmetry_orbit_size": clause_payload[
                            "certificate_symmetry_orbit_sizes"
                        ][0],
                        "candidate_support_no_goods": clause_payload[
                            "candidate_support_no_goods"
                        ],
                        "solver_clause_insertions": solver_insertions,
                    }
                )
                print(
                    f"[certified clause set] support {support}",
                    flush=True,
                )
                if (
                    len(pending_verified_supports)
                    >= args.materialize_every
                ):
                    materialize_pending(support)
            else:
                result = run(
                    [
                        sys.executable,
                        "tools/generate/augment_fourteen_vertex_rule_cnf_with_"
                        "binomial_support_closures.py",
                        "--base-cnf",
                        str(current_cnf),
                        "--verified-support",
                        str(verified_support),
                        (
                            "--full-support-orbit-closure"
                            if args.full_support_orbit_closure
                            else "--stabilizer-orbit-closure"
                        ),
                        "--output-cnf",
                        str(output_cnf),
                        "--output",
                        str(augmentation),
                        "--summary-only",
                    ]
                )
                if result.returncode != 0:
                    raise RuntimeError(
                        f"support {support} augmentation failed with "
                        f"exit code {result.returncode}"
                    )

                result = run(
                    [
                        sys.executable,
                        "verify_fourteen_vertex_binomial_"
                        "support_closure_augmentation.py",
                        str(augmentation),
                        "--output",
                        str(verified_augmentation),
                    ]
                )
                if result.returncode != 0:
                    raise RuntimeError(
                        f"support {support} augmentation audit failed "
                        f"with exit code {result.returncode}"
                    )
                audit = read_json(verified_augmentation)
                if audit.get("verified") is not True:
                    raise RuntimeError(
                        f"support {support} augmentation auditor did "
                        "not certify"
                    )
                augmentation_payload = read_json(augmentation)
                if solver is not None:
                    for clause in augmentation_payload[
                        "support_no_goods"
                    ]:
                        solver.add_clause(list(map(int, clause)))
                records.append(
                    {
                        "support": support,
                        "partial_analysis": str(partial),
                        "analysis": str(analysis),
                        "verified_support": str(verified_support),
                        "augmentation": str(augmentation),
                        "verified_augmentation": str(
                            verified_augmentation
                        ),
                        "model_record": (
                            str(model_record)
                            if solver is not None
                            else None
                        ),
                        "selected_initial_relations": verified[
                            "selected_initial_relations"
                        ],
                        "derived_relations": verified[
                            "derived_relations_checked"
                        ],
                        "final_lattice_rank": verified[
                            "final_lattice_rank"
                        ],
                        "target_active_matchings": verified[
                            "target_active_matchings"
                        ],
                        "symmetry_orbit_size": augmentation_payload[
                            "certificate_symmetry_orbit_sizes"
                        ][0],
                        "new_support_no_goods": augmentation_payload[
                            "new_support_no_goods"
                        ],
                        "output_cnf": str(output_cnf),
                        "output_cnf_sha256": augmentation_payload[
                            "output_cnf_sha256"
                        ],
                        "output_clauses": augmentation_payload[
                            "output_clauses"
                        ],
                    }
                )
                current_cnf = output_cnf
                print(f"[certified] support {support}", flush=True)
        if (
            args.deferred_materialization
            and pending_verified_supports
        ):
            materialize_pending(int(records[-1]["support"]))
            if terminal.get("mode") == "selector_unsat":
                terminal["cnf"] = str(current_cnf)
    finally:
        if solver_context is not None:
            solver_context.delete()

    payload = {
        "status": "symmetry_binomial_cegar_stopped",
        "scope": (
            "bounded selector-support iteration with independent "
            "mandatory-unit and symmetry-closed DIMACS audits"
        ),
        "partition": [int(item) for item in args.partition.split(",")],
        "orbit": args.orbit,
        "start_support": args.start_support,
        "maximum_support": args.maximum_support,
        "incremental_solver": args.incremental_solver,
        "deferred_materialization": args.deferred_materialization,
        "materialize_every": args.materialize_every,
        "full_support_orbit_closure": (
            args.full_support_orbit_closure
        ),
        "initial_cnf": str(args.base_cnf),
        "certified_supports": len(records),
        "new_support_no_goods": (
            sum(
                int(record["new_support_no_goods"])
                for record in materializations
            )
            if args.deferred_materialization
            else sum(
                int(record["new_support_no_goods"])
                for record in records
            )
        ),
        "records": records,
        "materializations": materializations,
        "terminal": terminal,
        "final_cnf": str(current_cnf),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
