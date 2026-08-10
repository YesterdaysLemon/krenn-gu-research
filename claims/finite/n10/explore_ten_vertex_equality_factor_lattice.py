"""Explore one deterministic ``n=10`` equality support with exact lattices.

The support has three diagonal singleton perfect matchings and a disjoint
full-block ``C4+C6`` 2-factor.  Hence every colouring has four full-only
matching monomials.  A colouring with exactly those four terms yields a
two-way choice between the alternating-product relation on the C4 and the
one on the C6.

This script runs exact signed-lattice CEGAR on those cycle-factor choices.
It is exploratory: even an UNSAT result is about one fixed support, not all
ten-vertex supports or the Krenn--Gu conjecture.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from pysat.solvers import Solver

from signed_binomial_lattice import _basis_data

N = 10
D = 3

Edge = tuple[int, int]
Entry = tuple[Edge, int, int]

SINGLETON_MATCHINGS: tuple[frozenset[Edge], ...] = (
    frozenset({(1, 2), (4, 9), (0, 5), (3, 6), (7, 8)}),
    frozenset({(3, 8), (0, 4), (1, 7), (2, 5), (6, 9)}),
    frozenset({(0, 7), (5, 8), (4, 6), (2, 3), (1, 9)}),
)
FULL_EDGES = frozenset(
    {
        (0, 1),
        (0, 6),
        (1, 8),
        (2, 4),
        (2, 6),
        (3, 7),
        (3, 9),
        (4, 8),
        (5, 7),
        (5, 9),
    }
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def singleton_colours() -> dict[Edge, int]:
    output: dict[Edge, int] = {}
    for colour, matching in enumerate(SINGLETON_MATCHINGS):
        for edge in matching:
            if edge in output:
                raise AssertionError("singleton matchings overlap")
            output[edge] = colour
    return output


def cycle_components(edges: frozenset[Edge]) -> list[list[int]]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    if any(len(adjacency[vertex]) != 2 for vertex in range(N)):
        raise AssertionError("full edges are not a 2-factor")
    unseen = set(range(N))
    output: list[list[int]] = []
    while unseen:
        start = min(unseen)
        order = [start]
        previous = None
        current = start
        while True:
            choices = sorted(adjacency[current] - {previous})
            following = choices[0]
            if following == start:
                break
            order.append(following)
            previous, current = current, following
        unseen -= set(order)
        output.append(order)
    output.sort(key=lambda row: (len(row), row))
    return output


def graph_matchings(edges: set[Edge]) -> list[tuple[Edge, ...]]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    output: list[tuple[Edge, ...]] = []

    def recurse(remaining: set[int], chosen: list[Edge]) -> None:
        if not remaining:
            output.append(tuple(chosen))
            return
        first = min(remaining)
        for second in sorted(adjacency[first] & remaining):
            recurse(
                remaining - {first, second},
                [*chosen, canonical_edge(first, second)],
            )

    recurse(set(range(N)), [])
    return output


def entry_variables(
    singleton: dict[Edge, int],
) -> tuple[list[Entry], dict[Entry, int]]:
    entries: list[Entry] = []
    for edge in sorted(singleton):
        colour = singleton[edge]
        entries.append((edge, colour, colour))
    for edge in sorted(FULL_EDGES):
        for first_colour in range(D):
            for second_colour in range(D):
                entries.append((edge, first_colour, second_colour))
    positions = {entry: index for index, entry in enumerate(entries)}
    if len(entries) != 105 or len(positions) != len(entries):
        raise AssertionError("unexpected ten-vertex entry layout")
    return entries, positions


def active(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    singleton: dict[Edge, int],
) -> bool:
    return all(
        edge not in singleton
        or (
            colouring[edge[0]]
            == colouring[edge[1]]
            == singleton[edge]
        )
        for edge in matching
    )


def monomial(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    singleton: dict[Edge, int],
    positions: dict[Entry, int],
) -> tuple[int, ...]:
    variables: list[int] = []
    for edge in matching:
        if edge in singleton:
            colour = singleton[edge]
            entry = (edge, colour, colour)
        else:
            entry = (
                edge,
                int(colouring[edge[0]]),
                int(colouring[edge[1]]),
            )
        variables.append(positions[entry])
    return tuple(sorted(variables))


def dense_monomial(
    sparse: Iterable[int],
    variable_count: int,
) -> np.ndarray:
    vector = np.zeros(variable_count, dtype=np.int64)
    for variable in sparse:
        vector[int(variable)] += 1
    return vector


def canonical_vector(vector: np.ndarray) -> tuple[int, ...]:
    direct = tuple(map(int, vector))
    negative = tuple(map(int, -vector))
    return min(direct, negative)


def alternating_relation(
    cycle: Sequence[int],
    colouring: Sequence[int],
    positions: dict[Entry, int],
) -> tuple[int, ...]:
    even: list[int] = []
    odd: list[int] = []
    for index in range(len(cycle)):
        edge = canonical_edge(
            cycle[index],
            cycle[(index + 1) % len(cycle)],
        )
        variable = positions[
            (
                edge,
                int(colouring[edge[0]]),
                int(colouring[edge[1]]),
            )
        ]
        (even if index % 2 == 0 else odd).append(variable)
    return canonical_vector(
        dense_monomial(even, len(positions))
        - dense_monomial(odd, len(positions))
    )


def exact_sparse_conflict(
    selected_relation_ids: Sequence[int],
    relations: Sequence[tuple[int, ...]],
    activities: Sequence[Sequence[int]],
    colourings: Sequence[Sequence[int]],
    matchings: Sequence[Sequence[Edge]],
    singleton: dict[Edge, int],
    positions: dict[Entry, int],
    only_equation: int | None = None,
) -> dict[str, object] | None:
    rows = [list(relations[index]) for index in selected_relation_ids]
    data = _basis_data(rows)
    if data is None:
        return None
    independent, pivots, raw_basis, raw_inverse = data
    basis_ids = [
        int(selected_relation_ids[position]) for position in independent
    ]
    basis = np.asarray(raw_basis.tolist(), dtype=np.int64)
    inverse = np.asarray(raw_inverse.tolist(), dtype=np.int64)
    pivot_array = np.asarray(pivots, dtype=np.int64)

    def coordinates(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        coordinate = vector[pivot_array] @ inverse
        return coordinate, vector - coordinate @ basis

    for relation_id in selected_relation_ids:
        vector = np.asarray(relations[relation_id], dtype=np.int64)
        coordinate, residual = coordinates(vector)
        if not np.any(residual) and int(coordinate.sum()) % 2 == 0:
            return {
                "certificate_mode": "inconsistent_factor_sign",
                "basis_relation_ids": basis_ids,
                "target_relation_id": int(relation_id),
                "target_coordinates": list(map(int, coordinate)),
            }

    equation_indices: Iterable[int]
    if only_equation is None:
        equation_indices = range(len(activities))
    elif only_equation < 0:
        equation_indices = ()
    else:
        equation_indices = (only_equation,)
    for equation in equation_indices:
        activity = activities[equation]
        if not activity:
            continue
        classes: dict[
            tuple[int, ...],
            list[tuple[int, int]],
        ] = defaultdict(list)
        for matching_index in activity:
            sparse = monomial(
                matchings[matching_index],
                colourings[equation],
                singleton,
                positions,
            )
            vector = dense_monomial(sparse, len(positions))
            coordinate, residual = coordinates(vector)
            sign = -1 if int(coordinate.sum()) % 2 else 1
            classes[tuple(map(int, residual))].append(
                (int(matching_index), sign)
            )
        coefficients = [
            sum(sign for _matching, sign in members)
            for members in classes.values()
        ]
        nonzero = [value for value in coefficients if value]
        target = len(set(colourings[equation])) == 1
        if not target and len(nonzero) == 1:
            return {
                "certificate_mode": "isolated_factor_lattice_class",
                "basis_relation_ids": basis_ids,
                "target_equation_index": equation,
                "target_colouring": list(
                    map(int, colourings[equation])
                ),
                "target_activity": len(activity),
                "nonzero_signed_coefficients": list(map(int, nonzero)),
            }
        if target and not nonzero:
            return {
                "certificate_mode": "annihilated_required_amplitude",
                "basis_relation_ids": basis_ids,
                "target_equation_index": equation,
                "target_colouring": list(
                    map(int, colourings[equation])
                ),
                "target_activity": len(activity),
                "nonzero_signed_coefficients": [],
            }
    return None


def minimize_conflict_core(
    conflict: dict[str, object],
    relations: Sequence[tuple[int, ...]],
    activities: Sequence[Sequence[int]],
    colourings: Sequence[Sequence[int]],
    matchings: Sequence[Sequence[Edge]],
    singleton: dict[Edge, int],
    positions: dict[Entry, int],
) -> tuple[list[int], dict[str, object]]:
    """Greedily shrink one exact contradiction to a relation core."""

    core = list(map(int, conflict["basis_relation_ids"]))
    if conflict["certificate_mode"] == "inconsistent_factor_sign":
        core.append(int(conflict["target_relation_id"]))
        only_equation = -1
    else:
        only_equation = int(conflict["target_equation_index"])
    core = sorted(set(core))
    changed = True
    minimized = conflict
    while changed:
        changed = False
        for relation_id in list(core):
            trial = [
                other for other in core if other != relation_id
            ]
            candidate = exact_sparse_conflict(
                trial,
                relations,
                activities,
                colourings,
                matchings,
                singleton,
                positions,
                only_equation=only_equation,
            )
            if candidate is not None:
                core = trial
                minimized = candidate
                changed = True
    final = exact_sparse_conflict(
        core,
        relations,
        activities,
        colourings,
        matchings,
        singleton,
        positions,
        only_equation=only_equation,
    )
    if final is None:
        raise AssertionError("minimized conflict core lost contradiction")
    return core, final


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-branches", type=int, default=500)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    singleton = singleton_colours()
    if singleton.keys() & FULL_EDGES:
        raise AssertionError("singleton and full blocks overlap")
    cycles = cycle_components(FULL_EDGES)
    if sorted(map(len, cycles)) != [4, 6]:
        raise AssertionError("full factor is not C4+C6")
    skeleton = set(singleton) | set(FULL_EDGES)
    if any(
        sum(vertex in edge for edge in skeleton) != 5
        for vertex in range(N)
    ):
        raise AssertionError("skeleton is not 5-regular")
    matchings = graph_matchings(skeleton)
    full_only = {
        index
        for index, matching in enumerate(matchings)
        if all(edge in FULL_EDGES for edge in matching)
    }
    if len(full_only) != 4:
        raise AssertionError("C4+C6 does not have four full-only matchings")
    entries, positions = entry_variables(singleton)

    colourings = list(itertools.product(range(D), repeat=N))
    activities = [
        tuple(
            index
            for index, matching in enumerate(matchings)
            if active(matching, colouring, singleton)
        )
        for colouring in colourings
    ]
    relation_index: dict[tuple[int, ...], int] = {}
    relations: list[tuple[int, ...]] = []
    origins: list[dict[str, object]] = []
    clauses: list[tuple[int, int]] = []
    for equation, (colouring, activity) in enumerate(
        zip(colourings, activities, strict=True)
    ):
        if len(set(colouring)) == 1:
            continue
        if len(activity) != 4 or set(activity) != full_only:
            continue
        ids: list[int] = []
        for cycle in cycles:
            vector = alternating_relation(
                cycle,
                colouring,
                positions,
            )
            if vector not in relation_index:
                relation_index[vector] = len(relations)
                relations.append(vector)
                origins.append(
                    {
                        "cycle": list(cycle),
                        "local_colouring": [
                            int(colouring[vertex]) for vertex in cycle
                        ],
                    }
                )
            ids.append(relation_index[vector])
        clauses.append((ids[0] + 1, ids[1] + 1))

    branches: list[dict[str, object]] = []
    status = "running"
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        solver.set_phases(
            [-(index + 1) for index in range(len(relations))]
        )
        while solver.solve():
            raw_model = set(solver.get_model())
            selected_ids = [
                index
                for index in range(len(relations))
                if index + 1 in raw_model
            ]
            conflict = exact_sparse_conflict(
                selected_ids,
                relations,
                activities,
                colourings,
                matchings,
                singleton,
                positions,
            )
            if conflict is None:
                status = "survivor"
                branches.append(
                    {
                        "selected_relations": len(selected_ids),
                        "certificate": None,
                    }
                )
                break
            original_core_size = len(
                conflict["basis_relation_ids"]
            )
            core, minimized = minimize_conflict_core(
                conflict,
                relations,
                activities,
                colourings,
                matchings,
                singleton,
                positions,
            )
            clause = tuple(-(index + 1) for index in core)
            if not clause:
                raise AssertionError("empty exact-lattice no-good")
            solver.add_clause(clause)
            branches.append(
                {
                    "selected_relations": len(selected_ids),
                    "original_core_size": original_core_size,
                    "minimized_core_size": len(core),
                    "blocking_clause": list(clause),
                    "certificate": minimized,
                }
            )
            print(
                f"branch={len(branches)} selected={len(selected_ids)} "
                f"core={original_core_size}->{len(core)} "
                f"mode={minimized['certificate_mode']}",
                flush=True,
            )
            if (
                args.max_branches
                and len(branches) >= args.max_branches
            ):
                status = "limit"
                break
        else:
            status = "UNSAT"

    activity_histogram = Counter(map(len, activities))
    payload = {
        "status": status,
        "scope": (
            "one deterministic n=10,d=3 5-regular C4+C6 "
            "full-factor/diagonal-singleton equality support"
        ),
        "necessary_conditions_only": status != "UNSAT",
        "n": N,
        "d": D,
        "singleton_matchings": [
            [list(edge) for edge in sorted(matching)]
            for matching in SINGLETON_MATCHINGS
        ],
        "full_edges": [list(edge) for edge in sorted(FULL_EDGES)],
        "full_cycles": cycles,
        "skeleton_edges": len(skeleton),
        "selected_entries": len(entries),
        "skeleton_perfect_matchings": len(matchings),
        "full_only_perfect_matchings": len(full_only),
        "colourings": len(colourings),
        "activity_histogram": dict(sorted(activity_histogram.items())),
        "factor_clauses": len(clauses),
        "factor_relations": len(relations),
        "relation_origins": origins,
        "branches": branches,
        "solve_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    payload["output"] = str(args.output)
    payload["output_sha256"] = sha256(args.output)
    print(
        json.dumps(
            {
                "status": status,
                "selected_entries": len(entries),
                "factor_clauses": len(clauses),
                "factor_relations": len(relations),
                "branches": len(branches),
                "solve_seconds": payload["solve_seconds"],
                "output": payload["output"],
                "output_sha256": payload["output_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
