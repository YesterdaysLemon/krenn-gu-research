"""Add exact support consequences of one or more degree-three singleton stars.

If a degree-three vertex ``v`` has its colour-c singleton on ``u_c``, expansion
at ``v`` proves that the perfect-matching tensor after deleting ``v,u_c`` is a
nonzero scalar multiple of ``e_c`` to the tensor power ``n-2``.  On supports:

* the all-c amplitude has at least one supported matching monomial;
* every other amplitude has either zero or at least two supported monomials.

The input CNF uses the normalized n=8, d=3 local entry allocation.  A star is
given as ``CENTER:N0,N1,N2``, where ``Nc`` is its colour-c singleton neighbour.
The appended constraints are intentionally unguarded, so the resulting CNF is
case-specific unless the supplied stars have already been forced by the base.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


Edge = tuple[int, int]
Star = tuple[int, tuple[int, int, int]]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError("input is not a DIMACS CNF")
    return int(variables), int(clauses)


def allowed_edges() -> tuple[Edge, ...]:
    return tuple(
        edge
        for edge in itertools.combinations(range(8), 2)
        if edge[0] != 0 or edge[1] <= 3
    )


def entry(
    first: int,
    second: int,
    first_colour: int,
    second_colour: int,
) -> int:
    edges = allowed_edges()
    if first < second:
        edge = (first, second)
        row, column = first_colour, second_colour
    else:
        edge = (second, first)
        row, column = second_colour, first_colour
    return 1 + 9 * edges.index(edge) + 3 * row + column


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[tuple[Edge, ...]] = []
    allowed = set(allowed_edges())
    for index in range(1, len(vertices)):
        second = vertices[index]
        edge = tuple(sorted((first, second)))
        if edge not in allowed:
            continue
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            result.append((edge, *tail))
    return tuple(result)


def parse_star(text: str) -> Star:
    try:
        center_text, neighbours_text = text.split(":", 1)
        center = int(center_text)
        neighbours = tuple(map(int, neighbours_text.split(",")))
    except (TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError(
            "star must have form CENTER:N0,N1,N2"
        ) from error
    if len(neighbours) != 3:
        raise argparse.ArgumentTypeError(
            "star must list exactly three colour neighbours"
        )
    if not 0 <= center < 8 or any(not 0 <= value < 8 for value in neighbours):
        raise argparse.ArgumentTypeError("star vertices must lie in 0..7")
    if center in neighbours or len(set(neighbours)) != 3:
        raise argparse.ArgumentTypeError("star vertices must be distinct")
    return center, (neighbours[0], neighbours[1], neighbours[2])


def pure_conditions(stars: list[Star]) -> list[tuple[tuple[int, ...], int]]:
    conditions: list[tuple[tuple[int, ...], int]] = []
    seen: set[tuple[tuple[int, ...], int]] = set()
    for center, neighbours in stars:
        for colour, neighbour in enumerate(neighbours):
            remaining = tuple(
                vertex
                for vertex in range(8)
                if vertex not in {center, neighbour}
            )
            key = (remaining, colour)
            if key not in seen:
                seen.add(key)
                conditions.append(key)
    return conditions


def build_tail(
    old_variables: int,
    conditions: list[tuple[tuple[int, ...], int]],
) -> tuple[list[list[int]], list[dict[str, object]], int]:
    next_variable = old_variables + 1
    indicator_for: dict[tuple[int, ...], int] = {}
    clauses: list[list[int]] = []
    rows: list[dict[str, object]] = []

    for vertices, target_colour in conditions:
        matchings = perfect_matchings(vertices)
        required_rows = 0
        forbidden_rows = 0
        for colouring in itertools.product(range(3), repeat=len(vertices)):
            colour_of = dict(zip(vertices, colouring, strict=True))
            indicators: list[int] = []
            for matching in matchings:
                factors = tuple(
                    sorted(
                        entry(
                            first,
                            second,
                            colour_of[first],
                            colour_of[second],
                        )
                        for first, second in matching
                    )
                )
                indicator = indicator_for.get(factors)
                if indicator is None:
                    indicator = next_variable
                    next_variable += 1
                    indicator_for[factors] = indicator
                    for factor in factors:
                        clauses.append([-indicator, factor])
                    clauses.append([indicator, *(-factor for factor in factors)])
                indicators.append(indicator)

            is_target = all(colour == target_colour for colour in colouring)
            if is_target:
                clauses.append(indicators)
                required_rows += 1
            else:
                for index, indicator in enumerate(indicators):
                    clauses.append(
                        [
                            -indicator,
                            *(
                                other
                                for other_index, other in enumerate(indicators)
                                if other_index != index
                            ),
                        ]
                    )
                forbidden_rows += 1
        rows.append(
            {
                "vertices": list(vertices),
                "target_colour": target_colour,
                "perfect_matchings": len(matchings),
                "colourings": 3 ** len(vertices),
                "required_rows": required_rows,
                "forbidden_rows": forbidden_rows,
            }
        )
    return clauses, rows, next_variable - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--star",
        action="append",
        type=parse_star,
        required=True,
        help="forced singleton star CENTER:N0,N1,N2; repeat as needed",
    )
    args = parser.parse_args()

    old_variables, old_clauses = header(args.base_cnf)
    conditions = pure_conditions(args.star)
    appended, rows, new_variables = build_tail(old_variables, conditions)

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("r", encoding="ascii") as reader, (
        args.output_cnf.open("w", encoding="ascii")
    ) as writer:
        next(reader)
        writer.write(
            f"p cnf {new_variables} {old_clauses + len(appended)}\n"
        )
        for line in reader:
            writer.write(line)
        for clause in appended:
            writer.write(" ".join(map(str, clause)) + " 0\n")

    payload = {
        "scope": (
            "support consequences of forced pure deleted tensors from "
            "degree-three singleton stars"
        ),
        "warning": (
            "constraints are unguarded and the output is case-specific "
            "unless every listed star is already forced"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "stars": [
            {"center": center, "colour_neighbours": list(neighbours)}
            for center, neighbours in args.star
        ],
        "old_variables": old_variables,
        "new_variables": new_variables,
        "old_clauses": old_clauses,
        "new_clauses": old_clauses + len(appended),
        "pure_tensors": len(conditions),
        "monomial_indicators": new_variables - old_variables,
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
