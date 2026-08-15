"""Independent no-import audit of the support-two low incidence theorem."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations_with_replacement, product

Monomial = frozenset[int]
Polynomial = dict[Monomial, Fraction]
Vector = tuple[Fraction, ...]


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the square-free quotient, discarding repeated variables."""
    answer: Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            if monomial_left & monomial_right:
                continue
            monomial = monomial_left | monomial_right
            answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient_left * coefficient_right
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def linear_form(entries: dict[int, int]) -> Polynomial:
    """Create a linear form as a square-free polynomial dictionary."""
    return {frozenset((index,)): Fraction(value) for index, value in entries.items() if value}


def factored_polynomial(coefficient: int, factors: tuple[Polynomial, ...]) -> Polynomial:
    """Multiply factors and apply an overall coefficient."""
    result: Polynomial = {frozenset(): Fraction(coefficient)}
    for factor in factors:
        result = multiply(result, factor)
    return result


def fixed_quartics() -> dict[str, Polynomial]:
    """Reconstruct the five quartics as monomial dictionaries."""
    x = tuple(linear_form({i: 1}) for i in range(6))
    x0, x1, x2, x3, x4, x5 = x
    return {
        "m1": factored_polynomial(1, (x4, x5, x1, linear_form({3: 1, 2: -1, 0: -1}))),
        "m2": factored_polynomial(1, (x4, x5, x0, linear_form({3: 1, 2: -1, 1: -1}))),
        "d0": factored_polynomial(1, (x4, x5, linear_form({1: 1, 2: 1}), linear_form({3: 1, 0: -1}))),
        "d1": factored_polynomial(1, (x4, x5, linear_form({0: 1, 2: 1}), linear_form({3: 1, 1: -1}))),
        "d2": factored_polynomial(-2, (x4, x5, x0, x1)),
    }


def contract(polynomial: Polynomial, vector: Vector) -> Polynomial:
    """Contract a square-free polynomial once by a vector."""
    answer: Polynomial = {}
    for monomial, coefficient in polynomial.items():
        for index in monomial:
            residual = monomial - {index}
            answer[residual] = answer.get(residual, Fraction(0)) + coefficient * vector[index]
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def double_contractions(left: Vector, right: Vector) -> dict[str, Fraction]:
    """Extract the x4*x5 coefficient after two independent contractions."""
    target = frozenset((4, 5))
    return {
        name: contract(contract(polynomial, left), right).get(target, Fraction(0))
        for name, polynomial in fixed_quartics().items()
    }


def exceptional_lines(family: int) -> dict[str, tuple[Vector, int, frozenset[int]]]:
    """Return rational line representatives and support metadata."""
    if family == 1:
        return {
            "N": ((0, 0, 1, 1, 0, 0), 2, frozenset((0, 1))),
            "A0": ((1, 0, 0, 1, 0, 0), 0, frozenset((1, 2))),
            "C0": ((1, 0, -1, 0, 0, 0), 1, frozenset((0, 2))),
        }
    return {
        "N": ((0, 0, 1, 1, 0, 0), 2, frozenset((0, 1))),
        "A1": ((0, 1, 0, 1, 0, 0), 1, frozenset((0, 2))),
        "C1": ((0, 1, -1, 0, 0, 0), 0, frozenset((1, 2))),
    }


def diagonal_support(row: dict[str, Fraction]) -> frozenset[int]:
    """Return the nonzero diagonal scalar positions."""
    return frozenset(colour for colour in range(3) if row[f"d{colour}"])


def audit_line_pairs() -> dict[str, object]:
    """Independently classify all cross- and same-family line pairs."""
    first, second = exceptional_lines(1), exceptional_lines(2)
    cross_excluded: list[str] = []
    cross_allowed: list[tuple[str, int]] = []
    for name1, (vector1, missing1, support1) in first.items():
        for name2, (vector2, missing2, support2) in second.items():
            row = double_contractions(vector1, vector2)
            assert not row["m1"] and not row["m2"]
            overlap = support1 & support2
            assert diagonal_support(row) == overlap
            if missing1 == missing2:
                assert len(overlap) == 2
                cross_excluded.append(f"{name1}/{name2}")
            else:
                assert len(overlap) == 1
                cross_allowed.append((f"{name1}/{name2}", next(iter(overlap))))
    assert cross_excluded == ["N/N", "A0/C1", "C0/A1"]
    assert len(cross_allowed) == 6

    same: dict[str, object] = {}
    for family in (1, 2):
        lines = exceptional_lines(family)
        allowed: list[tuple[str, int]] = []
        impossible_two_non_n = 0
        impossible_two_n = 0
        for name1, name2 in combinations_with_replacement(lines, 2):
            vector1, _missing1, support1 = lines[name1]
            vector2, _missing2, support2 = lines[name2]
            row = double_contractions(vector1, vector2)
            if name1 != "N" and name2 != "N":
                assert 2 in support1 & support2
                assert not row["d2"]
                impossible_two_non_n += 1
            elif name1 == name2 == "N":
                assert diagonal_support(row) == frozenset((0, 1))
                impossible_two_n += 1
            else:
                overlap = support1 & support2
                assert len(overlap) == 1
                assert diagonal_support(row) == overlap
                allowed.append((f"{name1}/{name2}", next(iter(overlap))))
        assert len(allowed) == 2
        assert impossible_two_non_n == 3
        assert impossible_two_n == 1
        same[f"Phi_{family}"] = {
            "allowed": allowed,
            "two_non_N_pairs": impossible_two_non_n,
            "N_N_pairs": impossible_two_n,
        }
    return {
        "cross_excluded": cross_excluded,
        "cross_allowed": cross_allowed,
        "same_family": same,
    }


