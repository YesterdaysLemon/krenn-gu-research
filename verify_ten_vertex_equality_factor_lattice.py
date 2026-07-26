"""Verify and materialize the deterministic n=10 C4+C6 factor proof.

This checker does not import the exploratory producer.  It reconstructs the
support and all factor-choice clauses, then validates every recorded no-good
by exact signed quotient arithmetic using a small Fraction-based unimodular
basis implementation.  Finally it emits a canonical DIMACS instance whose
UNSAT proof can be replayed independently.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

from pysat.solvers import Solver

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


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def singleton_colours() -> dict[Edge, int]:
    result: dict[Edge, int] = {}
    for colour, matching in enumerate(SINGLETON_MATCHINGS):
        for item in matching:
            if item in result:
                raise AssertionError("singleton matchings overlap")
            result[item] = colour
    return result


def cycle_components(edges: frozenset[Edge]) -> list[list[int]]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    if any(len(neighbours) != 2 for neighbours in adjacency.values()):
        raise AssertionError("full graph is not a 2-factor")
    unseen = set(range(N))
    cycles: list[list[int]] = []
    while unseen:
        start = min(unseen)
        previous: int | None = None
        current = start
        cycle = [start]
        while True:
            following = min(adjacency[current] - {previous})
            if following == start:
                break
            cycle.append(following)
            previous, current = current, following
        unseen -= set(cycle)
        cycles.append(cycle)
    return sorted(cycles, key=lambda item: (len(item), item))


def perfect_matchings(edges: set[Edge]) -> list[tuple[Edge, ...]]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    result: list[tuple[Edge, ...]] = []

    def visit(remaining: frozenset[int], chosen: tuple[Edge, ...]) -> None:
        if not remaining:
            result.append(chosen)
            return
        first = min(remaining)
        for second in sorted(adjacency[first] & remaining):
            visit(
                remaining - {first, second},
                (*chosen, edge(first, second)),
            )

    visit(frozenset(range(N)), ())
    return result


def variable_layout(
    singleton: dict[Edge, int],
) -> tuple[list[Entry], dict[Entry, int]]:
    entries: list[Entry] = [
        (item, singleton[item], singleton[item])
        for item in sorted(singleton)
    ]
    entries.extend(
        (item, first_colour, second_colour)
        for item in sorted(FULL_EDGES)
        for first_colour in range(D)
        for second_colour in range(D)
    )
    if len(entries) != 105 or len(set(entries)) != 105:
        raise AssertionError("unexpected selected-entry layout")
    return entries, {entry: index for index, entry in enumerate(entries)}


def is_active(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    singleton: dict[Edge, int],
) -> bool:
    for item in matching:
        if item not in singleton:
            continue
        colour = singleton[item]
        if colouring[item[0]] != colour or colouring[item[1]] != colour:
            return False
    return True


def monomial_vector(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    singleton: dict[Edge, int],
    positions: dict[Entry, int],
) -> tuple[int, ...]:
    vector = [0] * len(positions)
    for item in matching:
        if item in singleton:
            colour = singleton[item]
            entry = (item, colour, colour)
        else:
            entry = (
                item,
                int(colouring[item[0]]),
                int(colouring[item[1]]),
            )
        vector[positions[entry]] += 1
    return tuple(vector)


def canonical(values: Sequence[int]) -> tuple[int, ...]:
    direct = tuple(map(int, values))
    negative = tuple(-value for value in direct)
    return min(direct, negative)


def alternating_relation(
    cycle: Sequence[int],
    colouring: Sequence[int],
    positions: dict[Entry, int],
) -> tuple[int, ...]:
    vector = [0] * len(positions)
    for index, first in enumerate(cycle):
        item = edge(first, cycle[(index + 1) % len(cycle)])
        variable = positions[
            (
                item,
                int(colouring[item[0]]),
                int(colouring[item[1]]),
            )
        ]
        vector[variable] += 1 if index % 2 == 0 else -1
    return canonical(vector)


def reconstruct() -> dict[str, object]:
    singleton = singleton_colours()
    if set(singleton) & set(FULL_EDGES):
        raise AssertionError("full and singleton blocks overlap")
    cycles = cycle_components(FULL_EDGES)
    if list(map(len, cycles)) != [4, 6]:
        raise AssertionError("full factor is not C4+C6")
    skeleton = set(singleton) | set(FULL_EDGES)
    if any(
        sum(vertex in item for item in skeleton) != 5
        for vertex in range(N)
    ):
        raise AssertionError("skeleton is not 5-regular")
    matchings = perfect_matchings(skeleton)
    full_only = {
        index
        for index, matching in enumerate(matchings)
        if set(matching) <= set(FULL_EDGES)
    }
    if len(matchings) != 68 or len(full_only) != 4:
        raise AssertionError("perfect-matching census changed")
    entries, positions = variable_layout(singleton)
    colourings = list(itertools.product(range(D), repeat=N))
    activities = [
        tuple(
            index
            for index, matching in enumerate(matchings)
            if is_active(matching, colouring, singleton)
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
            relation = alternating_relation(cycle, colouring, positions)
            if relation not in relation_index:
                relation_index[relation] = len(relations)
                relations.append(relation)
                origins.append(
                    {
                        "cycle": list(cycle),
                        "local_colouring": [
                            int(colouring[vertex]) for vertex in cycle
                        ],
                    }
                )
            ids.append(relation_index[relation])
        clauses.append((ids[0] + 1, ids[1] + 1))
    return {
        "singleton": singleton,
        "cycles": cycles,
        "skeleton": skeleton,
        "matchings": matchings,
        "full_only": full_only,
        "entries": entries,
        "positions": positions,
        "colourings": colourings,
        "activities": activities,
        "relations": relations,
        "origins": origins,
        "clauses": clauses,
    }


def inverse(matrix: Sequence[Sequence[int]]) -> list[list[Fraction]]:
    size = len(matrix)
    augmented = [
        [
            *(Fraction(value) for value in row),
            *(
                Fraction(1 if column == row_index else 0)
                for column in range(size)
            ),
        ]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if augmented[row][column]
            ),
            None,
        )
        if pivot is None:
            raise ValueError("singular matrix")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        divisor = augmented[column][column]
        augmented[column] = [
            value / divisor for value in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            multiplier = augmented[row][column]
            if multiplier:
                augmented[row] = [
                    left - multiplier * right
                    for left, right in zip(
                        augmented[row], augmented[column], strict=True
                    )
                ]
    return [row[size:] for row in augmented]


def unimodular_coordinates(
    basis: Sequence[tuple[int, ...]],
) -> tuple[list[int], list[list[Fraction]]]:
    rank = len(basis)
    candidates = sorted(
        {
            coordinate
            for row in basis
            for coordinate, value in enumerate(row)
            if value
        }
    )
    for columns in itertools.combinations(candidates, rank):
        square = [[row[column] for column in columns] for row in basis]
        try:
            raw_inverse = inverse(square)
        except ValueError:
            continue
        if all(value.denominator == 1 for row in raw_inverse for value in row):
            return list(columns), raw_inverse
    raise AssertionError("relation core has no unimodular coordinate minor")


def quotient(
    vector: Sequence[int],
    basis: Sequence[tuple[int, ...]],
    pivots: Sequence[int],
    pivot_inverse: Sequence[Sequence[Fraction]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    coordinates_fraction = [
        sum(
            Fraction(vector[pivots[row]]) * pivot_inverse[row][column]
            for row in range(len(pivots))
        )
        for column in range(len(pivots))
    ]
    if any(value.denominator != 1 for value in coordinates_fraction):
        raise AssertionError("nonintegral quotient coordinates")
    coordinates = tuple(int(value) for value in coordinates_fraction)
    residual = tuple(
        int(
            value
            - sum(
                coordinates[row] * basis[row][column]
                for row in range(len(basis))
            )
        )
        for column, value in enumerate(vector)
    )
    return coordinates, residual


def validate_no_good(
    relation_ids: Sequence[int],
    expected: dict[str, object],
    data: dict[str, object],
) -> dict[str, object]:
    relations = data["relations"]
    basis = [relations[index] for index in relation_ids]
    pivots, pivot_inverse = unimodular_coordinates(basis)
    equation = int(expected["target_equation_index"])
    colouring = data["colourings"][equation]
    activity = data["activities"][equation]
    if list(map(int, colouring)) != list(
        map(int, expected["target_colouring"])
    ):
        raise AssertionError("target colouring changed")
    if len(activity) != int(expected["target_activity"]):
        raise AssertionError("target activity changed")
    target = len(set(colouring)) == 1
    classes: dict[tuple[int, ...], int] = {}
    for matching_id in activity:
        vector = monomial_vector(
            data["matchings"][matching_id],
            colouring,
            data["singleton"],
            data["positions"],
        )
        coordinates, residual = quotient(
            vector, basis, pivots, pivot_inverse
        )
        sign = -1 if sum(coordinates) % 2 else 1
        classes[residual] = classes.get(residual, 0) + sign
    nonzero = [value for _key, value in sorted(classes.items()) if value]
    mode = str(expected["certificate_mode"])
    if mode == "isolated_factor_lattice_class":
        if target or len(nonzero) != 1:
            raise AssertionError("no-good does not isolate one forbidden class")
    elif mode == "annihilated_required_amplitude":
        if not target or nonzero:
            raise AssertionError("no-good does not annihilate required target")
    else:
        raise AssertionError(f"unexpected certificate mode {mode}")
    if nonzero != list(map(int, expected["nonzero_signed_coefficients"])):
        raise AssertionError("signed quotient coefficients changed")
    if list(map(int, expected["basis_relation_ids"])) != list(relation_ids):
        raise AssertionError("certificate relation IDs changed")
    return {
        "relation_ids": list(map(int, relation_ids)),
        "unimodular_pivots": pivots,
        "target_equation_index": equation,
        "target_activity": len(activity),
        "nonzero_signed_coefficients": nonzero,
        "verified": True,
    }


def dimacs_bytes(
    variables: int,
    clauses: Sequence[Sequence[int]],
) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}"]
    lines.extend(
        " ".join(map(str, clause)) + " 0" for clause in clauses
    )
    return ("\n".join(lines) + "\n").encode("ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--producer",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_minimized.json"
        ),
    )
    parser.add_argument(
        "--cnf",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_minimized.cnf"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_minimized_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    data = reconstruct()

    expected_static = {
        "n": N,
        "d": D,
        "singleton_matchings": [
            [list(item) for item in sorted(matching)]
            for matching in SINGLETON_MATCHINGS
        ],
        "full_edges": [list(item) for item in sorted(FULL_EDGES)],
        "full_cycles": data["cycles"],
        "skeleton_edges": len(data["skeleton"]),
        "selected_entries": len(data["entries"]),
        "skeleton_perfect_matchings": len(data["matchings"]),
        "full_only_perfect_matchings": len(data["full_only"]),
        "colourings": len(data["colourings"]),
        "activity_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(map(len, data["activities"])).items()
            )
        },
        "factor_clauses": len(data["clauses"]),
        "factor_relations": len(data["relations"]),
        "relation_origins": data["origins"],
    }
    for key, value in expected_static.items():
        if producer[key] != value:
            raise AssertionError(f"producer field changed: {key}")
    if producer["status"] != "UNSAT" or producer["necessary_conditions_only"]:
        raise AssertionError("producer did not terminate UNSAT")

    blocking_clauses: list[tuple[int, ...]] = []
    checks: list[dict[str, object]] = []
    for branch_index, branch in enumerate(producer["branches"]):
        clause = tuple(map(int, branch["blocking_clause"]))
        if any(literal >= 0 for literal in clause):
            raise AssertionError("blocking clause is not purely negative")
        relation_ids = sorted(-literal - 1 for literal in clause)
        if len(relation_ids) != int(branch["minimized_core_size"]):
            raise AssertionError("minimized core size mismatch")
        if len(relation_ids) not in {1, 3}:
            raise AssertionError("unexpected minimized core size")
        check = validate_no_good(
            relation_ids, branch["certificate"], data
        )
        check["branch_index"] = branch_index
        checks.append(check)
        blocking_clauses.append(clause)
        print(
            f"branch={branch_index + 1}/{len(producer['branches'])} "
            f"core={len(relation_ids)} verified",
            flush=True,
        )

    all_clauses: list[Sequence[int]] = [
        *data["clauses"],
        *blocking_clauses,
    ]
    with Solver(name="cadical195", bootstrap_with=all_clauses) as solver:
        if solver.solve():
            raise AssertionError("reconstructed n=10 factor CNF is SAT")
    raw_cnf = dimacs_bytes(len(data["relations"]), all_clauses)
    args.cnf.parent.mkdir(parents=True, exist_ok=True)
    args.cnf.write_bytes(raw_cnf)

    payload = {
        "verified": True,
        "scope": (
            "independent semantic reconstruction of one deterministic "
            "n=10 C4+C6 equality-support signed-factor obstruction"
        ),
        "producer": str(args.producer),
        "producer_sha256": sha256(args.producer),
        "n": N,
        "d": D,
        "selected_entries": len(data["entries"]),
        "skeleton_edges": len(data["skeleton"]),
        "skeleton_perfect_matchings": len(data["matchings"]),
        "factor_relations": len(data["relations"]),
        "factor_clauses": len(data["clauses"]),
        "blocking_clauses": len(blocking_clauses),
        "checks": checks,
        "final_cnf": str(args.cnf),
        "final_cnf_sha256": sha256(args.cnf),
        "final_cnf_variables": len(data["relations"]),
        "final_cnf_clauses": len(all_clauses),
        "independent_solver_unsat": True,
        "verify_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "checks"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
