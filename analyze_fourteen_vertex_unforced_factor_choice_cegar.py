"""Global factor-choice CEGAR for one all-even order-14 support.

Unlike the forced-slice analysis, this program keeps every full-cycle
binomial cancellation as a Boolean choice.

* A full-only forbidden amplitude contributes one clause over its cycle
  binomials.
* If one of those binomials vanishes, a full-containing ten-term
  amplitude forces its two extra monomials to cancel.
* Under the same premise, a factorable twelve-term amplitude forces one
  of the two Laurent directions of its four-extra parallelogram.
* Larger full-containing amplitudes are exact signed-lattice targets once
  at least one of their cycle binomials has been selected.

Every Boolean branch is checked by exact integer lattice arithmetic.
UNSAT is a support-local obstruction; SAT is only a surviving necessary
condition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from array import array
from collections import deque
from pathlib import Path
from typing import Sequence

import numpy as np
from pysat.solvers import Solver

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_even_cycle_double_pair_fork import (
    activity_arrays,
)
from analyze_fourteen_vertex_forced_slice_factor_cegar import (
    SparseRelation,
    dense_relation,
    difference,
    extras_at,
    full_containing_indices,
    monomial_variables,
    parallelogram_directions,
    selected_lattice_conflict,
)
from explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cycle_relation(
    cycle: Sequence[int],
    colouring: Sequence[int],
    labels: dict[tuple[int, int], int],
    full_edges: frozenset[tuple[int, int]],
) -> SparseRelation:
    edges = tuple(
        engine.edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )
    vectors = [
        monomial_variables(
            matching, colouring, labels, full_edges
        )
        for matching in (edges[0::2], edges[1::2])
    ]
    relation = difference(vectors[0], vectors[1])
    if not relation:
        raise AssertionError("cycle alternatings became one monomial")
    return relation


def build_dual_horn_index(
    clauses: Sequence[Sequence[int]],
) -> tuple[list[list[int]], bytearray, array]:
    """Index a dual-Horn CNF for deterministic false propagation."""

    variable_count = max(
        (
            abs(int(literal))
            for clause in clauses
            for literal in clause
        ),
        default=0,
    )
    positive_occurrences: list[list[int]] = [
        [] for _ in range(variable_count + 1)
    ]
    positive_counts = bytearray(len(clauses))
    negative_antecedents = array("i", [0]) * len(clauses)
    for clause_index, clause in enumerate(clauses):
        negatives = [
            -int(literal) for literal in clause if int(literal) < 0
        ]
        if len(negatives) > 1:
            raise ValueError("formula is not dual-Horn")
        if negatives:
            negative_antecedents[clause_index] = negatives[0]
        positives = [
            int(literal) for literal in clause if int(literal) > 0
        ]
        if len(positives) > 255:
            raise ValueError("dual-Horn clause is unexpectedly wide")
        positive_counts[clause_index] = len(positives)
        for variable in positives:
            positive_occurrences[variable].append(clause_index)
    return (
        positive_occurrences,
        positive_counts,
        negative_antecedents,
    )


def dual_horn_forcing_core(
    clauses: Sequence[Sequence[int]],
    target_variable: int,
    index: tuple[list[list[int]], bytearray, array] | None = None,
) -> dict[str, object] | None:
    """Prove that one variable is true in every dual-Horn model.

    Seed the canonical maximal-model algorithm with the target set false.
    Whenever all positive literals of ``-a | b_1 | ... | b_k`` are
    false, it must also set ``a`` false.  Reaching an all-positive clause
    whose literals are all false gives a deterministic contradiction.
    The returned reason DAG is a small independently replayable core.
    """

    if target_variable < 1:
        raise ValueError("target variables are one-based")
    if index is None:
        index = build_dual_horn_index(clauses)
    occurrences, initial_counts, antecedents = index
    if target_variable >= len(occurrences):
        raise ValueError("target variable is outside the formula")

    counts = bytearray(initial_counts)
    false_variables = {target_variable}
    reasons: dict[int, int] = {}
    queue: deque[int] = deque([target_variable])
    terminal_clause = None
    for clause_index, count in enumerate(counts):
        if count:
            continue
        antecedent = int(antecedents[clause_index])
        if antecedent == 0:
            terminal_clause = clause_index
            break
        if antecedent not in false_variables:
            false_variables.add(antecedent)
            reasons[antecedent] = clause_index
            queue.append(antecedent)
    while queue and terminal_clause is None:
        variable = queue.popleft()
        for clause_index in occurrences[variable]:
            if counts[clause_index] == 0:
                continue
            counts[clause_index] -= 1
            if counts[clause_index]:
                continue
            antecedent = int(antecedents[clause_index])
            if antecedent == 0:
                terminal_clause = clause_index
                break
            if antecedent not in false_variables:
                false_variables.add(antecedent)
                reasons[antecedent] = clause_index
                queue.append(antecedent)
    if terminal_clause is None:
        return None

    core_indices = {terminal_clause}
    needed = deque(
        int(literal)
        for literal in clauses[terminal_clause]
        if int(literal) > 0
    )
    while needed:
        variable = needed.popleft()
        if variable == target_variable:
            continue
        reason = reasons.get(variable)
        if reason is None:
            raise AssertionError(
                "false-propagation trace lost a variable reason"
            )
        if reason in core_indices:
            continue
        core_indices.add(reason)
        needed.extend(
            int(literal)
            for literal in clauses[reason]
            if int(literal) > 0
        )
    return {
        "target_variable": target_variable,
        "false_closure_size": len(false_variables),
        "terminal_positive_clause_index": terminal_clause,
        "core_factor_clause_indices": sorted(core_indices),
    }


def dual_horn_unsat_core(
    clauses: Sequence[Sequence[int]],
    index: tuple[list[list[int]], bytearray, array] | None = None,
) -> dict[str, object] | None:
    """Extract a deterministic core when a dual-Horn CNF is itself UNSAT."""

    if index is None:
        index = build_dual_horn_index(clauses)
    occurrences, initial_counts, antecedents = index
    counts = bytearray(initial_counts)
    false_variables: set[int] = set()
    reasons: dict[int, int] = {}
    queue: deque[int] = deque()
    terminal_clause = None
    for clause_index, count in enumerate(counts):
        if count:
            continue
        antecedent = int(antecedents[clause_index])
        if antecedent == 0:
            terminal_clause = clause_index
            break
        if antecedent not in false_variables:
            false_variables.add(antecedent)
            reasons[antecedent] = clause_index
            queue.append(antecedent)
    while queue and terminal_clause is None:
        variable = queue.popleft()
        for clause_index in occurrences[variable]:
            if counts[clause_index] == 0:
                continue
            counts[clause_index] -= 1
            if counts[clause_index]:
                continue
            antecedent = int(antecedents[clause_index])
            if antecedent == 0:
                terminal_clause = clause_index
                break
            if antecedent not in false_variables:
                false_variables.add(antecedent)
                reasons[antecedent] = clause_index
                queue.append(antecedent)
    if terminal_clause is None:
        return None

    core_indices = {terminal_clause}
    needed = deque(
        int(literal)
        for literal in clauses[terminal_clause]
        if int(literal) > 0
    )
    while needed:
        variable = needed.popleft()
        reason = reasons.get(variable)
        if reason is None:
            raise AssertionError(
                "dual-Horn UNSAT trace lost a variable reason"
            )
        if reason in core_indices:
            continue
        core_indices.add(reason)
        needed.extend(
            int(literal)
            for literal in clauses[reason]
            if int(literal) > 0
        )
    return {
        "false_closure_size": len(false_variables),
        "terminal_positive_clause_index": terminal_clause,
        "core_factor_clause_indices": sorted(core_indices),
    }


def one_extra_cycle_blocking_clauses(
    trigger_ids: Sequence[int], extra_count: int
) -> tuple[tuple[int, ...], ...]:
    """Return the direct blocks from a one-extra target amplitude.

    Cancelling any full-cycle binomial makes the factored full-only
    contribution vanish.  If exactly one additional monomial remains, the
    forbidden amplitude cannot be zero, independently of every other
    signed relation.
    """

    if extra_count != 1:
        return ()
    return tuple(
        (-(int(trigger_id) + 1),)
        for trigger_id in sorted(set(map(int, trigger_ids)))
    )


def is_forbidden_equation(equation: int) -> bool:
    """Return false for the three required monochromatic amplitudes."""

    return len(set(engine.indexed_colouring(int(equation)))) > 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--maximum-activity", type=int, default=21)
    parser.add_argument(
        "--target-activities",
        default="13,15,21",
        help="comma-separated full-containing activity levels",
    )
    parser.add_argument("--max-models", type=int, default=0)
    parser.add_argument(
        "--solver",
        default="cadical195",
        choices=("cadical195", "glucose4", "maplechrono"),
    )
    parser.add_argument(
        "--compact-output",
        action="store_true",
        help=(
            "omit the multi-million-clause provenance tables while "
            "retaining relations, learned clauses, and exact branches"
        ),
    )
    parser.add_argument(
        "--dual-horn-core",
        action="store_true",
        help=(
            "extract a deterministic forcing core for a terminal "
            "single signed-lattice blocking clause"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_unforced_factor_choice_cegar.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    cycles = contiguous_cycles(lengths)
    if (
        sum(lengths) != 14
        or len(cycles) < 2
        or any(len(cycle) % 2 for cycle in cycles)
    ):
        raise ValueError("this analysis requires an all-even partition")
    target_activities = tuple(
        sorted(
            {
                int(item)
                for item in args.target_activities.split(",")
                if item.strip()
            }
        )
    )
    baseline = 1 << len(cycles)
    if any(
        level <= baseline or level > args.maximum_activity
        for level in target_activities
    ):
        raise ValueError("invalid target activity level")

    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = full_edges
    factors = [
        tuple(engine.edge(*map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    matchings = engine.perfect_matchings(set(full_edges) | set(labels))
    full_only = frozenset(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    if len(full_only) != baseline:
        raise AssertionError("full-only matching count changed")

    support_variables = sorted(
        {
            9 * engine.EDGE_INDEX[item]
            + 3 * first_colour
            + second_colour
            for item in full_edges
            for first_colour in range(3)
            for second_colour in range(3)
        }
        | {
            9 * engine.EDGE_INDEX[item] + 4 * colour
            for item, colour in labels.items()
        }
    )
    variable_positions = {
        variable: position
        for position, variable in enumerate(support_variables)
    }
    counts, slots, total_extensions = activity_arrays(
        matchings, labels, args.maximum_activity
    )

    relation_index: dict[SparseRelation, int] = {}
    relations: list[SparseRelation] = []
    origins: list[dict[str, object]] = []
    clauses: set[tuple[int, ...]] = set()
    clause_origins: dict[tuple[int, ...], dict[str, object]] = {}
    clause_equations: dict[tuple[int, ...], int] = {}

    def record_clause(
        clause: tuple[int, ...],
        origin: dict[str, object],
    ) -> None:
        clauses.add(clause)
        if args.dual_horn_core:
            clause_equations.setdefault(
                clause, int(origin["equation_index"])
            )
        if not args.compact_output:
            clause_origins.setdefault(clause, origin)

    def relation_id(
        relation: SparseRelation,
        origin: dict[str, object],
    ) -> int:
        if relation not in relation_index:
            relation_index[relation] = len(relations)
            relations.append(relation)
            origins.append(origin)
        return relation_index[relation]

    def cycle_ids_at(equation: int) -> tuple[int, ...]:
        colouring = engine.indexed_colouring(equation)
        return tuple(
            relation_id(
                cycle_relation(
                    cycle, colouring, labels, full_edges
                ),
                {
                    "certificate_mode": "full_cycle_binomial",
                    "cycle_id": cycle_id,
                    "cycle": list(cycle),
                    "equation_index": equation,
                },
            )
            for cycle_id, cycle in enumerate(cycles)
        )

    base_indices = full_containing_indices(
        counts, slots, full_only, baseline
    )
    base_equation_count = 0
    for equation_value in base_indices:
        equation = int(equation_value)
        if not is_forbidden_equation(equation):
            continue
        base_equation_count += 1
        ids = cycle_ids_at(equation)
        clause = tuple(sorted({item_id + 1 for item_id in ids}))
        record_clause(
            clause,
            {
                "certificate_mode": "full_only_cycle_factorization",
                "equation_index": equation,
                "cycle_relation_ids": list(ids),
            },
        )

    ten_indices = full_containing_indices(
        counts, slots, full_only, baseline + 2
    )
    ten_equation_count = 0
    for equation_value in ten_indices:
        equation = int(equation_value)
        colouring = engine.indexed_colouring(equation)
        if not is_forbidden_equation(equation):
            continue
        ten_equation_count += 1
        extras = extras_at(
            equation, baseline + 2, slots, full_only
        )
        vectors = tuple(
            monomial_variables(
                matchings[matching_id],
                colouring,
                labels,
                full_edges,
            )
            for matching_id in extras
        )
        extra_relation = difference(vectors[0], vectors[1])
        if not extra_relation:
            raise AssertionError(
                "two extra matchings became one monomial"
            )
        extra_id = relation_id(
            extra_relation,
            {
                "certificate_mode": "two_extra_relation",
                "equation_index": equation,
                "matching_ids": list(extras),
            },
        )
        for cycle_id in cycle_ids_at(equation):
            clause = (-(cycle_id + 1), extra_id + 1)
            record_clause(
                clause,
                {
                    "certificate_mode": (
                        "cycle_cancellation_implies_two_extra_relation"
                    ),
                    "equation_index": equation,
                    "cycle_relation_id": cycle_id,
                    "extra_relation_id": extra_id,
                    "matching_ids": list(extras),
                },
            )

    twelve_indices = full_containing_indices(
        counts, slots, full_only, baseline + 4
    )
    factorable_twelve = 0
    nonfactorable_twelve = 0
    twelve_equation_count = 0
    literal_impossibility = None
    for equation_value in twelve_indices:
        equation = int(equation_value)
        colouring = engine.indexed_colouring(equation)
        if not is_forbidden_equation(equation):
            continue
        twelve_equation_count += 1
        extras = extras_at(
            equation, baseline + 4, slots, full_only
        )
        vectors = tuple(
            monomial_variables(
                matchings[matching_id],
                colouring,
                labels,
                full_edges,
            )
            for matching_id in extras
        )
        directions = parallelogram_directions(vectors)
        if directions is None:
            nonfactorable_twelve += 1
            continue
        factorable_twelve += 1
        if not directions:
            for cycle_id in cycle_ids_at(equation):
                clause = (-(cycle_id + 1),)
                record_clause(
                    clause,
                    {
                        "certificate_mode": (
                            "four_identical_extras_forbid_cycle_"
                            "cancellation"
                        ),
                        "equation_index": equation,
                        "cycle_relation_id": cycle_id,
                        "matching_ids": list(extras),
                    },
                )
            continue
        direction_ids = tuple(
            sorted(
                {
                    relation_id(
                        relation,
                        {
                            "certificate_mode": (
                                "four_extra_parallelogram_factor"
                            ),
                            "equation_index": equation,
                            "matching_ids": list(extras),
                        },
                    )
                    for relation in directions
                }
            )
        )
        for cycle_id in cycle_ids_at(equation):
            clause = (
                -(cycle_id + 1),
                *(item_id + 1 for item_id in direction_ids),
            )
            record_clause(
                clause,
                {
                    "certificate_mode": (
                        "cycle_cancellation_implies_four_extra_factor"
                    ),
                    "equation_index": equation,
                    "cycle_relation_id": cycle_id,
                    "direction_relation_ids": list(direction_ids),
                    "matching_ids": list(extras),
                },
            )

    relation_rows = [
        dense_relation(relation, variable_positions)
        for relation in relations
    ]
    target_rows = []
    target_level_counts: dict[int, int] = {}
    for level in target_activities:
        indices = full_containing_indices(
            counts, slots, full_only, level
        )
        target_level_counts[level] = 0
        for equation_value in indices:
            equation = int(equation_value)
            colouring = engine.indexed_colouring(equation)
            if not is_forbidden_equation(equation):
                continue
            target_level_counts[level] += 1
            extras = extras_at(
                equation, level, slots, full_only
            )
            vectors = tuple(
                monomial_variables(
                    matchings[matching_id],
                    colouring,
                    labels,
                    full_edges,
                )
                for matching_id in extras
            )
            trigger_ids = cycle_ids_at(equation)
            for clause in one_extra_cycle_blocking_clauses(
                trigger_ids, len(extras)
            ):
                record_clause(
                    clause,
                    {
                        "certificate_mode": (
                            "one_extra_forbids_cycle_cancellation"
                        ),
                        "equation_index": equation,
                        "cycle_relation_id": -clause[0] - 1,
                        "matching_ids": list(extras),
                    },
                )
            target_rows.append(
                (equation, extras, vectors, trigger_ids)
            )

    sorted_clauses = sorted(clauses, key=lambda row: (len(row), row))
    learned: list[list[int]] = []
    branches: list[dict[str, object]] = []
    terminal_status = "literal_contradiction"
    if literal_impossibility is None:
        terminal_status = "running"
        with Solver(
            name=args.solver, bootstrap_with=sorted_clauses
        ) as solver:
            solver.set_phases(
                [-(index + 1) for index in range(len(relations))]
            )
            while solver.solve():
                model = set(solver.get_model())
                selected_ids = [
                    index
                    for index in range(len(relations))
                    if index + 1 in model
                ]
                selected_set = set(selected_ids)
                active_targets = []
                trigger_by_equation: dict[int, int] = {}
                for (
                    equation,
                    matching_ids,
                    vectors,
                    trigger_ids,
                ) in target_rows:
                    selected_triggers = sorted(
                        selected_set & set(trigger_ids)
                    )
                    if not selected_triggers:
                        continue
                    trigger_by_equation[equation] = selected_triggers[0]
                    active_targets.append(
                        (equation, matching_ids, vectors)
                    )
                certificate = selected_lattice_conflict(
                    selected_ids,
                    relations,
                    relation_rows,
                    variable_positions,
                    active_targets,
                )
                if certificate is None:
                    terminal_status = "survivor"
                    branches.append(
                        {
                            "selected_relation_ids": selected_ids,
                            "active_target_rows": len(active_targets),
                            "certificate": None,
                        }
                    )
                    break
                blocking_ids = set(
                    map(int, certificate["basis_relation_ids"])
                )
                if certificate["certificate_mode"] == (
                    "inconsistent_factor_sign"
                ):
                    blocking_ids.add(
                        int(certificate["target_relation_id"])
                    )
                else:
                    equation = int(
                        certificate["target_equation_index"]
                    )
                    trigger_id = trigger_by_equation[equation]
                    certificate["target_trigger_relation_id"] = (
                        trigger_id
                    )
                    blocking_ids.add(trigger_id)
                clause = [
                    -(index + 1) for index in sorted(blocking_ids)
                ]
                if not clause:
                    raise AssertionError(
                        "empty exact-lattice blocking clause"
                    )
                solver.add_clause(clause)
                learned.append(clause)
                branches.append(
                    {
                        "selected_relation_count": len(selected_ids),
                        "active_target_rows": len(active_targets),
                        "blocking_clause": clause,
                        "certificate": certificate,
                    }
                )
                print(
                    f"branch={len(branches)} "
                    f"selected={len(selected_ids)} "
                    f"active_targets={len(active_targets)} "
                    f"rank={len(certificate['basis_relation_ids'])} "
                    f"mode={certificate['certificate_mode']}",
                    flush=True,
                )
                if args.max_models and len(branches) >= args.max_models:
                    terminal_status = "limit"
                    break
            else:
                terminal_status = "UNSAT"

    dual_horn_core = None
    if args.dual_horn_core:
        if terminal_status != "UNSAT":
            raise AssertionError(
                "dual-Horn core requires a terminal UNSAT result"
            )
        if len(branches) > 1:
            raise AssertionError(
                "dual-Horn core currently supports zero or one branch"
            )
        dual_horn_index = build_dual_horn_index(sorted_clauses)
        if not branches:
            blocking_clause: list[int] = []
            proof = dual_horn_unsat_core(
                sorted_clauses, dual_horn_index
            )
            if proof is None:
                raise AssertionError(
                    "base dual-Horn formula lacks a propagation core"
                )
            forcing_proofs = [proof]
            core_factor_indices = set(
                map(
                    int,
                    proof["core_factor_clause_indices"],
                )
            )
            core_status = "UNSAT_dual_horn_base_core"
        else:
            if branches[0]["certificate"]["certificate_mode"] not in {
                "inconsistent_factor_sign",
                "isolated_factor_lattice_class",
            }:
                raise AssertionError(
                    "unsupported terminal exact lattice branch"
                )
            blocking_clause = list(
                map(int, branches[0]["blocking_clause"])
            )
            if not blocking_clause or any(
                literal >= 0 for literal in blocking_clause
            ):
                raise AssertionError(
                    "signed-lattice blocking clause is not all-negative"
                )
            forcing_proofs = []
            core_factor_indices = set()
            for literal in blocking_clause:
                proof = dual_horn_forcing_core(
                    sorted_clauses,
                    -literal,
                    dual_horn_index,
                )
                if proof is None:
                    raise AssertionError(
                        "blocking relation is not dual-Horn forced"
                    )
                forcing_proofs.append(proof)
                core_factor_indices.update(
                    map(
                        int,
                        proof["core_factor_clause_indices"],
                    )
                )
            core_status = "UNSAT_dual_horn_forcing_core"
        core_factor_indices_sorted = sorted(core_factor_indices)
        core_clauses = [
            list(map(int, sorted_clauses[index]))
            for index in core_factor_indices_sorted
        ]
        core_formula = (
            [*core_clauses, blocking_clause]
            if blocking_clause
            else core_clauses
        )
        # Some PySAT backends index clause[0] while bootstrapping and
        # therefore reject the perfectly valid DIMACS empty clause before
        # reporting UNSAT.  Treat that syntactic contradiction directly;
        # all nonempty cores still receive the independent SAT-backend
        # check below.
        if not any(not clause for clause in core_formula):
            with Solver(
                name=args.solver,
                bootstrap_with=core_formula,
            ) as core_solver:
                if core_solver.solve():
                    raise AssertionError(
                        "extracted dual-Horn core unexpectedly became SAT"
                    )
        dual_horn_core = {
            "status": core_status,
            "blocking_clause": blocking_clause,
            "forcing_proofs": forcing_proofs,
            "core_factor_clause_indices": core_factor_indices_sorted,
            "core_factor_clauses": core_clauses,
            "core_factor_clause_equations": [
                clause_equations[sorted_clauses[index]]
                for index in core_factor_indices_sorted
            ],
            "core_factor_clause_count": len(core_clauses),
            "core_plus_blocking_unsat": True,
        }

    payload = {
        "status": terminal_status,
        "necessary_conditions_only": terminal_status
        not in {"UNSAT", "literal_contradiction"},
        "scope": (
            "one fixed all-even order-14 equality support, unforced "
            "full-cycle and extra-monomial factor choices"
        ),
        "exploration": str(args.exploration),
        "exploration_sha256": sha256(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": len(full_only),
        "matching_extensions_accumulated": total_extensions,
        "full_only_equations": base_equation_count,
        "full_containing_ten_term_equations": ten_equation_count,
        "full_containing_twelve_term_equations": (
            twelve_equation_count
        ),
        "factorable_twelve_term_equations": factorable_twelve,
        "nonfactorable_twelve_term_equations": nonfactorable_twelve,
        "factor_relation_count": len(relations),
        "factor_clause_count": len(sorted_clauses),
        "unit_clause_count": sum(
            len(clause) == 1 for clause in sorted_clauses
        ),
        "binary_clause_count": sum(
            len(clause) == 2 for clause in sorted_clauses
        ),
        "target_activity_counts": target_level_counts,
        "target_rows": len(target_rows),
        "compact_output": args.compact_output,
        "dual_horn_core": dual_horn_core,
        "factor_relations": [
            {
                "relation_id": index,
                "signature": [list(item) for item in relation],
                "origin": origins[index],
            }
            for index, relation in enumerate(relations)
        ],
        "learned_clauses": learned,
        "branches": branches,
        "literal_certificate": literal_impossibility,
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": True,
        "global_conjecture_resolved": False,
    }
    if args.compact_output:
        payload["omitted_factor_clause_details"] = True
    else:
        payload["factor_clauses"] = [
            list(map(int, clause)) for clause in sorted_clauses
        ]
        payload["factor_clause_origins"] = [
            clause_origins[clause] for clause in sorted_clauses
        ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key
                not in {
                    "factor_relations",
                    "factor_clauses",
                    "factor_clause_origins",
                    "learned_clauses",
                    "branches",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
