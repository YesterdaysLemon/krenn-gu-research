"""Laurent CEGAR for sparse n=8 supports with one degree-four vertex.

Each SAT model fixes a zero/nonzero entry stratum.  The exact amplitude
equations on that torus are reduced by their primitive binomials.  When a
sign-incompatible Laurent equation becomes a unit, the small set of source
amplitudes yields a support conflict cube.  The cube and all twelve
symmetries preserving the canonical degree-four star are appended to the
support CNF.

This script performs one fail-closed learning step.  If Laurent reduction
does not find a unit, it refuses to learn a clause; that residual support
must instead go through an exact Gröbner fallback.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

from cancellation_transport import (
    support_cancellation_transport_conflict,
    support_two_monomial_rectangle_conflict,
)
from eight_vertex_sparse_exact import (
    local_allowed_edges,
    positive_model_literals,
    selected_flat_indices,
)
from generate_prism_singular import amplitude_polynomial
from odd_binomial_cycle import support_odd_binomial_triangle_conflict
from prism_laurent_reduction import primitive_binomial_reduction
from search_witness import EquationSystem
from signed_binomial_lattice import (
    signed_lattice_used_equations,
    support_signed_binomial_lattice_conflict,
)

Polynomial = Counter[tuple[str, ...]]


def full_equations(
    system: EquationSystem,
) -> tuple[list[Polynomial], dict[int, str], dict[str, int]]:
    names = {
        flat_index: f"w{flat_index}"
        for flat_index in range(system.variable_count)
    }
    name_to_flat = {name: flat for flat, name in names.items()}
    fixed = np.zeros(system.variable_count, dtype=np.complex128)
    equations: list[Polynomial] = []
    for raw_colouring, required in zip(
        system.colourings, system.target, strict=True
    ):
        polynomial = amplitude_polynomial(
            system,
            fixed,
            names,
            tuple(int(value) for value in raw_colouring),
        )
        if required:
            polynomial[()] -= 1
        equations.append(
            Counter(
                {
                    monomial: coefficient
                    for monomial, coefficient in polynomial.items()
                    if coefficient
                }
            )
        )
    return equations, names, name_to_flat


def laurent_conflict(
    system: EquationSystem,
    equations: list[Polynomial],
    names: dict[int, str],
    name_to_flat: dict[str, int],
    nonzero_flat: set[int],
    center_degree: int = 4,
    prefer_transport: bool = False,
) -> tuple[set[int], set[int], dict[str, object]]:
    allowed = set(local_allowed_edges(center_degree))
    structural_zero = {
        9 * system.edge_index[edge] + 3 * row + column
        for edge in system.edges
        if edge not in allowed
        for row in range(3)
        for column in range(3)
    }
    if prefer_transport:
        transport = support_cancellation_transport_conflict(
            system, nonzero_flat, structural_zero
        )
        if transport is not None:
            positive, negative, certificate = transport
            used_equations = sorted(
                (
                    int(certificate["source_equation_index"]),
                    int(certificate["transport_equation_index"]),
                )
            )
            return positive, negative, {
                "certificate_kind": "cancellation_transport",
                "selected_entries": len(nonzero_flat),
                "restricted_equations": 2,
                "binomial_equations": None,
                "binomial_rank": None,
                "unit_restricted_index": -1,
                "linear_monomial_unit_relation": None,
                "transport_certificate": certificate,
                "used_equation_indices": used_equations,
                "used_colourings": [
                    [
                        int(value)
                        for value in system.colourings[equation_index]
                    ]
                    for equation_index in used_equations
                ],
                "positive_entries": sorted(positive),
                "negative_entries": sorted(negative),
            }
        rectangle = support_two_monomial_rectangle_conflict(
            system, nonzero_flat, structural_zero
        )
        if rectangle is not None:
            positive, negative, certificate = rectangle
            used_equations = sorted(
                map(int, certificate["corner_equation_indices"])
            )
            return positive, negative, {
                "certificate_kind": "two_monomial_rectangle",
                "selected_entries": len(nonzero_flat),
                "restricted_equations": 4,
                "binomial_equations": None,
                "binomial_rank": None,
                "unit_restricted_index": -1,
                "linear_monomial_unit_relation": None,
                "rectangle_certificate": certificate,
                "used_equation_indices": used_equations,
                "used_colourings": [
                    [
                        int(value)
                        for value in system.colourings[equation_index]
                    ]
                    for equation_index in used_equations
                ],
                "positive_entries": sorted(positive),
                "negative_entries": sorted(negative),
            }
        triangle = support_odd_binomial_triangle_conflict(
            system, nonzero_flat, structural_zero
        )
        if triangle is not None:
            positive, negative, certificate = triangle
            used_equations = sorted(
                map(int, certificate["equation_indices"])
            )
            return positive, negative, {
                "certificate_kind": "odd_binomial_triangle",
                "selected_entries": len(nonzero_flat),
                "restricted_equations": 3,
                "binomial_equations": 3,
                "binomial_rank": 2,
                "unit_restricted_index": -1,
                "linear_monomial_unit_relation": None,
                "odd_triangle_certificate": certificate,
                "used_equation_indices": used_equations,
                "used_colourings": [
                    [
                        int(value)
                        for value in system.colourings[equation_index]
                    ]
                    for equation_index in used_equations
                ],
                "positive_entries": sorted(positive),
                "negative_entries": sorted(negative),
            }
        lattice = support_signed_binomial_lattice_conflict(
            system, nonzero_flat, structural_zero
        )
        if lattice is not None:
            positive, negative, certificate = lattice
            used_equations = signed_lattice_used_equations(certificate)
            return positive, negative, {
                "certificate_kind": "signed_binomial_lattice",
                "selected_entries": len(nonzero_flat),
                "restricted_equations": len(used_equations),
                "binomial_equations": len(
                    certificate["basis_relations"]
                ),
                "binomial_rank": len(
                    certificate["basis_relations"]
                ),
                "unit_restricted_index": -1,
                "linear_monomial_unit_relation": None,
                "signed_lattice_certificate": certificate,
                "used_equation_indices": used_equations,
                "used_colourings": [
                    [
                        int(value)
                        for value in system.colourings[equation_index]
                    ]
                    for equation_index in used_equations
                ],
                "positive_entries": sorted(positive),
                "negative_entries": sorted(negative),
            }

    nonzero_names = {names[index] for index in nonzero_flat}
    restricted: list[Polynomial] = []
    sources: list[int] = []
    for equation_index, polynomial in enumerate(equations):
        surviving = Counter(
            {
                monomial: coefficient
                for monomial, coefficient in polynomial.items()
                if all(variable in nonzero_names for variable in monomial)
            }
        )
        if surviving:
            restricted.append(surviving)
            sources.append(equation_index)
    active_names = [names[index] for index in sorted(nonzero_flat)]
    _, _, metadata = primitive_binomial_reduction(
        restricted, active_names
    )
    unit_indices = list(metadata["unit_equation_indices"])
    linear_units = list(metadata["linear_monomial_unit_relations"])
    if not unit_indices and not linear_units:
        raise RuntimeError(
            "Laurent reduction found no unit; exact fallback required"
        )
    if unit_indices:
        unit = int(unit_indices[0])
        used_restricted = [
            *metadata["unit_basis_equation_indices"][str(unit)],
            unit,
        ]
        linear_unit: dict[str, object] | None = None
    else:
        unit = -1
        linear_unit = dict(linear_units[0])
        output_sources = list(metadata["output_equation_sources"])
        used_restricted = [
            *metadata["basis_equation_indices"],
            *(
                output_sources[int(index)]
                for index in linear_unit["output_equation_indices"]
            ),
        ]
    used_equations = {sources[int(index)] for index in used_restricted}

    positive: set[int] = set()
    negative: set[int] = set()
    for equation_index in used_equations:
        for monomial, coefficient in equations[equation_index].items():
            if not coefficient:
                continue
            zero_factors = [
                name_to_flat[variable]
                for variable in monomial
                if variable not in nonzero_names
            ]
            if zero_factors:
                if not any(
                    factor in structural_zero
                    for factor in zero_factors
                ):
                    negative.add(zero_factors[0])
            else:
                positive.update(
                    name_to_flat[variable] for variable in monomial
                )
    if positive & negative:
        raise AssertionError("learned cube has contradictory entry signs")
    return positive, negative, {
        "certificate_kind": "laurent",
        "selected_entries": len(nonzero_flat),
        "restricted_equations": len(restricted),
        "binomial_equations": metadata["binomial_equations"],
        "binomial_rank": metadata["binomial_rank"],
        "unit_restricted_index": unit,
        "linear_monomial_unit_relation": linear_unit,
        "used_equation_indices": sorted(used_equations),
        "used_colourings": [
            [int(value) for value in system.colourings[index]]
            for index in sorted(used_equations)
        ],
        "positive_entries": sorted(positive),
        "negative_entries": sorted(negative),
    }


def transform_flat(
    system: EquationSystem,
    flat_index: int,
    vertex_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> int:
    edge_index, within = divmod(flat_index, 9)
    row, column = divmod(within, 3)
    first, second = system.edges[edge_index]
    mapped_first = vertex_permutation[first]
    mapped_second = vertex_permutation[second]
    mapped_row = colour_permutation[row]
    mapped_column = colour_permutation[column]
    if mapped_first < mapped_second:
        edge = (mapped_first, mapped_second)
    else:
        edge = (mapped_second, mapped_first)
        mapped_row, mapped_column = mapped_column, mapped_row
    return (
        9 * system.edge_index[edge]
        + 3 * mapped_row
        + mapped_column
    )


def stabilizer(
    center_degree: int = 4,
) -> tuple[
    tuple[tuple[int, ...], tuple[int, ...]], ...
]:
    if center_degree == 0:
        vertices = tuple(range(8))
        return tuple(
            (vertices, tuple(colours))
            for colours in itertools.permutations((0, 1, 2))
        )
    if center_degree in (1, 3):
        result = []
        for colours in itertools.permutations((0, 1, 2)):
            for tail in itertools.permutations((4, 5, 6, 7)):
                vertices = list(range(8))
                for old_colour, new_colour in enumerate(colours):
                    vertices[old_colour + 1] = new_colour + 1
                (
                    vertices[4],
                    vertices[5],
                    vertices[6],
                    vertices[7],
                ) = tail
                result.append((tuple(vertices), tuple(colours)))
        return tuple(result)
    if center_degree != 4:
        raise ValueError(
            "center_degree must be zero, one, three, or four"
        )
    result = []
    for tail in itertools.permutations((5, 6, 7)):
        for swap in (False, True):
            vertices = list(range(8))
            vertices[5], vertices[6], vertices[7] = tail
            colours = [0, 1, 2]
            if swap:
                vertices[2], vertices[3] = 3, 2
                colours[1], colours[2] = 2, 1
            result.append((tuple(vertices), tuple(colours)))
    return tuple(result)


def local_variable_map(
    system: EquationSystem,
    center_degree: int = 4,
) -> dict[int, int]:
    result: dict[int, int] = {}
    for local_edge_index, edge in enumerate(
        local_allowed_edges(center_degree)
    ):
        global_edge_index = system.edge_index[edge]
        for row in range(3):
            for column in range(3):
                flat = 9 * global_edge_index + 3 * row + column
                result[flat] = (
                    1 + 9 * local_edge_index + 3 * row + column
                )
    return result


def symmetry_clauses(
    system: EquationSystem,
    positive: set[int],
    negative: set[int],
    center_degree: int = 4,
) -> list[tuple[int, ...]]:
    flat_to_variable = local_variable_map(system, center_degree)
    clauses: set[tuple[int, ...]] = set()
    for vertices, colours in stabilizer(center_degree):
        transformed_positive = {
            transform_flat(
                system, index, vertices, colours
            )
            for index in positive
        }
        transformed_negative = {
            transform_flat(
                system, index, vertices, colours
            )
            for index in negative
        }
        if not (
            transformed_positive | transformed_negative
        ) <= flat_to_variable.keys():
            raise AssertionError(
                "canonical stabilizer left the allowed entry set"
            )
        clause = tuple(
            [
                *(
                    -flat_to_variable[index]
                    for index in sorted(transformed_positive)
                ),
                *(
                    flat_to_variable[index]
                    for index in sorted(transformed_negative)
                ),
            ]
        )
        clauses.add(clause)
    return sorted(clauses)


def read_dimacs_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError("input is not a DIMACS CNF")
    return int(variables), int(clauses)


def write_augmented_cnf(
    source: Path,
    destination: Path,
    clauses: list[tuple[int, ...]],
) -> None:
    variables, old_clause_count = read_dimacs_header(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="ascii") as reader, destination.open(
        "w", encoding="ascii"
    ) as writer:
        next(reader)
        writer.write(
            f"p cnf {variables} {old_clause_count + len(clauses)}\n"
        )
        for line in reader:
            writer.write(line)
        for clause in clauses:
            writer.write(
                " ".join(str(literal) for literal in clause) + " 0\n"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=4,
    )
    parser.add_argument(
        "--fix-skeleton",
        action="store_true",
        help="also add unit clauses for the model's 25 block indicators",
    )
    parser.add_argument(
        "--prefer-transport",
        action="store_true",
        help=(
            "prefer elementary cancellation-transport or "
            "two-monomial-rectangle cubes"
        ),
    )
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    positive_model = positive_model_literals(args.model)
    selected = set(
        selected_flat_indices(
            system,
            positive_model,
            center_degree=args.center_degree,
        )
    )
    equations, names, name_to_flat = full_equations(system)
    positive, negative, metadata = laurent_conflict(
        system,
        equations,
        names,
        name_to_flat,
        selected,
        center_degree=args.center_degree,
        prefer_transport=args.prefer_transport,
    )
    clauses = symmetry_clauses(
        system,
        positive,
        negative,
        center_degree=args.center_degree,
    )
    skeleton_units: list[tuple[int, ...]] = []
    if args.fix_skeleton:
        first_block_variable = 1 + 9 * len(
            local_allowed_edges(args.center_degree)
        )
        skeleton_units = [
            (
                variable
                if variable in positive_model
                else -variable,
            )
            for variable in range(
                first_block_variable,
                first_block_variable
                + len(local_allowed_edges(args.center_degree)),
            )
        ]
        clauses = [*clauses, *skeleton_units]
    write_augmented_cnf(args.base_cnf, args.output_cnf, clauses)
    payload = {
        "scope": "one-step n=8 degree-four Laurent CEGAR",
        "center_degree": args.center_degree,
        "model": str(args.model),
        "base_cnf": str(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        **metadata,
        "cube_size": len(positive) + len(negative),
        "stabilizer_size": len(stabilizer(args.center_degree)),
        "distinct_learned_clauses": len(clauses),
        "skeleton_fixed": args.fix_skeleton,
        "skeleton_unit_clauses": len(skeleton_units),
        "learned_clauses": [list(clause) for clause in clauses],
    }
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
