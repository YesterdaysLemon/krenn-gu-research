"""Support screen for the 4-regular eight-vertex frontier.

A minimal counterexample is 4-connected.  The complement of a 4-regular
graph on eight vertices is cubic, and the five connected cubic graph
isomorphism classes are stored in ``tmp/cub08.g6``.  Four complements are
4-connected.  The remaining class can also be screened directly with
``--include-non-four-connected``; doing so avoids relying on a reduction
through the exceptional four-vertex witness.

For each such skeleton this script imposes necessary conditions for a
three-colour complex witness:

* every monochromatic amplitude has a nonzero matching monomial;
* no forbidden amplitude has exactly one nonzero matching monomial;
* every (vertex, colour) has an eligible generic killer block;
* every skeleton edge is a nonzero block;
* the degree-four singleton theorem: every vertex is incident with a block
  supported on one nonzero diagonal entry.

SAT means only that this support relaxation survives.  UNSAT would be an
exact obstruction over every field.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.rankone_support_sat import (
    CNF,
    matching_indicator,
    solve_with_cadical,
)
from krenn_gu.search_witness import perfect_matchings

Edge = tuple[int, int]


def decode_graph6(line: str) -> tuple[Edge, ...]:
    """Decode the small (n <= 62) graph6 format used by ``cub08.g6``."""
    data = line.strip()
    if not data:
        raise ValueError("empty graph6 row")
    n = ord(data[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("only the small graph6 header is supported")
    bits = [
        (ord(character) - 63 >> shift) & 1
        for character in data[1:]
        for shift in range(5, -1, -1)
    ]
    pairs = [
        (first, second)
        for second in range(1, n)
        for first in range(second)
    ]
    return tuple(
        edge for edge, present in zip(pairs, bits, strict=False) if present
    )


def complement_edges(n: int, edges: tuple[Edge, ...]) -> tuple[Edge, ...]:
    present = set(edges)
    return tuple(
        edge
        for edge in itertools.combinations(range(n), 2)
        if edge not in present
    )


def connected_after_deletion(
    n: int,
    edges: tuple[Edge, ...],
    deleted: frozenset[int],
) -> bool:
    remaining = set(range(n)) - deleted
    if len(remaining) <= 1:
        return True
    adjacency = {vertex: set() for vertex in remaining}
    for first, second in edges:
        if first in remaining and second in remaining:
            adjacency[first].add(second)
            adjacency[second].add(first)
    seen: set[int] = set()
    pending = [next(iter(remaining))]
    while pending:
        vertex = pending.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        pending.extend(adjacency[vertex] - seen)
    return seen == remaining


def is_four_connected(n: int, edges: tuple[Edge, ...]) -> bool:
    return all(
        connected_after_deletion(n, edges, frozenset(deleted))
        for size in range(4)
        for deleted in itertools.combinations(range(n), size)
    )


def skeleton_matchings(
    n: int, edges: tuple[Edge, ...]
) -> tuple[tuple[Edge, ...], ...]:
    present = set(edges)
    return tuple(
        matching
        for matching in perfect_matchings(tuple(range(n)))
        if all(edge in present for edge in matching)
    )


def degree_four_support_cnf(
    edges: tuple[Edge, ...],
    n: int = 8,
    d: int = 3,
) -> tuple[CNF, dict[str, int]]:
    if n != 8 or d != 3:
        raise ValueError("this frontier screen is fixed at n=8, d=3")
    degree = [0] * n
    for first, second in edges:
        degree[first] += 1
        degree[second] += 1
    if degree != [4] * n:
        raise ValueError(f"skeleton is not 4-regular: {degree}")

    cnf = CNF()
    entries = {
        (first, second, row, column): cnf.variable()
        for first, second in edges
        for row in range(d)
        for column in range(d)
    }

    def entry(
        first: int,
        second: int,
        first_colour: int,
        second_colour: int,
    ) -> int:
        if first < second:
            key = (first, second, first_colour, second_colour)
        else:
            key = (second, first, second_colour, first_colour)
        return entries[key]

    neighbours = {vertex: [] for vertex in range(n)}
    for first, second in edges:
        neighbours[first].append(second)
        neighbours[second].append(first)

    # The fixed skeleton is exactly the set of nonzero blocks.
    for first, second in edges:
        cnf.add(
            *(
                entries[first, second, row, column]
                for row in range(d)
                for column in range(d)
            )
        )

    candidates: dict[tuple[int, int, int], int] = {}
    for vertex in range(n):
        for colour in range(d):
            for neighbour in neighbours[vertex]:
                candidate = cnf.variable()
                candidates[vertex, colour, neighbour] = candidate
                inside = [
                    entry(vertex, neighbour, row, colour)
                    for row in range(d)
                ]
                outside = [
                    entry(vertex, neighbour, row, column)
                    for row in range(d)
                    for column in range(d)
                    if column != colour
                ]
                for literal in outside:
                    cnf.add(-candidate, -literal)
                cnf.add(-candidate, *inside)
                for literal in inside:
                    cnf.add(*outside, -literal, candidate)
            cnf.add(
                *(
                    candidates[vertex, colour, neighbour]
                    for neighbour in neighbours[vertex]
                )
            )

    # Exact singleton indicators.  A singleton at (c,c) is orientation
    # independent and is automatically an eligible colour-c killer at both
    # endpoints.
    singleton_count = 0
    for vertex in range(n):
        incident_singletons: list[int] = []
        for neighbour in neighbours[vertex]:
            first, second = sorted((vertex, neighbour))
            for colour in range(d):
                singleton = cnf.variable()
                singleton_count += 1
                diagonal = entry(
                    vertex, neighbour, colour, colour
                )
                others = [
                    entries[first, second, row, column]
                    for row in range(d)
                    for column in range(d)
                    if (row, column) != (colour, colour)
                ]
                cnf.add(-singleton, diagonal)
                for literal in others:
                    cnf.add(-singleton, -literal)
                cnf.add(-diagonal, *others, singleton)
                incident_singletons.append(singleton)
        cnf.add(*incident_singletons)

    matchings = skeleton_matchings(n, edges)
    required_colourings = 0
    forbidden_colourings = 0
    for colouring in itertools.product(range(d), repeat=n):
        indicators = [
            matching_indicator(
                cnf,
                tuple(
                    entry(
                        first,
                        second,
                        colouring[first],
                        colouring[second],
                    )
                    for first, second in matching
                ),
            )
            for matching in matchings
        ]
        if all(value == colouring[0] for value in colouring):
            required_colourings += 1
            cnf.add(*indicators)
        else:
            forbidden_colourings += 1
            for indicator in indicators:
                cnf.add(
                    -indicator,
                    *(
                        other
                        for other in indicators
                        if other != indicator
                    ),
                )

    return cnf, {
        "entries": len(entries),
        "killer_candidates": len(candidates),
        "singleton_indicators": singleton_count,
        "perfect_matchings": len(matchings),
        "required_colourings": required_colourings,
        "forbidden_colourings": forbidden_colourings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph6",
        type=Path,
        default=Path("tmp/cub08.g6"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/eight_vertex_degree4_support.json"),
    )
    parser.add_argument(
        "--cnf-directory",
        type=Path,
        default=Path("tmp/eight_vertex_degree4_cnf"),
    )
    parser.add_argument(
        "--include-non-four-connected",
        action="store_true",
        help="also screen the one complement with a three-vertex cut",
    )
    parser.add_argument(
        "--indices",
        type=int,
        nargs="*",
        help="only (re)compute the selected cubic catalogue indices",
    )
    args = parser.parse_args()

    rows = [
        line.strip()
        for line in args.graph6.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    results_by_index: dict[int, dict[str, object]] = {}
    if args.output.exists():
        previous = json.loads(args.output.read_text(encoding="utf-8"))
        results_by_index = {
            int(row["cubic_index"]): row
            for row in previous.get("graphs", [])
        }
    args.cnf_directory.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def checkpoint() -> None:
        results = [
            results_by_index[index]
            for index in sorted(results_by_index)
        ]
        args.output.write_text(
            json.dumps(
                {
                    "scope": (
                        "4-regular eight-vertex skeleton "
                        "support relaxation"
                    ),
                    "necessary_conditions_only": True,
                    "graphs": results,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    for cubic_index, graph6 in enumerate(rows):
        if args.indices is not None and cubic_index not in args.indices:
            continue
        cubic = decode_graph6(graph6)
        skeleton = complement_edges(8, cubic)
        four_connected = is_four_connected(8, skeleton)
        if not four_connected and not args.include_non_four_connected:
            results_by_index[cubic_index] = {
                "cubic_index": cubic_index,
                "graph6": graph6,
                "four_connected_complement": False,
                "status": "SKIPPED",
            }
            checkpoint()
            continue
        started = time.perf_counter()
        cnf, metadata = degree_four_support_cnf(skeleton)
        build_seconds = time.perf_counter() - started
        cnf_path = (
            args.cnf_directory / f"complement_cubic_{cubic_index}.cnf"
        )
        solve_started = time.perf_counter()
        status = solve_with_cadical(cnf, cnf_path)
        solve_seconds = time.perf_counter() - solve_started
        results_by_index[cubic_index] = {
            "cubic_index": cubic_index,
            "graph6": graph6,
            "four_connected_complement": four_connected,
            "skeleton_edges": [list(edge) for edge in skeleton],
            **metadata,
            "variables": cnf.variable_count,
            "clauses": len(cnf.clauses),
            "cnf": str(cnf_path),
            "status": status,
            "build_seconds": build_seconds,
            "solve_seconds": solve_seconds,
        }
        print(
            f"cubic {cubic_index}: {status}; "
            f"vars={cnf.variable_count} clauses={len(cnf.clauses)}",
            flush=True,
        )
        checkpoint()

    checkpoint()
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
