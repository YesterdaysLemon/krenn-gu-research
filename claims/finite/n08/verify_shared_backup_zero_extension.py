"""Independently audit the shared-backup zero-column CNF extension.

The checked theorem is local.  If one incident block ``B`` is a
failure-hyperplane backup for two distinct colours ``c,d``, then its third
colour-column is zero.  The two backup conditions imply

    B[:,d] in span(a_c) but not in span(a_d),
    B[:,c] in span(a_d) but not in span(a_c),

so the primary lines are distinct.  The remaining column lies in both
lines and must vanish.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


N = 8
D = 3
CANDIDATE_BASE = 905


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, raw_variables, raw_clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError(f"{path} is not DIMACS CNF")
    return int(raw_variables), int(raw_clauses)


def allocations() -> tuple[
    dict[tuple[int, int, int, int], int],
    dict[tuple[int, int, int, int], int],
    dict[int, list[int]],
]:
    edges = tuple(itertools.combinations(range(N), 2))
    entries: dict[tuple[int, int, int, int], int] = {}
    next_entry = 1
    for first, second in edges:
        for row in range(D):
            for column in range(D):
                entries[first, second, row, column] = next_entry
                next_entry += 1

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

    neighbours = {
        vertex: [
            other for other in range(N) if other != vertex
        ]
        for vertex in range(N)
    }
    next_variable = CANDIDATE_BASE - 1
    for vertex in range(N):
        for colour in range(D):
            for _neighbour in neighbours[vertex]:
                # Candidate, non-coordinate flag, diagonal anchor.
                next_variable += 3
    if next_variable != 1408:
        raise AssertionError("candidate allocation changed")

    support_products: dict[tuple[int, ...], int] = {}
    backups: dict[tuple[int, int, int, int], int] = {}
    for vertex in range(N):
        for colour in range(D):
            for killer_neighbour in neighbours[vertex]:
                first_vector = [
                    entry(vertex, killer_neighbour, row, colour)
                    for row in range(D)
                ]
                for backup_neighbour in neighbours[vertex]:
                    if backup_neighbour == killer_neighbour:
                        continue
                    next_variable += 1
                    backups[
                        vertex,
                        colour,
                        killer_neighbour,
                        backup_neighbour,
                    ] = next_variable
                    second_vector = [
                        entry(vertex, backup_neighbour, row, colour)
                        for row in range(D)
                    ]
                    for first_row, second_row in itertools.permutations(
                        range(D), 2
                    ):
                        key = tuple(
                            sorted(
                                (
                                    first_vector[first_row],
                                    second_vector[second_row],
                                )
                            )
                        )
                        if key not in support_products:
                            next_variable += 1
                            support_products[key] = next_variable
    if len(backups) != 1008:
        raise AssertionError("backup allocation count changed")
    return entries, backups, neighbours


def expected_clauses() -> list[str]:
    entries, backups, neighbours = allocations()

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
        for first_colour, second_colour in itertools.combinations(
            range(D), 2
        ):
            remaining_colour = next(
                colour
                for colour in range(D)
                if colour not in {first_colour, second_colour}
            )
            for first_neighbour in neighbours[vertex]:
                for second_neighbour in neighbours[vertex]:
                    if second_neighbour == first_neighbour:
                        continue
                    for backup_neighbour in neighbours[vertex]:
                        if backup_neighbour in {
                            first_neighbour,
                            second_neighbour,
                        }:
                            continue
                        first_backup = backups[
                            vertex,
                            first_colour,
                            first_neighbour,
                            backup_neighbour,
                        ]
                        second_backup = backups[
                            vertex,
                            second_colour,
                            second_neighbour,
                            backup_neighbour,
                        ]
                        for row in range(D):
                            clauses.append(
                                f"-{first_backup} -{second_backup} "
                                f"-{entry(vertex, backup_neighbour, row, remaining_colour)} 0\n"
                            )
    if len(clauses) != 15_120:
        raise AssertionError("shared-backup clause count changed")
    return clauses


def audit_extension(
    base: Path, extended: Path, inserted: list[str]
) -> None:
    base_variables, base_clauses = header(base)
    extended_variables, extended_clauses = header(extended)
    if extended_variables != base_variables:
        raise AssertionError("extension changed the variable count")
    if extended_clauses != base_clauses + len(inserted):
        raise AssertionError("extension clause count is inconsistent")

    with base.open(
        "r", encoding="ascii"
    ) as original, extended.open("r", encoding="ascii") as augmented:
        next(original)
        next(augmented)
        inserted_checked = False
        new_line = augmented.readline()
        for clause_index, old_line in enumerate(original, start=1):
            if new_line != old_line and not inserted_checked:
                for expected in inserted:
                    if new_line != expected:
                        raise AssertionError(
                            "shared-backup clause block changed at base "
                            f"clause {clause_index}"
                        )
                    new_line = augmented.readline()
                inserted_checked = True
            if new_line != old_line:
                raise AssertionError(
                    f"base clause {clause_index} changed"
                )
            new_line = augmented.readline()
        if not inserted_checked:
            for expected in inserted:
                if new_line != expected:
                    raise AssertionError(
                        "trailing shared-backup clause block changed"
                    )
                new_line = augmented.readline()
            inserted_checked = True
        if new_line:
            raise AssertionError("extended CNF has an unexpected tail")


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
        int(manifest["shared_backup_zero_clauses"]) != len(clauses)
        or int(manifest["variables"]) != header(args.extended_cnf)[0]
        or int(manifest["clauses"]) != header(args.extended_cnf)[1]
        or Path(str(manifest["cnf"])) != args.extended_cnf
    ):
        raise AssertionError("extended generator manifest changed")

    payload = {
        "verified": True,
        "scope": "shared failure-backup zero-column CNF extension",
        "clauses": len(clauses),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "extended_cnf": str(args.extended_cnf),
        "extended_cnf_sha256": sha256(args.extended_cnf),
        "extended_manifest": str(args.extended_manifest),
        "extended_manifest_sha256": sha256(args.extended_manifest),
    }
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
