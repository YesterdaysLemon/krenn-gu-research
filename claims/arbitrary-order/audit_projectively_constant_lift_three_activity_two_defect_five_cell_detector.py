"""Independent no-import audit for the three-activity two-defect theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

MODES4 = tuple(range(4))
WORDS4 = tuple(product(range(3), repeat=4))
WORD4_INDEX = {word: index for index, word in enumerate(WORDS4)}
PAIRS = tuple(combinations(range(4), 2))

ZERO = (0, 0, 0)
AXIS_A = (1, 0, 0)
AXIS_B = (0, 1, 0)
TYPE_ROWS = {
    "T": (AXIS_A, AXIS_B),
    "A": (AXIS_A, ZERO),
    "B": (ZERO, AXIS_A),
    "Z": (ZERO, ZERO),
}


def rref(
    matrix: list[list[int | Fraction]],
) -> tuple[list[list[Fraction]], list[int]]:
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return work, []
    row_count = len(work)
    column_count = len(work[0])
    pivots: list[int] = []
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, pivots


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


def collision_matrix_four(
    a_rows: list[tuple[int, int, int]],
    b_rows: list[tuple[int, int, int]],
) -> list[list[int]]:
    matrix = [[0 for _ in range(12)] for _ in range(81)]
    for h_mode in MODES4:
        for h_coord in range(3):
            column = 3 * h_mode + h_coord
            for b_mode in MODES4:
                if b_mode == h_mode:
                    continue
                local_rows: list[tuple[int, int, int]] = []
                for mode in MODES4:
                    if mode == h_mode:
                        local_rows.append(tuple(int(coord == h_coord) for coord in range(3)))
                    elif mode == b_mode:
                        local_rows.append(b_rows[mode])
                    else:
                        local_rows.append(a_rows[mode])
                for word in WORDS4:
                    coefficient = 2
                    for mode, coord in enumerate(word):
                        coefficient *= local_rows[mode][coord]
                    if coefficient:
                        matrix[WORD4_INDEX[word]][column] += coefficient
    return matrix


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(value * vector[column] for column, value in enumerate(row)) for row in matrix]


def candidate_span_matches(matrix: list[list[int]], candidates: list[list[int]]) -> None:
    assert len(nullspace(matrix)) == len(candidates)
    assert rank([list(row) for row in zip(*candidates, strict=True)]) == len(candidates)
    assert all(not any(matvec(matrix, candidate)) for candidate in candidates)


def audit_one_sided_kernels() -> tuple[int, int, int]:
    a_only = collision_matrix_four([AXIS_A] * 4, [ZERO, AXIS_B, AXIS_B, AXIS_B])
    a_kernel = [-2, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
    assert rank(a_only) == 11
    candidate_span_matches(a_only, [a_kernel])

    b_only = collision_matrix_four(
        [ZERO, AXIS_A, AXIS_A, AXIS_A],
        [AXIS_A, AXIS_B, AXIS_B, AXIS_B],
    )
    alpha_12 = [0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0]
    alpha_13 = [0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0]
    gamma = [-1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    assert rank(b_only) == 9
    candidate_span_matches(b_only, [alpha_12, alpha_13, gamma])

    zero_mode = collision_matrix_four(
        [ZERO, AXIS_A, AXIS_A, AXIS_A],
        [ZERO, AXIS_B, AXIS_B, AXIS_B],
    )
    zero_candidates: list[list[int]] = []
    for mode in range(1, 4):
        for coord in range(3):
            vector = [0] * 12
            vector[3 * mode + coord] = 1
            zero_candidates.append(vector)
    assert rank(zero_mode) == 3
    candidate_span_matches(zero_mode, zero_candidates)
    return 11, 9, 3


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
                assert (
                    local_entry(vector, quotient_dimension, first_row, first_column)
                    * local_entry(vector, quotient_dimension, second_row, second_column)
                    - local_entry(vector, quotient_dimension, first_row, second_column)
                    * local_entry(vector, quotient_dimension, second_row, first_column)
                ) == 0
            for left_index, left in enumerate(basis):
                for right in basis[left_index + 1 :]:
                    assert (
                        local_entry(left, quotient_dimension, first_row, first_column)
                        * local_entry(right, quotient_dimension, second_row, second_column)
                        + local_entry(right, quotient_dimension, first_row, first_column)
                        * local_entry(left, quotient_dimension, second_row, second_column)
                        - local_entry(left, quotient_dimension, first_row, second_column)
                        * local_entry(right, quotient_dimension, second_row, first_column)
                        - local_entry(right, quotient_dimension, first_row, second_column)
                        * local_entry(left, quotient_dimension, second_row, first_column)
                    ) == 0


def audit_three_activity_charts() -> int:
    frames = (
        ((1, 0), (0, 1), (1, 1), (1, 2)),
        ((1, 0), (2, 0), (0, 1), (0, 3)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((0, 0), (1, 0), (2, 0), (0, 1)),
        ((0, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (1, 1), (2, 2)),
    )
    retained_sets = (
        ((1,), (2,), (-1,), (3,)),
        ((1, 0), (0, 1), (1, 1), (1, -1)),
        ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)),
        ((2, -1, 1), (-1, 2, 1), (1, 1, -2), (3, 1, 1)),
    )
    active_masks = (*combinations(range(4), 3), tuple(range(4)))
    chart_count = 0
    for frame in frames:
        for active in active_masks:
            for retained_base in retained_sets:
                retained = tuple(
                    row if index in active else tuple(0 for _ in row)
                    for index, row in enumerate(retained_base)
                )
                for quotient_dimension in (2, 3):
                    basis = nullspace(
                        local_invisibility_matrix(frame, retained, quotient_dimension)
                    )
                    audit_rank_one_subspace(basis, quotient_dimension)
                    chart_count += 1
    assert chart_count == 240
    return chart_count


def deletion_collision_matrix(types: tuple[str, ...], deleted: int) -> list[list[int]]:
    retained_modes = tuple(mode for mode in range(5) if mode != deleted)
    a_rows = [TYPE_ROWS[mode_type][0] for mode_type in types]
    b_rows = [TYPE_ROWS[mode_type][1] for mode_type in types]
    matrix = [[0 for _ in range(15)] for _ in range(81)]
    for h_mode in retained_modes:
        for h_coord in range(3):
            column = 3 * h_mode + h_coord
            for b_mode in retained_modes:
                if b_mode == h_mode:
                    continue
                local_rows: list[tuple[int, int, int]] = []
                for mode in retained_modes:
                    if mode == h_mode:
                        local_rows.append(tuple(int(coord == h_coord) for coord in range(3)))
                    elif mode == b_mode:
                        local_rows.append(b_rows[mode])
                    else:
                        local_rows.append(a_rows[mode])
                for word in WORDS4:
                    coefficient = 2
                    for local_mode, coord in enumerate(word):
                        coefficient *= local_rows[local_mode][coord]
                    if coefficient:
                        matrix[WORD4_INDEX[word]][column] += coefficient
    return matrix


def stack(top: list[list[int]], bottom: list[list[int]]) -> list[list[int]]:
    return [*top, *bottom]


def audit_two_defect_kernels() -> dict[str, int]:
    expected = {"AA": 1, "AB": 0, "AZ": 1, "BB": 3, "BZ": 3, "ZZ": 9}
    observed: dict[str, int] = {}
    for pair, expected_nullity in expected.items():
        types = (pair[0], pair[1], "T", "T", "T")
        combined = stack(
            deletion_collision_matrix(types, 0), deletion_collision_matrix(types, 1)
        )
        nullity = 15 - rank(combined)
        assert nullity == expected_nullity
        observed[pair] = nullity

    aa_types = ("A", "A", "T", "T", "T")
    aa_combined = stack(
        deletion_collision_matrix(aa_types, 0), deletion_collision_matrix(aa_types, 1)
    )
    aa_vector = [-2, 0, 0, -2, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
    candidate_span_matches(aa_combined, [aa_vector])

    bb_types = ("B", "B", "T", "T", "T")
    bb_combined = stack(
        deletion_collision_matrix(bb_types, 0), deletion_collision_matrix(bb_types, 1)
    )
    alpha_23 = [0, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0]
    alpha_24 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0]
    gamma = [-1, 0, 0, -1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    candidate_span_matches(bb_combined, [alpha_23, alpha_24, gamma])
    return observed


def audit_zero_mode_factorization() -> int:
    checked = 0
    for other_type in ("A", "B", "Z"):
        matrix = deletion_collision_matrix(("Z", other_type, "T", "T", "T"), 1)
        assert rank(matrix) == 3
        nonzero_columns = [
            column
            for column in range(15)
            if any(matrix[row][column] for row in range(81))
        ]
        assert nonzero_columns == [0, 1, 2]
        checked += 1
    return checked


def audit_inactive_set_ledger() -> tuple[int, int]:
    roots = set(range(4))
    subsets = [
        set(indices)
        for size in range(2, 5)
        for indices in combinations(range(4), size)
    ]
    disjoint = [(left, right) for left in subsets for right in subsets if not left & right]
    assert len(disjoint) == 6
    assert all(len(left) == len(right) == 2 and left | right == roots for left, right in disjoint)
    residual = [(left, right) for left in subsets for right in subsets if left | right != roots]
    assert len(residual) == 58
    assert all(left & right and roots - (left | right) for left, right in residual)
    return len(disjoint), len(residual)


def main() -> None:
    kernel_ranks = audit_one_sided_kernels()
    charts = audit_three_activity_charts()
    pair_nullities = audit_two_defect_kernels()
    zero_factorizations = audit_zero_mode_factorization()
    mixed_partitions, residual_patterns = audit_inactive_set_ledger()
    print(f"AUDIT PASS: independently reconstructed A/B/Z collision ranks {kernel_ranks}")
    print(f"AUDIT PASS: {charts} polarized three-activity charts have rank-one kernels")
    print(f"AUDIT PASS: two-defect common-kernel nullities {pair_nullities}")
    print(f"AUDIT PASS: {zero_factorizations} zero-mode factorization ledgers have rank three")
    print(
        f"AUDIT PASS: inactive sets give {mixed_partitions} AB partitions and "
        f"{residual_patterns} same-type crowded patterns"
    )
    print("AUDIT SCOPE: AB/AZ/BZ/ZZ detected; AA/BB reduced but open")
    print("AUDIT SCOPE: three-or-more defects and global Krenn-Gu remain open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
