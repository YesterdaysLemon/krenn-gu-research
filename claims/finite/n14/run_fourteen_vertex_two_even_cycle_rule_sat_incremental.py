"""Incrementally learn two-even-cycle factor-fork transport no-goods."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF
from pysat.solvers import Solver

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    Factor,
    activation_literals,
    edge_variable,
    parse_factor,
    transform_colouring,
    transform_factor,
    validate_simple_certificate,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
    full_automorphisms,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges


def certificate_no_goods(
    factors: Sequence[Factor],
    colourings: Sequence[Sequence[int]],
    representative_id: dict[Factor, int],
    selector_variables: Sequence[int],
    actions: Sequence[dict[int, int]],
    eligible_edges: Sequence[tuple[int, int]],
) -> set[tuple[int, ...]]:
    first_orbit = representative_id.get(factors[0])
    if first_orbit is None:
        raise AssertionError(
            "source first factor is not its pinned representative"
        )
    selector = selector_variables[first_orbit]
    output: set[tuple[int, ...]] = set()
    for action in actions:
        if transform_factor(factors[0], action) != factors[0]:
            continue
        moved_factors = tuple(
            transform_factor(factor, action) for factor in factors
        )
        for permutation in ((0, 1, 2), (0, 2, 1)):
            moved_colourings = tuple(
                transform_colouring(colouring, action, permutation)
                for colouring in colourings
            )
            conditions: dict[int, bool] = {}
            for old_role in (1, 2):
                new_role = permutation[old_role]
                for variable, value in activation_literals(
                    new_role,
                    moved_factors[old_role],
                    moved_colourings,
                    eligible_edges,
                ).items():
                    previous = conditions.get(variable)
                    if previous is not None and previous != value:
                        raise AssertionError(
                            "transport conditions conflict"
                        )
                    conditions[variable] = value
            clause = [-selector]
            clause.extend(
                -variable if value else variable
                for variable, value in conditions.items()
            )
            normalized = tuple(
                sorted(set(clause), key=lambda item: (abs(item), item))
            )
            if any(-literal in normalized for literal in normalized):
                raise AssertionError("transport no-good became tautological")
            output.add(normalized)
    return output


def minimum_condition_no_goods(
    factors: Sequence[Factor],
    conditions: Sequence[Sequence[object]],
    representative_id: dict[Factor, int],
    selector_variables: Sequence[int],
    actions: Sequence[dict[int, int]],
    eligible_edges: Sequence[tuple[int, int]],
) -> set[tuple[int, ...]]:
    """Transport an independently verified partial activity assignment."""

    first_orbit = representative_id.get(factors[0])
    if first_orbit is None:
        raise AssertionError(
            "source first factor is not its pinned representative"
        )
    selector = selector_variables[first_orbit]
    edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    decoded = []
    for raw_variable, raw_value in conditions:
        variable = int(raw_variable)
        zero = variable - 1
        role, item_id = divmod(zero, len(eligible_edges))
        if role not in (1, 2) or item_id >= len(eligible_edges):
            raise AssertionError(
                "minimum activity condition variable changed"
            )
        decoded.append(
            (role, eligible_edges[item_id], bool(raw_value))
        )
    output: set[tuple[int, ...]] = set()
    for action in actions:
        if transform_factor(factors[0], action) != factors[0]:
            continue
        for permutation in ((0, 1, 2), (0, 2, 1)):
            moved: dict[int, bool] = {}
            for role, item, value in decoded:
                moved_role = permutation[role]
                moved_item = tuple(
                    sorted((action[item[0]], action[item[1]]))
                )
                moved_variable = edge_variable(
                    moved_role,
                    edge_id[moved_item],
                    len(eligible_edges),
                )
                previous = moved.get(moved_variable)
                if previous is not None and previous != value:
                    raise AssertionError(
                        "transported minimum conditions conflict"
                    )
                moved[moved_variable] = value
            output.add(
                tuple(
                    sorted(
                        {
                            -selector,
                            *(
                                -variable if value else variable
                                for variable, value in moved.items()
                            ),
                        },
                        key=lambda item: (abs(item), item),
                    )
                )
            )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiled-cnf", type=Path, required=True)
    parser.add_argument("--compiled-result", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument("--candidate-bases", type=int, default=1000)
    parser.add_argument(
        "--refine-candidate-bases", type=int, default=10000
    )
    parser.add_argument(
        "--refine-score-threshold", type=int, default=8
    )
    parser.add_argument(
        "--structural-minimum",
        action="store_true",
        help=(
            "minimize activity premises relative to perfect-matching and "
            "edge-disjointness constraints"
        ),
    )
    parser.add_argument(
        "--connected-structural-minimum",
        action="store_true",
        help=(
            "also minimize relative to the required connected support "
            "union"
        ),
    )
    parser.add_argument(
        "--three-connected-structural-minimum",
        action="store_true",
        help=(
            "minimize relative to the unconditional Krenn-Gu necessary "
            "condition that skeleton vertex connectivity is at least 3"
        ),
    )
    parser.add_argument(
        "--certificates-per-support",
        type=int,
        default=1,
        help=(
            "learn this many distinct factor-fork rules from each SAT "
            "residual support"
        ),
    )
    parser.add_argument("--orbit-min", type=int, default=0)
    parser.add_argument("--orbit-max", type=int)
    parser.add_argument(
        "--prefix",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_even_cycle_rule_sat_incremental"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_even_cycle_"
            "rule_sat_incremental_chain.json"
        ),
    )
    args = parser.parse_args()
    if args.rounds < 1:
        raise ValueError("--rounds must be positive")
    if args.candidate_bases < 1:
        raise ValueError("--candidate-bases must be positive")
    if args.refine_candidate_bases < args.candidate_bases:
        raise ValueError(
            "--refine-candidate-bases must be at least --candidate-bases"
        )
    if args.refine_score_threshold < 1:
        raise ValueError("--refine-score-threshold must be positive")
    if args.certificates_per_support < 1:
        raise ValueError(
            "--certificates-per-support must be positive"
        )

    started = time.perf_counter()
    compiled = json.loads(
        args.compiled_result.read_text(encoding="utf-8")
    )
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, census["partition"]))
    if tuple(map(int, compiled["partition"])) != lengths:
        raise AssertionError("compiled result and census partitions differ")
    if (
        len(lengths) != 2
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("partition is not two even cycles")
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
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    edge_variable_count = 3 * len(eligible_edges)
    selector_variables = tuple(
        edge_variable_count + 1 + index
        for index in range(len(representatives))
    )
    orbit_max = (
        len(representatives) - 1
        if args.orbit_max is None
        else args.orbit_max
    )
    if not (
        0 <= args.orbit_min <= orbit_max < len(representatives)
    ):
        raise ValueError("orbit range is outside the census")
    actions = full_automorphisms(cycles)
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("full-factor automorphism count changed")

    cnf = CNF(from_file=str(args.compiled_cnf))
    if args.orbit_min != 0 or orbit_max != len(representatives) - 1:
        cnf.append(
            list(
                selector_variables[args.orbit_min : orbit_max + 1]
            )
        )
    known_clauses = {
        tuple(
            sorted(
                set(map(int, clause)),
                key=lambda item: (abs(item), item),
            )
        )
        for clause in cnf.clauses
    }
    survivors: list[dict[str, object]] = []
    iterations: list[dict[str, object]] = []
    added_clauses: set[tuple[int, ...]] = set()
    terminal_status = "round_limit"
    samples_path = Path(f"{args.prefix}_samples.json")
    analysis_pattern = f"{args.prefix}_{{index}}_factor_fork.json"
    final_cnf = Path(f"{args.prefix}_final.cnf")

    with Solver(
        name="cadical195", bootstrap_with=cnf.clauses
    ) as solver:
        for iteration in range(args.rounds):
            sat = solver.solve()
            if not sat:
                iterations.append(
                    {
                        "iteration": iteration,
                        "sat": False,
                        "incremental_no_goods": len(added_clauses),
                    }
                )
                terminal_status = "UNSAT"
                break
            model = solver.get_model()
            if model is None:
                raise AssertionError("SAT solver returned no model")
            positive = {literal for literal in model if literal > 0}
            factors = []
            for colour in range(3):
                factor = tuple(
                    item
                    for edge_id, item in enumerate(eligible_edges)
                    if edge_variable(
                        colour, edge_id, len(eligible_edges)
                    )
                    in positive
                )
                if len(factor) != N // 2:
                    raise AssertionError(
                        "SAT model is not a perfect matching"
                    )
                factors.append(factor)
            selected_orbits = [
                index
                for index, selector in enumerate(selector_variables)
                if selector in positive
            ]
            if len(selected_orbits) != 1:
                raise AssertionError(
                    "SAT model has no unique orbit selector"
                )
            survivor = {
                "orbit_id": selected_orbits[0],
                "first": [list(item) for item in factors[0]],
                "second": [list(item) for item in factors[1]],
                "third": [list(item) for item in factors[2]],
            }
            survivors.append(survivor)
            samples_payload = {
                "status": "two_even_cycle_rule_sat_incremental_samples",
                "partition": list(lengths),
                "source_census": str(args.census),
                "survivors": survivors,
                "exploratory_only": True,
            }
            samples_path.parent.mkdir(parents=True, exist_ok=True)
            samples_path.write_text(
                json.dumps(samples_payload, indent=2) + "\n",
                encoding="utf-8",
            )
            survivor_index = len(survivors) - 1
            analysis_path = Path(
                analysis_pattern.format(index=survivor_index)
            )
            subprocess.run(
                [
                    sys.executable,
                    str(HERE / "analyze_fourteen_vertex_two_even_cycle_fork.py"),
                    str(samples_path),
                    "--survivor-index",
                    str(survivor_index),
                    "--candidate-bases",
                    str(args.candidate_bases),
                    "--target-policy",
                    "first",
                    "--certificates-per-support",
                    str(args.certificates_per_support),
                    "--output",
                    str(analysis_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            analysis = json.loads(
                analysis_path.read_text(encoding="utf-8")
            )
            status = str(analysis["status"])
            initial_score = analysis.get(
                "certificate_activation_constraint_score"
            )
            if (
                status == "two_even_cycle_factor_fork"
                and isinstance(initial_score, int)
                and initial_score > args.refine_score_threshold
                and args.refine_candidate_bases > args.candidate_bases
            ):
                subprocess.run(
                    [
                        sys.executable,
                        str(HERE / "analyze_fourteen_vertex_two_even_cycle_fork.py"),
                        str(samples_path),
                        "--survivor-index",
                        str(survivor_index),
                        "--candidate-bases",
                        str(args.refine_candidate_bases),
                        "--target-policy",
                        "first-min",
                        "--certificates-per-support",
                        str(args.certificates_per_support),
                        "--output",
                        str(analysis_path),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                analysis = json.loads(
                    analysis_path.read_text(encoding="utf-8")
                )
                status = str(analysis["status"])
            row: dict[str, object] = {
                "iteration": iteration,
                "sat": True,
                "orbit_id": selected_orbits[0],
                "analysis_status": status,
                "initial_activation_score": initial_score,
                "final_activation_score": analysis.get(
                    "certificate_activation_constraint_score"
                ),
                "target_policy": analysis.get("target_policy"),
                "incremental_no_goods_before": len(added_clauses),
            }
            if status != "two_even_cycle_factor_fork":
                iterations.append(row)
                terminal_status = status
                print(json.dumps(row), flush=True)
                break
            candidate_rows = analysis.get(
                "certificate_candidates"
            ) or [
                {
                    "activation_constraint_score": analysis[
                        "certificate_activation_constraint_score"
                    ],
                    "certificate": analysis["certificate"],
                }
            ]
            new_clauses: set[tuple[int, ...]] = set()
            minimum_rows: list[dict[str, object]] = []
            validated_factors = None
            for candidate_id, candidate_row in enumerate(
                candidate_rows
            ):
                if candidate_id == 0:
                    candidate_path = analysis_path
                    candidate_analysis = analysis
                else:
                    candidate_path = Path(
                        f"{args.prefix}_{survivor_index}_"
                        f"factor_fork_candidate{candidate_id}.json"
                    )
                    candidate_analysis = dict(analysis)
                    candidate_analysis["certificate"] = candidate_row[
                        "certificate"
                    ]
                    candidate_analysis[
                        "certificate_activation_constraint_score"
                    ] = int(
                        candidate_row[
                            "activation_constraint_score"
                        ]
                    )
                    candidate_path.write_text(
                        json.dumps(candidate_analysis, indent=2) + "\n",
                        encoding="utf-8",
                    )
                candidate_factors, _candidate_colourings = (
                    validate_simple_certificate(
                        candidate_analysis,
                        survivor,
                        cycles,
                        full_edges,
                    )
                )
                if validated_factors is None:
                    validated_factors = candidate_factors
                elif candidate_factors != validated_factors:
                    raise AssertionError(
                        "candidate singleton factors changed"
                    )
                suffix = (
                    ""
                    if len(candidate_rows) == 1
                    else f"_candidate{candidate_id}"
                )
                minimum_path = Path(
                    f"{args.prefix}_{survivor_index}{suffix}_"
                    "minimum_activity.json"
                )
                minimum_audit_path = Path(
                    f"{args.prefix}_{survivor_index}{suffix}_"
                    "minimum_activity_verified.json"
                )
                minimum_command = [
                    sys.executable,
                    str(
                        HERE
                        / "minimize_fourteen_vertex_two_even_cycle_"
                        "certificate_activation.py"
                    ),
                    str(samples_path),
                    str(candidate_path),
                    "--survivor-index",
                    str(survivor_index),
                    "--output",
                    str(minimum_path),
                ]
                if args.three_connected_structural_minimum:
                    minimum_command.append(
                        "--three-connected-structural-feasibility"
                    )
                elif args.connected_structural_minimum:
                    minimum_command.append(
                        "--connected-structural-feasibility"
                    )
                elif args.structural_minimum:
                    minimum_command.append(
                        "--structural-feasibility"
                    )
                subprocess.run(
                    minimum_command,
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                subprocess.run(
                    [
                        sys.executable,
                        str(
                            HERE
                            / "verify_fourteen_vertex_two_even_cycle_"
                            "minimum_activity_certificate.py"
                        ),
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
                if minimum_audit.get("verified") is not True:
                    raise AssertionError(
                        "minimum activity audit did not verify"
                    )
                generated = minimum_condition_no_goods(
                    candidate_factors,
                    minimum["activation_conditions"],
                    representative_id,
                    selector_variables,
                    actions,
                    eligible_edges,
                )
                new_clauses.update(generated)
                minimum_rows.append(
                    {
                        "candidate_id": candidate_id,
                        "analysis": str(candidate_path),
                        "analysis_activation_score": int(
                            candidate_row[
                                "activation_constraint_score"
                            ]
                        ),
                        "minimum_activity_score": int(
                            minimum[
                                "activation_constraint_score"
                            ]
                        ),
                        "minimum_activity_certificate": str(
                            minimum_path
                        ),
                        "minimum_activity_audit": str(
                            minimum_audit_path
                        ),
                        "transport_clauses": len(generated),
                    }
                )
            if validated_factors is None:
                raise AssertionError(
                    "factor fork has no retained certificate"
                )
            row["certificate_mode"] = (
                "verified_minimum_activity_factor_fork"
            )
            row["certificate_candidates_used"] = len(minimum_rows)
            row["minimum_activity_scores"] = [
                item["minimum_activity_score"]
                for item in minimum_rows
            ]
            row["minimum_activity_candidates"] = minimum_rows
            if len(minimum_rows) == 1:
                row["minimum_activity_score"] = minimum_rows[0][
                    "minimum_activity_score"
                ]
                row["minimum_activity_certificate"] = minimum_rows[0][
                    "minimum_activity_certificate"
                ]
                row["minimum_activity_audit"] = minimum_rows[0][
                    "minimum_activity_audit"
                ]
            genuinely_new = new_clauses - known_clauses
            if not genuinely_new:
                raise AssertionError(
                    "new SAT model produced no new transport clause"
                )
            for clause in genuinely_new:
                solver.add_clause(list(clause))
                cnf.append(list(clause))
            added_clauses.update(genuinely_new)
            known_clauses.update(genuinely_new)
            row["new_no_goods"] = len(genuinely_new)
            row["incremental_no_goods_after"] = len(added_clauses)
            iterations.append(row)
            print(json.dumps(row), flush=True)

    final_cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(final_cnf))
    payload = {
        "status": terminal_status,
        "partition": list(lengths),
        "orbit_range": [args.orbit_min, orbit_max],
        "initial_simple_sources": compiled["simple_sources_replayed"],
        "initial_transport_no_goods": compiled[
            "deduplicated_transport_no_goods"
        ],
        "initial_cnf_clauses": compiled["cnf_clauses"],
        "incremental_no_goods": len(added_clauses),
        "final_cnf_clauses": len(cnf.clauses),
        "iterations": iterations,
        "new_samples": len(survivors),
        "samples": str(samples_path),
        "analysis_pattern": analysis_pattern,
        "initial_cnf": str(args.compiled_cnf),
        "final_cnf": str(final_cnf),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": terminal_status != "UNSAT",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
