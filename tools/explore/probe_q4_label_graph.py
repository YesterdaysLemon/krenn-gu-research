#!/usr/bin/env python3
"""Exact CEGIS search for the Q4 labelled component graph mechanism.

The fixed graph is the order-five projective-plane incidence graph in its
cyclic (31,6,1) difference-set presentation.  The synthesis SAT instance
ranges over all proper six-edge-colourings of this graph, not only the cyclic
factorization.  A counterexample SAT instance finds a nonconstant ternary
vertex colouring that avoids every forbidden ordered pair.  Each such
colouring is added back as an exact blocking clause.

SAT and bounded-search outcomes are experimental unless accompanied by the
explicit graph and an independently checked UNSAT certificate for its colour
CNF.  The graph premises themselves are checked combinatorially.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical195


ORDER = 31
DIFFERENCE_SET = (0, 1, 3, 8, 12, 18)
LABELS = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))


def exactly_one(cnf: CNF, variables: list[int]) -> None:
    cnf.append(variables)
    for left, right in itertools.combinations(variables, 2):
        cnf.append([-left, -right])


def singer_edges() -> list[tuple[int, int]]:
    return [(left, (left + delta) % ORDER) for left in range(ORDER) for delta in DIFFERENCE_SET]


def validate_fixed_graph(edges: list[tuple[int, int]]) -> dict[str, object]:
    if len(edges) != ORDER * 6 or len(set(edges)) != len(edges):
        raise AssertionError("the Singer graph is not simple with 186 edges")
    left_degrees = Counter(left for left, _ in edges)
    right_degrees = Counter(right for _, right in edges)
    if set(left_degrees.values()) != {6} or set(right_degrees.values()) != {6}:
        raise AssertionError("the Singer graph is not six-regular")
    differences = Counter(
        (left - right) % ORDER
        for left in DIFFERENCE_SET
        for right in DIFFERENCE_SET
        if left != right
    )
    if set(differences) != set(range(1, ORDER)) or set(differences.values()) != {1}:
        raise AssertionError("the supplied set is not a (31,6,1) difference set")
    neighbors = {
        left: {right for edge_left, right in edges if edge_left == left}
        for left in range(ORDER)
    }
    maximum_codegree = max(
        len(neighbors[left] & neighbors[right])
        for left, right in itertools.combinations(range(ORDER), 2)
    )
    if maximum_codegree > 1:
        raise AssertionError("the fixed bipartite graph has a four-cycle")
    reached_left = {0}
    reached_right: set[int] = set()
    changed = True
    while changed:
        changed = False
        for left, right in edges:
            if left in reached_left and right not in reached_right:
                reached_right.add(right)
                changed = True
            if right in reached_right and left not in reached_left:
                reached_left.add(left)
                changed = True
    if len(reached_left) != ORDER or len(reached_right) != ORDER:
        raise AssertionError("the fixed graph is disconnected")
    return {
        "parts": [ORDER, ORDER],
        "edge_count": len(edges),
        "degree": 6,
        "simple": True,
        "connected": True,
        "maximum_left_codegree": maximum_codegree,
        "girth_at_least_six": True,
        "difference_multiset_is_every_nonzero_residue_once": True,
        "moore_lower_bound_part_size": 1 + 6 * 5,
    }


def parallel_edge_control() -> dict[str, object]:
    allowed = []
    for left_colour, right_colour in itertools.product(range(3), repeat=2):
        if all((left_colour, right_colour) != label for label in LABELS):
            allowed.append((left_colour, right_colour))
    if allowed != [(0, 0), (1, 1), (2, 2)]:
        raise AssertionError("parallel-edge control does not have only constants")
    return {
        "part_size": 1,
        "parallel_edges": 6,
        "allowed_colourings": [list(pair) for pair in allowed],
        "only_three_constants": True,
        "premise_failures": ["not simple", "not girth at least six"],
    }


def build_label_solver(edges: list[tuple[int, int]]):
    pool = IDPool()
    cnf = CNF()
    variables = {
        (edge_index, label_index): pool.id(("edge_label", edge_index, label_index))
        for edge_index in range(len(edges))
        for label_index in range(len(LABELS))
    }
    for edge_index in range(len(edges)):
        exactly_one(cnf, [variables[edge_index, label] for label in range(6)])
    for side in (0, 1):
        for vertex in range(ORDER):
            incident = [
                edge_index
                for edge_index, edge in enumerate(edges)
                if edge[side] == vertex
            ]
            if len(incident) != 6:
                raise AssertionError("unexpected fixed-graph degree")
            for label in range(6):
                exactly_one(cnf, [variables[edge_index, label] for edge_index in incident])
    return pool, cnf, variables


def decode_labels(model: list[int], edges, variables) -> list[int]:
    positive = set(literal for literal in model if literal > 0)
    output = []
    for edge_index in range(len(edges)):
        selected = [label for label in range(6) if variables[edge_index, label] in positive]
        if len(selected) != 1:
            raise AssertionError("SAT model does not assign one label to an edge")
        output.append(selected[0])
    validate_labeling(edges, output)
    return output


def validate_labeling(edges, edge_labels) -> None:
    for side in (0, 1):
        for vertex in range(ORDER):
            incident_labels = sorted(
                edge_labels[index]
                for index, edge in enumerate(edges)
                if edge[side] == vertex
            )
            if incident_labels != list(range(6)):
                raise AssertionError("a vertex does not see all six labels exactly once")


def colour_cnf(edges, edge_labels):
    pool = IDPool()
    cnf = CNF()
    colour_variables = {
        (side, vertex, colour): pool.id(("colour", side, vertex, colour))
        for side in (0, 1)
        for vertex in range(ORDER)
        for colour in range(3)
    }
    for side in (0, 1):
        for vertex in range(ORDER):
            exactly_one(
                cnf,
                [colour_variables[side, vertex, colour] for colour in range(3)],
            )
    for edge, label_index in zip(edges, edge_labels, strict=True):
        left, right = edge
        forbidden_left, forbidden_right = LABELS[label_index]
        cnf.append(
            [
                -colour_variables[0, left, forbidden_left],
                -colour_variables[1, right, forbidden_right],
            ]
        )
    for colour in range(3):
        cnf.append(
            [
                -colour_variables[side, vertex, colour]
                for side in (0, 1)
                for vertex in range(ORDER)
            ]
        )
    return pool, cnf, colour_variables


def find_nonconstant_colouring(edges, edge_labels):
    pool, cnf, variables = colour_cnf(edges, edge_labels)
    del pool
    with Cadical195(bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
        if not satisfiable:
            return None, cnf
        positive = {literal for literal in solver.get_model() if literal > 0}
    colouring = []
    for side in (0, 1):
        row = []
        for vertex in range(ORDER):
            selected = [
                colour for colour in range(3) if variables[side, vertex, colour] in positive
            ]
            if len(selected) != 1:
                raise AssertionError("counterexample model has no unique colour")
            row.append(selected[0])
        colouring.append(row)
    if len(set(colouring[0] + colouring[1])) == 1:
        raise AssertionError("constant colouring escaped its exclusion clause")
    return colouring, cnf


def find_nonconstant_colouring_batch(edges, edge_labels, batch_size: int):
    _, cnf, variables = colour_cnf(edges, edge_labels)
    colourings = []
    exhausted = False
    with Cadical195(bootstrap_with=cnf.clauses) as solver:
        for _ in range(batch_size):
            if not solver.solve():
                exhausted = True
                break
            positive = {literal for literal in solver.get_model() if literal > 0}
            colouring = []
            selected_literals = []
            for side in (0, 1):
                row = []
                for vertex in range(ORDER):
                    selected = [
                        colour
                        for colour in range(3)
                        if variables[side, vertex, colour] in positive
                    ]
                    if len(selected) != 1:
                        raise AssertionError("counterexample model has no unique colour")
                    row.append(selected[0])
                    selected_literals.append(variables[side, vertex, selected[0]])
                colouring.append(row)
            if len(set(colouring[0] + colouring[1])) == 1:
                raise AssertionError("constant colouring escaped its exclusion clause")
            colourings.append(colouring)
            solver.add_clause([-literal for literal in selected_literals])
    return colourings, exhausted, cnf


def colouring_blocker(colouring, edges, variables) -> list[int]:
    clause = []
    for edge_index, (left, right) in enumerate(edges):
        endpoint_pair = (colouring[0][left], colouring[1][right])
        if endpoint_pair in LABELS:
            clause.append(variables[edge_index, LABELS.index(endpoint_pair)])
    if not clause:
        raise AssertionError("a nonconstant colouring cannot be blocked by any labeling")
    return clause


def colouring_record(colouring) -> dict[str, object]:
    flat = colouring[0] + colouring[1]
    return {
        "left": colouring[0],
        "right": colouring[1],
        "total_colour_counts": [flat.count(colour) for colour in range(3)],
        "left_colour_counts": [colouring[0].count(colour) for colour in range(3)],
        "right_colour_counts": [colouring[1].count(colour) for colour in range(3)],
    }


def validate_avoiding_colouring(colouring, edges, edge_labels) -> None:
    if len(set(colouring[0] + colouring[1])) == 1:
        raise AssertionError("expected a nonconstant colouring")
    for (left, right), label in zip(edges, edge_labels, strict=True):
        if (colouring[0][left], colouring[1][right]) == LABELS[label]:
            raise AssertionError("constructed colouring violates a labelled edge")


def binary_cycle_witnesses(edges, edge_labels):
    matchings = {label: {} for label in range(6)}
    for (left, right), label in zip(edges, edge_labels, strict=True):
        matchings[label][left] = right
    witnesses = []
    profile = {}
    for base, changed in ((0, 1), (0, 2), (1, 2)):
        forward_changed_base = matchings[LABELS.index((changed, base))]
        forward_base_changed = matchings[LABELS.index((base, changed))]
        inverse_base_changed = {
            right: left for left, right in forward_base_changed.items()
        }
        permutation = {
            left: inverse_base_changed[forward_changed_base[left]]
            for left in range(ORDER)
        }
        unseen = set(range(ORDER))
        cycles = []
        while unseen:
            start = min(unseen)
            cycle = []
            vertex = start
            while vertex in unseen:
                unseen.remove(vertex)
                cycle.append(vertex)
                vertex = permutation[vertex]
            cycles.append(cycle)
        profile[f"{base}{changed}"] = sorted(
            (len(cycle) for cycle in cycles), reverse=True
        )
        if len(cycles) == 1:
            continue
        for cycle in cycles:
            left_colours = [base] * ORDER
            right_colours = [base] * ORDER
            for left in cycle:
                left_colours[left] = changed
                right_colours[forward_changed_base[left]] = changed
            colouring = [left_colours, right_colours]
            validate_avoiding_colouring(colouring, edges, edge_labels)
            witnesses.append(colouring)
    return witnesses, profile


def cyclic_factorization_control(edges) -> dict[str, object]:
    edge_by_shift = {
        (left, (left + delta) % ORDER): shift_index
        for left in range(ORDER)
        for shift_index, delta in enumerate(DIFFERENCE_SET)
    }
    survivors = 0
    blocker_lengths = Counter()
    for label_per_shift in itertools.permutations(range(6)):
        labels = [label_per_shift[edge_by_shift[edge]] for edge in edges]
        colouring, _ = find_nonconstant_colouring(edges, labels)
        if colouring is None:
            raise AssertionError("cyclic factorization unexpectedly gives a construction")
        survivors += 1
        blocker_lengths[len(colouring_blocker(colouring, edges, {
            (edge_index, label): edge_index * 6 + label + 1
            for edge_index in range(len(edges))
            for label in range(6)
        }))] += 1
    return {
        "factorizations_checked": survivors,
        "all_have_nonconstant_avoiding_colouring": survivors == 720,
        "witness_blocker_length_histogram": dict(sorted(blocker_lengths.items())),
        "scope": "all 6! assignments of ordered labels to the six cyclic matchings only",
    }


def write_dimacs(cnf: CNF, path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_cegis(
    edges,
    *,
    maximum_iterations: int,
    colouring_batch_size: int,
    deadline: float,
    output_dir: Path,
    resume_cnf: Path | None,
):
    _, label_cnf, variables = build_label_solver(edges)
    initial_variables = label_cnf.nv
    initial_clauses = len(label_cnf.clauses)
    resumed_blockers = 0
    if resume_cnf is not None:
        resumed = CNF(from_file=str(resume_cnf))
        if resumed.clauses[:initial_clauses] != label_cnf.clauses:
            raise AssertionError("resume CNF does not have the exact synthesis prefix")
        for clause in resumed.clauses[initial_clauses:]:
            label_cnf.append(clause)
        resumed_blockers = len(resumed.clauses) - initial_clauses
    history = []
    label_models_checked = 0
    final_labels = None
    final_colour_cnf = None
    status = "ITERATION_LIMIT"
    with Cadical195(bootstrap_with=label_cnf.clauses) as label_solver:
        for iteration in range(maximum_iterations):
            if time.monotonic() >= deadline:
                status = "TIME_LIMIT"
                break
            if not label_solver.solve():
                status = "FIXED_GRAPH_LABELING_UNSAT_AFTER_CEGIS"
                break
            labels = decode_labels(label_solver.get_model(), edges, variables)
            label_models_checked += 1
            binary_colourings, binary_profile = binary_cycle_witnesses(edges, labels)
            if binary_colourings:
                colourings = binary_colourings
                colouring_kinds = ["binary_cycle"] * len(colourings)
                exhausted = False
                candidate_colour_cnf = None
            else:
                colourings, exhausted, candidate_colour_cnf = (
                    find_nonconstant_colouring_batch(edges, labels, colouring_batch_size)
                )
                colouring_kinds = ["ternary_sat"] * len(colourings)
            if not colourings:
                status = "CANDIDATE_FOUND"
                final_labels = labels
                final_colour_cnf = candidate_colour_cnf
                break
            for batch_index, (colouring, kind) in enumerate(
                zip(colourings, colouring_kinds, strict=True), start=1
            ):
                blocker = colouring_blocker(colouring, edges, variables)
                label_solver.add_clause(blocker)
                label_cnf.append(blocker)
                history.append(
                    {
                        "label_model": iteration + 1,
                        "batch_index": batch_index,
                        "kind": kind,
                        "binary_cycle_profile": binary_profile,
                        "batch_exhausted_after_this_model": exhausted,
                        "blocker_length": len(blocker),
                        "colouring": colouring_record(colouring),
                    }
                )
            if (iteration + 1) % 100 == 0:
                print(
                    f"cegis label_models={iteration + 1} "
                    f"new_counterexamples={len(history)}",
                    flush=True,
                )
    result = {
        "status": status,
        "resumed_counterexample_blockers": resumed_blockers,
        "label_models_checked": label_models_checked,
        "colouring_batch_size": colouring_batch_size,
        "iterations_with_counterexample": len(history),
        "counterexample_blocker_length_histogram": dict(
            sorted(Counter(item["blocker_length"] for item in history).items())
        ),
        "counterexample_kind_histogram": dict(
            sorted(Counter(item["kind"] for item in history).items())
        ),
        "first_counterexamples": history[:5],
        "last_counterexamples": history[-5:],
        "label_cnf_initial_variables": initial_variables,
        "label_cnf_initial_clauses": initial_clauses,
        "label_cnf_final_clauses": len(label_cnf.clauses),
    }
    synthesis_cnf_path = output_dir / "fixed-graph-labeling-cegis.cnf"
    result["label_cnf"] = str(synthesis_cnf_path)
    result["label_cnf_sha256"] = write_dimacs(label_cnf, synthesis_cnf_path)
    if final_labels is not None and final_colour_cnf is not None:
        validate_labeling(edges, final_labels)
        result["labelled_edges"] = [
            {"left": left, "right": right, "label": list(LABELS[label])}
            for (left, right), label in zip(edges, final_labels, strict=True)
        ]
        cnf_path = output_dir / "candidate-nonconstant-colouring.cnf"
        result["candidate_colour_cnf"] = str(cnf_path)
        result["candidate_colour_cnf_sha256"] = write_dimacs(final_colour_cnf, cnf_path)
        with Cadical195(bootstrap_with=final_colour_cnf.clauses) as replay:
            result["candidate_colour_cnf_replay_sat"] = replay.solve()
            if result["candidate_colour_cnf_replay_sat"]:
                raise AssertionError("candidate colour CNF replay became satisfiable")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=10000)
    parser.add_argument("--colouring-batch-size", type=int, default=64)
    parser.add_argument("--internal-seconds", type=float, default=840.0)
    parser.add_argument("--resume-label-cnf", type=Path)
    parser.add_argument("--skip-cyclic-control", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    edges = singer_edges()
    graph = validate_fixed_graph(edges)
    cyclic = (
        {"status": "SKIPPED"}
        if args.skip_cyclic_control
        else cyclic_factorization_control(edges)
    )
    deadline = started + args.internal_seconds
    cegis = run_cegis(
        edges,
        maximum_iterations=args.maximum_iterations,
        colouring_batch_size=args.colouring_batch_size,
        deadline=deadline,
        output_dir=args.output.parent,
        resume_cnf=args.resume_label_cnf,
    )
    result = {
        "schema": "q4-labelled-component-graph-cegis-v1",
        "status": cegis["status"],
        "scope": {
            "fixed_unlabelled_graph": "cyclic incidence graph of PG(2,5)",
            "labeling_search": "all proper six-edge-labelings of the fixed graph",
            "colour_counterexample_search": "exact SAT over all nonconstant ternary colourings",
            "sat_only_unsat_is_not_a_checked_proof": True,
            "global_krenn_gu_status_changed": False,
        },
        "labels": [list(label) for label in LABELS],
        "difference_set": list(DIFFERENCE_SET),
        "parallel_edge_control": parallel_edge_control(),
        "fixed_graph_validation": graph,
        "cyclic_factorization_control": cyclic,
        "cegis": cegis,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2) + "\n"
    args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
