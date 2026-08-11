"""Primary exact checks for the three-activity two-defect detector theorem."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

MODES4 = tuple(range(4))
WORDS4 = tuple(product(range(3), repeat=4))
WORD4_INDEX = {word: index for index, word in enumerate(WORDS4)}
PAIRS = tuple(combinations(range(4), 2))

ZERO = (sp.Integer(0), sp.Integer(0), sp.Integer(0))
AXIS_A = (sp.Integer(1), sp.Integer(0), sp.Integer(0))
AXIS_B = (sp.Integer(0), sp.Integer(1), sp.Integer(0))
TYPE_ROWS = {
    "T": (AXIS_A, AXIS_B),
    "A": (AXIS_A, ZERO),
    "B": (ZERO, AXIS_A),
    "Z": (ZERO, ZERO),
}


def collision_matrix_four(
    a_rows: list[tuple[sp.Expr, sp.Expr, sp.Expr]],
    b_rows: list[tuple[sp.Expr, sp.Expr, sp.Expr]],
) -> sp.Matrix:
    matrix = sp.zeros(81, 12)
    for h_mode in MODES4:
        for h_coord in range(3):
            column = 3 * h_mode + h_coord
            for b_mode in MODES4:
                if b_mode == h_mode:
                    continue
                local_rows = []
                for mode in MODES4:
                    if mode == h_mode:
                        local_rows.append(
                            tuple(sp.Integer(coord == h_coord) for coord in range(3))
                        )
                    elif mode == b_mode:
                        local_rows.append(b_rows[mode])
                    else:
                        local_rows.append(a_rows[mode])
                for word in WORDS4:
                    coefficient = sp.Integer(2)
                    for mode, coord in enumerate(word):
                        coefficient *= local_rows[mode][coord]
                    if coefficient:
                        matrix[WORD4_INDEX[word], column] += coefficient
    return matrix


def candidate_span_matches(matrix: sp.Matrix, candidates: list[sp.Matrix]) -> None:
    kernel = matrix.nullspace()
    assert len(kernel) == len(candidates)
    candidate_matrix = sp.Matrix.hstack(*candidates)
    assert candidate_matrix.rank() == len(candidates)
    assert matrix * candidate_matrix == sp.zeros(matrix.rows, len(candidates))


def assert_one_sided_kernels() -> tuple[int, int, int]:
    transverse_a = [AXIS_A] * 4
    transverse_b = [AXIS_B] * 4

    a_only = collision_matrix_four(transverse_a, [ZERO, *transverse_b[1:]])
    a_kernel = sp.Matrix([-2, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0])
    assert a_only.rank() == 11
    candidate_span_matches(a_only, [a_kernel])

    b_only = collision_matrix_four([ZERO, *transverse_a[1:]], [AXIS_A, *transverse_b[1:]])
    alpha_12 = sp.Matrix([0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0])
    alpha_13 = sp.Matrix([0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0])
    gamma = sp.Matrix([-1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0])
    assert b_only.rank() == 9
    candidate_span_matches(b_only, [alpha_12, alpha_13, gamma])

    zero_mode = collision_matrix_four([ZERO, *transverse_a[1:]], [ZERO, *transverse_b[1:]])
    zero_candidates = []
    for mode in range(1, 4):
        for coord in range(3):
            vector = sp.zeros(12, 1)
            vector[3 * mode + coord] = 1
            zero_candidates.append(vector)
    assert zero_mode.rank() == 3
    candidate_span_matches(zero_mode, zero_candidates)
    return a_only.rank(), b_only.rank(), zero_mode.rank()


def local_invisibility_matrix(
    frame: tuple[tuple[int, int], ...],
    retained: tuple[tuple[int, ...], ...],
    quotient_dimension: int,
) -> sp.Matrix:
    retained_dimension = len(retained[0])
    matrix = sp.zeros(4 * 2 * quotient_dimension * retained_dimension, 4 * quotient_dimension)
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
                        companion_value = sp.Integer(frame[x_column][companion_coord])
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
                            matrix[output, column] += companion_value * retained_value
    return matrix


def local_matrix(vector: sp.Matrix, quotient_dimension: int) -> sp.Matrix:
    return sp.Matrix(
        quotient_dimension,
        4,
        lambda row, column: vector[column * quotient_dimension + row],
    )


def assert_rank_one_subspace(kernel: list[sp.Matrix], quotient_dimension: int) -> None:
    matrices = [local_matrix(vector, quotient_dimension) for vector in kernel]
    for first_row, second_row in combinations(range(quotient_dimension), 2):
        for first_column, second_column in combinations(range(4), 2):
            for matrix in matrices:
                assert (
                    matrix[first_row, first_column] * matrix[second_row, second_column]
                    - matrix[first_row, second_column] * matrix[second_row, first_column]
                ) == 0
            for left_index, left in enumerate(matrices):
                for right in matrices[left_index + 1 :]:
                    assert (
                        left[first_row, first_column] * right[second_row, second_column]
                        + right[first_row, first_column] * left[second_row, second_column]
                        - left[first_row, second_column] * right[second_row, first_column]
                        - right[first_row, second_column] * left[second_row, first_column]
                    ) == 0


def assert_three_activity_charts() -> int:
    frames = (
        ((1, 0), (0, 1), (1, 1), (1, 2)),
        ((1, 0), (2, 0), (0, 1), (0, 3)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((0, 0), (1, 0), (2, 0), (0, 1)),
        ((0, 0), (0, 0), (1, 0), (0, 1)),
    )
    retained_sets = (
        ((1,), (2,), (-1,), (3,)),
        ((1, 0), (0, 1), (1, 1), (1, -1)),
        ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
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
                    matrix = local_invisibility_matrix(frame, retained, quotient_dimension)
                    assert_rank_one_subspace(matrix.nullspace(), quotient_dimension)
                    chart_count += 1
    assert chart_count == 150
    return chart_count


def deletion_collision_matrix(types: tuple[str, ...], deleted: int) -> sp.Matrix:
    retained_modes = tuple(mode for mode in range(5) if mode != deleted)
    a_rows = [TYPE_ROWS[mode_type][0] for mode_type in types]
    b_rows = [TYPE_ROWS[mode_type][1] for mode_type in types]
    matrix = sp.zeros(81, 15)
    for h_mode in retained_modes:
        for h_coord in range(3):
            column = 3 * h_mode + h_coord
            for b_mode in retained_modes:
                if b_mode == h_mode:
                    continue
                local_rows = []
                for mode in retained_modes:
                    if mode == h_mode:
                        local_rows.append(
                            tuple(sp.Integer(coord == h_coord) for coord in range(3))
                        )
                    elif mode == b_mode:
                        local_rows.append(b_rows[mode])
                    else:
                        local_rows.append(a_rows[mode])
                for word in WORDS4:
                    coefficient = sp.Integer(2)
                    for local_mode, coord in enumerate(word):
                        coefficient *= local_rows[local_mode][coord]
                    if coefficient:
                        matrix[WORD4_INDEX[word], column] += coefficient
    return matrix


def assert_two_defect_kernels() -> dict[str, int]:
    expected = {"AA": 1, "AB": 0, "AZ": 1, "BB": 3, "BZ": 3, "ZZ": 9}
    observed: dict[str, int] = {}
    for pair in ("AA", "AB", "AZ", "BB", "BZ", "ZZ"):
        types = (pair[0], pair[1], "T", "T", "T")
        combined = deletion_collision_matrix(types, 0).col_join(
            deletion_collision_matrix(types, 1)
        )
        nullity = 15 - combined.rank()
        assert nullity == expected[pair]
        observed[pair] = nullity

    aa_types = ("A", "A", "T", "T", "T")
    aa_combined = deletion_collision_matrix(aa_types, 0).col_join(
        deletion_collision_matrix(aa_types, 1)
    )
    aa_vector = sp.Matrix([-2, 0, 0, -2, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0])
    candidate_span_matches(aa_combined, [aa_vector])

    bb_types = ("B", "B", "T", "T", "T")
    bb_combined = deletion_collision_matrix(bb_types, 0).col_join(
        deletion_collision_matrix(bb_types, 1)
    )
    alpha_23 = sp.Matrix([0, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0])
    alpha_24 = sp.Matrix([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0])
    gamma = sp.Matrix([-1, 0, 0, -1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0])
    candidate_span_matches(bb_combined, [alpha_23, alpha_24, gamma])
    return observed


def assert_zero_mode_factorization() -> int:
    checked = 0
    for other_type in ("A", "B", "Z"):
        types = ("Z", other_type, "T", "T", "T")
        matrix = deletion_collision_matrix(types, 1)
        assert matrix.rank() == 3
        nonzero_columns = [column for column in range(15) if any(matrix[:, column])]
        assert nonzero_columns == [0, 1, 2]
        checked += 1
    return checked


def assert_inactive_set_ledger() -> tuple[int, int]:
    roots = set(range(4))
    subsets = [
        set(indices)
        for size in range(2, 5)
        for indices in combinations(range(4), size)
    ]
    disjoint = [(left, right) for left in subsets for right in subsets if not left & right]
    assert len(disjoint) == 6
    assert all(len(left) == len(right) == 2 and left | right == roots for left, right in disjoint)

    same_type_residual = [
        (left, right) for left in subsets for right in subsets if left | right != roots
    ]
    assert len(same_type_residual) == 58
    assert all(left & right and roots - (left | right) for left, right in same_type_residual)
    return len(disjoint), len(same_type_residual)


def main() -> None:
    kernel_ranks = assert_one_sided_kernels()
    charts = assert_three_activity_charts()
    pair_nullities = assert_two_defect_kernels()
    zero_factorizations = assert_zero_mode_factorization()
    mixed_partitions, residual_patterns = assert_inactive_set_ledger()
    print(f"PASS: exact A/B/Z collision ranks are {kernel_ranks}")
    print(f"PASS: {charts} three-activity companion charts have rank-one quotient kernels")
    print(f"PASS: two-defect common-kernel nullities {pair_nullities}")
    print(f"PASS: {zero_factorizations} zero-mode deletions factor through a rank-three P3 tensor")
    print(
        f"PASS: inactive-set ledger has {mixed_partitions} mixed partitions and "
        f"{residual_patterns} same-type crowded patterns"
    )
    print("SCOPE: AB/AZ/BZ/ZZ two-defect cells detected")
    print("SCOPE: AA/BB double-kernel cells and three-or-more defects remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
