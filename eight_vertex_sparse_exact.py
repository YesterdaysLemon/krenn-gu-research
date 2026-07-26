"""Exact torus ideal for the sparse n=8 degree-four support survivor.

The input is a CaDiCaL witness for the support CNF.  Only the first 225
variables encode matrix-entry support; the remaining variables are auxiliary
SAT indicators.  This script translates the selected 34-entry stratum into
the complete characteristic-zero perfect-matching equations, adds the exact
degree-four proportionality minors, and saturates by every selected entry.

SAT at the support level is only a relaxation.  A Singular result
``reduce(1,G) = 0`` for the generated program proves that the entire selected
nonzero stratum is empty over the complex numbers.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

from generate_prism_singular import (
    amplitude_polynomial,
    polynomial_text,
)
from search_witness import EquationSystem

Polynomial = Counter[tuple[str, ...]]
Edge = tuple[int, int]


def positive_model_literals(path: Path) -> set[int]:
    values: set[int] = set()
    for raw_line in path.read_text(encoding="ascii").splitlines():
        line = raw_line.strip()
        if not line or line == "SAT" or line == "SATISFIABLE":
            continue
        if line.startswith("c"):
            continue
        tokens = line.split()
        if tokens and tokens[0] in {"s", "v"}:
            tokens = tokens[1:]
        for token in tokens:
            if token in {
                "SAT",
                "SATISFIABLE",
                "UNSAT",
                "UNSATISFIABLE",
            }:
                continue
            literal = int(token)
            if literal > 0:
                values.add(literal)
            if literal == 0:
                continue
    return values


def local_allowed_edges(center_degree: int = 4) -> tuple[Edge, ...]:
    if center_degree not in (0, 1, 3, 4):
        raise ValueError(
            "center_degree must be zero, one, three, or four"
        )
    return tuple(
        edge
        for edge in itertools.combinations(range(8), 2)
        if center_degree in (0, 1)
        or edge[0] != 0
        or 1 <= edge[1] <= center_degree
    )


def selected_flat_indices(
    system: EquationSystem,
    positive: set[int],
    center_degree: int = 4,
) -> tuple[int, ...]:
    selected: list[int] = []
    for local_edge_index, edge in enumerate(
        local_allowed_edges(center_degree)
    ):
        global_edge_index = system.edge_index[edge]
        for row in range(3):
            for column in range(3):
                local_variable = (
                    1 + 9 * local_edge_index + 3 * row + column
                )
                if local_variable in positive:
                    selected.append(
                        9 * global_edge_index + 3 * row + column
                    )
    return tuple(sorted(selected))


def proportionality_minors(
    variable_names: dict[int, str],
    system: EquationSystem,
) -> list[Polynomial]:
    """Return the twelve 2x2 minors forced at the two degree-four stars."""

    def flat(
        first: int, second: int, first_colour: int, second_colour: int
    ) -> int:
        if first < second:
            edge = (first, second)
            row, column = first_colour, second_colour
        else:
            edge = (second, first)
            row, column = second_colour, first_colour
        return 9 * system.edge_index[edge] + 3 * row + column

    vector_pairs = [
        # At vertex 0: W02[:,1] || W04[:,2] and
        #              W03[:,2] || W04[:,1].
        (
            [flat(0, 2, row, 1) for row in range(3)],
            [flat(0, 4, row, 2) for row in range(3)],
        ),
        (
            [flat(0, 3, row, 2) for row in range(3)],
            [flat(0, 4, row, 1) for row in range(3)],
        ),
        # The same forced structure at vertex 1.
        (
            [flat(1, 2, row, 1) for row in range(3)],
            [flat(1, 4, row, 2) for row in range(3)],
        ),
        (
            [flat(1, 3, row, 2) for row in range(3)],
            [flat(1, 4, row, 1) for row in range(3)],
        ),
    ]
    result: list[Polynomial] = []
    for first_vector, second_vector in vector_pairs:
        if any(
            index not in variable_names
            for index in (*first_vector, *second_vector)
        ):
            raise AssertionError("model does not have the expected star support")
        for first_row, second_row in itertools.combinations(range(3), 2):
            polynomial: Polynomial = Counter()
            polynomial[
                tuple(
                    sorted(
                        (
                            variable_names[first_vector[first_row]],
                            variable_names[second_vector[second_row]],
                        )
                    )
                )
            ] += 1
            polynomial[
                tuple(
                    sorted(
                        (
                            variable_names[first_vector[second_row]],
                            variable_names[second_vector[first_row]],
                        )
                    )
                )
            ] -= 1
            result.append(polynomial)
    return result


def exact_equations(
    system: EquationSystem,
    variable_names: dict[int, str],
) -> list[Polynomial]:
    fixed = np.zeros(system.variable_count, dtype=np.complex128)
    equations: list[Polynomial] = []
    seen: set[tuple[tuple[tuple[str, ...], int], ...]] = set()
    for raw_colouring, required in zip(
        system.colourings, system.target, strict=True
    ):
        colouring = tuple(int(value) for value in raw_colouring)
        polynomial = amplitude_polynomial(
            system, fixed, variable_names, colouring
        )
        if required:
            polynomial[()] -= 1
        # Do not use unary ``+Counter`` or ``Counter +=`` here: both discard
        # negative coefficients, including the required-amplitude constant
        # ``-1``.
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
        if signature in seen:
            continue
        seen.add(signature)
        equations.append(polynomial)
    return equations


def singular_program(
    names: list[str],
    equations: list[Polynomial],
    characteristic: int,
    saturation_names: list[str] | None = None,
) -> str:
    saturation = "sat"
    all_names = [*names, saturation]
    saturated = names if saturation_names is None else saturation_names
    if not set(saturated) <= set(names):
        raise ValueError("saturation variables are not ring variables")
    saturation_equation: Polynomial = Counter(
        {
            tuple(sorted([*saturated, saturation])): 1,
            (): -1,
        }
    )
    generators = [*equations, saturation_equation]
    lines = [
        f"ring r={characteristic},({','.join(all_names)}),dp;",
        "option(redSB);",
        "ideal I=",
    ]
    for index, polynomial in enumerate(generators):
        suffix = "," if index + 1 < len(generators) else ";"
        lines.append(f"  {polynomial_text(polynomial)}{suffix}")
    lines.extend(
        [
            'print("EQUATIONS");',
            "size(I);",
            "timer=1;",
            "ideal G=slimgb(I);",
            'print("SECONDS");',
            "timer;",
            'print("GB_SIZE");',
            "size(G);",
            'print("REDUCE_ONE");',
            "reduce(1,G);",
            "quit;",
        ]
    )
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=Path,
        default=Path("tmp/eight_vertex_local_degree4_max16.model"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/eight_vertex_sparse_exact_Q.sing"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("tmp/eight_vertex_sparse_exact.json"),
    )
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument(
        "--no-minors",
        action="store_true",
        help="omit the derived degree-four proportionality minors",
    )
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    positive = positive_model_literals(args.model)
    selected = selected_flat_indices(system, positive)
    names = [f"x{index}" for index in range(len(selected))]
    variable_names = {
        flat_index: name
        for flat_index, name in zip(selected, names, strict=True)
    }
    equations = exact_equations(system, variable_names)
    minors = (
        []
        if args.no_minors
        else proportionality_minors(variable_names, system)
    )
    program = singular_program(
        names,
        [*equations, *minors],
        args.characteristic,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(program, encoding="utf-8")
    payload = {
        "scope": "exact torus ideal for sparse n=8 support survivor",
        "model": str(args.model),
        "model_sha256": sha256(args.model),
        "characteristic": args.characteristic,
        "selected_entries": len(selected),
        "selected_flat_indices": list(selected),
        "distinct_amplitude_equations": len(equations),
        "proportionality_minors": len(minors),
        "program": str(args.output),
        "program_sha256": sha256(args.output),
    }
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
