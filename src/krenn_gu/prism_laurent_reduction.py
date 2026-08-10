"""Eliminate the generic prism binomial torus before Gröbner computation.

Support SAT forces every entry of every free rank-one block to be nonzero.
After outer-product parameterization, each two-term forbidden amplitude is
therefore a Laurent-binomial relation.  Their exponent lattice has rank 13.
This module selects a unimodular basis, solves 13 factor variables as signed
Laurent monomials in the other 23, substitutes into all remaining amplitudes,
and removes invertible common monomial factors.  The six outer-product gauge
coordinates then disappear, leaving a substantially smaller polynomial
system.
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
import math
from collections import Counter
from fractions import Fraction
from functools import reduce
from pathlib import Path

from krenn_gu.prism_orbit_screen import (
    Polynomial,
    clean_polynomial,
    prism_orbit_representatives,
    singular_program,
)
from krenn_gu.prism_rankone_parameterization import (
    parameter_names,
    parameterized_orbit_equations,
)
from krenn_gu.search_witness import EquationSystem


def modular_independent_indices(
    vectors: list[list[int]], prime: int = 1_000_003
) -> list[int]:
    """Select independent vectors quickly over a large prime field."""
    basis: dict[int, list[int]] = {}
    selected: list[int] = []
    for vector_index, raw_vector in enumerate(vectors):
        vector = [value % prime for value in raw_vector]
        for pivot in sorted(basis):
            factor = vector[pivot]
            if not factor:
                continue
            pivot_vector = basis[pivot]
            vector = [
                (value - factor * pivot_value) % prime
                for value, pivot_value in zip(vector, pivot_vector)
            ]
        nonzero = next(
            (index for index, value in enumerate(vector) if value),
            None,
        )
        if nonzero is None:
            continue
        inverse = pow(vector[nonzero], -1, prime)
        vector = [(value * inverse) % prime for value in vector]
        basis[nonzero] = vector
        selected.append(vector_index)
    return selected


def exponent_vector(
    monomial: tuple[str, ...],
    variable_index: dict[str, int],
    size: int,
) -> list[int]:
    result = [0] * size
    for variable in monomial:
        result[variable_index[variable]] += 1
    return result


def linear_monomial_unit_relations(
    equations: list[Polynomial],
) -> list[dict[str, object]]:
    """Find monomials in the constant-coefficient row span of equations.

    On a Laurent torus every monomial is invertible.  Thus a rational linear
    combination of reduced equations equal to one monomial is already a unit
    contradiction, even when no individual reduced equation is a monomial.
    The returned coefficients give an exact replay witness.
    """

    monomials = sorted(
        {
            monomial
            for equation in equations
            for monomial, coefficient in equation.items()
            if coefficient
        }
    )
    monomial_index = {
        monomial: index for index, monomial in enumerate(monomials)
    }
    rows: list[list[Fraction]] = []
    combinations: list[list[Fraction]] = []
    for equation_index, equation in enumerate(equations):
        row = [Fraction(0)] * len(monomials)
        for monomial, coefficient in equation.items():
            if coefficient:
                row[monomial_index[monomial]] = Fraction(coefficient)
        combination = [Fraction(0)] * len(equations)
        combination[equation_index] = Fraction(1)
        rows.append(row)
        combinations.append(combination)

    pivot_row = 0
    for column in range(len(monomials)):
        pivot = next(
            (
                index
                for index in range(pivot_row, len(rows))
                if rows[index][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        combinations[pivot_row], combinations[pivot] = (
            combinations[pivot],
            combinations[pivot_row],
        )
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        combinations[pivot_row] = [
            value / scale for value in combinations[pivot_row]
        ]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    rows[index], rows[pivot_row], strict=True
                )
            ]
            combinations[index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    combinations[index],
                    combinations[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break

    relations: list[dict[str, object]] = []
    seen: set[tuple[str, ...]] = set()
    for row, combination in zip(rows, combinations, strict=True):
        support = [index for index, value in enumerate(row) if value]
        if len(support) != 1:
            continue
        monomial = monomials[support[0]]
        if monomial in seen:
            continue
        seen.add(monomial)
        used = [
            index for index, coefficient in enumerate(combination) if coefficient
        ]
        relations.append(
            {
                "monomial": list(monomial),
                "output_equation_indices": used,
                "coefficients": [
                    str(combination[index]) for index in used
                ],
                "result_coefficient": str(row[support[0]]),
            }
        )
    return relations


def primitive_binomial_reduction(
    equations: list[Polynomial],
    original_names: list[str] | None = None,
) -> tuple[list[str], list[Polynomial], dict[str, object]]:
    from sympy import Matrix

    if original_names is None:
        original_names = parameter_names()
    original_index = {
        variable: index for index, variable in enumerate(original_names)
    }
    binomials: list[
        tuple[list[int], Fraction, int]
    ] = []
    for equation_index, equation in enumerate(equations):
        terms = [(monomial, coefficient) for monomial, coefficient in equation.items() if coefficient]
        if len(terms) != 2:
            continue
        (first_monomial, first_coefficient), (
            second_monomial,
            second_coefficient,
        ) = terms
        first_exponents = exponent_vector(
            first_monomial, original_index, len(original_names)
        )
        second_exponents = exponent_vector(
            second_monomial, original_index, len(original_names)
        )
        difference = [
            first - second
            for first, second in zip(first_exponents, second_exponents)
        ]
        binomials.append(
            (
                difference,
                Fraction(-second_coefficient, first_coefficient),
                equation_index,
            )
        )
    exponent_rows = [row for row, _, _ in binomials]
    if exponent_rows:
        independent_rows = modular_independent_indices(exponent_rows)
        basis_rows = [
            exponent_rows[index] for index in independent_rows
        ]
        pivot_columns = modular_independent_indices(
            [list(column) for column in zip(*basis_rows)]
        )
        basis_matrix = Matrix(basis_rows)
        binomial_rank = len(independent_rows)
        pivot_matrix = basis_matrix[:, pivot_columns]
        determinant = int(pivot_matrix.det())
        if abs(determinant) != 1:
            # A modular echelon choice need not expose the unimodular minor
            # even when one exists.  Fall back to exact RREF before
            # rejecting it.
            exponent_matrix = Matrix(exponent_rows)
            independent_rows = list(exponent_matrix.T.rref()[1])
            basis_matrix = exponent_matrix[independent_rows, :]
            pivot_columns = list(basis_matrix.rref()[1])
            binomial_rank = len(independent_rows)
            pivot_matrix = basis_matrix[:, pivot_columns]
            determinant = int(pivot_matrix.det())
            if abs(determinant) != 1:
                raise ValueError(
                    "selected binomial basis is not unimodular: "
                    f"det={determinant}"
                )
        inverse = pivot_matrix.inv()
        if any(value.q != 1 for value in inverse):
            raise ValueError(
                "unimodular inverse unexpectedly has denominators"
            )
    else:
        independent_rows = []
        pivot_columns = []
        basis_matrix = Matrix.zeros(0, len(original_names))
        binomial_rank = 0
        determinant = 1
        inverse = Matrix.zeros(0, 0)
    free_columns = [
        index
        for index in range(len(original_names))
        if index not in pivot_columns
    ]
    free_position = {
        original_column: position
        for position, original_column in enumerate(free_columns)
    }
    if binomial_rank:
        free_matrix = basis_matrix[:, free_columns]
        exponent_substitution = -(inverse * free_matrix)
    else:
        exponent_substitution = Matrix.zeros(
            0, len(free_columns)
        )
    basis_rhs = [binomials[index][1] for index in independent_rows]

    substitutions: list[tuple[Fraction, tuple[int, ...]]] = []
    pivot_position = {
        original_column: position
        for position, original_column in enumerate(pivot_columns)
    }
    for original_column in range(len(original_names)):
        if original_column in free_position:
            exponents = [0] * len(free_columns)
            exponents[free_position[original_column]] = 1
            substitutions.append((Fraction(1), tuple(exponents)))
            continue
        row = pivot_position[original_column]
        constant = Fraction(1)
        for rhs, power in zip(basis_rhs, inverse.row(row)):
            constant *= rhs ** int(power)
        exponents = tuple(
            int(value) for value in exponent_substitution.row(row)
        )
        substitutions.append((constant, exponents))

    reduced_laurent: list[Counter[tuple[int, ...]]] = []
    reduced_sources: list[int] = []
    zero_equations = 0
    for equation_index, equation in enumerate(equations):
        result: Counter[tuple[int, ...]] = Counter()
        for monomial, coefficient in equation.items():
            scalar = Fraction(coefficient)
            exponents = [0] * len(free_columns)
            for variable in monomial:
                substitution_scalar, substitution_exponents = substitutions[
                    original_index[variable]
                ]
                scalar *= substitution_scalar
                exponents = [
                    first + second
                    for first, second in zip(
                        exponents, substitution_exponents
                    )
                ]
            result[tuple(exponents)] += scalar
        result = Counter(
            {
                monomial: coefficient
                for monomial, coefficient in result.items()
                if coefficient
            }
        )
        if not result:
            zero_equations += 1
            continue
        minimum_exponents = [
            min(monomial[index] for monomial in result)
            for index in range(len(free_columns))
        ]
        shifted = Counter(
            {
                tuple(
                    exponent - minimum
                    for exponent, minimum in zip(
                        monomial, minimum_exponents
                    )
                ): coefficient
                for monomial, coefficient in result.items()
            }
        )
        reduced_laurent.append(shifted)
        reduced_sources.append(equation_index)

    active_positions = sorted(
        {
            position
            for equation in reduced_laurent
            for monomial in equation
            for position, exponent in enumerate(monomial)
            if exponent
        }
    )
    output_names = [f"z{index}" for index in range(len(active_positions))]
    output_position = {
        free_position: output_index
        for output_index, free_position in enumerate(active_positions)
    }
    output_equations: list[Polynomial] = []
    unit_equation_indices: list[int] = []
    for equation, source_index in zip(
        reduced_laurent, reduced_sources
    ):
        denominators = [
            coefficient.denominator for coefficient in equation.values()
        ]
        common_denominator = math.lcm(*denominators)
        integer_coefficients = [
            int(coefficient * common_denominator)
            for coefficient in equation.values()
        ]
        common_factor = reduce(math.gcd, map(abs, integer_coefficients))
        output: Polynomial = Counter()
        for (exponents, _), integer_coefficient in zip(
            equation.items(), integer_coefficients
        ):
            monomial: list[str] = []
            for free_index, exponent in enumerate(exponents):
                if not exponent:
                    continue
                variable = output_names[output_position[free_index]]
                monomial.extend([variable] * exponent)
            output[tuple(sorted(monomial))] += (
                integer_coefficient // common_factor
            )
        normalized_output = clean_polynomial(output)
        output_equations.append(normalized_output)
        if len(normalized_output) == 1 and () in normalized_output:
            unit_equation_indices.append(source_index)

    unit_basis_equation_indices: dict[str, list[int]] = {}
    basis_equation_indices = [
        binomials[index][2] for index in independent_rows
    ]
    for unit_index in unit_equation_indices:
        terms = [
            monomial
            for monomial, coefficient in equations[unit_index].items()
            if coefficient
        ]
        if not terms:
            continue
        reference = exponent_vector(
            terms[0], original_index, len(original_names)
        )
        required_basis_positions: set[int] = set()
        for monomial in terms[1:]:
            exponents = exponent_vector(
                monomial, original_index, len(original_names)
            )
            difference = [
                exponent - reference_exponent
                for exponent, reference_exponent in zip(
                    exponents, reference
                )
            ]
            pivot_difference = Matrix(
                [[difference[index] for index in pivot_columns]]
            )
            coordinates = pivot_difference * inverse
            if any(value.q != 1 for value in coordinates):
                raise ValueError(
                    "unit relation has nonintegral lattice coordinates"
                )
            required_basis_positions.update(
                index
                for index, value in enumerate(coordinates.row(0))
                if value
            )
        unit_basis_equation_indices[str(unit_index)] = sorted(
            basis_equation_indices[index]
            for index in required_basis_positions
        )

    linear_unit_relations = linear_monomial_unit_relations(output_equations)

    # A sign-incompatible binomial becomes a unit after substitution and is
    # itself an immediate torus contradiction.
    inconsistent_binomial_indices: list[int] = []
    for row, rhs, equation_index in binomials:
        equation = equations[equation_index]
        # It was substituted above; locate it by repeating the cheap check.
        result: Counter[tuple[int, ...]] = Counter()
        for monomial, coefficient in equation.items():
            scalar = Fraction(coefficient)
            exponents = [0] * len(free_columns)
            for variable in monomial:
                substitution_scalar, substitution_exponents = substitutions[
                    original_index[variable]
                ]
                scalar *= substitution_scalar
                exponents = [
                    first + second
                    for first, second in zip(
                        exponents, substitution_exponents
                    )
                ]
            result[tuple(exponents)] += scalar
        if any(result.values()):
            inconsistent_binomial_indices.append(equation_index)

    metadata: dict[str, object] = {
        "input_variables": len(original_names),
        "binomial_equations": len(binomials),
        "binomial_rank": binomial_rank,
        "basis_equation_indices": basis_equation_indices,
        "pivot_variables": [
            original_names[index] for index in pivot_columns
        ],
        "unimodular_determinant": determinant,
        "free_laurent_variables": len(free_columns),
        "active_polynomial_variables": len(output_names),
        "active_free_variables": [
            original_names[free_columns[position]]
            for position in active_positions
        ],
        "identically_eliminated_equations": zero_equations,
        "output_equations": len(output_equations),
        "output_equation_sources": reduced_sources,
        "unit_equation_indices": unit_equation_indices,
        "unit_basis_equation_indices": unit_basis_equation_indices,
        "linear_monomial_unit_relations": linear_unit_relations,
        "inconsistent_binomial_indices": inconsistent_binomial_indices,
    }
    return output_names, output_equations, metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--algorithm", choices=("std", "slimgb"), default="slimgb")
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    pattern = prism_orbit_representatives()[args.index]
    _, equations = parameterized_orbit_equations(system, pattern)
    names, reduced, metadata = primitive_binomial_reduction(equations)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        singular_program(
            args.index,
            names,
            reduced,
            args.characteristic,
            "full",
            args.algorithm,
        ),
        encoding="utf-8",
    )
    print(metadata)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
