"""Primary exact checks for the rank-one-mode five-cell detector theorem."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

MODES = tuple(range(4))
WORDS = tuple(product(range(3), repeat=4))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
PAIRS = tuple(combinations(range(4), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def collision_matrix(
    a_rows: list[tuple[sp.Expr, sp.Expr, sp.Expr]],
    b_rows: list[tuple[sp.Expr, sp.Expr, sp.Expr]],
) -> sp.Matrix:
    """Matrix of h -> P4(h,a,a,b), with the labelled-a factor included."""

    matrix = sp.zeros(81, 12)
    for h_mode in MODES:
        for h_coord in range(3):
            column = 3 * h_mode + h_coord
            for b_mode in MODES:
                if b_mode == h_mode:
                    continue
                local_rows = []
                for mode in MODES:
                    if mode == h_mode:
                        local_rows.append(
                            tuple(sp.Integer(coord == h_coord) for coord in range(3))
                        )
                    elif mode == b_mode:
                        local_rows.append(b_rows[mode])
                    else:
                        local_rows.append(a_rows[mode])
                for word in WORDS:
                    coefficient = sp.Integer(2)
                    for mode, coord in enumerate(word):
                        coefficient *= local_rows[mode][coord]
                    if coefficient:
                        matrix[WORD_INDEX[word], column] += coefficient
    return matrix


def assert_collision_classification() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    a_rows = [(sp.Integer(1), sp.Integer(0), sp.Integer(0))] * 4
    b_rows = [
        (lam, sp.Integer(0), sp.Integer(0)),
        *[(sp.Integer(0), sp.Integer(1), sp.Integer(0))] * 3,
    ]
    symbolic = collision_matrix(a_rows, b_rows)
    certificate_rows = (0, 1, 2, 3, 4, 6, 9, 10, 12, 18, 28, 55)
    determinant = sp.factor(symbolic[list(certificate_rows), :].det())
    assert determinant == -24576 * lam**4

    zero = (sp.Integer(0), sp.Integer(0), sp.Integer(0))
    axis_a = (sp.Integer(1), sp.Integer(0), sp.Integer(0))
    axis_b = (sp.Integer(0), sp.Integer(1), sp.Integer(0))

    one_sided_b_zero = collision_matrix([axis_a] * 4, [zero, axis_b, axis_b, axis_b])
    kernel_a = sp.Matrix([-2, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0])
    assert one_sided_b_zero.rank() == 11
    assert one_sided_b_zero * kernel_a == sp.zeros(81, 1)

    one_sided_a_zero = collision_matrix(
        [zero, axis_a, axis_a, axis_a],
        [axis_a, axis_b, axis_b, axis_b],
    )
    kernel_b = sp.Matrix([0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0])
    assert one_sided_a_zero.rank() == 9
    assert one_sided_a_zero * kernel_b == sp.zeros(81, 1)

    both_zero = collision_matrix(
        [zero, axis_a, axis_a, axis_a],
        [zero, axis_b, axis_b, axis_b],
    )
    kernel_zero = sp.Matrix([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    assert both_zero.rank() == 3
    assert both_zero * kernel_zero == sp.zeros(81, 1)


def companion_map(frame: tuple[tuple[int, int], ...]) -> sp.Matrix:
    """Map the six B_pq entries to XL, including the complement indexing."""

    matrix = sp.zeros(8, 6)
    for pair, column in PAIR_INDEX.items():
        complement = tuple(index for index in range(4) if index not in pair)
        left, right = complement
        for companion_coord in range(2):
            matrix[2 * left + companion_coord, column] += frame[right][
                companion_coord
            ]
            matrix[2 * right + companion_coord, column] += frame[left][
                companion_coord
            ]
    return matrix


def projective_direction(row: tuple[int, int]) -> tuple[int, int] | None:
    x_coord, y_coord = row
    if x_coord == y_coord == 0:
        return None
    if x_coord:
        ratio = sp.Rational(y_coord, x_coord)
        return (ratio.p, ratio.q)
    return (1, 0)


def is_balanced(frame: tuple[tuple[int, int], ...]) -> bool:
    directions = [projective_direction(row) for row in frame]
    if any(direction is None for direction in directions):
        return False
    counts = sorted(directions.count(direction) for direction in set(directions))
    return counts == [2, 2]


def assert_companion_census() -> tuple[int, int, int]:
    rows = ((0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (1, 2))
    good_count = 0
    zero_count = 0
    balanced_count = 0
    for frame in product(rows, repeat=4):
        if sp.Matrix(frame).rank() != 2:
            continue
        kernel = companion_map(frame).nullspace()
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
        if is_balanced(frame):
            balanced_count += 1
            assert len(kernel) == 1
            direction_groups: dict[tuple[int, int], list[int]] = {}
            for index, row in enumerate(frame):
                direction = projective_direction(row)
                assert direction is not None
                direction_groups.setdefault(direction, []).append(index)
            groups = list(direction_groups.values())
            assert sorted(len(group) for group in groups) == [2, 2]
            vector = kernel[0]
            for group in groups:
                coordinate = PAIR_INDEX[tuple(sorted(group))]
                assert vector[coordinate] == 0
            cross_coordinates = [
                PAIR_INDEX[tuple(sorted((left, right)))]
                for left in groups[0]
                for right in groups[1]
            ]
            assert all(vector[coordinate] != 0 for coordinate in cross_coordinates)
            continue
        good_count += 1
        assert not kernel
    assert (good_count, zero_count, balanced_count) == (560, 600, 60)
    return good_count, zero_count, balanced_count


def local_invisibility_matrix(
    frame: tuple[tuple[int, int], ...],
    retained: tuple[tuple[int, ...], ...],
    quotient_dimension: int,
) -> sp.Matrix:
    """Linear map v_p -> quotient of the four collective coefficients."""

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


def basis_as_local_matrix(vector: sp.Matrix, quotient_dimension: int) -> sp.Matrix:
    return sp.Matrix(
        quotient_dimension,
        4,
        lambda row, column: vector[column * quotient_dimension + row],
    )


def assert_rank_one_kernel(kernel: list[sp.Matrix], quotient_dimension: int) -> None:
    matrices = [basis_as_local_matrix(vector, quotient_dimension) for vector in kernel]
    for first_row, second_row in combinations(range(quotient_dimension), 2):
        for first_column, second_column in combinations(range(4), 2):
            for matrix in matrices:
                minor = (
                    matrix[first_row, first_column] * matrix[second_row, second_column]
                    - matrix[first_row, second_column] * matrix[second_row, first_column]
                )
                assert minor == 0
            for left_index, left in enumerate(matrices):
                for right in matrices[left_index + 1 :]:
                    polarized = (
                        left[first_row, first_column] * right[second_row, second_column]
                        + right[first_row, first_column] * left[second_row, second_column]
                        - left[first_row, second_column] * right[second_row, first_column]
                        - right[first_row, second_column] * left[second_row, first_column]
                    )
                    assert polarized == 0


def assert_local_trapping_charts() -> int:
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
    )
    chart_count = 0
    for frame in frames:
        for retained in retained_sets:
            assert all(any(value != 0 for value in row) for row in retained)
            for quotient_dimension in (2, 3):
                matrix = local_invisibility_matrix(frame, retained, quotient_dimension)
                assert_rank_one_kernel(matrix.nullspace(), quotient_dimension)
                chart_count += 1
    assert chart_count == 40
    return chart_count


def assert_defect_ledger() -> tuple[int, int, int, int]:
    mode_types = ("T", "D", "A", "B", "Z")
    one_defect = 0
    regular_two_defect = 0
    residual_two_defect = 0
    higher_defect = 0
    for word in product(mode_types, repeat=5):
        defects = [index for index, mode_type in enumerate(word) if mode_type != "T"]
        if len(defects) == 1:
            one_defect += 1
            retained = [word[index] for index in range(5) if index != defects[0]]
            assert retained == ["T"] * 4
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
    assert_collision_classification()
    good, zero, balanced = assert_companion_census()
    charts = assert_local_trapping_charts()
    one, regular_two, residual_two, higher = assert_defect_ledger()
    print("PASS: symbolic one-regular-defect collision minor -24576*lambda^4")
    print("PASS: exact one-sided/zero collision kernels have ranks 11, 9, 3")
    print(
        f"PASS: 1220 rank-two companion frames: good={good}, zero={zero}, balanced={balanced}"
    )
    print(f"PASS: {charts} quotient trapping charts have rank-at-most-one kernels")
    print(
        "PASS: 3125 defect words: "
        f"one={one}, regular-two={regular_two}, residual-two={residual_two}, higher={higher}"
    )
    print("SCOPE: one arbitrary defect or two defects with a regular member")
    print("SCOPE: two degenerate defects, higher defects, and global Krenn-Gu remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
