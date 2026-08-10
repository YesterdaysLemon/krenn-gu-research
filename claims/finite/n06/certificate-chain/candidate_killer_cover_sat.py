"""Global support SAT for the minimum union of all eligible killer arcs.

Rather than selecting one killer neighbour for every ``(vertex, colour)``
in advance, this encoding derives every eligible arc from the zero/nonzero
support of the edge blocks.  It then asks whether *no* set of at most ``k``
undirected edges can contain one eligible arc for every task.

UNSAT for ``k=10`` proves that every hypothetical six-vertex witness admits
a killer selection on at most ten edges, regardless of which selection was
initially exposed by the contraction lemma.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from global_support_sat import flat_entry
from rankone_support_sat import (
    CNF,
    matching_indicator,
    solve_with_cadical,
    solve_with_minisat,
)
from search_witness import EquationSystem

Edge = tuple[int, int]


def candidate_support_problem(
) -> tuple[CNF, dict[tuple[int, int, int], int]]:
    """Build the global support relaxation and all eligible killer arcs."""
    system = EquationSystem(6, 3)
    cnf = CNF()
    entries = [cnf.variable() for _ in range(system.variable_count)]
    candidates: dict[tuple[int, int, int], int] = {}

    for vertex in range(6):
        for colour in range(3):
            for neighbour in range(6):
                if neighbour == vertex:
                    continue
                candidate = cnf.variable()
                candidates[(vertex, colour, neighbour)] = candidate
                inside: list[int] = []
                outside: list[int] = []
                for vertex_colour in range(3):
                    for neighbour_colour in range(3):
                        entry = entries[
                            flat_entry(
                                system,
                                vertex,
                                neighbour,
                                vertex_colour,
                                neighbour_colour,
                            )
                        ]
                        if neighbour_colour == colour:
                            inside.append(entry)
                        else:
                            outside.append(entry)
                # candidate iff the block is nonzero and supported on the
                # required leaf-colour line.
                for entry in outside:
                    cnf.add(-candidate, -entry)
                cnf.add(-candidate, *inside)
                for entry in inside:
                    cnf.add(
                        *(outside),
                        -entry,
                        candidate,
                    )

    for vertex in range(6):
        for colour in range(3):
            cnf.add(
                *(
                    candidates[(vertex, colour, neighbour)]
                    for neighbour in range(6)
                    if neighbour != vertex
                )
            )

    for colouring_index, raw_colouring in enumerate(system.colourings):
        colouring = tuple(int(value) for value in raw_colouring)
        indicators: list[int] = []
        for matching in system.matchings:
            factors = tuple(
                entries[
                    flat_entry(
                        system,
                        edge[0],
                        edge[1],
                        colouring[edge[0]],
                        colouring[edge[1]],
                    )
                ]
                for edge in matching
            )
            indicators.append(matching_indicator(cnf, factors))
        if system.target[colouring_index]:
            cnf.add(*indicators)
        else:
            for indicator in indicators:
                cnf.add(
                    -indicator,
                    *(other for other in indicators if other != indicator),
                )
    return cnf, candidates


def candidate_support_cnf() -> CNF:
    """Return the global support relaxation without a cover constraint."""
    cnf, _ = candidate_support_problem()
    return cnf


def candidate_cover_cnf(max_cover_edges: int) -> CNF:
    if not 1 <= max_cover_edges <= 15:
        raise ValueError("max_cover_edges must lie in 1..15")
    system = EquationSystem(6, 3)
    cnf, candidates = candidate_support_problem()

    all_edges = tuple(system.edges)
    # Every selection using at most k edges is contained in a k-edge set.
    # For each such set S, assert that some task has no candidate in S.
    for allowed_edges in itertools.combinations(
        all_edges, max_cover_edges
    ):
        allowed = set(allowed_edges)
        missing_task_indicators: list[int] = []
        for vertex in range(6):
            for colour in range(3):
                relevant = [
                    candidates[(vertex, colour, neighbour)]
                    for neighbour in range(6)
                    if neighbour != vertex
                    and tuple(sorted((vertex, neighbour))) in allowed
                ]
                missing = cnf.variable()
                missing_task_indicators.append(missing)
                for candidate in relevant:
                    cnf.add(-missing, -candidate)
                cnf.add(*relevant, missing)
        cnf.add(*missing_task_indicators)
    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cover-edges", type=int, default=10)
    parser.add_argument(
        "--cnf", type=Path, default=Path("tmp/candidate_cover.cnf")
    )
    parser.add_argument(
        "--solver", choices=("minisat", "cadical"), default="cadical"
    )
    args = parser.parse_args()
    args.cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf = candidate_cover_cnf(args.max_cover_edges)
    status = (
        solve_with_cadical(cnf, args.cnf)
        if args.solver == "cadical"
        else solve_with_minisat(cnf, args.cnf)
    )
    print(
        json.dumps(
            {
                "status": status,
                "max_cover_edges": args.max_cover_edges,
                "solver": args.solver,
                "variables": cnf.variable_count,
                "clauses": len(cnf.clauses),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
