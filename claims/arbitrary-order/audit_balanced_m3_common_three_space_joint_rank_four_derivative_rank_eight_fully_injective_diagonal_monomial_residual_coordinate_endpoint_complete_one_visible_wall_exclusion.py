#!/usr/bin/env python3
"""Independent Fraction audit of the complete one-visible-wall exclusion.

This standard-library-only replay independently enumerates the twenty support
cells on the one-visible diagonal endpoint and checks their exact partition:
two same-coordinate cells, four radical-shore cells, seven remaining
``T_0`` cross-pair cells, six ``T_1`` cells with an ``e_0`` shore, and the
final ``(101,101)`` cell.  It then checks the corrected-cube coefficients,
the retained-face indices, the source-recovery signs, both incidence-quotient
interfaces, the full unsliced matrix separation, and the final graph-gauge
and rank interface, all over :class:`fractions.Fraction`.

The coordinate-free S2CG assertions remain analytic inputs of the owning
proof: the full-sensor radical-line bound, the classification of zero pairs,
and the resulting split-three-space/common-split-plane dichotomy are not
reproved here.  This audit checks the exact finite-dimensional interfaces to
those assertions.  It imports no primary verifier, SymPy, or solver.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction
DIM = 3
ROOT_DIM = DIM * DIM
SOURCE_INDICES = tuple(reversed(tuple(product(range(DIM), repeat=3))))
PERMUTATIONS = tuple(reversed(tuple(permutations(range(3)))))

Vector = tuple[Q, ...]
Matrix = tuple[Q, ...]
MaskPair = tuple[int, int]


def zero(size: int) -> Vector:
    return (Q(0),) * size


def unit(size: int, index: int) -> Vector:
    return tuple(Q(candidate == index) for candidate in range(size))


def add(*vectors: Vector) -> Vector:
    assert vectors
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: int | Q, vector: Vector) -> Vector:
    scalar = Q(coefficient)
    return tuple(scalar * entry for entry in vector)


def dot(first: Vector, second: Vector) -> Q:
    return sum(
        (left * right for left, right in zip(first, second, strict=True)),
        Q(0),
    )


def outer(first: Vector, second: Vector) -> Matrix:
    return tuple(left * right for left in first for right in second)


def matrix_add(*matrices: Matrix) -> Matrix:
    return add(*matrices)


def matrix_scale(coefficient: int | Q, matrix: Matrix) -> Matrix:
    return scale(coefficient, matrix)


def column_rank(columns: tuple[Vector, ...] | list[Vector]) -> int:
    if not columns:
        return 0
    row_count = len(columns[0])
    assert all(len(column) == row_count for column in columns)
    matrix = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (
                candidate
                for candidate in range(pivot_row, row_count)
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for candidate in range(row_count):
            if candidate == pivot_row or not matrix[candidate][column]:
                continue
            multiplier = matrix[candidate][column]
            matrix[candidate] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[candidate], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def source_position(index: tuple[int, int, int]) -> int:
    return SOURCE_INDICES.index(index)


def target(colour: int) -> Vector:
    return unit(len(SOURCE_INDICES), source_position((colour,) * 3))


def source_row(source: int, colour_vector: Vector) -> Vector:
    blocks = [zero(DIM), zero(DIM), zero(DIM)]
    blocks[source] = colour_vector
    return tuple(entry for block in blocks for entry in block)


def split_source_row(row: Vector) -> tuple[Vector, Vector, Vector]:
    assert len(row) == DIM * DIM
    return row[:DIM], row[DIM : 2 * DIM], row[2 * DIM :]


def permanent(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = [Q(0) for _ in SOURCE_INDICES]
    for permutation in PERMUTATIONS:
        x_part = split_source_row(rows[permutation[0]])[0]
        y_part = split_source_row(rows[permutation[1]])[1]
        z_part = split_source_row(rows[permutation[2]])[2]
        for index in SOURCE_INDICES:
            i, j, k = index
            result[source_position(index)] += x_part[i] * y_part[j] * z_part[k]
    return tuple(result)


def triple_quotient(tensor: Vector, visible_colour: int) -> Vector:
    kept = tuple(colour for colour in range(DIM) if colour != visible_colour)
    return tuple(
        tensor[source_position(index)] for index in product(kept, repeat=3)
    )


def generic_source_row(seed: int) -> Vector:
    return tuple(Q(seed + 3 * index + 1, index + 2) for index in range(9))


def mask_name(mask: int) -> str:
    return f"{mask:03b}"


def has_colour(mask: int, colour: int) -> bool:
    return bool(mask & (1 << colour))


def representative(mask: int, role: str) -> Vector:
    weights = {
        "x": (Q(2), Q(-3), Q(5)),
        "y": (Q(7), Q(11), Q(-13)),
    }[role]
    return tuple(weights[colour] if has_colour(mask, colour) else Q(0) for colour in range(DIM))


def target_visibility(pair: MaskPair) -> tuple[bool, bool]:
    x_mask, y_mask = pair
    t0_visible = (
        x_mask != 0b001
        and y_mask != 0b001
        and (has_colour(x_mask, 1) or has_colour(y_mask, 1))
    )
    t1_visible = (
        x_mask != 0b010
        and y_mask != 0b010
        and (has_colour(x_mask, 0) or has_colour(y_mask, 0))
    )
    return t0_visible, t1_visible


def check_support_partition() -> dict[str, set[MaskPair]]:
    admissible_masks = tuple(
        reversed(tuple(mask for mask in range(1, 8) if mask != 0b100))
    )
    one_visible = {
        pair
        for pair in product(admissible_masks, repeat=2)
        if sum(target_visibility(pair)) == 1
    }
    assert len(one_visible) == 20

    partition = {
        "same": {(0b010, 0b010), (0b001, 0b001)},
        "radical": {
            (0b010, 0b101),
            (0b101, 0b010),
            (0b001, 0b110),
            (0b110, 0b001),
        },
        "t0_cross": {
            (0b010, 0b011),
            (0b011, 0b010),
            (0b010, 0b110),
            (0b110, 0b010),
            (0b010, 0b111),
            (0b111, 0b010),
            (0b110, 0b110),
        },
        "t1_e0_shore": {
            (0b001, 0b011),
            (0b011, 0b001),
            (0b001, 0b101),
            (0b101, 0b001),
            (0b001, 0b111),
            (0b111, 0b001),
        },
        "final": {(0b101, 0b101)},
    }
    assert {name: len(cells) for name, cells in partition.items()} == {
        "same": 2,
        "radical": 4,
        "t0_cross": 7,
        "t1_e0_shore": 6,
        "final": 1,
    }
    cells = [pair for family in partition.values() for pair in family]
    assert len(cells) == len(set(cells))
    assert set(cells) == one_visible

    t0_only = {pair for pair in one_visible if target_visibility(pair) == (True, False)}
    t1_only = {pair for pair in one_visible if target_visibility(pair) == (False, True)}
    assert len(t0_only) == len(t1_only) == 10
    assert t0_only == (
        {(0b010, 0b010), (0b010, 0b101), (0b101, 0b010)}
        | partition["t0_cross"]
    )
    assert t1_only == (
        {(0b001, 0b001), (0b001, 0b110), (0b110, 0b001)}
        | partition["t1_e0_shore"]
        | partition["final"]
    )
    return partition


def cube_coefficients(alpha: Vector, beta: Vector, lam: Q) -> tuple[tuple[Q, Q], ...]:
    """Return coefficients of ``T_k`` and ``S_k`` in the corrected cube."""
    return tuple(
        (alpha[colour] * beta[colour], lam * alpha[2] * beta[2])
        for colour in range(DIM)
    )


def all_cube_coefficients_zero(alpha: Vector, beta: Vector, lam: Q) -> bool:
    return all(
        target_coefficient == correction_coefficient == 0
        for target_coefficient, correction_coefficient in cube_coefficients(
            alpha, beta, lam
        )
    )


def check_retained_indices_and_source_recovery() -> None:
    retained = {
        (i, j, k)
        for k in (1, 2)
        for i in range(DIM)
        for j in range(DIM)
        if (i, j) != (2, 2)
    }
    assert len(retained) == 16
    assert (1, 1, 1) in retained
    assert (2, 2, 1) not in retained and (2, 2, 2) not in retained
    assert {(2, 0, 1), (2, 0, 2), (0, 2, 1), (0, 2, 2)} < retained
    same_t0_equal_plane_faces = {
        *((1, j, k) for j in (0, 2) for k in (1, 2)),
        *((i, 1, k) for i in (0, 2) for k in (1, 2)),
    }
    assert len(same_t0_equal_plane_faces) == 8
    assert same_t0_equal_plane_faces < retained

    lam = Q(-17, 6)
    source_1 = add(scale(Q(2, 5), target(0)), scale(Q(-7, 9), target(1)))
    source_2 = add(scale(Q(11, 8), target(1)), scale(Q(13, 7), target(2)))
    p_221 = scale(lam, source_1)
    p_222 = add(target(2), scale(lam, source_2))
    assert scale(1 / lam, p_221) == source_1
    assert scale(1 / lam, add(p_222, scale(-1, target(2)))) == source_2


def complete_target_coefficient(
    i: int,
    j: int,
    k: int,
    x: Vector,
    y: Vector,
    a_lifts: tuple[Vector, Vector, Vector],
    b_lifts: tuple[Vector, Vector, Vector],
    sources: tuple[Vector, Vector, Vector],
    lam: Q,
) -> Vector:
    result = target(i) if i == j == k else zero(len(SOURCE_INDICES))
    if k == 0:
        for colour in reversed(range(DIM)):
            tangent_coefficient = (
                a_lifts[colour][i] * y[j] - x[i] * b_lifts[colour][j]
            )
            result = add(result, scale(tangent_coefficient, sources[colour]))
    if i == j == 2:
        result = add(result, scale(lam, sources[k]))
    return result


def check_e0_shore_source_identities() -> None:
    lam = Q(37, 10)
    sources = (
        add(scale(Q(2), target(0)), scale(Q(-1, 3), target(2))),
        add(scale(Q(5, 7), target(0)), scale(Q(11, 4), target(1))),
        add(scale(Q(-13, 9), target(1)), scale(Q(17, 6), target(2))),
    )
    a_lifts = (
        (Q(2), Q(-3), Q(5)),
        (Q(7), Q(11), Q(-13)),
        (Q(17), Q(-19), Q(23)),
    )
    b_lifts = (
        (Q(-29), Q(31), Q(37)),
        (Q(41), Q(-43), Q(47)),
        (Q(53), Q(59), Q(-61)),
    )

    # x=e0 orientation: equations (16)--(17) of the owning theorem.
    x = representative(0b001, "x")
    y = representative(0b111, "y")
    p = {
        (i, j, k): complete_target_coefficient(
            i, j, k, x, y, a_lifts, b_lifts, sources, lam
        )
        for i, j, k in product(reversed(range(DIM)), repeat=3)
    }
    assert not any(p[2, 0, 1]) and not any(p[2, 0, 2])
    for k in reversed(range(DIM)):
        contracted = add(scale(y[2], p[2, 0, k]), scale(-y[0], p[2, 2, k]))
        expected = scale(-y[0] * lam, sources[k])
        if k == 2:
            expected = add(expected, scale(-y[0], target(2)))
        assert contracted == expected

    tangent_sum = zero(len(SOURCE_INDICES))
    for colour in reversed(range(DIM)):
        tangent_sum = add(
            tangent_sum, scale(a_lifts[colour][2], sources[colour])
        )
    assert p[2, 0, 0] == scale(y[0], tangent_sum)
    assert p[2, 2, 0] == add(
        scale(y[2], tangent_sum), scale(lam, sources[0])
    )

    # Root-exchanged orientation: equations (19a).
    x = representative(0b111, "x")
    y = representative(0b001, "y")
    p = {
        (i, j, k): complete_target_coefficient(
            i, j, k, x, y, a_lifts, b_lifts, sources, lam
        )
        for i, j, k in product(reversed(range(DIM)), repeat=3)
    }
    assert not any(p[0, 2, 1]) and not any(p[0, 2, 2])
    for k in reversed(range(DIM)):
        contracted = add(scale(x[2], p[0, 2, k]), scale(-x[0], p[2, 2, k]))
        expected = scale(-x[0] * lam, sources[k])
        if k == 2:
            expected = add(expected, scale(-x[0], target(2)))
        assert contracted == expected


def check_radical_shores(radical_cells: set[MaskPair]) -> None:
    lam = Q(19, 7)
    e0, e1, e2 = (unit(DIM, colour) for colour in range(DIM))
    data = {
        (0b010, 0b101): ((e0, e2), (e1,)),
        (0b101, 0b010): ((e1,), (e0, e2)),
        (0b001, 0b110): ((e1, e2), (e0,)),
        (0b110, 0b001): ((e0,), (e1, e2)),
    }
    assert set(data) == radical_cells
    for pair, (alpha_shore, beta_shore) in data.items():
        x = representative(pair[0], "x")
        y = representative(pair[1], "y")
        assert all(dot(x, alpha) == 0 for alpha in alpha_shore)
        assert all(dot(y, beta) == 0 for beta in beta_shore)
        assert max(column_rank(alpha_shore), column_rank(beta_shore)) == 2
        for alpha, beta in product(alpha_shore, beta_shore):
            assert all_cube_coefficients_zero(alpha, beta, lam)


def t0_cross_data(pair: MaskPair) -> tuple[Vector, Vector, Vector, Vector]:
    x = representative(pair[0], "x")
    y = representative(pair[1], "y")
    e0, _, e2 = (unit(DIM, colour) for colour in range(DIM))
    if pair[0] == 0b010:
        return (
            e0,
            e2,
            (y[1], -y[0], Q(0)),
            (Q(0), y[2], -y[1]),
        )
    if pair[1] == 0b010:
        return (
            (x[1], -x[0], Q(0)),
            (Q(0), x[2], -x[1]),
            e0,
            e2,
        )
    assert pair == (0b110, 0b110)
    return (
        e0,
        (Q(0), x[2], -x[1]),
        e0,
        (Q(0), y[2], -y[1]),
    )


def t1_cross_data(pair: MaskPair) -> tuple[Vector, Vector, Vector, Vector]:
    x = representative(pair[0], "x")
    y = representative(pair[1], "y")
    _, e1, e2 = (unit(DIM, colour) for colour in range(DIM))
    if pair[0] == 0b001:
        return (
            e1,
            e2,
            (y[1], -y[0], Q(0)),
            (y[2], Q(0), -y[0]),
        )
    if pair[1] == 0b001:
        return (
            (x[1], -x[0], Q(0)),
            (x[2], Q(0), -x[0]),
            e1,
            e2,
        )
    assert pair == (0b101, 0b101)
    return (
        e1,
        (x[2], Q(0), -x[0]),
        e1,
        (y[2], Q(0), -y[0]),
    )


def visible_colour(pair: MaskPair) -> int:
    visibility = target_visibility(pair)
    assert sum(visibility) == 1
    return 0 if visibility[0] else 1


def check_cross_pair_cube(
    pair: MaskPair,
    data: tuple[Vector, Vector, Vector, Vector],
    lam: Q,
) -> Q:
    x = representative(pair[0], "x")
    y = representative(pair[1], "y")
    a, c, b, d = data
    assert dot(x, a) == dot(x, c) == 0
    assert dot(y, b) == dot(y, d) == 0
    assert column_rank((a, c)) == column_rank((b, d)) == 2
    assert all_cube_coefficients_zero(a, d, lam)
    assert all_cube_coefficients_zero(c, b, lam)

    colour = visible_colour(pair)
    coefficients = cube_coefficients(a, b, lam)
    assert all(correction == 0 for _, correction in coefficients)
    nonzero_targets = {
        index: coefficient
        for index, (coefficient, _) in enumerate(coefficients)
        if coefficient
    }
    assert set(nonzero_targets) == {colour}
    return nonzero_targets[colour]


def line_row(source: int, colour: int, coefficient: int | Q = 1) -> Vector:
    return source_row(source, scale(coefficient, unit(DIM, colour)))


def check_incidence_quotient_interfaces() -> None:
    for colour in (0, 1):
        pure_lines = tuple(line_row(source, colour) for source in range(3))
        q_in_split_q = add(
            scale(Q(2), pure_lines[0]),
            scale(Q(-3), pure_lines[1]),
            scale(Q(5), pure_lines[2]),
        )
        value = permanent(
            generic_source_row(7 + colour),
            generic_source_row(19 + colour),
            q_in_split_q,
        )
        assert not any(triple_quotient(value, colour))

        split_h = pure_lines[:2]
        q_in_h = add(scale(Q(-7, 3), split_h[0]), scale(Q(11, 5), split_h[1]))
        value = permanent(
            generic_source_row(29 + colour),
            generic_source_row(37 + colour),
            q_in_h,
        )
        assert not any(triple_quotient(value, colour))

        first_h = add(split_h[0], scale(Q(3, 2), split_h[1]))
        second_h = add(scale(Q(-5, 4), split_h[0]), split_h[1])
        value = permanent(first_h, second_h, generic_source_row(43 + colour))
        assert not any(triple_quotient(value, colour))

        recovered_colour = 1 - colour
        assert any(triple_quotient(target(recovered_colour), colour))
        assert not any(triple_quotient(target(colour), colour))


def check_same_t0_equal_plane_retained_faces() -> None:
    # This is the exact omitted-source interface used by the original
    # same-coordinate proof.  The eight retained zero faces eliminate the
    # omitted-source components of r_1 and p_1.
    x_line = line_row(0, 0)
    y_line = line_row(1, 0)
    omitted_basis = tuple(line_row(2, colour) for colour in range(DIM))
    omitted_images = tuple(
        permanent(x_line, y_line, row) for row in omitted_basis
    )
    assert column_rank(omitted_images) == DIM

    r_1 = add(scale(Q(2), x_line), scale(Q(-3), y_line))
    p_1 = add(scale(Q(5), x_line), scale(Q(7), y_line))
    q_1 = add(scale(Q(11), x_line), scale(Q(-13), y_line))
    assert not any(permanent(r_1, p_1, q_1))
    assert any(target(1))


def root_source_tensor(root_matrix: Matrix, source_tensor: Vector) -> Vector:
    return tuple(
        root_coefficient * source_coefficient
        for root_coefficient in root_matrix
        for source_coefficient in source_tensor
    )


def quotient_target(colour: int, visible: int) -> Vector:
    return triple_quotient(target(colour), visible)


def check_t1_source_and_unsliced_contradiction(
    cells: set[MaskPair],
    include_same: bool,
) -> None:
    lam = Q(-23, 9)
    e00 = unit(ROOT_DIM, 0)
    bar_t0 = quotient_target(0, 1)
    bar_t2 = quotient_target(2, 1)
    assert column_rank((bar_t0, bar_t2)) == 2

    cells_to_check = set(cells)
    if include_same:
        cells_to_check.add((0b001, 0b001))
    for pair in sorted(cells_to_check, reverse=True):
        data = t1_cross_data(pair)
        check_cross_pair_cube(pair, data, lam)
        _, c, _, d = data
        coefficients = cube_coefficients(c, d, lam)
        correction = coefficients[0][1]
        assert correction != 0
        assert coefficients[0][0] == coefficients[1][0] == 0
        assert coefficients[2][0] == correction / lam

        # In either S2CG incidence fork the quotient of M_(C,D)(q_k) is zero.
        # Solving the three exact cube equations gives these source images.
        bar_s0 = zero(len(bar_t0))
        bar_s1 = zero(len(bar_t0))
        bar_s2 = scale(-1 / lam, bar_t2)
        assert add(
            scale(coefficients[0][0], bar_t0),
            scale(correction, bar_s0),
        ) == zero(len(bar_t0))
        assert scale(correction, bar_s1) == zero(len(bar_t0))
        assert add(
            scale(coefficients[2][0], bar_t2),
            scale(correction, bar_s2),
        ) == zero(len(bar_t0))

        # The quotient of all P^(0) entries is zero in both incidence forks.
        # The unsliced matrix has a nonzero T0 coefficient on the left and no
        # T0 coefficient on the right, regardless of H2.
        h2 = tuple(Q(index - 4, index + 2) for index in range(ROOT_DIM))
        left = root_source_tensor(matrix_scale(-1, e00), bar_t0)
        right = root_source_tensor(matrix_scale(-1 / lam, h2), bar_t2)
        t0_position = next(index for index, entry in enumerate(bar_t0) if entry)
        assert bar_t0[t0_position] == 1 and bar_t2[t0_position] == 0
        left_t0_matrix = tuple(
            left[root_index * len(bar_t0) + t0_position]
            for root_index in range(ROOT_DIM)
        )
        right_t0_matrix = tuple(
            right[root_index * len(bar_t0) + t0_position]
            for root_index in range(ROOT_DIM)
        )
        assert left_t0_matrix == matrix_scale(-1, e00)
        assert right_t0_matrix == zero(ROOT_DIM)
        assert left != right


def tangent_matrix(a: Vector, b: Vector, x: Vector, y: Vector) -> Matrix:
    return matrix_add(outer(a, y), matrix_scale(-1, outer(x, b)))


def tangent_kernel_columns(x: Vector, y: Vector) -> tuple[Vector, ...]:
    columns: list[Vector] = []
    for index in range(DIM):
        columns.append(tangent_matrix(unit(DIM, index), zero(DIM), x, y))
    for index in range(DIM):
        columns.append(tangent_matrix(zero(DIM), unit(DIM, index), x, y))
    return tuple(columns)


def contract_rows(coefficients: Vector, rows: tuple[Vector, ...]) -> Vector:
    return tuple(
        sum(
            (
                coefficients[index] * rows[index][coordinate]
                for index in range(DIM)
            ),
            Q(0),
        )
        for coordinate in range(len(rows[0]))
    )


def graph_rows(
    shared: Vector,
    first_lift: Vector,
    second_lift: Vector,
    third_lift: Vector,
) -> tuple[Vector, ...]:
    return tuple(
        (
            shared[index],
            first_lift[index],
            second_lift[index],
            third_lift[index],
        )
        for index in range(DIM)
    )


def check_final_cell_full_matrix_gauge_and_rank() -> None:
    pair = (0b101, 0b101)
    lam = Q(-29, 8)
    x = representative(pair[0], "x")
    y = representative(pair[1], "y")
    data = t1_cross_data(pair)
    check_cross_pair_cube(pair, data, lam)
    _, c, _, d = data

    rho = x[2] * y[2] / (x[0] * y[0])
    assert rho != 0
    coefficients = cube_coefficients(c, d, lam)
    common_correction = lam * x[0] * y[0]
    assert coefficients == (
        (x[2] * y[2], common_correction),
        (Q(0), common_correction),
        (x[0] * y[0], common_correction),
    )

    bar_t0 = quotient_target(0, 1)
    bar_t2 = quotient_target(2, 1)
    assert column_rank((bar_t0, bar_t2)) == 2
    bar_s0 = scale(-rho / lam, bar_t0)
    bar_s1 = zero(len(bar_t0))
    bar_s2 = scale(-1 / lam, bar_t2)
    assert add(
        scale(coefficients[0][0], bar_t0),
        scale(coefficients[0][1], bar_s0),
    ) == zero(len(bar_t0))
    assert scale(coefficients[1][1], bar_s1) == zero(len(bar_t0))
    assert add(
        scale(coefficients[2][0], bar_t2),
        scale(coefficients[2][1], bar_s2),
    ) == zero(len(bar_t0))

    e00 = unit(ROOT_DIM, 0)
    kappa = matrix_scale(lam / rho, e00)
    h2 = zero(ROOT_DIM)
    left = root_source_tensor(matrix_scale(-1, e00), bar_t0)
    right = add(
        root_source_tensor(kappa, bar_s0),
        root_source_tensor(h2, bar_s2),
    )
    assert left == right

    # Independence of bar(T0),bar(T2) makes these the unique matrix
    # coefficients forced by the quotient of the complete unsliced slice.
    assert matrix_scale(-1, e00) == matrix_scale(-rho / lam, kappa)
    assert zero(ROOT_DIM) == matrix_scale(-1 / lam, h2)

    # The exact tangent kernel has dimension one and is generated by (x,y).
    # Thus H2=0 permits the graph gauge a2=b2=0.
    tangent_columns = tangent_kernel_columns(x, y)
    assert column_rank(tangent_columns) == 5
    assert not any(tangent_matrix(x, y, x, y))
    for scalar in (Q(-7, 3), Q(0), Q(11, 5)):
        a2 = scale(scalar, x)
        b2 = scale(scalar, y)
        assert not any(tangent_matrix(a2, b2, x, y))
        assert add(a2, scale(-scalar, x)) == zero(DIM)
        assert add(b2, scale(-scalar, y)) == zero(DIM)

    # After that gauge, the restrictions of both injective root-row maps to
    # x^perp and y^perp lie in G=<q0,q1> and have rank two, hence R=P=G.
    a0, a1 = (Q(0), Q(1), Q(0)), (Q(1), Q(0), Q(0))
    b0, b1 = (Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0))
    r_rows = graph_rows(x, a0, a1, zero(DIM))
    p_rows = graph_rows(y, b0, b1, zero(DIM))
    assert column_rank(r_rows) == column_rank(p_rows) == 3
    alpha_basis = (unit(DIM, 1), (x[2], Q(0), -x[0]))
    beta_basis = (unit(DIM, 1), (y[2], Q(0), -y[0]))
    r_plane = tuple(contract_rows(alpha, r_rows) for alpha in alpha_basis)
    p_plane = tuple(contract_rows(beta, p_rows) for beta in beta_basis)
    assert column_rank(r_plane) == column_rank(p_plane) == 2
    assert all(row[0] == row[3] == 0 for row in (*r_plane, *p_plane))
    assert column_rank((*r_plane, *p_plane)) == 2

    # Once the analytic zero-pair classification identifies G as a split
    # two-source plane, every permanent of r1,p1,q1 in G is zero, while the
    # retained complete face requires P111=T1.
    first_line = line_row(0, 1)
    second_line = line_row(1, 1)
    r_1 = add(first_line, scale(Q(2), second_line))
    p_1 = add(scale(Q(-3), first_line), second_line)
    q_1 = add(scale(Q(5), first_line), scale(Q(7), second_line))
    assert not any(permanent(r_1, p_1, q_1))
    assert any(target(1))


def check_all_cross_cells(partition: dict[str, set[MaskPair]]) -> None:
    lam = Q(31, 12)
    for pair in sorted(partition["t0_cross"] | {(0b010, 0b010)}, reverse=True):
        visible = check_cross_pair_cube(pair, t0_cross_data(pair), lam)
        assert visible != 0 and visible_colour(pair) == 0

    for pair in sorted(
        partition["t1_e0_shore"] | {(0b001, 0b001)} | partition["final"],
        reverse=True,
    ):
        visible = check_cross_pair_cube(pair, t1_cross_data(pair), lam)
        assert visible != 0 and visible_colour(pair) == 1


def main() -> None:
    partition = check_support_partition()
    check_retained_indices_and_source_recovery()
    check_e0_shore_source_identities()
    check_radical_shores(partition["radical"])
    check_all_cross_cells(partition)
    check_incidence_quotient_interfaces()
    check_same_t0_equal_plane_retained_faces()
    check_t1_source_and_unsliced_contradiction(
        partition["t1_e0_shore"], include_same=True
    )
    check_final_cell_full_matrix_gauge_and_rank()

    family_summary = ", ".join(
        f"{name}={len(cells)}" for name, cells in partition.items()
    )
    print(f"one-visible support partition ({family_summary}): PASS")
    print("all radical-shore and cross-pair cube coefficients: PASS")
    print("sixteen retained face indices and source-recovery signs: PASS")
    print("split-Q/common-split-plane quotient interfaces: PASS")
    print("T1 shore unsliced source separation: PASS")
    print("final 101x101 full-matrix, graph-gauge, and rank interfaces: PASS")
    print("S2CG zero-pair/radical classification remains analytic proof input")
    print("scope: exact complete one-visible diagonal coordinate-endpoint atlas")


if __name__ == "__main__":
    main()
