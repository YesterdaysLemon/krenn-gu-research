"""Independent no-import audit for the rank-one-mode five-cell detector."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

MODES = tuple(range(4))
WORDS = tuple(product(range(3), repeat=4))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
PAIRS = tuple(combinations(range(4), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def collision_matrix(
    a_rows: list[tuple[int, int, int]],
    b_rows: list[tuple[int, int, int]],
) -> list[list[int]]:
    matrix = [[0 for _ in range(12)] for _ in range(81)]
    for h_mode in MODES:
        for h_coord in range(3):
            column = 3 * h_mode + h_coord
            for b_mode in MODES:
                if b_mode == h_mode:
                    continue
                local_rows: list[tuple[int, int, int]] = []
                for mode in MODES:
                    if mode == h_mode:
                        local_rows.append(tuple(int(coord == h_coord) for coord in range(3)))
                    elif mode == b_mode:
                        local_rows.append(b_rows[mode])
                    else:
                        local_rows.append(a_rows[mode])
                for word in WORDS:
                    coefficient = 2
                    for mode, coord in enumerate(word):
                        coefficient *= local_rows[mode][coord]
                    if coefficient:
                        matrix[WORD_INDEX[word]][column] += coefficient
    return matrix


def rref(
    matrix: list[list[int | Fraction]],
) -> tuple[list[list[Fraction]], list[int]]:
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return work, []
    row_count = len(work)
    column_count = len(work[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [value / pivot for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, pivot_columns


def rank(matrix: list[list[int | Fraction]]) -> int:
    return len(rref(matrix)[1])


def nullspace(matrix: list[list[int | Fraction]]) -> list[list[Fraction]]:
    reduced, pivots = rref(matrix)
    column_count = len(matrix[0]) if matrix else 0
    free_columns = [column for column in range(column_count) if column not in pivots]
    basis: list[list[Fraction]] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(column_count)]
        vector[free] = Fraction(1)
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[pivot_row][free]
        basis.append(vector)
    return basis


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(value * vector[column] for column, value in enumerate(row)) for row in matrix]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def determinant_bareiss(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    dimension = len(work)
    sign = 1
    previous = 1
    for pivot_index in range(dimension - 1):
        selected = next(
            (
                row
                for row in range(pivot_index, dimension)
                if work[row][pivot_index] != 0
            ),
            None,
        )
        if selected is None:
            return 0
        if selected != pivot_index:
            work[pivot_index], work[selected] = work[selected], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, dimension):
            for column in range(pivot_index + 1, dimension):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
            work[row][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]


def audit_collision_classification() -> tuple[int, tuple[int, int, int]]:
    axis_a = (1, 0, 0)
    axis_b = (0, 1, 0)
    zero = (0, 0, 0)
    reference = collision_matrix([axis_a] * 4, [axis_a, axis_b, axis_b, axis_b])
    _, independent_rows = rref(transpose(reference))
    assert len(independent_rows) == 12

    normalized_determinants = []
    for scalar in (1, -2, 3):
        matrix = collision_matrix(
            [axis_a] * 4,
            [(scalar, 0, 0), axis_b, axis_b, axis_b],
        )
        minor = [matrix[row] for row in independent_rows]
        determinant = determinant_bareiss(minor)
        normalized_determinants.append(Fraction(determinant, scalar**4))
    assert normalized_determinants == [Fraction(-24576)] * 3

    one_sided_b_zero = collision_matrix([axis_a] * 4, [zero, axis_b, axis_b, axis_b])
    kernel_a = [-2, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
    assert rank(one_sided_b_zero) == 11
    assert not any(matvec(one_sided_b_zero, kernel_a))

    one_sided_a_zero = collision_matrix(
        [zero, axis_a, axis_a, axis_a],
        [axis_a, axis_b, axis_b, axis_b],
    )
    kernel_b = [0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0]
    assert rank(one_sided_a_zero) == 9
    assert not any(matvec(one_sided_a_zero, kernel_b))

    both_zero = collision_matrix(
        [zero, axis_a, axis_a, axis_a],
        [zero, axis_b, axis_b, axis_b],
    )
    kernel_zero = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    assert rank(both_zero) == 3
    assert not any(matvec(both_zero, kernel_zero))
    return len(independent_rows), (11, 9, 3)


def companion_map(frame: tuple[tuple[int, int], ...]) -> list[list[int]]:
    matrix = [[0 for _ in range(6)] for _ in range(8)]
    for pair, column in PAIR_INDEX.items():
        complement = tuple(index for index in range(4) if index not in pair)
        left, right = complement
        for companion_coord in range(2):
            matrix[2 * left + companion_coord][column] += frame[right][companion_coord]
            matrix[2 * right + companion_coord][column] += frame[left][companion_coord]
    return matrix


def frame_rank_two(frame: tuple[tuple[int, int], ...]) -> bool:
    return any(
        frame[left][0] * frame[right][1] - frame[left][1] * frame[right][0]
        for left, right in PAIRS
    )


def projective_direction(row: tuple[int, int]) -> tuple[str, Fraction] | None:
    x_coord, y_coord = row
    if x_coord == y_coord == 0:
        return None
    if x_coord:
        return ("finite", Fraction(y_coord, x_coord))
    return ("infinite", Fraction(0))


def balanced_groups(frame: tuple[tuple[int, int], ...]) -> list[list[int]] | None:
    groups: dict[tuple[str, Fraction], list[int]] = {}
    for index, row in enumerate(frame):
        direction = projective_direction(row)
        if direction is None:
            return None
        groups.setdefault(direction, []).append(index)
    values = list(groups.values())
    if sorted(len(group) for group in values) == [2, 2]:
        return values
    return None


def audit_companion_census() -> tuple[int, int, int]:
    rows = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1))
    good_count = 0
    zero_count = 0
    balanced_count = 0
    for frame in product(rows, repeat=4):
        if not frame_rank_two(frame):
            continue
        kernel = nullspace(companion_map(frame))
        zero_indices = [index for index, row in enumerate(frame) if row == (0, 0)]
        if zero_indices:
            zero_count += 1
            for zero_index in zero_indices:
                for other in range(4):
                    if other == zero_index:
                        continue
                    coordinate = PAIR_INDEX[tuple(sorted((zero_index, other)))]
                    assert all(vector[coordinate] == 0 for vector in kernel)
            continue
        groups = balanced_groups(frame)
        if groups is not None:
            balanced_count += 1
            assert len(kernel) == 1
            vector = kernel[0]
            for group in groups:
                assert vector[PAIR_INDEX[tuple(sorted(group))]] == 0
            for left in groups[0]:
                for right in groups[1]:
                    assert vector[PAIR_INDEX[tuple(sorted((left, right)))]] != 0
            continue
        good_count += 1
        assert not kernel
    assert (good_count, zero_count, balanced_count) == (1200, 1020, 90)
    return good_count, zero_count, balanced_count


def local_invisibility_matrix(
    frame: tuple[tuple[int, int], ...],
    retained: tuple[tuple[int, ...], ...],
    quotient_dimension: int,
) -> list[list[int]]:
    retained_dimension = len(retained[0])
    matrix = [
        [0 for _ in range(4 * quotient_dimension)]
        for _ in range(4 * 2 * quotient_dimension * retained_dimension)
    ]
    for root in range(4):
        for quotient_coord in range(quotient_dimension):
            column = root * quotient_dimension + quotient_coord
            for pair in PAIRS:
                if root not in pair:
                    continue
                other = pair[1] if root == pair[0] else pair[0]
                complement = tuple(index for index in range(4) if index not in pair)
                for x_row, x_column in (complement, tuple(reversed(complement))):
                    for companion_coord in range(2):
                        companion_value = frame[x_column][companion_coord]
                        if not companion_value:
                            continue
                        for retained_coord, retained_value in enumerate(retained[other]):
                            if not retained_value:
                                continue
                            output = (
                                ((2 * x_row + companion_coord) * quotient_dimension + quotient_coord)
                                * retained_dimension
                                + retained_coord
                            )
                            matrix[output][column] += companion_value * retained_value
    return matrix


def local_entry(
    vector: list[Fraction], quotient_dimension: int, row: int, column: int
) -> Fraction:
    return vector[column * quotient_dimension + row]


def audit_rank_one_subspace(
    basis: list[list[Fraction]], quotient_dimension: int
) -> None:
    for first_row, second_row in combinations(range(quotient_dimension), 2):
        for first_column, second_column in combinations(range(4), 2):
            for vector in basis:
                minor = (
                    local_entry(vector, quotient_dimension, first_row, first_column)
                    * local_entry(vector, quotient_dimension, second_row, second_column)
                    - local_entry(vector, quotient_dimension, first_row, second_column)
                    * local_entry(vector, quotient_dimension, second_row, first_column)
                )
                assert minor == 0
            for left_index, left in enumerate(basis):
                for right in basis[left_index + 1 :]:
                    polarized = (
                        local_entry(left, quotient_dimension, first_row, first_column)
                        * local_entry(right, quotient_dimension, second_row, second_column)
                        + local_entry(right, quotient_dimension, first_row, first_column)
                        * local_entry(left, quotient_dimension, second_row, second_column)
                        - local_entry(left, quotient_dimension, first_row, second_column)
                        * local_entry(right, quotient_dimension, second_row, first_column)
                        - local_entry(right, quotient_dimension, first_row, second_column)
                        * local_entry(left, quotient_dimension, second_row, first_column)
                    )
                    assert polarized == 0


def audit_local_trapping_charts() -> int:
    frames = (
        ((1, 0), (0, 1), (1, 1), (1, 2)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((0, 0), (0, 0), (1, 0), (0, 1)),
        ((1, 0), (2, 0), (0, 1), (0, 3)),
    )
    retained_sets = (
        ((1,), (2,), (-1,), (3,)),
        ((1, 0), (0, 1), (1, 1), (1, -1)),
        ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)),
        ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
        ((1, 2), (1, 2), (-1, 1), (2, -1)),
        ((2, -1, 1), (-1, 2, 1), (1, 1, -2), (3, 1, 1)),
    )
    chart_count = 0
    for frame in frames:
        for retained in retained_sets:
            assert all(any(value != 0 for value in row) for row in retained)
            for quotient_dimension in (2, 3):
                basis = nullspace(
                    local_invisibility_matrix(frame, retained, quotient_dimension)
                )
                audit_rank_one_subspace(basis, quotient_dimension)
                chart_count += 1
    assert chart_count == 48
    return chart_count


def audit_defect_ledger() -> tuple[int, int, int, int]:
    mode_types = ("T", "D", "A", "B", "Z")
    one_defect = 0
    regular_two_defect = 0
    residual_two_defect = 0
    higher_defect = 0
    for word in product(mode_types, repeat=5):
        defects = [index for index, mode_type in enumerate(word) if mode_type != "T"]
        if len(defects) == 1:
            one_defect += 1
            assert all(word[index] == "T" for index in range(5) if index != defects[0])
        elif len(defects) == 2 and any(word[index] == "D" for index in defects):
            regular_two_defect += 1
            regular = next(index for index in defects if word[index] == "D")
            deleted = next(index for index in defects if index != regular)
            retained = sorted(word[index] for index in range(5) if index != deleted)
            assert retained == ["D", "T", "T", "T"]
        elif len(defects) == 2:
            residual_two_defect += 1
        elif len(defects) >= 3:
            higher_defect += 1
    assert (one_defect, regular_two_defect, residual_two_defect, higher_defect) == (
        20,
        70,
        90,
        2944,
    )
    return one_defect, regular_two_defect, residual_two_defect, higher_defect


def main() -> None:
    minor_size, exceptional_ranks = audit_collision_classification()
    good, zero, balanced = audit_companion_census()
    charts = audit_local_trapping_charts()
    one, regular_two, residual_two, higher = audit_defect_ledger()
    print(
        f"AUDIT PASS: independent {minor_size}x{minor_size} collision minor scales as -24576*lambda^4"
    )
    print(f"AUDIT PASS: one-sided/zero collision ranks are {exceptional_ranks}")
    print(
        f"AUDIT PASS: 2310 companion frames: good={good}, zero={zero}, balanced={balanced}"
    )
    print(f"AUDIT PASS: {charts} polarized quotient charts have rank-at-most-one kernels")
    print(
        "AUDIT PASS: defect ledger "
        f"one={one}, regular-two={regular_two}, residual-two={residual_two}, higher={higher}"
    )
    print("AUDIT SCOPE: complete only for one arbitrary or regular-two defects")
    print("AUDIT SCOPE: two degenerate defects, higher defects, and global conjecture remain open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
