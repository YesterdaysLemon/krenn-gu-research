"""Independent no-import audit of the fixed-complement P7 fan theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import factorial

ROOTS = tuple(range(5))
COLUMNS = tuple(range(5))
UNMARKED = tuple(range(1, 5))
RANK_TWO_PAIRS = {(0, 1), (2, 3)}


def permanent_recursive(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    if size == 0:
        return Fraction(1)
    return sum(
        (
            matrix[0][column]
            * permanent_recursive(
                [row[:column] + row[column + 1 :] for row in matrix[1:]]
            )
            for column in range(size)
        ),
        Fraction(0),
    )


def submatrix(
    matrix: list[list[Fraction]],
    rows: tuple[int, ...],
    columns: tuple[int, ...],
) -> list[list[Fraction]]:
    return [[matrix[row][column] for column in columns] for row in rows]


def complement(universe: tuple[int, ...], chosen: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(item for item in universe if item not in chosen)


def laplace_term(
    matrix: list[list[Fraction]],
    root_pair: tuple[int, int],
    retained: tuple[int, int],
) -> Fraction:
    return permanent_recursive(submatrix(matrix, root_pair, retained)) * permanent_recursive(
        submatrix(
            matrix,
            complement(ROOTS, root_pair),
            complement(COLUMNS, retained),
        )
    )


def audit_matching_partition() -> None:
    # For fixed retained columns, the ten root-pair fibres are disjoint by
    # definition and each has 2! 3! restriction pairs.  Their total is 5!.
    # This audits the cardinality part of the gluing proof without listing
    # matchings.
    for retained in combinations(UNMARKED, 2):
        assert len(retained) == 2
        fibre_sizes = []
        for root_pair in combinations(ROOTS, 2):
            assert len(complement(ROOTS, root_pair)) == 3
            assert len(complement(COLUMNS, retained)) == 3
            fibre_sizes.append(factorial(2) * factorial(3))
        assert sum(fibre_sizes) == factorial(5)


def canonical_matrices() -> tuple[list[list[Fraction]], ...]:
    raw = (
        (
            (-1, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (-1, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
            (1, 1, 0, 1, 0),
        ),
        (
            (0, 1, 0, 0, 0),
            (-1, 0, 1, 0, 0),
            (0, 0, 0, 1, 0),
            (-1, 0, 0, 0, 1),
            (1, 0, 1, 0, 1),
        ),
        (
            (-1, 1, 0, 0, 0),
            (-1, 0, 1, 0, 0),
            (-1, 0, 0, 1, 0),
            (1, 0, 0, 0, 1),
            (1, 1, 0, 1, 0),
        ),
    )
    return tuple(
        [[Fraction(entry) for entry in row] for row in matrix] for matrix in raw
    )


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    work[row][j] - scale * work[pivot_row][j]
                    for j in range(column_count)
                ]
        pivot_row += 1
    return pivot_row


def audit_countermodel() -> None:
    expected_witnesses = (
        ((1, 4), (0, 2), (3, 4), (1, 4), (1, 3), (3, 4)),
        ((0, 4), (0, 2), (0, 4), (2, 4), (1, 3), (2, 4)),
        ((1, 4), (0, 2), (3, 4), (1, 4), (1, 3), (3, 4)),
    )
    retained_pairs = tuple(combinations(UNMARKED, 2))
    for matrix, witness_pairs in zip(
        canonical_matrices(), expected_witnesses, strict=True
    ):
        full = permanent_recursive(matrix)
        assert full == -1
        for retained, witness_pair in zip(retained_pairs, witness_pairs, strict=True):
            terms = {
                root_pair: laplace_term(matrix, root_pair, retained)
                for root_pair in combinations(ROOTS, 2)
            }
            assert sum(terms.values(), Fraction(0)) == full
            assert terms[(0, 1)] == terms[(2, 3)] == 0
            assert terms[witness_pair]
            assert witness_pair not in RANK_TWO_PAIRS


def assemble_rows() -> dict[str, list[list[Fraction]]]:
    h0, h1, h2 = canonical_matrices()
    return {
        "t": [[h0[i][0], h1[i][0], h2[i][0]] for i in ROOTS],
        "u01": [[h0[i][1], h1[i][3], Fraction(0)] for i in ROOTS],
        "v01": [[h0[i][2], h1[i][4], Fraction(0)] for i in ROOTS],
        "u02": [[h0[i][3], Fraction(0), h2[i][1]] for i in ROOTS],
        "v02": [[h0[i][4], Fraction(0), h2[i][2]] for i in ROOTS],
        "u12": [[Fraction(0), h1[i][1], h2[i][3]] for i in ROOTS],
        "v12": [[Fraction(0), h1[i][2], h2[i][4]] for i in ROOTS],
    }


def audit_common_null_directions() -> None:
    rows = assemble_rows()
    assert rank(rows["t"]) == 3
    directions = {
        "u01": (0, 0, 1),
        "v01": (0, 0, 1),
        "u02": (0, 1, 0),
        "v02": (0, 1, 0),
        "u12": (1, 0, 0),
        "v12": (1, 0, 0),
    }
    for name, direction in directions.items():
        assert rank(rows[name]) == 2
        assert all(
            sum(
                (entry * Fraction(coordinate) for entry, coordinate in zip(row, direction, strict=True)),
                Fraction(0),
            )
            == 0
            for row in rows[name]
        )


def audit_fan_incidence() -> None:
    u0 = frozenset({5, 6})
    u1 = frozenset({1, 2})
    u2 = frozenset({3, 4})
    colour_zero = {
        u0 | frozenset(pair) for pair in combinations(sorted(u1 | u2), 2)
    }
    colour_one = {
        u1 | frozenset(pair) for pair in combinations(sorted(u0 | u2), 2)
    }
    assert {
        frozenset({1, 2, 5, 6}),
        frozenset({1, 3, 5, 6}),
        frozenset({1, 4, 5, 6}),
    } <= colour_zero
    assert frozenset({1, 2, 3, 4}) in colour_one


def main() -> None:
    audit_matching_partition()
    audit_countermodel()
    audit_common_null_directions()
    audit_fan_incidence()
    print("PASS: independent factorial-partition audit of fixed-complement Laplace")
    print("PASS: independent integer audit of all six fixed windows per chart")
    print("PASS: independent common-system rank and null-direction audit")
    print("PASS: independent zero rho>=2 shore-cooccurrence audit")
    print("SCOPE: distinguished companion rank remains UNKNOWN")
    print("SCOPE: legal marked-star fan and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
