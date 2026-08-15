"""Independent no-import audit for the distinct-two-low reduction.

This audit does not import the primary verifier or SymPy.  It reconstructs
the quartics in the square-free algebra and uses separate rational and
finite-field linear algebra.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

Vector = tuple[int, ...]
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]


@dataclass(frozen=True)
class Occurrence:
    """A noncommon low-line occurrence and its actual support."""

    family: int
    line: str
    missing: int
    support: frozenset[int]
    vector: Vector


def add_polynomials(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add square-free polynomials."""
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply_polynomials(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the square-free quotient."""
    result: Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        set_left = set(monomial_left)
        for monomial_right, coefficient_right in right.items():
            if set_left & set(monomial_right):
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            result[monomial] = (
                result.get(monomial, Fraction(0))
                + coefficient_left * coefficient_right
            )
    return {monomial: value for monomial, value in result.items() if value}


def scale_polynomial(value: int, polynomial: Polynomial) -> Polynomial:
    """Scale a polynomial."""
    return {monomial: value * coefficient for monomial, coefficient in polynomial.items()}


def linear_form(terms: dict[int, int]) -> Polynomial:
    """Build a linear form from coordinate coefficients."""
    return {(coordinate,): Fraction(value) for coordinate, value in terms.items() if value}


def product_of_factors(*factors: Polynomial) -> Polynomial:
    """Multiply a list of factors in the square-free algebra."""
    result: Polynomial = {(): Fraction(1)}
    for factor in factors:
        result = multiply_polynomials(result, factor)
    return result


def fixed_quartics() -> dict[str, Polynomial]:
    """Reconstruct the five complementary quartics independently."""
    x = tuple(linear_form({coordinate: 1}) for coordinate in range(6))
    ell_1 = linear_form({3: 1, 2: -1, 0: -1})
    ell_2 = linear_form({3: 1, 2: -1, 1: -1})
    return {
        "m1": product_of_factors(x[4], x[5], x[1], ell_1),
        "m2": product_of_factors(x[4], x[5], x[0], ell_2),
        "d0": product_of_factors(
            x[4], x[5], linear_form({1: 1, 2: 1}), linear_form({3: 1, 0: -1})
        ),
        "d1": product_of_factors(
            x[4], x[5], linear_form({0: 1, 2: 1}), linear_form({3: 1, 1: -1})
        ),
        "d2": scale_polynomial(-2, product_of_factors(x[4], x[5], x[0], x[1])),
    }


def polar_evaluate(polynomial: Polynomial, vectors: tuple[Vector, ...]) -> Fraction:
    """Evaluate complete polarization from square-free monomial coefficients."""
    assert len(vectors) == 4
    total = Fraction(0)
    for monomial, coefficient in polynomial.items():
        assert len(monomial) == 4
        total += coefficient * sum(
            multiply_values(vectors[slot][coordinate] for slot, coordinate in enumerate(order))
            for order in permutations(monomial)
        )
    return total


def multiply_values(values: object) -> int:
    """Multiply an iterable of integers without importing math.prod."""
    result = 1
    for value in values:
        result *= int(value)
    return result


def double_contractions(left: Vector, right: Vector) -> dict[str, Fraction]:
    """Independently double-contract every quartic."""
    e4 = (0, 0, 0, 0, 1, 0)
    e5 = (0, 0, 0, 0, 0, 1)
    return {
        name: polar_evaluate(polynomial, (left, right, e4, e5))
        for name, polynomial in fixed_quartics().items()
    }


def nonempty_subsets(values: frozenset[int]) -> tuple[frozenset[int], ...]:
    """Return nonempty subsets of a two-element colour set."""
    first, second = sorted(values)
    return (frozenset({first}), frozenset({second}), values)


def occurrences(family: int) -> tuple[Occurrence, ...]:
    """Build all noncommon line/support occurrences."""
    raw = (
        (("A0", 0, frozenset({1, 2}), (1, 0, 0, 1, 0, 0)),
         ("C0", 1, frozenset({0, 2}), (1, 0, -1, 0, 0, 0)))
        if family == 1
        else (("A1", 1, frozenset({0, 2}), (0, 1, 0, 1, 0, 0)),
              ("C1", 0, frozenset({1, 2}), (0, 1, -1, 0, 0, 0)))
    )
    return tuple(
        Occurrence(family, line, missing, support, vector)
        for line, missing, maximal, vector in raw
        for support in nonempty_subsets(maximal)
    )


def classify_pair(left: Occurrence, right: Occurrence) -> str | None:
    """Classify a pair directly from the audited contraction scalars."""
    row = double_contractions(left.vector, right.vector)
    overlap = left.support & right.support
    if row["m1"] or row["m2"]:
        return "Z" if not overlap else None
    nonzero_diagonals = {colour for colour in range(3) if row[f"d{colour}"]}
    if not overlap:
        return "Z"
    if len(overlap) == 1 and nonzero_diagonals == set(overlap):
        return f"E{next(iter(overlap))}"
    return None


def audit_pair_rules() -> dict[str, int]:
    """Independently exhaust the pair rules and three-low pigeonhole."""
    first, second = occurrences(1), occurrences(2)
    same_compatible = 0
    for family_occurrences in (first, second):
        for left in family_occurrences:
            for right in family_occurrences:
                outcome = classify_pair(left, right)
                assert outcome == ("Z" if not (left.support & right.support) else None)
                same_compatible += outcome is not None

    cross_compatible = 0
    cross_e22 = 0
    for left in first:
        for right in second:
            outcome = classify_pair(left, right)
            overlap = left.support & right.support
            if left.missing == right.missing:
                expected = (
                    "Z"
                    if not overlap and len(left.support) == len(right.support) == 1
                    else None
                )
            elif 2 in overlap:
                expected = "E2"
            else:
                expected = "Z"
                assert not overlap
            assert outcome == expected
            cross_compatible += outcome is not None
            cross_e22 += outcome == "E2"

    compatible_triples = 0
    for majority_family in (1, 2):
        majority = occurrences(majority_family)
        minority = occurrences(3 - majority_family)
        local_count = 0
        for index, left in enumerate(majority):
            for right in majority[index:]:
                if classify_pair(left, right) != "Z":
                    continue
                for third in minority:
                    outcomes = (
                        classify_pair(left, third),
                        classify_pair(right, third),
                    )
                    if None in outcomes:
                        continue
                    assert sum(outcome == "E2" for outcome in outcomes) <= 1
                    local_count += 1
        assert local_count == 14
        compatible_triples += local_count

    exception_choices = (frozenset(), frozenset({0}), frozenset({1}), frozenset({2}))
    assert all(
        first_choice | second_choice != {0, 1, 2}
        for first_choice in exception_choices
        for second_choice in exception_choices
    )
    assert (same_compatible, cross_compatible, cross_e22) == (28, 22, 8)
    return {
        "same_family_compatible": same_compatible,
        "cross_family_compatible": cross_compatible,
        "cross_family_E22": cross_e22,
        "compatible_2_plus_1_triples": compatible_triples,
    }


def rational_rank(matrix: list[list[int | Fraction]]) -> int:
    """Compute rank by independent exact rational row reduction."""
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def multiply_matrices(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    """Multiply small integer matrices."""
    return [
        [sum(left_row[k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for left_row in left
    ]


def rows_from_columns(columns: tuple[Vector, ...]) -> list[list[int]]:
    """Transpose a tuple of columns to row-major form."""
    return [[column[row] for column in columns] for row in range(6)]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Transpose a nonempty matrix."""
    return [list(column) for column in zip(*matrix, strict=True)]


def pairing_matrix(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    """Compute left^T J right for two-row A maps."""
    j_right = [right[1], right[0]]
    return multiply_matrices(transpose(left), j_right)


ZERO_FIXTURE = (
    ((0, 1, 0, 0, 0, 1), (1, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 1)),
    ((0, 1, 0, 1, 0, 0), (1, 0, 0, 0, 0, 1), (0, 0, 0, 1, 0, 1)),
    ((1, 0, 0, -1, 0, 0), (0, 1, 0, 0, 1, 0), (0, 0, 0, 1, 1, 0)),
    ((1, 0, 0, 0, 1, 0), (0, 1, 0, -1, 0, 0), (0, 0, 0, 1, 1, 0)),
)

E22_FIXTURE = (
    ((2, 1, 0, 2, 1, 0), (2, 1, 1, -2, 0, 1), (1, 0, 0, 1, 0, 0)),
    ((-2, 0, 0, 0, 0, 1), (-1, 0, -1, 2, 1, 0), (0, 1, 0, 1, 0, 0)),
    ((1, 0, 0, -1, 0, 0), (0, 1, 0, -1, 0, 0), (-1, 1, -2, 2, 1, 0)),
    ((1, 0, 0, 0, 1, 0), (0, 2, 0, -2, 1, 0), (-1, -2, 1, 0, 0, 1)),
)


def audit_fixture(
    fixture: tuple[tuple[Vector, ...], ...],
    expected_a_ranks: tuple[int, ...],
    expected_c01_ranks: tuple[int, ...],
    expected_pairing: list[list[int]],
    combined_companions: bool,
) -> dict[str, object]:
    """Check a rational incidence fixture without symbolic libraries."""
    modes = tuple(rows_from_columns(columns) for columns in fixture)
    phi_1 = [
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [-1, 0, -1, 1, 0, 0],
    ]
    phi_2 = [
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, -1, -1, 1, 0, 0],
    ]
    projection_ranks = tuple(
        (rational_rank(multiply_matrices(phi_1, mode)), rational_rank(multiply_matrices(phi_2, mode)))
        for mode in modes
    )
    assert projection_ranks == ((2, 3), (3, 2), (3, 3), (3, 3))
    assert all(rational_rank(mode) == 3 for mode in modes)

    low_column = 2 if combined_companions else 1
    assert all(value == 0 for value in [row[low_column] for row in multiply_matrices(phi_1, modes[0])])
    low_column = 2 if combined_companions else 0
    assert all(value == 0 for value in [row[low_column] for row in multiply_matrices(phi_2, modes[1])])

    if combined_companions:
        assert fixture[2][0] == (1, 0, 0, -1, 0, 0)
        assert fixture[2][1] == (0, 1, 0, -1, 0, 0)
    else:
        assert fixture[2][0] == (1, 0, 0, -1, 0, 0)
        assert fixture[3][1] == (0, 1, 0, -1, 0, 0)

    a_maps = tuple([row[:] for row in mode[4:6]] for mode in modes)
    assert tuple(rational_rank(a_map) for a_map in a_maps) == expected_a_ranks
    assert tuple(rational_rank([row[:2] for row in a_map]) for a_map in a_maps) == expected_c01_ranks
    assert pairing_matrix(a_maps[2], a_maps[3]) == expected_pairing

    for colour in range(3):
        assert any(
            a_maps[left][0][colour] * a_maps[right][1][colour]
            + a_maps[left][1][colour] * a_maps[right][0][colour]
            != 0
            for left in range(4)
            for right in range(left + 1, 4)
        )

    mixed_0000 = polar_evaluate(
        fixed_quartics()["m1"], tuple(fixture[mode][0] for mode in range(4))
    )
    assert mixed_0000 == -2
    return {
        "projection_ranks": projection_ranks,
        "A_ranks": expected_a_ranks,
        "colour_01_A_ranks": expected_c01_ranks,
        "mixed_m1_0000": int(mixed_0000),
    }


def rank_mod(matrix: tuple[tuple[int, ...], tuple[int, ...]], prime: int) -> int:
    """Compute rank of a two-row matrix modulo a prime."""
    work = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(3):
        pivot = next((row for row in range(pivot_row, 2) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [(inverse * entry) % prime for entry in work[pivot_row]]
        for row in range(2):
            if row == pivot_row:
                continue
            factor = work[row][column]
            work[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == 2:
            break
    return pivot_row


def pairing_mod(
    left: tuple[tuple[int, ...], tuple[int, ...]],
    right: tuple[tuple[int, ...], tuple[int, ...]],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    """Compute left^T J right modulo a prime."""
    return tuple(
        tuple(
            (left[0][i] * right[1][j] + left[1][i] * right[0][j]) % prime
            for j in range(3)
        )
        for i in range(3)
    )


def audit_rank_boundaries_over_f3() -> dict[str, int]:
    """Stress the two high-shore rank boundaries over F3."""
    prime = 3
    maps = tuple((entries[:3], entries[3:]) for entries in product(range(prime), repeat=6))
    ranks = {matrix: rank_mod(matrix, prime) for matrix in maps}
    zero_pairs = 0
    e22_pairs = 0
    for left in maps:
        if ranks[left] == 0:
            continue
        for right in maps:
            if ranks[right] == 0:
                continue
            matrix = pairing_mod(left, right, prime)
            if not any(value for row in matrix for value in row):
                assert (ranks[left], ranks[right]) == (1, 1)
                zero_pairs += 1
            elif all(
                matrix[i][j] == 0
                for i in range(3)
                for j in range(3)
                if (i, j) != (2, 2)
            ):
                assert (ranks[left], ranks[right]) in {(1, 1), (1, 2), (2, 1)}
                if ranks[left] == 1:
                    assert left[0][:2] == left[1][:2] == (0, 0)
                if ranks[right] == 1:
                    assert right[0][:2] == right[1][:2] == (0, 0)
                e22_pairs += 1
    assert zero_pairs and e22_pairs
    return {"zero_pairs": zero_pairs, "E22_pairs": e22_pairs}


def main() -> None:
    """Run the independent audit."""
    report = {
        "pair_rules": audit_pair_rules(),
        "finite_field_rank_boundaries": audit_rank_boundaries_over_f3(),
        "zero_fixture": audit_fixture(
            ZERO_FIXTURE,
            (1, 1, 1, 1),
            (1, 1, 1, 1),
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            combined_companions=False,
        ),
        "E22_fixture": audit_fixture(
            E22_FIXTURE,
            (2, 2, 1, 2),
            (2, 2, 0, 1),
            [[0, 0, 0], [0, 0, 0], [0, 0, 1]],
            combined_companions=True,
        ),
        "primary_imported": False,
        "symbolic_library_used": False,
        "status": "UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
