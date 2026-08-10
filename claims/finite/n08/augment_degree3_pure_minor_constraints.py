"""Add killer and anchor consequences of the three pure deleted minors.

For the normalized degree-three singleton star

    W_01 = a0 e0 e0^T,
    W_02 = a1 e1 e1^T,
    W_03 = a2 e2 e2^T,

expansion at vertex 0 shows that deleting vertices 0 and c+1 leaves a
six-vertex matching tensor equal to a nonzero multiple of e_c^{tensor 6}.
The one-term annihilator argument applied inside that induced tensor says
that every remaining vertex has a colour-c killer and a colour-c diagonal
anchor whose other endpoint also remains in the induced tensor.

The center-degree-three support CNF allocates, for each (v,c,u), a killer
candidate followed by a non-coordinate flag and an anchor.  Candidate
allocation begins at variable 750.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from augment_reciprocal_cardinality import candidate_map


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError("input is not a DIMACS CNF")
    return int(variables), int(clauses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--star-center", type=int, default=0)
    parser.add_argument("--colour-0-neighbour", type=int, default=1)
    parser.add_argument("--colour-1-neighbour", type=int, default=2)
    parser.add_argument("--colour-2-neighbour", type=int, default=3)
    args = parser.parse_args()

    variables, clauses = header(args.base_cnf)
    candidates = candidate_map(center_degree=3, candidate_base=750)
    colour_neighbours = [
        args.colour_0_neighbour,
        args.colour_1_neighbour,
        args.colour_2_neighbour,
    ]
    if (
        args.star_center in colour_neighbours
        or len(set(colour_neighbours)) != 3
    ):
        raise ValueError("the labelled star vertices are not distinct")
    if any(
        (args.star_center, colour, neighbour) not in candidates
        for colour, neighbour in enumerate(colour_neighbours)
    ):
        raise ValueError("a labelled star edge is structurally absent")
    appended: list[list[int]] = []
    rows: list[dict[str, object]] = []
    for colour in range(3):
        deleted = {
            args.star_center,
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
                and (vertex, colour, neighbour) in candidates
            ]
            if not neighbours:
                raise AssertionError(
                    "a pure-minor vertex has no structurally allowed "
                    "candidate neighbour"
                )
            killer_clause = [
                candidates[vertex, colour, neighbour]
                for neighbour in neighbours
            ]
            anchor_clause = [
                candidates[vertex, colour, neighbour] + 2
                for neighbour in neighbours
            ]
            appended.extend([killer_clause, anchor_clause])
            rows.append(
                {
                    "colour": colour,
                    "deleted_vertices": sorted(deleted),
                    "vertex": vertex,
                    "eligible_neighbours": neighbours,
                    "killer_clause": killer_clause,
                    "anchor_clause": anchor_clause,
                }
            )

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("r", encoding="ascii") as reader, (
        args.output_cnf.open("w", encoding="ascii")
    ) as writer:
        next(reader)
        writer.write(
            f"p cnf {variables} {clauses + len(appended)}\n"
        )
        for line in reader:
            writer.write(line)
        for clause in appended:
            writer.write(" ".join(map(str, clause)) + " 0\n")

    payload = {
        "scope": (
            "killer and diagonal-anchor consequences of the three pure "
            "six-vertex deleted minors at a normalized degree-three star"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "variables": variables,
        "old_clauses": clauses,
        "new_clauses": clauses + len(appended),
        "candidate_base": 750,
        "star_center": args.star_center,
        "colour_neighbours": colour_neighbours,
        "pure_minors": 3,
        "vertices_per_minor": 6,
        "killer_clauses": len(rows),
        "anchor_clauses": len(rows),
        "appended_clauses": len(appended),
        "rows": rows,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