def rank_mod_rows(matrix: list[list[int]], prime: int) -> int:
    """Compute exact row rank over a prime field."""
    if not matrix or not matrix[0]:
        return 0
    work = [[entry % prime for entry in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], prime - 2, prime)
        work[row] = [(inverse * entry) % prime for entry in work[row]]
        for i in range(len(work)):
            if i == row:
                continue
            factor = work[i][column]
            work[i] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(work[i], work[row], strict=True)
            ]
        row += 1
        if row == len(work):
            break
    return row


def column_rank(columns: tuple[tuple[int, int], ...], prime: int) -> int:
    """Return the rank of a two-row matrix given by its columns."""
    return rank_mod_rows(
        [[column[row] for column in columns] for row in range(2)],
        prime,
    )


def j_form(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the hyperbolic form modulo an odd prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def audit_rank_one_shore(prime: int) -> dict[str, int]:
    """Exhaust all maps satisfying a one-diagonal-cell pairing equation."""
    vectors = tuple(product(range(prime), repeat=2))
    maps = tuple(product(vectors, repeat=3))
    configurations = 0
    rank_patterns: set[tuple[int, int]] = set()
    for left in maps:
        rank_left = column_rank(left, prime)
        if not rank_left:
            continue
        common_orthogonal = tuple(
            vector
            for vector in vectors
            if all(not j_form(column, vector, prime) for column in left)
        )
        for colour in range(3):
            eligible_centre = tuple(
                vector
                for vector in vectors
                if j_form(left[colour], vector, prime)
                and all(
                    not j_form(left[index], vector, prime)
                    for index in range(3)
                    if index != colour
                )
            )
            for centre in eligible_centre:
                off_colours = tuple(index for index in range(3) if index != colour)
                for first_off in common_orthogonal:
                    for second_off in common_orthogonal:
                        right_list = [(0, 0), (0, 0), (0, 0)]
                        right_list[colour] = centre
                        right_list[off_colours[0]] = first_off
                        right_list[off_colours[1]] = second_off
                        right = tuple(right_list)
                        rank_right = column_rank(right, prime)
                        assert rank_right
                        pattern = (rank_left, rank_right)
                        assert pattern in {(1, 1), (1, 2), (2, 1)}
                        if rank_left == 1:
                            assert all(left[index] == (0, 0) for index in off_colours)
                        if rank_right == 1:
                            assert all(right[index] == (0, 0) for index in off_colours)
                        if rank_left == 2:
                            assert rank_right == 1
                            assert all(
                                not j_form(left[index], centre, prime)
                                for index in off_colours
                            )
                        configurations += 1
                        rank_patterns.add(pattern)
    assert rank_patterns == {(1, 1), (1, 2), (2, 1)}
    return {
        "linear_maps_checked": len(maps),
        "one_cell_configurations": configurations,
        "rank_patterns": len(rank_patterns),
    }


def rational_rank(columns: tuple[Vector, ...]) -> int:
    """Compute rational column rank through exact elimination."""
    matrix = [[column[row] for column in columns] for row in range(6)]
    work = [row[:] for row in matrix]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, 6) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(6):
            if row == pivot_row:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def audit_same_mode_boundary() -> dict[str, int]:
    """Check that the two ambient kernels intersect only in the N line."""
    kernel1 = (
        (1, 0, 0, 1, 0, 0),
        (0, 0, 1, 1, 0, 0),
    )
    kernel2 = (
        (0, 1, 0, 1, 0, 0),
        (0, 0, 1, 1, 0, 0),
    )
    union_rank = rational_rank(kernel1 + kernel2)
    intersection_dimension = 2 + 2 - union_rank
    assert union_rank == 3
    assert intersection_dimension == 1
    assert kernel1[1] == kernel2[1]
    return {
        "kernel_union_rank": union_rank,
        "kernel_intersection_dimension": intersection_dimension,
    }


def main() -> None:
    """Run the independent exact audit."""
    report = {
        "line_pair_audit": audit_line_pairs(),
        "rank_one_shore_F3": audit_rank_one_shore(3),
        "rank_one_shore_F5": audit_rank_one_shore(5),
        "same_mode_boundary": audit_same_mode_boundary(),
        "implementation": "stdlib-only; no repository imports",
        "scope": "exact rational identities and finite-field case audits",
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
