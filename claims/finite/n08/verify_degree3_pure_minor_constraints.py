"""Independently audit the pure-deleted-minor support augmentation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError("invalid DIMACS header")
    return int(variables), int(clauses)


def allowed_edges() -> tuple[tuple[int, int], ...]:
    return tuple(
        edge
        for edge in itertools.combinations(range(8), 2)
        if edge[0] != 0 or edge[1] <= 3
    )


def allocations() -> dict[tuple[int, int, int], tuple[int, int]]:
    neighbours = {vertex: [] for vertex in range(8)}
    for first, second in allowed_edges():
        neighbours[first].append(second)
        neighbours[second].append(first)
    result: dict[tuple[int, int, int], tuple[int, int]] = {}
    next_variable = 750
    for vertex in range(8):
        for colour in range(3):
            for neighbour in neighbours[vertex]:
                result[vertex, colour, neighbour] = (
                    next_variable,
                    next_variable + 2,
                )
                next_variable += 3
    return result


def edge_index(first: int, second: int) -> int:
    if first > second:
        first, second = second, first
    return allowed_edges().index((first, second))


def entry(
    vertex: int,
    neighbour: int,
    vertex_colour: int,
    neighbour_colour: int,
) -> int:
    if vertex < neighbour:
        row, column = vertex_colour, neighbour_colour
    else:
        row, column = neighbour_colour, vertex_colour
    return (
        1
        + 9 * edge_index(vertex, neighbour)
        + 3 * row
        + column
    )


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
            "tmp/degree3_pure_minor_constraints_audit.json"
        ),
    )
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    base = Path(manifest["base_cnf"])
    output = Path(manifest["output_cnf"])
    if sha256(base) != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash mismatch")
    if sha256(output) != manifest["output_cnf_sha256"]:
        raise AssertionError("output CNF hash mismatch")
    old_variables, old_clauses = header(base)
    new_variables, new_clauses = header(output)
    if new_variables != old_variables:
        raise AssertionError("augmentation unexpectedly added variables")

    variable_map = allocations()
    star_center = int(manifest.get("star_center", 0))
    colour_neighbours = list(
        map(int, manifest.get("colour_neighbours", [1, 2, 3]))
    )
    if (
        star_center in colour_neighbours
        or len(set(colour_neighbours)) != 3
    ):
        raise AssertionError("malformed labelled star")
    all_special = {
        variable
        for pair in variable_map.values()
        for variable in pair
    }
    observed_definitions: set[tuple[int, ...]] = set()
    with base.open("r", encoding="ascii") as handle:
        next(handle)
        for line in handle:
            clause = parse_clause(line)
            if any(abs(literal) in all_special for literal in clause):
                observed_definitions.add(clause)

    for (vertex, colour, neighbour), (
        candidate,
        anchor,
    ) in variable_map.items():
        inside = [
            entry(vertex, neighbour, row, colour)
            for row in range(3)
        ]
        outside = [
            entry(vertex, neighbour, row, other)
            for row in range(3)
            for other in range(3)
            if other != colour
        ]
        candidate_clauses = {
            *{(-candidate, -literal) for literal in outside},
            tuple([-candidate, *inside]),
            *{
                tuple([*outside, -literal, candidate])
                for literal in inside
            },
        }
        diagonal = entry(
            vertex, neighbour, colour, colour
        )
        row_outside = [
            entry(vertex, neighbour, colour, other)
            for other in range(3)
            if other != colour
        ]
        anchor_clauses = {
            (-anchor, diagonal),
            *{(-anchor, -literal) for literal in row_outside},
            tuple([-diagonal, *row_outside, anchor]),
        }
        missing = (
            candidate_clauses | anchor_clauses
        ) - observed_definitions
        if missing:
            raise AssertionError(
                "candidate or anchor definition changed for "
                f"{(vertex, colour, neighbour)}: {missing}"
            )

    expected_rows: list[dict[str, object]] = []
    expected_tail: list[list[int]] = []
    for colour in range(3):
        deleted = {
            star_center,
            colour_neighbours[colour],
        }
        remaining = [
            vertex for vertex in range(8) if vertex not in deleted
        ]
        for vertex in remaining:
            neighbours = [
                neighbour
                for neighbour in remaining
                if neighbour != vertex
                and (vertex, colour, neighbour) in variable_map
            ]
            if not neighbours:
                raise AssertionError(
                    "pure-minor vertex has no allowed neighbour"
                )
            killer_clause = [
                variable_map[vertex, colour, neighbour][0]
                for neighbour in neighbours
            ]
            anchor_clause = [
                variable_map[vertex, colour, neighbour][1]
                for neighbour in neighbours
            ]
            expected_tail.extend([killer_clause, anchor_clause])
            expected_rows.append(
                {
                    "colour": colour,
                    "deleted_vertices": sorted(deleted),
                    "vertex": vertex,
                    "eligible_neighbours": neighbours,
                    "killer_clause": killer_clause,
                    "anchor_clause": anchor_clause,
                }
            )
    if manifest["rows"] != expected_rows:
        raise AssertionError("pure-minor clause manifest changed")
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
        "base_cnf_sha256": sha256(base),
        "output_cnf_sha256": sha256(output),
        "candidate_anchor_definitions_checked": len(variable_map),
        "pure_minors": 3,
        "vertices_per_minor": 6,
        "killer_clauses": len(expected_rows),
        "anchor_clauses": len(expected_rows),
        "appended_clauses": len(expected_tail),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
