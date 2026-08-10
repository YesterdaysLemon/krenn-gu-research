"""Independently audit an augmented reciprocal-killer cardinality CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from pysat.card import CardEnc, EncType


N = 8
D = 3
CANDIDATE_BASE = 905


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError("invalid DIMACS header")
    return int(variables), int(clauses)


def allowed_edges(center_degree: int) -> tuple[tuple[int, int], ...]:
    neighbours_of_zero = (
        set(range(1, N))
        if center_degree == 1
        else set(range(1, center_degree + 1))
    )
    return tuple(
        edge
        for edge in itertools.combinations(range(N), 2)
        if edge[0] != 0 or edge[1] in neighbours_of_zero
    )


def candidate_map(
    center_degree: int, candidate_base: int
) -> dict[tuple[int, int, int], int]:
    neighbours = {vertex: [] for vertex in range(N)}
    for first, second in allowed_edges(center_degree):
        neighbours[first].append(second)
        neighbours[second].append(first)
    result: dict[tuple[int, int, int], int] = {}
    next_variable = candidate_base
    for vertex in range(N):
        for colour in range(D):
            for neighbour in neighbours[vertex]:
                result[vertex, colour, neighbour] = next_variable
                next_variable += 3
    return result


def edge_index(
    first: int, second: int, center_degree: int
) -> int:
    if not first < second:
        raise ValueError("edge is not ordered")
    for index, edge in enumerate(allowed_edges(center_degree)):
        if edge == (first, second):
            return index
    raise AssertionError("edge not found")


def entry(
    first: int,
    second: int,
    first_colour: int,
    second_colour: int,
    center_degree: int,
) -> int:
    if first > second:
        first, second = second, first
        first_colour, second_colour = (
            second_colour,
            first_colour,
        )
    return (
        1
        + 9 * edge_index(first, second, center_degree)
        + 3 * first_colour
        + second_colour
    )


def expected_candidate_clauses(
    vertex: int,
    colour: int,
    neighbour: int,
    center_degree: int,
    candidates: dict[tuple[int, int, int], int],
) -> set[tuple[int, ...]]:
    cand = candidates[vertex, colour, neighbour]
    inside = [
        entry(
            vertex,
            neighbour,
            row,
            colour,
            center_degree,
        )
        for row in range(D)
    ]
    outside = [
        entry(
            vertex,
            neighbour,
            row,
            column,
            center_degree,
        )
        for row in range(D)
        for column in range(D)
        if column != colour
    ]
    return {
        *{(-cand, -literal) for literal in outside},
        tuple([-cand, *inside]),
        *{
            tuple([*outside, -literal, cand])
            for literal in inside
        },
    }


def parse_clause(line: str) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    if not values or values[-1] != 0:
        raise AssertionError("unterminated DIMACS clause")
    return values[:-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_reciprocal_cardinality_audit.json"
        ),
    )
    args = parser.parse_args()

    manifest = json.loads(
        args.manifest.read_text(encoding="utf-8")
    )
    base = Path(manifest["base_cnf"])
    output = Path(manifest["output_cnf"])
    if sha256(base) != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash mismatch")
    if sha256(output) != manifest["output_cnf_sha256"]:
        raise AssertionError("output CNF hash mismatch")

    old_variables, old_clauses = header(base)
    new_variables, new_clauses = header(output)
    center_degree = int(manifest.get("center_degree", 1))
    candidate_base = int(
        manifest.get("candidate_base", CANDIDATE_BASE)
    )
    candidates = candidate_map(center_degree, candidate_base)
    if (old_variables, old_clauses) != (
        manifest["old_variables"],
        manifest["old_clauses"],
    ):
        raise AssertionError("base header mismatch")

    all_candidates = set(candidates.values())
    observed_candidate_clauses: set[tuple[int, ...]] = set()
    with base.open("r", encoding="ascii") as handle:
        next(handle)
        for line in handle:
            clause = parse_clause(line)
            if any(abs(literal) in all_candidates for literal in clause):
                observed_candidate_clauses.add(clause)
    for vertex, colour, neighbour in candidates:
                missing = (
                    expected_candidate_clauses(
                        vertex,
                        colour,
                        neighbour,
                        center_degree,
                        candidates,
                    )
                    - observed_candidate_clauses
                )
                if missing:
                    raise AssertionError(
                        "killer candidate definition changed for "
                        f"{(vertex, colour, neighbour)}: {missing}"
                    )

    reciprocal_variables: list[int] = []
    definition_clauses: list[list[int]] = []
    next_variable = old_variables
    for first, second in allowed_edges(center_degree):
            for first_colour in range(D):
                for second_colour in range(D):
                    next_variable += 1
                    reciprocal_variables.append(next_variable)
                    forward = candidates[first, first_colour, second]
                    reverse = candidates[second, second_colour, first]
                    definition_clauses.extend(
                        [
                            [-next_variable, forward],
                            [-next_variable, reverse],
                            [
                                next_variable,
                                -forward,
                                -reverse,
                            ],
                        ]
                    )

    cardinality = CardEnc.atleast(
        lits=reciprocal_variables,
        bound=int(manifest["minimum_reciprocals"]),
        top_id=next_variable,
        encoding=EncType.seqcounter,
    )
    expected_tail = [
        *definition_clauses,
        *(list(map(int, clause)) for clause in cardinality.clauses),
    ]
    if new_variables != cardinality.nv:
        raise AssertionError("augmented variable count mismatch")
    if new_clauses != old_clauses + len(expected_tail):
        raise AssertionError("augmented clause count mismatch")

    with base.open("r", encoding="ascii") as base_handle, (
        output.open("r", encoding="ascii")
    ) as output_handle:
        next(base_handle)
        next(output_handle)
        for line_number, base_line in enumerate(base_handle, start=2):
            if output_handle.readline() != base_line:
                raise AssertionError(
                    f"base prefix changed at line {line_number}"
                )
        observed_tail = [
            list(parse_clause(line)) for line in output_handle
        ]
    if observed_tail != expected_tail:
        raise AssertionError("appended DIMACS tail mismatch")

    payload = {
        "verified": True,
        "manifest": str(args.manifest),
        "center_degree": center_degree,
        "base_cnf_sha256": sha256(base),
        "output_cnf_sha256": sha256(output),
        "killer_candidates_checked": len(all_candidates),
        "directed_killer_incidences": N * D,
        "reciprocal_variables": len(reciprocal_variables),
        "minimum_reciprocals": int(
            manifest["minimum_reciprocals"]
        ),
        "definition_clauses": len(definition_clauses),
        "cardinality_clauses": len(cardinality.clauses),
        "counting_identity": (
            "if r selected edges receive two of the 24 directed "
            "incidences and s receive one, then 2r+s=24 and "
            "r+s<=m, hence r>=24-m"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
