"""Generate an exact Singular Gröbner-basis job for the prism stratum."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import numpy as np

from search_prism_stratum import (
    K33_MATCHINGS,
    PRISM_MATCHINGS,
    normalized_stratum,
)
from search_witness import EquationSystem


def amplitude_polynomial(
    system: EquationSystem,
    fixed: np.ndarray,
    variable_names: dict[int, str],
    colouring: tuple[int, ...],
) -> Counter[tuple[str, ...]]:
    blocks = system.edge_array(fixed)
    polynomial: Counter[tuple[str, ...]] = Counter()
    for matching in system.matchings:
        monomial: list[str] = []
        for edge in matching:
            edge_index = system.edge_index[edge]
            flat_index = (
                edge_index * 9
                + colouring[edge[0]] * 3
                + colouring[edge[1]]
            )
            if flat_index in variable_names:
                monomial.append(variable_names[flat_index])
            elif blocks[
                edge_index, colouring[edge[0]], colouring[edge[1]]
            ] == 0:
                break
        else:
            polynomial[tuple(sorted(monomial))] += 1
    return polynomial


def polynomial_text(polynomial: Counter[tuple[str, ...]]) -> str:
    terms: list[str] = []
    for monomial, coefficient in sorted(
        polynomial.items(), key=lambda item: (len(item[0]), item[0])
    ):
        if coefficient == 0:
            continue
        body = "*".join(monomial) if monomial else "1"
        magnitude = abs(coefficient)
        term = body if magnitude == 1 else f"{magnitude}*{body}"
        if not terms:
            terms.append(term if coefficient > 0 else f"-{term}")
        else:
            terms.append(("+" if coefficient > 0 else "-") + term)
    return "".join(terms) if terms else "0"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--characteristic", type=int, default=32003)
    parser.add_argument(
        "--stratum", choices=("prism", "k33"), default="prism"
    )
    parser.add_argument(
        "--mode",
        choices=(
            "full",
            "core",
            "core-and-constant",
            "nonconstant",
            "nonconstant-plus-one",
        ),
        default="full",
    )
    parser.add_argument(
        "--constant-index",
        type=int,
        default=0,
        help="constant equation used by nonconstant-plus-one",
    )
    parser.add_argument("--algorithm", choices=("std", "slimgb"), default="slimgb")
    parser.add_argument(
        "--no-redsb",
        action="store_true",
        help="skip reduced-basis postprocessing when only unit detection matters",
    )
    parser.add_argument(
        "--no-prot",
        action="store_true",
        help="disable verbose Groebner progress output",
    )
    parser.add_argument(
        "--probe-constant-terms",
        action="store_true",
        help="reduce every nonconstant term in each constant equation modulo G",
    )
    parser.add_argument(
        "--add-rank-one-minors",
        action="store_true",
        help="add all 2x2 minors of the six unrestricted blocks",
    )
    parser.add_argument(
        "--lambda-zero",
        type=int,
        action="append",
        default=[],
        help="add one prism matrix-core lambda (index 0..5) equal to zero",
    )
    parser.add_argument(
        "--zero-entry",
        action="append",
        default=[],
        help="set an active entry to zero, formatted as uv:row:column",
    )
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    matching_options = {
        "prism": PRISM_MATCHINGS,
        "k33": K33_MATCHINGS,
    }
    fixed, active = normalized_stratum(
        system, matching_options[args.stratum]
    )
    indices = np.flatnonzero(active)
    names = [f"x{index}" for index in range(len(indices))]
    variable_names = {
        int(flat_index): name
        for flat_index, name in zip(indices, names)
    }

    all_equations: list[Counter[tuple[str, ...]]] = []
    for raw_colouring in system.colourings:
        colouring = tuple(int(value) for value in raw_colouring)
        if len(set(colouring)) == 1:
            continue
        polynomial = amplitude_polynomial(
            system, fixed, variable_names, colouring
        )
        if not polynomial:
            continue
        all_equations.append(polynomial)

    constant_equations = [
        polynomial for polynomial in all_equations if () in polynomial
    ]
    equations: list[Counter[tuple[str, ...]]] = []
    for polynomial in all_equations:
        has_linear = any(len(monomial) == 1 for monomial in polynomial)
        has_constant = () in polynomial
        if args.mode == "core" and not has_linear:
            continue
        if (
            args.mode == "core-and-constant"
            and not has_linear
            and not has_constant
        ):
            continue
        if args.mode in ("nonconstant", "nonconstant-plus-one") and has_constant:
            continue
        equations.append(polynomial)
    if args.mode == "nonconstant-plus-one":
        if not 0 <= args.constant_index < len(constant_equations):
            raise ValueError(
                f"constant index {args.constant_index} outside "
                f"0..{len(constant_equations) - 1}"
            )
        equations.append(constant_equations[args.constant_index])
    if args.add_rank_one_minors:
        for edge_index in range(len(system.edges)):
            block_indices = [
                edge_index * 9 + row * 3 + column
                for row in range(3)
                for column in range(3)
            ]
            if not all(index in variable_names for index in block_indices):
                continue
            for first_row in range(3):
                for second_row in range(first_row + 1, 3):
                    for first_column in range(3):
                        for second_column in range(first_column + 1, 3):
                            diagonal = tuple(
                                sorted(
                                    (
                                        variable_names[
                                            edge_index * 9
                                            + first_row * 3
                                            + first_column
                                        ],
                                        variable_names[
                                            edge_index * 9
                                            + second_row * 3
                                            + second_column
                                        ],
                                    )
                                )
                            )
                            off_diagonal = tuple(
                                sorted(
                                    (
                                        variable_names[
                                            edge_index * 9
                                            + first_row * 3
                                            + second_column
                                        ],
                                        variable_names[
                                            edge_index * 9
                                            + second_row * 3
                                            + first_column
                                        ],
                                    )
                                )
                            )
                            minor: Counter[tuple[str, ...]] = Counter()
                            minor[diagonal] += 1
                            minor[off_diagonal] -= 1
                            equations.append(minor)
    if args.lambda_zero:
        lambda_pairs = (
            (((1, 3), 2, 0), ((2, 5), 0, 2)),
            (((1, 2), 1, 0), ((3, 4), 0, 1)),
            (((0, 5), 2, 0), ((3, 4), 2, 0)),
            (((0, 4), 1, 0), ((2, 5), 1, 0)),
            (((0, 4), 2, 1), ((1, 3), 1, 2)),
            (((0, 5), 1, 2), ((1, 2), 2, 1)),
        )

        def variable_for(specification: tuple[tuple[int, int], int, int]) -> str:
            edge, row, column = specification
            flat_index = system.edge_index[edge] * 9 + row * 3 + column
            if flat_index not in variable_names:
                raise ValueError(
                    f"lambda entry {specification} is not an active variable"
                )
            return variable_names[flat_index]

        for lambda_index in args.lambda_zero:
            if not 0 <= lambda_index < len(lambda_pairs):
                raise ValueError("lambda index must lie in 0..5")
            first, second = lambda_pairs[lambda_index]
            equation: Counter[tuple[str, ...]] = Counter()
            equation[()] = 1
            equation[
                tuple(sorted((variable_for(first), variable_for(second))))
            ] = 1
            equations.append(equation)
    for specification in args.zero_entry:
        edge_text, row_text, column_text = specification.split(":")
        edge = tuple(sorted((int(edge_text[0]), int(edge_text[1]))))
        row = int(row_text)
        column = int(column_text)
        flat_index = system.edge_index[edge] * 9 + row * 3 + column
        if flat_index not in variable_names:
            raise ValueError(f"zero entry {specification} is not active")
        equation = Counter()
        equation[(variable_names[flat_index],)] = 1
        equations.append(equation)

    lines = [f"ring r={args.characteristic},({','.join(names)}),dp;"]
    if not args.no_redsb:
        lines.append("option(redSB);")
    if not args.no_prot:
        lines.append("option(prot);")
    lines.append("ideal I=")
    for equation_index, equation in enumerate(equations):
        suffix = "," if equation_index + 1 < len(equations) else ";"
        lines.append(f"  {polynomial_text(equation)}{suffix}")
    lines.extend(
        [
            'print("EQUATIONS");',
            "size(I);",
            "timer=1;",
            f"ideal G={args.algorithm}(I);",
            'print("SECONDS");',
            "timer;",
            'print("GB_SIZE");',
            "size(G);",
            'print("REDUCE_ONE");',
            "reduce(1,G);",
        ]
    )
    if args.probe_constant_terms:
        for equation_index, equation in enumerate(constant_equations):
            for term_index, monomial in enumerate(
                monomial for monomial in equation if monomial
            ):
                term = "*".join(monomial)
                lines.extend(
                    [
                        f'print("CONSTANT_TERM_{equation_index}_{term_index}");',
                        f"reduce({term},G);",
                    ]
                )
            lines.extend(
                [
                    f'print("CONSTANT_EQUATION_{equation_index}");',
                    f"reduce({polynomial_text(equation)},G);",
                ]
            )
    lines.append("quit;")
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"wrote {args.output}: stratum={args.stratum} "
        f"characteristic={args.characteristic} "
        f"mode={args.mode} equations={len(equations)} variables={len(names)}"
    )


if __name__ == "__main__":
    main()
