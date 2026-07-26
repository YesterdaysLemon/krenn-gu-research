"""Conditionally encode the degree-three singleton-star theorem for n=8."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from eight_vertex_sparse_exact import local_allowed_edges


N = 8
D = 3


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError(f"{path} is not DIMACS CNF")
    return int(variables), int(clauses)


def extension(
    old_variables: int,
) -> tuple[list[list[int]], list[dict[str, object]], int]:
    edges = tuple(local_allowed_edges(3))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    first_block = 1 + 9 * len(edges)

    def ordered_edge(first: int, second: int) -> tuple[int, int]:
        return (
            (first, second)
            if first < second
            else (second, first)
        )

    def block(first: int, second: int) -> int:
        return first_block + edge_index[ordered_edge(first, second)]

    def entry(
        first: int,
        second: int,
        first_colour: int,
        second_colour: int,
    ) -> int:
        if first > second:
            first, second = second, first
            first_colour, second_colour = (
                second_colour,
                first_colour,
            )
        return (
            1
            + 9 * edge_index[first, second]
            + 3 * first_colour
            + second_colour
        )

    neighbours = {vertex: [] for vertex in range(N)}
    for first, second in edges:
        neighbours[first].append(second)
        neighbours[second].append(first)

    output: list[list[int]] = []
    rows: list[dict[str, object]] = []
    next_variable = old_variables
    for vertex in range(N):
        incident = tuple(neighbours[vertex])
        for chosen in itertools.combinations(incident, 3):
            next_variable += 1
            indicator = next_variable
            chosen_set = set(chosen)
            inside = [
                block(vertex, neighbour) for neighbour in chosen
            ]
            outside = [
                block(vertex, neighbour)
                for neighbour in incident
                if neighbour not in chosen_set
            ]
            output.extend(
                [-indicator, variable] for variable in inside
            )
            output.extend(
                [-indicator, -variable] for variable in outside
            )
            output.append(
                [
                    indicator,
                    *(-variable for variable in inside),
                    *outside,
                ]
            )

            diagonal: dict[tuple[int, int], int] = {}
            for neighbour in chosen:
                for first_colour in range(D):
                    for second_colour in range(D):
                        variable = entry(
                            vertex,
                            neighbour,
                            first_colour,
                            second_colour,
                        )
                        if first_colour != second_colour:
                            output.append([-indicator, -variable])
                diagonal.update(
                    {
                        (neighbour, colour): entry(
                            vertex,
                            neighbour,
                            colour,
                            colour,
                        )
                        for colour in range(D)
                    }
                )

            for neighbour in chosen:
                values = [
                    diagonal[neighbour, colour]
                    for colour in range(D)
                ]
                output.append([-indicator, *values])
                for first, second in itertools.combinations(values, 2):
                    output.append(
                        [-indicator, -first, -second]
                    )
            for colour in range(D):
                values = [
                    diagonal[neighbour, colour]
                    for neighbour in chosen
                ]
                output.append([-indicator, *values])
                for first, second in itertools.combinations(values, 2):
                    output.append(
                        [-indicator, -first, -second]
                    )
            rows.append(
                {
                    "vertex": vertex,
                    "neighbours": list(chosen),
                    "indicator": indicator,
                }
            )
    return output, rows, next_variable


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    old_variables, old_clauses = header(args.base_cnf)
    appended, rows, new_variables = extension(old_variables)
    new_clauses = old_clauses + len(appended)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("r", encoding="ascii") as reader, (
        args.output_cnf.open("w", encoding="ascii")
    ) as writer:
        next(reader)
        writer.write(f"p cnf {new_variables} {new_clauses}\n")
        for line in reader:
            writer.write(line)
        for row in appended:
            writer.write(" ".join(map(str, row)) + " 0\n")

    payload = {
        "scope": (
            "conditional degree-three singleton-star theorem for every "
            "allowed n=8 neighbourhood"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "center_degree": 3,
        "old_variables": old_variables,
        "old_clauses": old_clauses,
        "new_variables": new_variables,
        "new_clauses": new_clauses,
        "neighbourhood_indicators": len(rows),
        "appended_clauses": len(appended),
        "neighbourhoods": rows,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
