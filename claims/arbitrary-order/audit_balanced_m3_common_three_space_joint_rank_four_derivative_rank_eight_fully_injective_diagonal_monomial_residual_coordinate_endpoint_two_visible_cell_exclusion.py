#!/usr/bin/env python3
"""Independent Fraction audit of the diagonal two-visible-cell exclusion.

This standard-library-only replay traverses the colour masks,
source-coordinate triples, permanent summands, and chart rows in orders
reversed from the primary replay.  It
independently reconstructs the fourteen two-visible masks, checks the four
mixed-map covector pairs, and checks the zero corner and the two named
correction-free rank-one corners in each of the other ten masks.  Separate
``Fraction`` fixtures replay the coefficient and rank interfaces in the
two-transverse mixed-map lemma and in both branches of the zero-corner
rectangle lemma.

The source-support classifications are analytic inputs of the owning
theorem.  In particular, this script does not replace the tangent/secant
argument in the mixed-map lemma or S2CG's classification of independent and
dependent zero pairs.  It checks their exact finite-dimensional interfaces
and imports no primary verifier, SymPy, or solver.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Q = Fraction
COLOUR_DIM = 3
FACTOR_DIM = 2
COLOURS = tuple(reversed(range(COLOUR_DIM)))
FACTOR_INDICES = tuple(reversed(range(FACTOR_DIM)))
SOURCE_TRIPLES = tuple(product(FACTOR_INDICES, repeat=3))
PERMUTATIONS = tuple(reversed(tuple(permutations(range(3)))))

Vector = tuple[Q, ...]
MaskPair = tuple[int, int]
Corner = tuple[str, int]


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


def dot(left: Vector, right: Vector) -> Q:
    return sum(
        (first * second for first, second in zip(left, right, strict=True)),
        Q(0),
    )


def column_rank(columns: tuple[Vector, ...] | list[Vector]) -> int:
    if not columns:
        return 0
    row_count = len(columns[0])
    assert all(len(column) == row_count for column in columns)
    matrix = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in reversed(range(len(columns))):
        pivot = next(
            (
                candidate
                for candidate in reversed(range(pivot_row, row_count))
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for candidate in reversed(range(row_count)):
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


def support(vector: Vector) -> int:
    return sum(1 << index for index, entry in enumerate(vector) if entry)


def has_colour(mask: int, colour: int) -> bool:
    return bool(mask & (1 << colour))


def representative(mask: int, side: str) -> Vector:
    weights = {
        "x": (Q(-7, 3), Q(11, 5), Q(13, 2)),
        "y": (Q(17, 7), Q(-19, 11), Q(23, 13)),
    }[side]
    result = tuple(
        weights[colour] if has_colour(mask, colour) else Q(0)
        for colour in range(COLOUR_DIM)
    )
    assert support(result) == mask
    return result


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


def cross_covector(vector: Vector, first: int, second: int) -> Vector:
    result = [Q(0)] * COLOUR_DIM
    result[first] = vector[second]
    result[second] = -vector[first]
    covector = tuple(result)
    assert dot(covector, vector) == 0
    return covector


def v01(vector: Vector) -> Vector:
    return cross_covector(vector, 0, 1)


def v02(vector: Vector) -> Vector:
    return cross_covector(vector, 0, 2)


def v12(vector: Vector) -> Vector:
    return cross_covector(vector, 1, 2)


def cube_columns(alpha: Vector, beta: Vector, lam: Q) -> tuple[Vector, ...]:
    """Return columns in the reversed basis S2,S1,S0,T2,T1,T0."""
    columns = []
    for colour in COLOURS:
        column = [Q(0)] * (2 * COLOUR_DIM)
        column[COLOURS.index(colour)] = lam * alpha[2] * beta[2]
        column[COLOUR_DIM + COLOURS.index(colour)] = (
            alpha[colour] * beta[colour]
        )
        columns.append(tuple(column))
    return tuple(columns)


def cube_target_coefficients(alpha: Vector, beta: Vector) -> Vector:
    return tuple(alpha[colour] * beta[colour] for colour in range(COLOUR_DIM))


def correction_coefficient(alpha: Vector, beta: Vector, lam: Q) -> Q:
    return lam * alpha[2] * beta[2]


def is_zero_cube_map(alpha: Vector, beta: Vector, lam: Q) -> bool:
    return column_rank(cube_columns(alpha, beta, lam)) == 0


def check_rank_one_target_map(
    alpha: Vector,
    beta: Vector,
    colour: int,
    lam: Q,
) -> None:
    coefficients = cube_target_coefficients(alpha, beta)
    assert coefficients[colour] != 0
    assert all(
        coefficient == 0
        for index, coefficient in enumerate(coefficients)
        if index != colour
    )
    assert correction_coefficient(alpha, beta, lam) == 0
    assert column_rank(cube_columns(alpha, beta, lam)) == 1


def two_visible_masks() -> tuple[MaskPair, ...]:
    masks = tuple(reversed((0b001, 0b010, 0b011, 0b101, 0b110, 0b111)))
    cells = tuple(
        pair
        for pair in reversed(tuple(product(masks, repeat=2)))
        if target_visibility(pair) == (True, True)
    )
    assert len(cells) == len(set(cells)) == 14
    return cells


def boundary_data(
    pair: MaskPair,
    x: Vector,
    y: Vector,
) -> tuple[Vector, Vector, Vector, Vector, tuple[Corner, Corner]]:
    e0, e1, e2 = (unit(COLOUR_DIM, index) for index in range(COLOUR_DIM))
    table: dict[
        MaskPair,
        tuple[Vector, Vector, Vector, Vector, tuple[Corner, Corner]],
    ] = {
        (0b011, 0b101): (e2, v01(x), e1, v02(y), (("Ad", 1), ("AB", 0))),
        (0b011, 0b110): (e2, v01(x), e0, v12(y), (("Ad", 0), ("AB", 1))),
        (0b101, 0b011): (e1, v02(x), e2, v01(y), (("cB", 1), ("AB", 0))),
        (0b110, 0b011): (e0, v12(x), e2, v01(y), (("cB", 0), ("AB", 1))),
        (0b101, 0b110): (e1, v02(x), e0, v12(y), (("Ad", 0), ("cB", 1))),
        (0b110, 0b101): (e0, v12(x), e1, v02(y), (("Ad", 1), ("cB", 0))),
        (0b101, 0b111): (
            e1,
            v02(x),
            v02(y),
            v01(y),
            (("cB", 1), ("AB", 0)),
        ),
        (0b110, 0b111): (
            e0,
            v12(x),
            v12(y),
            v01(y),
            (("cB", 0), ("AB", 1)),
        ),
        (0b111, 0b101): (
            v02(x),
            v01(x),
            e1,
            v02(y),
            (("Ad", 1), ("AB", 0)),
        ),
        (0b111, 0b110): (
            v12(x),
            v01(x),
            e0,
            v12(y),
            (("Ad", 0), ("AB", 1)),
        ),
    }
    return table[pair]


def check_support_atlas_and_cube() -> tuple[set[MaskPair], set[MaskPair]]:
    cells = set(two_visible_masks())
    central = {
        pair
        for pair in cells
        if pair[0] in {0b011, 0b111} and pair[1] in {0b011, 0b111}
    }
    boundary = cells - central
    assert len(central) == 4
    assert len(boundary) == 10
    assert cells == {
        pair
        for pair in product((0b011, 0b101, 0b110, 0b111), repeat=2)
        if pair not in {(0b101, 0b101), (0b110, 0b110)}
    }

    lam = Q(-31, 17)
    for pair in sorted(central, reverse=True):
        x = representative(pair[0], "x")
        y = representative(pair[1], "y")
        alpha, beta = v01(x), v01(y)
        assert alpha[2] == beta[2] == 0
        assert cube_target_coefficients(alpha, beta) == (
            x[1] * y[1],
            x[0] * y[0],
            Q(0),
        )
        assert correction_coefficient(alpha, beta, lam) == 0
        assert column_rank(cube_columns(alpha, beta, lam)) == 2

    for pair in sorted(boundary, reverse=True):
        x = representative(pair[0], "x")
        y = representative(pair[1], "y")
        c, a_row, d, b_row, corners = boundary_data(pair, x, y)
        assert dot(c, x) == dot(a_row, x) == 0
        assert dot(d, y) == dot(b_row, y) == 0
        assert column_rank((c, a_row)) == column_rank((d, b_row)) == 2
        assert is_zero_cube_map(c, d, lam)

        corner_rows = {
            "Ad": (a_row, d),
            "cB": (c, b_row),
            "AB": (a_row, b_row),
        }
        seen_colours = set()
        for name, colour in reversed(corners):
            first, second = corner_rows[name]
            check_rank_one_target_map(first, second, colour, lam)
            seen_colours.add(colour)
        assert seen_colours == {0, 1}

    return central, boundary


def source_position(index: tuple[int, int, int]) -> int:
    return SOURCE_TRIPLES.index(index)


def tensor_from_factors(x_part: Vector, y_part: Vector, z_part: Vector) -> Vector:
    return tuple(
        x_part[i] * y_part[j] * z_part[k] for i, j, k in SOURCE_TRIPLES
    )


def pure_row(source: int, factor: Vector) -> Vector:
    blocks = [zero(FACTOR_DIM), zero(FACTOR_DIM), zero(FACTOR_DIM)]
    blocks[source] = factor
    return tuple(entry for block in blocks for entry in block)


def split_row(row: Vector) -> tuple[Vector, Vector, Vector]:
    assert len(row) == 3 * FACTOR_DIM
    return (
        row[:FACTOR_DIM],
        row[FACTOR_DIM : 2 * FACTOR_DIM],
        row[2 * FACTOR_DIM :],
    )


def permanent(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = [Q(0)] * len(SOURCE_TRIPLES)
    for permutation in PERMUTATIONS:
        x_part = split_row(rows[permutation[0]])[0]
        y_part = split_row(rows[permutation[1]])[1]
        z_part = split_row(rows[permutation[2]])[2]
        for index in SOURCE_TRIPLES:
            i, j, k = index
            result[source_position(index)] += (
                x_part[i] * y_part[j] * z_part[k]
            )
    return tuple(result)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def alternating(first: Vector, second: Vector, third: Vector) -> Vector:
    rows = first, second, third
    result = zero(len(SOURCE_TRIPLES))
    for permutation in PERMUTATIONS:
        x_part = split_row(rows[permutation[0]])[0]
        y_part = split_row(rows[permutation[1]])[1]
        z_part = split_row(rows[permutation[2]])[2]
        term = tensor_from_factors(x_part, y_part, z_part)
        result = add(result, scale(permutation_sign(permutation), term))
    return result


def contract_factor(tensor: Vector, factor: int, covector: Vector) -> Vector:
    remaining = tuple(index for index in range(3) if index != factor)
    result = []
    for pair in product(FACTOR_INDICES, repeat=2):
        value = Q(0)
        for coordinate in FACTOR_INDICES:
            index = [0, 0, 0]
            index[factor] = coordinate
            index[remaining[0]] = pair[0]
            index[remaining[1]] = pair[1]
            value += covector[coordinate] * tensor[source_position(tuple(index))]
        result.append(value)
    return tuple(result)


def line_annihilator(vector: Vector) -> Vector:
    assert len(vector) == 2 and any(vector)
    return vector[1], -vector[0]


def lies_in_factor_line(tensor: Vector, factor: int, line: Vector) -> bool:
    return not any(contract_factor(tensor, factor, line_annihilator(line)))


def map_columns(first: Vector, second: Vector, basis: tuple[Vector, ...]) -> tuple[Vector, ...]:
    return tuple(permanent(first, second, vector) for vector in basis)


def tensor_mode_rank(tensor: Vector, factor: int) -> int:
    other = tuple(index for index in range(3) if index != factor)
    columns = []
    for pair in product(FACTOR_INDICES, repeat=2):
        column = []
        for coordinate in FACTOR_INDICES:
            index = [0, 0, 0]
            index[factor] = coordinate
            index[other[0]] = pair[0]
            index[other[1]] = pair[1]
            column.append(tensor[source_position(tuple(index))])
        columns.append(tuple(column))
    return column_rank(columns)


def in_coordinate_support(tensor: Vector, predicate: object) -> bool:
    assert callable(predicate)
    return all(
        not coefficient or predicate(index)
        for index, coefficient in zip(SOURCE_TRIPLES, tensor, strict=True)
    )


def hyperdeterminant_222(tensor: Vector) -> Q:
    def entry(i: int, j: int, k: int) -> Q:
        return tensor[source_position((i, j, k))]

    a000 = entry(0, 0, 0)
    a001 = entry(0, 0, 1)
    a010 = entry(0, 1, 0)
    a011 = entry(0, 1, 1)
    a100 = entry(1, 0, 0)
    a101 = entry(1, 0, 1)
    a110 = entry(1, 1, 0)
    a111 = entry(1, 1, 1)
    squares = (
        a000 * a000 * a111 * a111
        + a001 * a001 * a110 * a110
        + a010 * a010 * a101 * a101
        + a100 * a100 * a011 * a011
    )
    crosses = (
        a000 * a001 * a110 * a111
        + a000 * a010 * a101 * a111
        + a000 * a100 * a011 * a111
        + a001 * a010 * a101 * a110
        + a001 * a100 * a011 * a110
        + a010 * a100 * a011 * a101
    )
    corners = a000 * a011 * a101 * a110 + a001 * a010 * a100 * a111
    return squares - 2 * crosses + 4 * corners


def check_hyperdeterminant_interface() -> None:
    e0, e1 = (unit(FACTOR_DIM, index) for index in range(FACTOR_DIM))
    t000 = tensor_from_factors(e0, e0, e0)
    t100 = tensor_from_factors(e1, e0, e0)
    t011 = tensor_from_factors(e0, e1, e1)
    t111 = tensor_from_factors(e1, e1, e1)
    samples = (Q(-5, 3), Q(-1), Q(0), Q(7, 4))
    for coefficients in reversed(tuple(product(samples, repeat=4))):
        base, x_step, y_step, z_step = coefficients
        tangent = add(
            scale(base, t000),
            scale(x_step, t100),
            scale(y_step, tensor_from_factors(e0, e1, e0)),
            scale(z_step, tensor_from_factors(e0, e0, e1)),
        )
        assert hyperdeterminant_222(tangent) == 0

    nonzero = (Q(-7, 5), Q(11, 6))
    for left, right in reversed(tuple(product(nonzero, repeat=2))):
        assert hyperdeterminant_222(add(scale(left, t000), scale(right, t111))) == (
            left * right
        ) ** 2
        assert hyperdeterminant_222(add(scale(left, t100), scale(right, t011))) == (
            left * right
        ) ** 2


def check_mixed_map_support_interfaces() -> None:
    e0, e1 = (unit(FACTOR_DIM, index) for index in range(FACTOR_DIM))
    x = pure_row(0, e0)
    y = pure_row(1, e0)
    z = pure_row(2, e0)
    t = tensor_from_factors(e0, e0, e0)

    # A pure first row fixes one source factor in every mixed value.
    pure_u = x
    pure_v = add(pure_row(0, e1), y, z)
    pure_q = add(x, pure_row(1, e1), pure_row(2, e1))
    pure_basis = (pure_u, pure_v, pure_q)
    assert column_rank(pure_basis) == 3
    assert all(
        lies_in_factor_line(value, 0, e0)
        for value in map_columns(pure_u, pure_v, pure_basis)
    )

    # Two-source u and v_Z=0 give one fixed X-Y matrix tensored with q_Z.
    two_u = add(x, y)
    two_v = add(pure_row(0, e1), pure_row(1, add(e0, e1)))
    q = add(pure_row(0, scale(Q(2), e1)), pure_row(2, e0))
    two_basis = (two_u, two_v, q)
    assert column_rank(two_basis) == 3
    assert not any(permanent(two_u, two_v, two_u))
    fixed_xy = add(
        tensor_from_factors(e0, add(e0, e1), e0),
        tensor_from_factors(e1, e0, e0),
    )
    expected = tuple(
        coefficient if index[2] == 0 else Q(0)
        for index, coefficient in zip(SOURCE_TRIPLES, fixed_xy, strict=True)
    )
    assert permanent(two_u, two_v, q) == expected
    assert tensor_mode_rank(expected, 0) == tensor_mode_rank(expected, 1) == 2

    parallel_v = add(scale(Q(2), x), scale(Q(-3), y))
    parallel_value = permanent(two_u, parallel_v, z)
    assert parallel_value == scale(Q(-1), t)
    assert all(tensor_mode_rank(parallel_value, factor) == 1 for factor in range(3))

    # If v_Z is a nonzero endpoint line and v_X,v_Y are the base lines,
    # the mixed image lies in the Segre tangent support at x*y*z.
    endpoint_v = add(scale(Q(2, 3), x), scale(Q(-5, 7), y), z)
    generic_q = add(
        pure_row(0, e1),
        scale(Q(3, 2), pure_row(1, e1)),
        scale(Q(-4, 5), pure_row(2, e1)),
    )
    endpoint_basis = (two_u, endpoint_v, generic_q)
    assert column_rank(endpoint_basis) == 3
    assert permanent(two_u, endpoint_v, two_u) == scale(2, t)
    assert permanent(two_u, endpoint_v, endpoint_v) == scale(Q(-2, 21), t)
    assert all(
        in_coordinate_support(value, lambda index: sum(index) <= 1)
        for value in map_columns(two_u, endpoint_v, endpoint_basis)
    )

    # Full-support square-zero branch: a+b+c=0 is exactly the kernel
    # coefficient and all mixed values retain the same tangent support.
    full_u = add(x, y, z)
    a, b, c = Q(2, 3), Q(-5, 4), Q(7, 12)
    assert a + b + c == 0
    full_v = add(scale(a, x), scale(b, y), scale(c, z))
    full_q = add(
        pure_row(0, e1),
        scale(Q(-3, 2), pure_row(1, e1)),
        scale(Q(5, 7), pure_row(2, e1)),
    )
    full_basis = (full_u, full_v, full_q)
    assert column_rank(full_basis) == 3
    assert not any(permanent(full_u, full_u, full_v))
    assert all(
        in_coordinate_support(value, lambda index: sum(index) <= 1)
        for value in map_columns(full_u, full_v, full_basis)
    )

    # Full-support endpoint branch: an endpoint sharing the Y,Z lines with
    # the base leaves the entire mixed image in the union of those shores.
    endpoint_full_v = scale(Q(1, 2), pure_row(0, e1))
    endpoint = tensor_from_factors(e1, e0, e0)
    transverse = tensor_from_factors(e0, e1, e1)
    endpoint_full_basis = (full_u, endpoint_full_v, full_q)
    assert column_rank(endpoint_full_basis) == 3
    assert permanent(full_u, full_u, endpoint_full_v) == endpoint
    assert all(
        in_coordinate_support(value, lambda index: index[1] == 0 or index[2] == 0)
        for value in map_columns(full_u, endpoint_full_v, endpoint_full_basis)
    )
    assert not in_coordinate_support(
        transverse, lambda index: index[1] == 0 or index[2] == 0
    )
    assert all(
        column_rank((left, right)) == 2
        for left, right in zip(
            (e1, e0, e0),
            (e0, e1, e1),
            strict=True,
        )
    )


def check_independent_zero_pair_interface() -> None:
    e0 = unit(FACTOR_DIM, 0)
    x = pure_row(0, e0)
    y = pure_row(1, e0)
    z = pure_row(2, add(e0, scale(Q(2), unit(FACTOR_DIM, 1))))
    q_basis = (x, y, z)
    c = add(x, y)
    d = add(x, scale(-1, y))
    a_row = z
    b_row = z
    assert column_rank(q_basis) == 3
    assert any(alternating(*q_basis))
    assert column_rank((c, a_row)) == column_rank((d, b_row)) == 2
    assert all(not any(value) for value in map_columns(c, d, q_basis))

    z_projections = tuple(split_row(row)[2] for row in q_basis)
    assert column_rank(z_projections) == 1
    for rows in reversed(tuple(product(q_basis, repeat=3))):
        assert lies_in_factor_line(permanent(*rows), 2, split_row(z)[2])

    ad_columns = map_columns(a_row, d, q_basis)
    cb_columns = map_columns(c, b_row, q_basis)
    assert column_rank(ad_columns) == column_rank(cb_columns) == 1
    assert all(
        lies_in_factor_line(value, 2, split_row(z)[2])
        for value in (*ad_columns, *cb_columns)
    )


def check_dependent_zero_pair_interfaces() -> None:
    e0, e1 = (unit(FACTOR_DIM, index) for index in range(FACTOR_DIM))
    x = pure_row(0, e0)
    y = pure_row(1, e0)
    z = pure_row(2, e0)
    split_basis = (x, y, z)
    assert any(alternating(*split_basis))
    assert all(not any(value) for value in map_columns(x, x, split_basis))

    # The two corners adjacent to a pure zero corner have the same fixed
    # source factor, even when both maps are nonzero and rank one.
    a_adjacent = add(y, z)
    b_adjacent = add(scale(Q(2), y), scale(Q(-3), z))
    first_adjacent = map_columns(a_adjacent, x, split_basis)
    second_adjacent = map_columns(x, b_adjacent, split_basis)
    assert column_rank(first_adjacent) == column_rank(second_adjacent) == 1
    assert all(
        lies_in_factor_line(value, 0, e0)
        for value in (*first_adjacent, *second_adjacent)
    )

    # Mixed orientation with A_Y=a and A_Z=b both nonzero.  The common
    # value vanishes exactly when B_Y=t*a and B_Z=-t*b.  Both resulting
    # maps are rank one in this independent exact fixture.
    a_row = add(y, z)
    t = Q(3)
    b_row = add(scale(Q(2), x), scale(t, y), scale(-t, z))
    q_basis = (x, a_row, b_row)
    assert column_rank(q_basis) == 3
    assert any(alternating(*q_basis))
    assert column_rank((x, a_row)) == column_rank((x, b_row)) == 2
    f_columns = map_columns(a_row, x, q_basis)
    h_columns = map_columns(a_row, b_row, q_basis)
    common = permanent(a_row, x, b_row)
    assert not any(common)
    assert column_rank(f_columns) == column_rank(h_columns) == 1
    assert all(
        in_coordinate_support(value, lambda index: index[1] == 0 or index[2] == 0)
        for value in h_columns
    )
    assert all(
        lies_in_factor_line(value, 1, e0)
        and lies_in_factor_line(value, 2, e0)
        for value in f_columns
    )

    # a=0, b!=0: rank(F)=1 is exactly the one-line Y projection.  The
    # common-value equation makes B_Y=0 and H retains that same Y line.
    a_zero = z
    b_zero_case = add(z, scale(Q(5, 2), x))
    a_zero_basis = (x, a_zero, y)
    assert any(alternating(*a_zero_basis))
    assert column_rank(tuple(split_row(row)[1] for row in a_zero_basis)) == 1
    assert not any(permanent(a_zero, x, b_zero_case))
    f_zero = map_columns(a_zero, x, a_zero_basis)
    h_zero = map_columns(a_zero, b_zero_case, a_zero_basis)
    assert column_rank(f_zero) == column_rank(h_zero) == 1
    assert all(lies_in_factor_line(value, 1, e0) for value in (*f_zero, *h_zero))

    # b=0, a!=0 is the Y/Z source-exchanged one-line Z projection branch.
    b_zero = y
    a_zero_case = add(y, scale(Q(-7, 3), x))
    b_zero_basis = (x, b_zero, z)
    assert any(alternating(*b_zero_basis))
    assert column_rank(tuple(split_row(row)[2] for row in b_zero_basis)) == 1
    assert not any(permanent(b_zero, x, a_zero_case))
    f_symmetric = map_columns(b_zero, x, b_zero_basis)
    h_symmetric = map_columns(b_zero, a_zero_case, b_zero_basis)
    assert column_rank(f_symmetric) == column_rank(h_symmetric) == 1
    assert all(
        lies_in_factor_line(value, 2, e0)
        for value in (*f_symmetric, *h_symmetric)
    )

    # If both A_Y and A_Z vanish, the allegedly nonzero first map is zero.
    pure_other_x = pure_row(0, e1)
    assert all(
        not any(value) for value in map_columns(pure_other_x, x, split_basis)
    )


def main() -> None:
    central, boundary = check_support_atlas_and_cube()
    check_hyperdeterminant_interface()
    check_mixed_map_support_interfaces()
    check_independent_zero_pair_interface()
    check_dependent_zero_pair_interfaces()

    print(f"two-visible support atlas central={len(central)}, boundary={len(boundary)}: PASS")
    print("four mixed-map and ten zero-corner cube charts: PASS")
    print("mixed-map support, tangent, and hyperdeterminant interfaces: PASS")
    print("independent/dependent zero-corner rank interfaces: PASS")
    print("analytic support classification remains owned by the written theorem")
    print("scope: exact diagonal coordinate-endpoint two-visible cell")


if __name__ == "__main__":
    main()
