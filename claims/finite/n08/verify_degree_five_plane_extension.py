"""Independently audit the degree-five shared-primary-plane extension.

At an exact degree-five neighbourhood with no monochromatic singleton,
suppose one spare block is a failure-hyperplane backup for primary colours
``c,d``.  The degree-five local flag theorem gives

    e_c in span(a_c,a_d) or e_d in span(a_c,a_d).

Each membership is one two-term determinant equation.  The support
extension forbids both determinants from having exactly one supported
monomial.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from verify_shared_backup_zero_extension import (
    D,
    N,
    allocations,
    audit_extension,
    header,
    sha256,
)


def expected_clauses() -> list[str]:
    entries, backups, neighbours = allocations()
    edges = tuple(itertools.combinations(range(N), 2))
    blocks = {
        edge: 1 + D * D * len(edges) + index
        for index, edge in enumerate(edges)
    }

    # With 28 block variables and a Sinz at-most-20 counter, the 27 by 20
    # auxiliary variables occupy 281..820.  The 84 singleton indicators
    # are then allocated edge-major, colour-minor at 821..904.
    singleton_base = D * D * len(edges) + len(edges) + 27 * 20 + 1
    singletons = {
        (edge, colour): singleton_base + D * index + colour
        for index, edge in enumerate(edges)
        for colour in range(D)
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

    clauses: list[str] = []
    for vertex in range(N):
        incident_edges = [
            tuple(sorted((vertex, neighbour)))
            for neighbour in neighbours[vertex]
        ]
        for exact_neighbourhood in itertools.combinations(
            incident_edges, 5
        ):
            exact = set(exact_neighbourhood)
            exact_activation = [
                *(-blocks[edge] for edge in exact_neighbourhood),
                *(
                    blocks[edge]
                    for edge in incident_edges
                    if edge not in exact
                ),
                *(
                    singletons[edge, colour]
                    for edge in exact_neighbourhood
                    for colour in range(D)
                ),
            ]
            exact_neighbours = [
                edge[1] if edge[0] == vertex else edge[0]
                for edge in exact_neighbourhood
            ]
            for first_colour, second_colour in itertools.combinations(
                range(D), 2
            ):
                for first_neighbour in exact_neighbours:
                    first_vector = [
                        entry(
                            vertex,
                            first_neighbour,
                            row,
                            first_colour,
                        )
                        for row in range(D)
                    ]
                    for second_neighbour in exact_neighbours:
                        if second_neighbour == first_neighbour:
                            continue
                        second_vector = [
                            entry(
                                vertex,
                                second_neighbour,
                                row,
                                second_colour,
                            )
                            for row in range(D)
                        ]
                        for backup_neighbour in exact_neighbours:
                            if backup_neighbour in {
                                first_neighbour,
                                second_neighbour,
                            }:
                                continue
                            shared = (
                                backups[
                                    vertex,
                                    first_colour,
                                    first_neighbour,
                                    backup_neighbour,
                                ],
                                backups[
                                    vertex,
                                    second_colour,
                                    second_neighbour,
                                    backup_neighbour,
                                ],
                            )
                            determinant_terms: dict[
                                int,
                                tuple[
                                    tuple[int, int],
                                    tuple[int, int],
                                ],
                            ] = {}
                            for coordinate in (
                                first_colour,
                                second_colour,
                            ):
                                first_row, second_row = [
                                    row
                                    for row in range(D)
                                    if row != coordinate
                                ]
                                determinant_terms[coordinate] = (
                                    (
                                        first_vector[first_row],
                                        second_vector[second_row],
                                    ),
                                    (
                                        first_vector[second_row],
                                        second_vector[first_row],
                                    ),
                                )
                            first_terms = determinant_terms[
                                first_colour
                            ]
                            second_terms = determinant_terms[
                                second_colour
                            ]
                            for first_active in range(2):
                                first_on = first_terms[first_active]
                                first_off = first_terms[
                                    1 - first_active
                                ]
                                for second_active in range(2):
                                    second_on = second_terms[
                                        second_active
                                    ]
                                    second_off = second_terms[
                                        1 - second_active
                                    ]
                                    for first_missing in first_off:
                                        for second_missing in second_off:
                                            literals = [
                                                *exact_activation,
                                                *(-value for value in shared),
                                                *(-value for value in first_on),
                                                first_missing,
                                                *(-value for value in second_on),
                                                second_missing,
                                            ]
                                            clauses.append(
                                                " ".join(
                                                    str(value)
                                                    for value in literals
                                                )
                                                + " 0\n"
                                            )
    if len(clauses) != 483_840:
        raise AssertionError("degree-five plane clause count changed")
    return clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--extended-cnf", type=Path, required=True)
    parser.add_argument("--extended-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(
        args.extended_manifest.read_text(encoding="utf-8")
    )
    clauses = expected_clauses()
    audit_extension(args.base_cnf, args.extended_cnf, clauses)
    if (
        int(manifest["degree_five_plane_clauses"]) != len(clauses)
        or int(manifest["variables"]) != header(args.extended_cnf)[0]
        or int(manifest["clauses"]) != header(args.extended_cnf)[1]
        or Path(str(manifest["cnf"])) != args.extended_cnf
    ):
        raise AssertionError("extended generator manifest changed")

    payload = {
        "verified": True,
        "scope": (
            "exact-degree-five shared-primary-plane support extension"
        ),
        "clauses": len(clauses),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "extended_cnf": str(args.extended_cnf),
        "extended_cnf_sha256": sha256(args.extended_cnf),
        "extended_manifest": str(args.extended_manifest),
        "extended_manifest_sha256": sha256(
            args.extended_manifest
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
