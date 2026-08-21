"""Focused exact checks for the GLS18 leading-shadow target theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


def rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def columns_to_rows(columns: list[tuple[Fraction, ...]], dimension: int):
    return [[column[row] for column in columns] for row in range(dimension)]


def quotient_reduce(
    nuisance: list[tuple[Fraction, ...]], vector: tuple[Fraction, ...]
) -> bool:
    """Return whether vector has nonzero quotient class."""

    dimension = len(vector)
    before = rank(columns_to_rows(nuisance, dimension))
    after = rank(columns_to_rows(nuisance + [vector], dimension))
    return after > before


def check_target_coupling() -> tuple[int, int]:
    cases = 0
    rank_one_cases = 0
    for b_nonzero, response_nonzero in product((False, True), repeat=2):
        b = (Fraction(1), Fraction(2)) if b_nonzero else (Fraction(0),) * 2
        response = (
            (Fraction(2), Fraction(-1), Fraction(3), Fraction(0), Fraction(0))
            if response_nonzero
            else (Fraction(0),) * 5
        )
        rhs = [[left * right for right in response] for left in b]
        pure_columns = [tuple(row[index] for row in rhs) for index in range(3)]
        mixed_columns = [tuple(row[index] for row in rhs) for index in range(3, 5)]
        assert all(not any(column) for column in mixed_columns)
        pure_rank = rank(columns_to_rows(pure_columns, len(b)))
        assert pure_rank == int(b_nonzero and response_nonzero)
        assert (any(any(row) for row in rhs)) == (b_nonzero and response_nonzero)
        rank_one_cases += pure_rank
        cases += 1
    return cases, rank_one_cases


def check_quotient_branches() -> tuple[int, int]:
    cases = 0
    useful = 0
    dimension = 3
    pure = [
        tuple(Fraction(row == column) for row in range(dimension))
        for column in range(dimension)
    ]
    nuisance_families = (
        [],
        [pure[0]],
        [pure[0], pure[1]],
        pure,
    )
    for nuisance in nuisance_families:
        pure_survival = [quotient_reduce(nuisance, vector) for vector in pure]
        rank_rise = any(pure_survival)
        nuisance_rank = rank(columns_to_rows(nuisance, dimension))
        augmented_rank = rank(columns_to_rows(nuisance + pure, dimension))
        assert rank_rise == (augmented_rank > nuisance_rank)
        if not rank_rise:
            assert nuisance_rank == dimension
        useful += int(rank_rise)
        cases += 1
    return cases, useful


def minors(matrix: list[list[Fraction]], size: int) -> list[Fraction]:
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    if size == 0:
        return [Fraction(1)]
    answer = []
    for row_set in combinations(range(rows), size):
        for column_set in combinations(range(columns), size):
            if size == 1:
                answer.append(matrix[row_set[0]][column_set[0]])
            elif size == 2:
                a, b = row_set
                c, d = column_set
                answer.append(matrix[a][c] * matrix[b][d] - matrix[a][d] * matrix[b][c])
            else:
                raise ValueError("bounded verifier only needs minors through size two")
    return answer


def check_rank_minor_tables() -> int:
    checks = 0
    values = tuple(Fraction(value) for value in (-2, -1, 0, 1, 2))
    for entries in product(values, repeat=4):
        nuisance = [[entries[0]], [entries[1]]]
        pure_columns = [[entries[2], 1], [entries[3], 0]]
        augmented = [nuisance[row] + pure_columns[row] for row in range(2)]
        rank_rise = rank(augmented) > rank(nuisance)
        detected = False
        for size in (1, 2):
            nuisance_minors = minors(nuisance, size)
            augmented_minors = minors(augmented, size)
            if not any(nuisance_minors) and any(augmented_minors):
                detected = True
        assert rank_rise == detected
        checks += 1
    return checks


def check_four_root_fullness() -> tuple[int, int]:
    basis = [tuple(Fraction(row == column) for row in range(3)) for column in range(3)]
    full_cases = 0
    proper_cases = 0
    for mask in range(1 << 3):
        nuisance = [basis[index] for index in range(3) if mask & (1 << index)]
        nuisance_rank = rank(columns_to_rows(nuisance, 3))
        all_pure_absorbed = all(
            not quotient_reduce(nuisance, vector) for vector in basis
        )
        assert all_pure_absorbed == (nuisance_rank == 3)
        full_cases += int(all_pure_absorbed)
        proper_cases += int(nuisance_rank < 3)
    return full_cases, proper_cases


def check_pair_diagonal_absorption() -> tuple[int, int]:
    dimension = 9
    diagonal = []
    for colour in range(3):
        vector = [Fraction(0)] * dimension
        vector[3 * colour + colour] = Fraction(1)
        diagonal.append(tuple(vector))
    assert rank(columns_to_rows(diagonal, dimension)) == 3
    nuisance = diagonal[:]
    assert all(not quotient_reduce(nuisance, vector) for vector in diagonal)
    assert rank(columns_to_rows(nuisance, dimension)) == 3 < dimension
    return len(diagonal), dimension


def main() -> None:
    coupling_cases = check_target_coupling()
    quotient_cases = check_quotient_branches()
    minor_checks = check_rank_minor_tables()
    four_root = check_four_root_fullness()
    pair_space = check_pair_diagonal_absorption()
    print("leading-shadow target coupling and Fitting checks: PASS")
    print("  response/leading cases and rank-one cases:", coupling_cases)
    print("  quotient nuisance cases and useful cases:", quotient_cases)
    print("  exact rank/minor tables:", minor_checks)
    print("  four-port full/proper shadow masks:", four_root)
    print("  pair diagonal span / ambient dimension:", pair_space)
    print("  scope: failure criterion only; no survival or node closure claim")


if __name__ == "__main__":
    main()
