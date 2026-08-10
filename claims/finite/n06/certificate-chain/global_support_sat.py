"""SAT relaxation of the full six-vertex, three-colour killer system.

This encodes both the unknown zero/nonzero support of all 135 edge entries
and one killer neighbour for every (vertex, colour) pair.  It is a necessary
condition for an exact witness.  The optional unpaired-arc clause asks whether
the 18 selected killer arcs can occupy more than nine undirected edges.
"""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import argparse
import itertools
import json
from pathlib import Path

from krenn_gu.rankone_support_sat import CNF, matching_indicator, solve_with_minisat
from krenn_gu.search_witness import EquationSystem


def flat_entry(
    system: EquationSystem, first: int, second: int, a: int, b: int
) -> int:
    if first < second:
        edge = (first, second)
        row, column = a, b
    else:
        edge = (second, first)
        row, column = b, a
    return system.edge_index[edge] * 9 + row * 3 + column


def global_support_cnf(
    require_unpaired: bool,
    require_all_edges: bool = False,
    min_killer_edges: int = 0,
    missing_edges: frozenset[tuple[int, int]] | None = None,
) -> CNF:
    system = EquationSystem(6, 3)
    cnf = CNF()
    entries = [cnf.variable() for _ in range(system.variable_count)]
    killers = {
        (vertex, colour, neighbour): cnf.variable()
        for vertex in range(6)
        for colour in range(3)
        for neighbour in range(6)
        if neighbour != vertex
    }

    for vertex in range(6):
        neighbours = [u for u in range(6) if u != vertex]
        for colour in range(3):
            choices = [killers[vertex, colour, u] for u in neighbours]
            cnf.add(*choices)
            for first_index, first in enumerate(choices):
                for second in choices[first_index + 1 :]:
                    cnf.add(-first, -second)

        # The three colours have distinct killer neighbours.
        for neighbour in neighbours:
            for first_colour in range(3):
                for second_colour in range(first_colour + 1, 3):
                    cnf.add(
                        -killers[vertex, first_colour, neighbour],
                        -killers[vertex, second_colour, neighbour],
                    )

    for vertex in range(6):
        for colour in range(3):
            for neighbour in range(6):
                if neighbour == vertex:
                    continue
                killer = killers[vertex, colour, neighbour]
                allowed: list[int] = []
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
                            allowed.append(entry)
                        else:
                            cnf.add(-killer, -entry)
                # The forced one-column/one-row block is nonzero.
                cnf.add(-killer, *allowed)

    if require_unpaired:
        unpaired_indicators: list[int] = []
        for vertex in range(6):
            for colour in range(3):
                for neighbour in range(6):
                    if neighbour == vertex:
                        continue
                    indicator = cnf.variable()
                    killer = killers[vertex, colour, neighbour]
                    reverse = [
                        killers[neighbour, other_colour, vertex]
                        for other_colour in range(3)
                    ]
                    cnf.add(-indicator, killer)
                    for reverse_killer in reverse:
                        cnf.add(-indicator, -reverse_killer)
                    cnf.add(-killer, *reverse, indicator)
                    unpaired_indicators.append(indicator)
        cnf.add(*unpaired_indicators)

    if require_all_edges:
        for first in range(6):
            for second in range(first + 1, 6):
                cnf.add(
                    *(
                        [
                            killers[first, colour, second]
                            for colour in range(3)
                        ]
                        + [
                            killers[second, colour, first]
                            for colour in range(3)
                        ]
                    )
                )

    if missing_edges is not None:
        all_edges = {
            (first, second)
            for first in range(6)
            for second in range(first + 1, 6)
        }
        if not missing_edges <= all_edges:
            raise ValueError(f"invalid missing edges: {missing_edges - all_edges}")
        for first, second in sorted(all_edges):
            incident_killers = [
                killers[first, colour, second] for colour in range(3)
            ] + [
                killers[second, colour, first] for colour in range(3)
            ]
            if (first, second) in missing_edges:
                for killer in incident_killers:
                    cnf.add(-killer)
            else:
                cnf.add(*incident_killers)

    if min_killer_edges:
        if not 1 <= min_killer_edges <= 15:
            raise ValueError("min_killer_edges must lie in 1..15")
        edge_indicators: list[int] = []
        for first in range(6):
            for second in range(first + 1, 6):
                indicator = cnf.variable()
                incident_killers = [
                    killers[first, colour, second]
                    for colour in range(3)
                ] + [
                    killers[second, colour, first]
                    for colour in range(3)
                ]
                cnf.add(-indicator, *incident_killers)
                for killer in incident_killers:
                    cnf.add(-killer, indicator)
                edge_indicators.append(indicator)
        # At least k of n variables are true iff every subset of n-k+1
        # variables contains a true variable.
        subset_size = len(edge_indicators) - min_killer_edges + 1
        for subset in itertools.combinations(edge_indicators, subset_size):
            cnf.add(*subset)

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
    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-unpaired", action="store_true")
    parser.add_argument("--require-all-edges", action="store_true")
    parser.add_argument("--min-killer-edges", type=int, default=0)
    parser.add_argument(
        "--missing-edges",
        help="comma-separated absent edges such as 01,02; all others are used",
    )
    parser.add_argument("--cnf", type=Path, default=Path("tmp/global.cnf"))
    args = parser.parse_args()

    missing_edges = None
    if args.missing_edges is not None:
        missing_edges = frozenset(
            tuple(sorted((int(token[0]), int(token[1]))))
            for token in args.missing_edges.split(",")
            if token
        )
    cnf = global_support_cnf(
        args.require_unpaired,
        args.require_all_edges,
        args.min_killer_edges,
        missing_edges,
    )
    args.cnf.parent.mkdir(parents=True, exist_ok=True)
    status = solve_with_minisat(cnf, args.cnf)
    print(
        json.dumps(
            {
                "status": status,
                "require_unpaired": args.require_unpaired,
                "require_all_edges": args.require_all_edges,
                "min_killer_edges": args.min_killer_edges,
                "missing_edges": (
                    sorted(missing_edges) if missing_edges is not None else None
                ),
                "variables": cnf.variable_count,
                "clauses": len(cnf.clauses),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
