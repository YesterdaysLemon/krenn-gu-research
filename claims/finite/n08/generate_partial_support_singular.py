"""Generate an exact Singular test for a partially specified support cube."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from eight_vertex_degree4_cegar import full_equations
from eight_vertex_sparse_exact import (
    exact_equations,
    local_allowed_edges,
    singular_program,
)
from search_witness import EquationSystem


def parse_pure_tensor(text: str) -> tuple[tuple[int, ...], int]:
    try:
        vertices_text, colour_text = text.split(":", 1)
        vertices = tuple(map(int, vertices_text.split(",")))
        colour = int(colour_text)
    except (TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError(
            "pure tensor must have form V0,V1,...:COLOUR"
        ) from error
    if (
        not vertices
        or len(vertices) % 2
        or len(set(vertices)) != len(vertices)
        or any(not 0 <= vertex < 8 for vertex in vertices)
        or colour not in range(3)
    ):
        raise argparse.ArgumentTypeError("invalid pure tensor descriptor")
    return tuple(sorted(vertices)), colour


def parse_star(text: str) -> tuple[int, tuple[int, int, int]]:
    try:
        center_text, neighbours_text = text.split(":", 1)
        center = int(center_text)
        neighbours = tuple(map(int, neighbours_text.split(",")))
    except (TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError(
            "star must have form CENTER:N0,N1,N2"
        ) from error
    if (
        not 0 <= center < 8
        or len(neighbours) != 3
        or center in neighbours
        or len(set(neighbours)) != 3
        or any(not 0 <= neighbour < 8 for neighbour in neighbours)
    ):
        raise argparse.ArgumentTypeError("invalid singleton star descriptor")
    return center, (neighbours[0], neighbours[1], neighbours[2])


def star_pure_tensors(
    stars: list[tuple[int, tuple[int, int, int]]],
) -> list[tuple[tuple[int, ...], int]]:
    result: list[tuple[tuple[int, ...], int]] = []
    seen: set[tuple[tuple[int, ...], int]] = set()
    for center, neighbours in stars:
        for colour, neighbour in enumerate(neighbours):
            descriptor = (
                tuple(
                    vertex
                    for vertex in range(8)
                    if vertex not in {center, neighbour}
                ),
                colour,
            )
            if descriptor not in seen:
                seen.add(descriptor)
                result.append(descriptor)
    return result


def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[tuple[tuple[int, int], ...]] = []
    for partner_index, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:partner_index] + vertices[partner_index + 1 :]
        for tail in perfect_matchings(rest):
            result.append(((first, partner), *tail))
    return tuple(result)


def pure_vanishing_equations(
    system: EquationSystem,
    variable_names: dict[int, str],
    descriptors: list[tuple[tuple[int, ...], int]],
) -> list[Counter[tuple[str, ...]]]:
    equations: list[Counter[tuple[str, ...]]] = []
    seen: set[tuple[tuple[tuple[str, ...], int], ...]] = set()
    for vertices, target_colour in descriptors:
        matchings = perfect_matchings(vertices)
        for colouring in itertools.product(range(3), repeat=len(vertices)):
            if all(colour == target_colour for colour in colouring):
                continue
            colour_of = dict(zip(vertices, colouring, strict=True))
            polynomial: Counter[tuple[str, ...]] = Counter()
            for matching in matchings:
                monomial: list[str] = []
                for first, second in matching:
                    row, column = colour_of[first], colour_of[second]
                    flat = (
                        9 * system.edge_index[(first, second)]
                        + 3 * row
                        + column
                    )
                    if flat not in variable_names:
                        break
                    monomial.append(variable_names[flat])
                else:
                    polynomial[tuple(sorted(monomial))] += 1
            polynomial = Counter(
                {
                    monomial: coefficient
                    for monomial, coefficient in polynomial.items()
                    if coefficient
                }
            )
            if not polynomial:
                continue
            signature = tuple(sorted(polynomial.items()))
            if signature not in seen:
                seen.add(signature)
                equations.append(polynomial)
    return equations


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--fallback-index", type=int, default=0)
    parser.add_argument(
        "--free-index",
        type=int,
        action="append",
        default=[],
        help=(
            "zero-based flat entry left unspecified; repeat as needed"
        ),
    )
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument(
        "--pure-tensor",
        action="append",
        type=parse_pure_tensor,
        default=[],
        help=(
            "known pure deleted tensor V0,V1,...:COLOUR; its forbidden "
            "amplitudes are added after division by the forced star weight"
        ),
    )
    parser.add_argument(
        "--star",
        action="append",
        type=parse_star,
        default=[],
        help=(
            "forced exact singleton star CENTER:N0,N1,N2; the support cube "
            "is checked and its three pure deleted tensors are derived"
        ),
    )
    args = parser.parse_args()

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    fallback_rows: list[tuple[dict[str, object], dict[str, object]]] = []
    for row in batch["rows"]:
        if "fallback" in row:
            fallback_rows.append((row, row["fallback"]))
        for fallback in row.get("fallbacks", []):
            fallback_rows.append((row, fallback))
    if not 0 <= args.fallback_index < len(fallback_rows):
        raise ValueError("--fallback-index is outside the fallback catalogue")
    row, fallback = fallback_rows[args.fallback_index]
    system = EquationSystem(8, 3)
    _, flat_names, _ = full_equations(system)
    allowed = {
        9 * system.edge_index[edge] + 3 * first + second
        for edge in local_allowed_edges(
            int(batch.get("center_degree", 4))
        )
        for first in range(3)
        for second in range(3)
    }
    original_positive = set(
        map(int, fallback["selected_flat_indices"])
    )
    free = set(map(int, args.free_index))
    if not free <= allowed:
        raise ValueError("a free entry is structurally zero")
    positive = original_positive - free
    variables = positive | free
    negative = allowed - variables
    for center, neighbours in args.star:
        for colour, neighbour in enumerate(neighbours):
            edge = tuple(sorted((center, neighbour)))
            edge_flat = {
                9 * system.edge_index[edge] + 3 * row + column
                for row in range(3)
                for column in range(3)
            }
            diagonal = (
                9 * system.edge_index[edge] + 3 * colour + colour
            )
            if diagonal not in positive or not (
                edge_flat - {diagonal}
            ) <= negative:
                raise ValueError(
                    "the partial cube does not force the declared singleton"
                )
        for other in range(8):
            if other == center or other in neighbours:
                continue
            edge = tuple(sorted((center, other)))
            if edge not in local_allowed_edges(
                int(batch.get("center_degree", 4))
            ):
                continue
            edge_flat = {
                9 * system.edge_index[edge] + 3 * row + column
                for row in range(3)
                for column in range(3)
            }
            if not edge_flat <= negative:
                raise ValueError(
                    "the partial cube does not force star degree exactly three"
                )
    ordered_variables = sorted(variables)
    ordered_positive = sorted(positive)
    variable_names = {
        index: flat_names[index] for index in ordered_variables
    }
    equations = exact_equations(system, variable_names)
    star_descriptors = star_pure_tensors(args.star)
    descriptors = list(dict.fromkeys([*star_descriptors, *args.pure_tensor]))
    derived = pure_vanishing_equations(system, variable_names, descriptors)
    existing = {tuple(sorted(equation.items())) for equation in equations}
    derived = [
        equation
        for equation in derived
        if tuple(sorted(equation.items())) not in existing
    ]
    equations = [*equations, *derived]
    program = singular_program(
        [variable_names[index] for index in ordered_variables],
        equations,
        args.characteristic,
        saturation_names=[
            variable_names[index] for index in ordered_positive
        ],
    )
    args.program.parent.mkdir(parents=True, exist_ok=True)
    args.program.write_text(program, encoding="utf-8")
    payload = {
        "scope": (
            "exact amplitude ideal on a partially specified support cube"
        ),
        "batch": str(args.batch),
        "batch_sha256": sha256(args.batch),
        "fallback_index": args.fallback_index,
        "role_index": int(row["role_index"]),
        "center_degree": int(batch.get("center_degree", 4)),
        "target_edges": batch.get("target_edges"),
        "characteristic": args.characteristic,
        "positive_flat_indices": ordered_positive,
        "negative_flat_indices": sorted(negative),
        "free_flat_indices": sorted(free),
        "ring_variables": len(ordered_variables),
        "saturated_variables": len(ordered_positive),
        "equations": len(equations),
        "base_amplitude_equations": len(equations) - len(derived),
        "pure_tensors": [
            {"vertices": list(vertices), "target_colour": colour}
            for vertices, colour in descriptors
        ],
        "forced_singleton_stars": [
            {"center": center, "colour_neighbours": list(neighbours)}
            for center, neighbours in args.star
        ],
        "all_pure_tensors_derived_from_forced_stars": (
            set(descriptors) == set(star_descriptors)
        ),
        "derived_pure_vanishing_equations": len(derived),
        "program": str(args.program),
        "program_sha256": sha256(args.program),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
