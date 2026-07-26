"""Generate exact polynomial jobs for all cubic prism killer labelings.

Every mutual killer edge has a single nonzero matrix entry.  Independent
half-edge scalings normalize the nine such entries to one.  The six
complement edges remain unrestricted 3 by 3 matrices.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter
from pathlib import Path

import numpy as np

from enumerate_cubic_rankone import (
    canonical_pattern,
    graph_automorphisms,
    graph_edges,
)
from generate_prism_singular import amplitude_polynomial, polynomial_text
from search_prism_stratum import PRISM_MATCHINGS
from search_witness import EquationSystem

Pattern = tuple[int, ...]
Polynomial = Counter[tuple[str, ...]]


def clean_polynomial(polynomial: Polynomial) -> Polynomial:
    """Remove zero coefficients without discarding negative coefficients."""
    return Counter(
        {
            monomial: coefficient
            for monomial, coefficient in polynomial.items()
            if coefficient
        }
    )


def prism_orbit_representatives() -> list[Pattern]:
    """Return the 718 half-edge labelings up to graph and colour symmetry."""
    edges = graph_edges(PRISM_MATCHINGS)
    automorphisms = graph_automorphisms(edges)
    neighbours = [
        tuple(
            sorted(
                other
                for edge in edges
                if vertex in edge
                for other in edge
                if other != vertex
            )
        )
        for vertex in range(6)
    ]
    representatives = {
        canonical_pattern(
            tuple(value for row in rows for value in row),
            automorphisms,
        )
        for rows in itertools.product(
            *(tuple(itertools.permutations(row)) for row in neighbours)
        )
    }
    return sorted(representatives)


def canonical_matching_pattern() -> Pattern:
    pattern = [-1] * 18
    for colour, matching in enumerate(PRISM_MATCHINGS):
        for first, second in matching:
            pattern[3 * first + colour] = second
            pattern[3 * second + colour] = first
    automorphisms = graph_automorphisms(graph_edges(PRISM_MATCHINGS))
    return canonical_pattern(tuple(pattern), automorphisms)


def normalized_pattern_stratum(
    system: EquationSystem, pattern: Pattern
) -> tuple[np.ndarray, np.ndarray]:
    """Normalize the nine mutual singleton blocks specified by ``pattern``."""
    if len(pattern) != 18:
        raise ValueError("a prism pattern must contain 18 neighbour choices")
    edges = graph_edges(PRISM_MATCHINGS)
    fixed = np.zeros(system.variable_count, dtype=np.complex128)
    blocks = system.edge_array(fixed)
    active = np.zeros(system.variable_count, dtype=bool)
    active_blocks = system.edge_array(active)

    for edge in system.edges:
        edge_index = system.edge_index[edge]
        if edge not in edges:
            active_blocks[edge_index, :, :] = True
            continue
        first, second = edge
        first_colours = [
            colour
            for colour in range(3)
            if pattern[3 * first + colour] == second
        ]
        second_colours = [
            colour
            for colour in range(3)
            if pattern[3 * second + colour] == first
        ]
        if len(first_colours) != 1 or len(second_colours) != 1:
            raise ValueError(f"pattern does not label prism edge {edge}")
        # The arc from ``first`` forces the colour at ``second`` and hence
        # selects a column; the reverse arc selects a row.  The singleton is
        # therefore (reverse-arc colour, forward-arc colour).
        blocks[
            edge_index,
            second_colours[0],
            first_colours[0],
        ] = 1
    return fixed, active


def orbit_equations(
    system: EquationSystem, pattern: Pattern
) -> tuple[list[str], list[Polynomial]]:
    fixed, active = normalized_pattern_stratum(system, pattern)
    indices = np.flatnonzero(active)
    names = [f"x{index}" for index in range(len(indices))]
    variable_names = {
        int(flat_index): name
        for flat_index, name in zip(indices, names)
    }
    equations: list[Polynomial] = []
    for raw_colouring in system.colourings:
        colouring = tuple(int(value) for value in raw_colouring)
        if len(set(colouring)) == 1:
            continue
        polynomial = amplitude_polynomial(
            system, fixed, variable_names, colouring
        )
        if polynomial:
            equations.append(polynomial)
    return names, equations


def multiply_polynomials(
    first: Polynomial, second: Polynomial
) -> Polynomial:
    product: Polynomial = Counter()
    for first_monomial, first_coefficient in first.items():
        for second_monomial, second_coefficient in second.items():
            product[tuple(sorted(first_monomial + second_monomial))] += (
                first_coefficient * second_coefficient
            )
    return clean_polynomial(product)


def core_rank_one_audit(
    system: EquationSystem, pattern: Pattern
) -> dict[str, object]:
    """Check whether the linear core forces every free block to rank at most 1.

    For every free block ``X``, this looks for nine identities

        lambda * X[row,column] + Y[row,column] = 0

    with the same polynomial ``lambda`` in all entries and with all formal
    2 by 2 minors of the polynomial matrix ``Y`` equal to zero.
    """
    names, equations = orbit_equations(system, pattern)
    return core_rank_one_audit_from_equations(names, equations)


def core_rank_one_audit_from_equations(
    names: list[str], equations: list[Polynomial]
) -> dict[str, object]:
    """Audit a precomputed normalized prism equation system."""
    equations_by_linear_variable: dict[str, Polynomial] = {}
    for equation in equations:
        linear_terms = [
            monomial
            for monomial, coefficient in equation.items()
            if len(monomial) == 1 and coefficient
        ]
        if len(linear_terms) != 1:
            continue
        variable = linear_terms[0][0]
        if variable in equations_by_linear_variable:
            return {"passes": False, "reason": "repeated linear variable"}
        equations_by_linear_variable[variable] = equation
    if set(equations_by_linear_variable) != set(names):
        return {
            "passes": False,
            "reason": "not every variable has one linear equation",
            "linear_variables": len(equations_by_linear_variable),
        }

    lambdas: list[Polynomial] = []
    remainder_matrices: list[list[list[Polynomial]]] = []
    for block_index in range(6):
        block_lambda: Polynomial | None = None
        remainder_matrix: list[list[Polynomial]] = [
            [Counter() for _ in range(3)] for _ in range(3)
        ]
        for row in range(3):
            for column in range(3):
                variable = f"x{9 * block_index + 3 * row + column}"
                equation = equations_by_linear_variable[variable]
                coefficient: Polynomial = Counter()
                remainder: Polynomial = Counter()
                for monomial, value in equation.items():
                    if variable in monomial:
                        reduced = list(monomial)
                        reduced.remove(variable)
                        coefficient[tuple(reduced)] += value
                    else:
                        remainder[monomial] += value
                coefficient = clean_polynomial(coefficient)
                remainder_matrix[row][column] = clean_polynomial(remainder)
                if block_lambda is None:
                    block_lambda = coefficient
                elif coefficient != block_lambda:
                    return {
                        "passes": False,
                        "reason": "entry-dependent lambda",
                        "block": block_index,
                    }
        assert block_lambda is not None
        lambdas.append(block_lambda)
        remainder_matrices.append(remainder_matrix)
        for first_row in range(3):
            for second_row in range(first_row + 1, 3):
                for first_column in range(3):
                    for second_column in range(first_column + 1, 3):
                        minor = multiply_polynomials(
                            remainder_matrix[first_row][first_column],
                            remainder_matrix[second_row][second_column],
                        )
                        minor.subtract(
                            multiply_polynomials(
                                remainder_matrix[first_row][second_column],
                                remainder_matrix[second_row][first_column],
                            )
                        )
                        if clean_polynomial(minor):
                            return {
                                "passes": False,
                                "reason": "remainder is not formally rank one",
                                "block": block_index,
                            }
    return {
        "passes": True,
        "linear_variables": len(equations_by_linear_variable),
        "lambdas": lambdas,
        "remainder_matrices": remainder_matrices,
    }


def minimal_monomial_zero_covers(
    matrix: list[list[Polynomial]],
) -> list[tuple[str, ...]]:
    """Return the minimal variable sets whose vanishing makes ``matrix`` zero."""
    monomials: list[tuple[str, ...]] = []
    for row in matrix:
        for polynomial in row:
            terms = [
                monomial
                for monomial, coefficient in polynomial.items()
                if coefficient
            ]
            if len(terms) != 1:
                raise ValueError(
                    "zero-cover extraction requires one monomial per entry"
                )
            monomials.append(terms[0])
    variables = sorted({variable for term in monomials for variable in term})
    covers: list[tuple[str, ...]] = []
    for size in range(1, len(variables) + 1):
        for candidate in itertools.combinations(variables, size):
            candidate_set = set(candidate)
            if not all(candidate_set.intersection(term) for term in monomials):
                continue
            if any(set(cover).issubset(candidate_set) for cover in covers):
                continue
            covers.append(candidate)
    return covers


def singular_program(
    orbit_index: int,
    names: list[str],
    equations: list[Polynomial],
    characteristic: int,
    mode: str,
    algorithm: str,
    add_rank_one_minors: bool = False,
    extra_equations: list[Polynomial] | None = None,
    certificate_support: bool = False,
) -> str:
    selected = list(equations)
    if mode == "nonconstant":
        selected = [
            polynomial for polynomial in equations if () not in polynomial
        ]
    if add_rank_one_minors:
        for block_index in range(6):
            for first_row in range(3):
                for second_row in range(first_row + 1, 3):
                    for first_column in range(3):
                        for second_column in range(first_column + 1, 3):
                            minor: Polynomial = Counter()
                            minor[
                                tuple(
                                    sorted(
                                        (
                                            f"x{9 * block_index + 3 * first_row + first_column}",
                                            f"x{9 * block_index + 3 * second_row + second_column}",
                                        )
                                    )
                                )
                            ] += 1
                            minor[
                                tuple(
                                    sorted(
                                        (
                                            f"x{9 * block_index + 3 * first_row + second_column}",
                                            f"x{9 * block_index + 3 * second_row + first_column}",
                                        )
                                    )
                                )
                            ] -= 1
                            selected.append(minor)
    if extra_equations:
        selected.extend(extra_equations)
    lines = [
        f"ring r={characteristic},({','.join(names)}),dp;",
        "option(redSB);",
        "option(prot);",
        "ideal I=",
    ]
    for equation_index, equation in enumerate(selected):
        suffix = "," if equation_index + 1 < len(selected) else ";"
        lines.append(f"  {polynomial_text(equation)}{suffix}")
    lines.extend(
        [
            f'print("ORBIT {orbit_index}");',
            'print("EQUATIONS");',
            "size(I);",
            "timer=1;",
            f"ideal G={algorithm}(I);",
            'print("SECONDS");',
            "timer;",
            'print("GB_SIZE");',
            "size(G);",
            'print("REDUCE_ONE");',
            "reduce(1,G);",
        ]
    )
    if certificate_support:
        lines.extend(
            [
                'print("LIFT_SECONDS");',
                "timer=1;",
                "matrix T=lift(I,G);",
                "timer;",
                'print("CERTIFICATE_SHAPE");',
                "nrows(T);",
                "ncols(T);",
                "int certificate_support=0;",
                'print("CERTIFICATE_INDICES");',
                "for (int certificate_row=1; certificate_row<=nrows(T); certificate_row++)",
                "{",
                "  if (T[certificate_row,1] != 0)",
                "  {",
                "    certificate_support=certificate_support+1;",
                "    print(certificate_row);",
                "  }",
                "}",
                'print("CERTIFICATE_SUPPORT");',
                "certificate_support;",
                'print("CERTIFICATE_CHECK");',
                "print(matrix(I)*T-matrix(G));",
            ]
        )
    lines.append("quit;")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--characteristic", type=int, default=32003)
    parser.add_argument("--mode", choices=("full", "nonconstant"), default="full")
    parser.add_argument("--algorithm", choices=("std", "slimgb"), default="slimgb")
    parser.add_argument("--add-rank-one-minors", action="store_true")
    parser.add_argument(
        "--certificate-support",
        action="store_true",
        help="lift the Gröbner basis back to the input generators",
    )
    parser.add_argument(
        "--lambda-zero",
        type=int,
        action="append",
        default=[],
        help="add a core lambda (block index 0..5) equal to zero",
    )
    parser.add_argument(
        "--zero-variable",
        action="append",
        default=[],
        help="set a free variable x0..x53 equal to zero",
    )
    args = parser.parse_args()

    representatives = prism_orbit_representatives()
    canonical_index = representatives.index(canonical_matching_pattern())
    if args.summary:
        print(f"orbits={len(representatives)} canonical_index={canonical_index}")
    if args.index is None:
        if not args.summary:
            parser.error("--index is required unless --summary is used")
        return
    if args.output is None:
        parser.error("--output is required with --index")
    if not 0 <= args.index < len(representatives):
        raise ValueError(f"index must lie in 0..{len(representatives) - 1}")

    system = EquationSystem(6, 3)
    names, equations = orbit_equations(system, representatives[args.index])
    audit = core_rank_one_audit(system, representatives[args.index])
    extra_equations: list[Polynomial] = []
    if args.lambda_zero:
        if not audit["passes"]:
            raise ValueError("lambda branches require a passing core audit")
        lambdas = audit["lambdas"]
        assert isinstance(lambdas, list)
        for block_index in args.lambda_zero:
            if not 0 <= block_index < 6:
                raise ValueError("lambda index must lie in 0..5")
            extra_equations.append(lambdas[block_index])
    for variable in args.zero_variable:
        if variable not in names:
            raise ValueError(f"unknown free variable {variable}")
        equation: Polynomial = Counter()
        equation[(variable,)] = 1
        extra_equations.append(equation)
    args.output.write_text(
        singular_program(
            args.index,
            names,
            equations,
            args.characteristic,
            args.mode,
            args.algorithm,
            args.add_rank_one_minors,
            extra_equations,
            args.certificate_support,
        ),
        encoding="utf-8",
    )
    constant_count = sum(() in polynomial for polynomial in equations)
    print(
        f"wrote {args.output}: orbit={args.index} equations={len(equations)} "
        f"constant_equations={constant_count} variables={len(names)}"
    )


if __name__ == "__main__":
    main()
