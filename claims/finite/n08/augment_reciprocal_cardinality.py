"""Add the reciprocal-killer counting consequence to a dense n=8 CNF.

In ``center_degree=1`` mode, ``eight_vertex_local_degree4_support.py``
allocates the complete-graph killer-candidate variables in a deterministic
order beginning at variable 905.  For every edge ``{u,v}`` and ordered
colour pair ``(c,d)``, this script introduces

    reciprocal(u,v,c,d) <-> candidate(u,c,v) & candidate(v,d,u).

A nonzero block can satisfy at most one such ordered colour pair.  Choosing
one candidate for each of the 24 (vertex, colour) pairs and double-counting
the selected undirected edges shows that a support with at most ``m`` blocks
has at least ``24-m`` reciprocal blocks.  The requested cardinality bound is
then encoded with PySAT's sequential counter.
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
        prefix, kind, raw_variables, raw_clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError("input is not a DIMACS CNF")
    return int(raw_variables), int(raw_clauses)


def allowed_edges(center_degree: int) -> tuple[tuple[int, int], ...]:
    if center_degree not in (1, 3, 4):
        raise ValueError("center degree must be one, three, or four")
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
                # The generator allocates candidate, non-coordinate, anchor.
                next_variable += 3
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--minimum-reciprocals", type=int, required=True)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(1, 3, 4),
        default=1,
    )
    parser.add_argument(
        "--candidate-base",
        type=int,
        default=CANDIDATE_BASE,
    )
    args = parser.parse_args()

    old_variables, old_clauses = header(args.base_cnf)
    candidates = candidate_map(
        args.center_degree, args.candidate_base
    )
    if args.center_degree == 1 and args.candidate_base == CANDIDATE_BASE:
        if candidates[0, 0, 1] != 905:
            raise AssertionError("normalized candidate allocation changed")
        if candidates[1, 0, 0] != 968:
            raise AssertionError(
                "same-colour reciprocal allocation changed"
            )
        if candidates[1, 1, 0] != 989:
            raise AssertionError(
                "different-colour reciprocal allocation changed"
            )

    reciprocal_rows: list[dict[str, object]] = []
    definition_clauses: list[list[int]] = []
    reciprocal_variables: list[int] = []
    next_variable = old_variables
    for first, second in allowed_edges(args.center_degree):
            for first_colour in range(D):
                for second_colour in range(D):
                    next_variable += 1
                    reciprocal = next_variable
                    forward = candidates[first, first_colour, second]
                    reverse = candidates[second, second_colour, first]
                    definition_clauses.extend(
                        [
                            [-reciprocal, forward],
                            [-reciprocal, reverse],
                            [reciprocal, -forward, -reverse],
                        ]
                    )
                    reciprocal_variables.append(reciprocal)
                    reciprocal_rows.append(
                        {
                            "edge": [first, second],
                            "colours": [
                                first_colour,
                                second_colour,
                            ],
                            "forward_candidate": forward,
                            "reverse_candidate": reverse,
                            "reciprocal_variable": reciprocal,
                        }
                    )

    bound = args.minimum_reciprocals
    if not 0 <= bound <= len(reciprocal_variables):
        raise ValueError("invalid reciprocal lower bound")
    cardinality = CardEnc.atleast(
        lits=reciprocal_variables,
        bound=bound,
        top_id=next_variable,
        encoding=EncType.seqcounter,
    )
    appended = [
        *definition_clauses,
        *(list(map(int, clause)) for clause in cardinality.clauses),
    ]
    new_variables = int(cardinality.nv)
    new_clauses = old_clauses + len(appended)

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("r", encoding="ascii") as reader, (
        args.output_cnf.open("w", encoding="ascii")
    ) as writer:
        next(reader)
        writer.write(f"p cnf {new_variables} {new_clauses}\n")
        for line in reader:
            writer.write(line)
        for clause in appended:
            writer.write(
                " ".join(map(str, clause)) + " 0\n"
            )

    payload = {
        "scope": (
            "reciprocal-killer cardinality consequence for the "
            "complete-ambient normalized n=8 support CNF"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "old_variables": old_variables,
        "old_clauses": old_clauses,
        "new_variables": new_variables,
        "new_clauses": new_clauses,
        "center_degree": args.center_degree,
        "allowed_edges": len(allowed_edges(args.center_degree)),
        "candidate_base": args.candidate_base,
        "directed_killer_incidences": N * D,
        "minimum_reciprocals": bound,
        "reciprocal_variables": len(reciprocal_variables),
        "definition_clauses": len(definition_clauses),
        "cardinality_clauses": len(cardinality.clauses),
        "reciprocals": reciprocal_rows,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
