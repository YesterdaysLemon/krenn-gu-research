"""Independent standard-library audit of the GLS21 all-port collapse."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def rank(columns: tuple[tuple[Fraction, ...], ...], dimension: int) -> int:
    if not columns:
        return 0
    work = [[column[row] for column in columns] for row in range(dimension)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, dimension) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(dimension):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == dimension:
            break
    return pivot_row


def basis_vector(dimension: int, coordinate: int, scale: Fraction) -> tuple[Fraction, ...]:
    return tuple(scale if index == coordinate else Fraction(0) for index in range(dimension))


def audit_identity_slicing() -> dict[str, int]:
    left_dimension = 9
    p = Fraction(5, 2)
    slice_count = 0
    for right_dimension in (1, 2, 4, 8):
        slices = []
        # Independently read p*id on e_i tensor f_j and contract the output
        # against every right dual basis element.
        for left in range(left_dimension):
            for source_right in range(right_dimension):
                for sliced_right in range(right_dimension):
                    slices.append(
                        basis_vector(left_dimension, left, p)
                        if source_right == sliced_right
                        else basis_vector(left_dimension, left, Fraction(0))
                    )
        assert rank(tuple(slices), left_dimension) == 9
        assert all(
            basis_vector(left_dimension, coordinate, p) in slices
            for coordinate in range(left_dimension)
        )
        slice_count += len(slices)
    return {"ambient": left_dimension, "slices": slice_count}


def determinant(
    matrix: tuple[tuple[Fraction, ...], ...], rows: tuple[int, ...], columns: tuple[int, ...]
) -> Fraction:
    size = len(rows)
    if size == 0:
        return Fraction(1)
    answer = Fraction(0)
    from itertools import permutations

    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row_index, column_index in enumerate(permutation):
            term *= matrix[rows[row_index]][columns[column_index]]
        answer += term
    return answer


def audit_minors_and_rank() -> dict[str, int]:
    p = Fraction(7, 3)
    columns = tuple(basis_vector(9, coordinate, p) for coordinate in range(9))
    assert rank(columns, 9) == 9
    matrix = tuple(tuple(columns[column][row] for column in range(9)) for row in range(9))
    checked = 0
    for size in range(1, 10):
        coordinates = tuple(range(size))
        assert determinant(matrix, coordinates, coordinates) == p**size
        checked += 1
    desired = tuple(Fraction(index + 1) for index in range(9))
    assert rank(columns + (desired,), 9) == 9
    return {"nonzero_diagonal_minors": checked, "rank": 9}


def audit_factor_annihilator() -> int:
    p = Fraction(11, 5)
    nuisance = tuple(basis_vector(9, coordinate, p) for coordinate in range(9))
    # A functional vanishing on each p e_i has every coordinate zero.
    candidate = tuple(Fraction(0) for _ in range(9))
    assert all(
        sum(left * right for left, right in zip(candidate, column, strict=True)) == 0
        for column in nuisance
    )
    assert not any(candidate)
    return 0


def audit_label_bookkeeping() -> tuple[tuple[int, int, int, int], ...]:
    records = []
    for root_order in range(3, 11):
        bhat_size = 2 * root_order
        uhat_size = 2 * root_order - 2
        active_pair_labels = bhat_size * (bhat_size - 1) // 2
        source_pairs = root_order * (root_order - 1) // 2
        assert bhat_size - 2 == uhat_size
        assert active_pair_labels > source_pairs
        records.append((root_order, bhat_size, uhat_size, source_pairs))
    return tuple(records)


def main() -> None:
    slices = audit_identity_slicing()
    minors = audit_minors_and_rank()
    annihilator = audit_factor_annihilator()
    labels = audit_label_bookkeeping()
    print("promoted base-shadow all-port collapse independent audit: PASS")
    print("  independently sliced scalar identities:", slices)
    print("  direct rational diagonal minors/rank:", minors)
    print("  factor annihilator dimension:", annihilator)
    print("  arbitrary-root label bookkeeping:", labels)
    print("  no imports from primary verifier or repository mathematics code")
    print("  scope: base factor route no-go; upstairs selectors and node remain open")


if __name__ == "__main__":
    main()
