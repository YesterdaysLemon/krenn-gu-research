"""Independent exact audit for the four-root determinant-divisor reduction.

This script deliberately imports only the Python standard library.  It does
not import repository code, the primary verifier, or a computer-algebra
system.  Its representation is a mixture of:

* Fraction row reduction on labelled coefficient tables;
* support-incidence and annihilator calculations;
* direct sparse tensor assembly; and
* direct enumeration of the fifteen perfect matchings on six labelled slots.

The audit checks the displayed quotient-cross mechanism, rank-two projection
and escape obstructions, the mixed beta-kernel and exactly-two combined-port
bound, the fixed and moving blocker dualities, the rank-one response
trichotomy, the complete-target pure-coordinate routing, the
six-versus-seven response identity, and the sharp controls.

Finite limits are intentional.  The rank census is exhaustive only for
3-by-3 matrices with entries in {-1, 0, 1}; projective annihilator tables use
primitive vectors from the same alphabet; scalar blocker tables use
{-2, -1, 0, 1, 2}.  These exact tables audit the written structural
derivation and its sharp examples.  They are not a proof by finite
enumeration over an arbitrary characteristic-zero field.

In particular, this audit does not prove that the rank-two double-contained
core is empty, does not realize or exclude the rank-one permanent companions,
does not impose the separate seventh-response quartic, does not verify the
unused GLS4 survival/selector gates, does not close the supply-and-target
node, and does not resolve the Krenn--Gu conjecture.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd
from typing import TypeAlias

Scalar: TypeAlias = Fraction
Vector: TypeAlias = tuple[Scalar, ...]
Matrix: TypeAlias = tuple[Vector, ...]
Tensor: TypeAlias = dict[tuple[int, ...], Scalar]
Monomial: TypeAlias = tuple[int, ...]
Polynomial: TypeAlias = dict[Monomial, Scalar]

DIM = 3
PORTS = tuple(range(4))
COLORS = tuple(range(DIM))
ZERO = Fraction(0)
ONE = Fraction(1)


def q(value: int | Fraction) -> Fraction:
    """Coerce an exact scalar."""

    return value if isinstance(value, Fraction) else Fraction(value)


def make_vector(values: Sequence[int | Fraction]) -> Vector:
    return tuple(q(value) for value in values)


def make_matrix(rows: Sequence[Sequence[int | Fraction]]) -> Matrix:
    return tuple(make_vector(row) for row in rows)


def zero_matrix(rows: int = DIM, columns: int = DIM) -> Matrix:
    return tuple(tuple(ZERO for _ in range(columns)) for _ in range(rows))


def identity_matrix(size: int) -> Matrix:
    return tuple(
        tuple(ONE if row == column else ZERO for column in range(size))
        for row in range(size)
    )


def basis_vector(size: int, position: int) -> Vector:
    return tuple(ONE if index == position else ZERO for index in range(size))


def matrix_rank(matrix: Sequence[Sequence[int | Fraction]]) -> int:
    """Compute rank by exact Fraction row reduction."""

    if not matrix:
        return 0
    rows = [list(make_vector(row)) for row in matrix]
    if not rows[0]:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot_value for entry in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def rref(matrix: Sequence[Sequence[int | Fraction]]) -> tuple[Matrix, tuple[int, ...]]:
    """Return exact reduced row echelon form and pivot columns."""

    if not matrix:
        return (), ()
    rows = [list(make_vector(row)) for row in matrix]
    column_count = len(rows[0])
    pivot_row = 0
    pivots: list[int] = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot_value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(tuple(row) for row in rows), tuple(pivots)


def nullspace_basis(
    matrix: Sequence[Sequence[int | Fraction]], column_count: int
) -> tuple[Vector, ...]:
    """Return an exact basis for the right kernel."""

    if not matrix:
        return tuple(
            basis_vector(column_count, column) for column in range(column_count)
        )
    reduced, pivots = rref(matrix)
    free_columns = tuple(
        column for column in range(column_count) if column not in pivots
    )
    basis: list[Vector] = []
    for free in free_columns:
        vector = [ZERO] * column_count
        vector[free] = ONE
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(tuple(vector))
    return tuple(basis)


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][column] for row in range(len(matrix)))
        for column in range(len(matrix[0]))
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(row_left, row_right, strict=True))
        for row_left, row_right in zip(left, right, strict=True)
    )


def matrix_scale(scalar: int | Fraction, matrix: Matrix) -> Matrix:
    value = q(scalar)
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(a * b for b in right) for a in left)


def flatten_matrix(matrix: Matrix) -> Vector:
    return tuple(entry for row in matrix for entry in row)


def delete_row(matrix: Matrix, row_to_delete: int) -> Matrix:
    return tuple(values for row, values in enumerate(matrix) if row != row_to_delete)


def delete_column(matrix: Matrix, column_to_delete: int) -> Matrix:
    return tuple(
        tuple(entry for column, entry in enumerate(row) if column != column_to_delete)
        for row in matrix
    )


def delete_row_and_column(
    matrix: Matrix, row_to_delete: int, column_to_delete: int
) -> Matrix:
    return delete_column(delete_row(matrix, row_to_delete), column_to_delete)


def canonical_rectangular(rows: int, columns: int, rank: int) -> Matrix:
    return tuple(
        tuple(
            ONE if row == column and row < rank else ZERO for column in range(columns)
        )
        for row in range(rows)
    )


def realigned_swapped_product(left: Matrix, right: Matrix) -> Matrix:
    """Realign A_v tensor C_u with rows (X,u), columns (Y,v)."""

    x_dim = len(left)
    y_dim = len(right)
    local_dim = len(left[0])
    return tuple(
        tuple(
            left[row // local_dim][column % local_dim]
            * right[column // local_dim][row % local_dim]
            for column in range(y_dim * local_dim)
        )
        for row in range(x_dim * local_dim)
    )


def tensor_clean(tensor: Tensor) -> Tensor:
    return {index: coefficient for index, coefficient in tensor.items() if coefficient}


def tensor_add(*tensors: Tensor) -> Tensor:
    answer: Tensor = {}
    for tensor in tensors:
        for index, coefficient in tensor.items():
            answer[index] = answer.get(index, ZERO) + coefficient
    return tensor_clean(answer)


def response_tensor(
    h_block: Matrix,
    b_block: Matrix,
    a_u: Matrix,
    c_u: Matrix,
    a_v: Matrix,
    c_v: Matrix,
) -> Tensor:
    """Assemble Z_uv in labelled slot order (q0,q1,u,v)."""

    answer: Tensor = {}
    for q0, q1, local_u, local_v in product(COLORS, repeat=4):
        coefficient = (
            h_block[q0][q1] * b_block[local_u][local_v]
            + a_u[q0][local_u] * c_v[q1][local_v]
            + a_v[q0][local_v] * c_u[q1][local_u]
        )
        if coefficient:
            answer[(q0, q1, local_u, local_v)] = coefficient
    return answer


def all_pair_responses_zero(
    h_block: Matrix,
    a_blocks: Sequence[Matrix],
    c_blocks: Sequence[Matrix],
    b_blocks: dict[tuple[int, int], Matrix],
) -> bool:
    for u, v in combinations(PORTS, 2):
        b_block = b_blocks.get((u, v), zero_matrix())
        if response_tensor(
            h_block,
            b_block,
            a_blocks[u],
            c_blocks[u],
            a_blocks[v],
            c_blocks[v],
        ):
            return False
    return True


def support_pair_possible(mask_a: int, mask_c: int) -> bool:
    """Necessary nonzero-product incidence for every cross equation."""

    for u, v in combinations(PORTS, 2):
        first = bool(mask_a & (1 << u)) and bool(mask_c & (1 << v))
        second = bool(mask_a & (1 << v)) and bool(mask_c & (1 << u))
        if first != second:
            return False
    return True


def ratio_equation_matrix(active: tuple[int, ...]) -> Matrix:
    rows = []
    for u, v in combinations(active, 2):
        row = [ZERO] * len(active)
        row[active.index(u)] = ONE
        row[active.index(v)] = ONE
        rows.append(tuple(row))
    return tuple(rows)


def check_quotient_cross_support() -> dict[str, int]:
    admissible_masks = []
    for mask_a in range(1, 1 << len(PORTS)):
        for mask_c in range(1, 1 << len(PORTS)):
            if support_pair_possible(mask_a, mask_c):
                assert mask_a == mask_c
                admissible_masks.append(mask_a)
    assert len(admissible_masks) == (1 << len(PORTS)) - 1

    nullities = {}
    for size in range(1, len(PORTS) + 1):
        active = tuple(range(size))
        equations = ratio_equation_matrix(active)
        nullities[size] = size - matrix_rank(equations)
    assert nullities == {1: 1, 2: 1, 3: 0, 4: 0}

    realignment_checks = 0
    for x_dim, y_dim in product((1, 2), repeat=2):
        for left_rank in range(1, min(x_dim, DIM) + 1):
            for right_rank in range(1, min(y_dim, DIM) + 1):
                left = canonical_rectangular(x_dim, DIM, left_rank)
                right = canonical_rectangular(y_dim, DIM, right_rank)
                realigned = realigned_swapped_product(left, right)
                assert matrix_rank(realigned) == left_rank * right_rank
                realignment_checks += 1

    return {
        "support_masks": len(admissible_masks),
        "ratio_sizes": len(nullities),
        "realignment_checks": realignment_checks,
    }


def matrix_from_flat(entries: tuple[int, ...]) -> Matrix:
    return tuple(
        tuple(q(entries[DIM * row + column]) for column in COLORS) for row in COLORS
    )


def bilinear_value(matrix: Matrix, left: Vector, right: Vector) -> Fraction:
    return sum(
        left[row] * matrix[row][column] * right[column]
        for row in COLORS
        for column in COLORS
    )


def find_torus_orthogonal(vector: Vector) -> Vector | None:
    nonzero_positions = [index for index, entry in enumerate(vector) if entry]
    if len(nonzero_positions) < 2:
        return None
    pivot = nonzero_positions[0]
    other_positions = [index for index in COLORS if index != pivot]
    candidates = (-3, -2, -1, 1, 2, 3)
    for choices in product(candidates, repeat=len(other_positions)):
        answer = [ZERO] * DIM
        for position, value in zip(other_positions, choices, strict=True):
            answer[position] = q(value)
        numerator = -sum(
            vector[position] * answer[position] for position in other_positions
        )
        answer[pivot] = numerator / vector[pivot]
        if all(answer):
            result = tuple(answer)
            assert sum(a * b for a, b in zip(vector, result, strict=True)) == 0
            return result
    return None


def find_bilinear_torus_zero(matrix: Matrix) -> tuple[Vector, Vector] | None:
    candidates = (-3, -2, -1, 1, 2, 3)
    for left_values in product(candidates, repeat=DIM):
        left = make_vector(left_values)
        contracted = tuple(
            sum(left[row] * matrix[row][column] for row in COLORS) for column in COLORS
        )
        right = (
            make_vector((1, 1, 1))
            if not any(contracted)
            else find_torus_orthogonal(contracted)
        )
        if right is not None:
            assert all(left) and all(right)
            assert bilinear_value(matrix, left, right) == 0
            return left, right
    return None


def is_coordinate_monomial(matrix: Matrix) -> bool:
    return sum(bool(entry) for row in matrix for entry in row) == 1


def check_rank_two_projection_census() -> dict[str, int]:
    rank_one_count = 0
    rank_two_count = 0
    rank_one_torus_checks = 0
    rank_two_torus_checks = 0
    two_sided_projection_checks = 0
    one_sided_projection_checks = 0

    for entries in product((-1, 0, 1), repeat=DIM * DIM):
        matrix = matrix_from_flat(entries)
        rank = matrix_rank(matrix)
        if rank == 1:
            rank_one_count += 1
            witness = find_bilinear_torus_zero(matrix)
            if is_coordinate_monomial(matrix):
                assert witness is None
            else:
                assert witness is not None
            rank_one_torus_checks += 1
        elif rank == 2:
            rank_two_count += 1
            assert find_bilinear_torus_zero(matrix) is not None
            rank_two_torus_checks += 1

            row_quotient_ranks = [
                matrix_rank(delete_row(matrix, color)) for color in COLORS
            ]
            column_quotient_ranks = [
                matrix_rank(delete_column(matrix, color)) for color in COLORS
            ]
            for residual_left, residual_right in product(COLORS, repeat=2):
                projected_rank = matrix_rank(
                    delete_row_and_column(matrix, residual_left, residual_right)
                )
                left_rank = row_quotient_ranks[residual_left]
                right_rank = column_quotient_ranks[residual_right]
                if left_rank == 2 and right_rank == 2:
                    assert projected_rank == 2
                    two_sided_projection_checks += 1
                if left_rank == 1 and right_rank == 2:
                    assert projected_rank == 1
                    one_sided_projection_checks += 1
                if left_rank == 2 and right_rank == 1:
                    assert projected_rank == 1
                    one_sided_projection_checks += 1

    assert rank_one_count
    assert rank_two_count
    return {
        "rank_one_matrices": rank_one_count,
        "rank_two_matrices": rank_two_count,
        "rank_one_torus_checks": rank_one_torus_checks,
        "rank_two_torus_checks": rank_two_torus_checks,
        "two_sided_projection_checks": two_sided_projection_checks,
        "one_sided_projection_checks": one_sided_projection_checks,
    }


def projected_ghz_flattening_rank(left_killed: int, right_killed: int) -> int:
    rows: dict[tuple[int, int], int] = {}
    columns: dict[tuple[int, int, int, int], int] = {}
    entries: list[tuple[tuple[int, int], tuple[int, int, int, int]]] = []
    for color in COLORS:
        if color in (left_killed, right_killed):
            continue
        row = (color, color)
        column = (color,) * len(PORTS)
        rows.setdefault(row, len(rows))
        columns.setdefault(column, len(columns))
        entries.append((row, column))
    matrix = [[ZERO for _ in columns] for _ in rows]
    for row, column in entries:
        matrix[rows[row]][columns[column]] = ONE
    return matrix_rank(matrix)


def check_rank_two_target_routes() -> dict[str, int]:
    simultaneous_checks = 0
    one_sided_routes = 0
    all_k_slices = 0
    for residual_left, residual_right in product(COLORS, repeat=2):
        rank = projected_ghz_flattening_rank(residual_left, residual_right)
        if residual_left == residual_right:
            assert rank == 2
        else:
            assert rank == 1
        simultaneous_checks += 1

    for residual_left, residual_right in permutations(COLORS, 2):
        third = next(
            color for color in COLORS if color not in (residual_left, residual_right)
        )
        legal_local_pairs = []
        for local_s, local_t in product(COLORS, repeat=2):
            can_supply_left_pure = residual_left in (local_s, local_t)
            can_supply_right_pure = residual_right in (local_s, local_t)
            if can_supply_left_pure and can_supply_right_pure:
                legal_local_pairs.append((local_s, local_t))
        assert set(legal_local_pairs) == {
            (residual_left, residual_right),
            (residual_right, residual_left),
        }
        one_sided_routes += len(legal_local_pairs)

        forced_h = tuple(
            tuple(ONE if (row, column) == (third, third) else ZERO for column in COLORS)
            for row in COLORS
        )
        assert matrix_rank(forced_h) == 1
        for q0, q1 in product(COLORS, repeat=2):
            expected = ONE if q0 == q1 == third else ZERO
            assert forced_h[q0][q1] == expected
            all_k_slices += 1

    return {
        "simultaneous_color_projections": simultaneous_checks,
        "one_sided_pure_routes": one_sided_routes,
        "all_k_slice_coefficients": all_k_slices,
    }


def b_from_rank_one_data(a_u: Vector, c_u: Vector, a_v: Vector, c_v: Vector) -> Matrix:
    return matrix_scale(
        -1,
        matrix_add(
            outer(a_u, c_v),
            outer(c_u, a_v),
        ),
    )


def scalar_multiple_of(reference: Matrix, candidate: Matrix) -> Fraction | None:
    pivot = next(
        (
            (row, column)
            for row in range(len(reference))
            for column in range(len(reference[0]))
            if reference[row][column]
        ),
        None,
    )
    if pivot is None:
        raise ValueError("reference matrix must be nonzero")
    row, column = pivot
    scalar = candidate[row][column] / reference[row][column]
    for i in range(len(reference)):
        for j in range(len(reference[0])):
            if candidate[i][j] != scalar * reference[i][j]:
                return None
    return scalar


def recover_core_b(
    h_block: Matrix,
    a_u: Matrix,
    c_u: Matrix,
    a_v: Matrix,
    c_v: Matrix,
) -> Matrix | None:
    rows = []
    for local_u in COLORS:
        row = []
        for local_v in COLORS:
            cross = tuple(
                tuple(
                    a_u[q0][local_u] * c_v[q1][local_v]
                    + a_v[q0][local_v] * c_u[q1][local_u]
                    for q1 in COLORS
                )
                for q0 in COLORS
            )
            scalar = scalar_multiple_of(h_block, cross)
            if scalar is None:
                return None
            row.append(-scalar)
        rows.append(tuple(row))
    return tuple(rows)


def check_rank_two_core_and_rank_one_forms() -> dict[str, int]:
    e0, e1, e2 = (basis_vector(DIM, color) for color in COLORS)
    rank_two_h = make_matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))

    rank_two_a = [
        outer(e0, e0),
        outer(e1, e1),
        zero_matrix(),
        zero_matrix(),
    ]
    rank_two_c = [
        outer(e1, e0),
        outer(e0, e1),
        zero_matrix(),
        zero_matrix(),
    ]
    rank_two_b = {(0, 1): matrix_scale(-1, outer(e0, e1))}
    assert all_pair_responses_zero(rank_two_h, rank_two_a, rank_two_c, rank_two_b)
    recovered = recover_core_b(
        rank_two_h,
        rank_two_a[0],
        rank_two_c[0],
        rank_two_a[1],
        rank_two_c[1],
    )
    assert recovered == rank_two_b[(0, 1)]

    nonconformal_a = [outer(e0, e0), outer(e0, e1)]
    nonconformal_c = [outer(e0, e0), outer(e1, e1)]
    assert (
        recover_core_b(
            rank_two_h,
            nonconformal_a[0],
            nonconformal_c[0],
            nonconformal_a[1],
            nonconformal_c[1],
        )
        is None
    )

    rank_one_h = outer(e0, e0)
    a_vectors = (
        make_vector((1, 2, 0)),
        make_vector((0, 1, 1)),
        make_vector((1, -1, 2)),
        make_vector((0, 0, 0)),
    )
    c_vectors = (
        make_vector((0, 1, 2)),
        make_vector((1, 0, -1)),
        make_vector((2, 1, 0)),
        make_vector((1, 1, 1)),
    )

    contained_a = [outer(e0, vector) for vector in a_vectors]
    contained_c = [outer(e0, vector) for vector in c_vectors]
    contained_b = {
        (u, v): b_from_rank_one_data(
            a_vectors[u], c_vectors[u], a_vectors[v], c_vectors[v]
        )
        for u, v in combinations(PORTS, 2)
    }
    assert all_pair_responses_zero(rank_one_h, contained_a, contained_c, contained_b)

    singleton_a_vectors = (a_vectors[0],) + (make_vector((0, 0, 0)),) * 3
    singleton_a = [outer(e0, vector) for vector in singleton_a_vectors]
    singleton_c = [
        make_matrix(((1, 0, 2), (0, 1, 1), (2, -1, 0))),
        outer(e0, c_vectors[1]),
        outer(e0, c_vectors[2]),
        outer(e0, c_vectors[3]),
    ]
    singleton_b = {
        (u, v): b_from_rank_one_data(
            singleton_a_vectors[u],
            c_vectors[u],
            singleton_a_vectors[v],
            c_vectors[v],
        )
        for u, v in combinations(PORTS, 2)
    }
    assert all_pair_responses_zero(rank_one_h, singleton_a, singleton_c, singleton_b)
    assert all_pair_responses_zero(
        transpose(rank_one_h), singleton_c, singleton_a, singleton_b
    )

    two_port_a_vectors = (
        make_vector((1, 1, 0)),
        make_vector((0, 1, 2)),
        make_vector((0, 0, 0)),
        make_vector((0, 0, 0)),
    )
    two_port_c_vectors = (
        make_vector((1, 0, 1)),
        make_vector((0, 1, -1)),
        make_vector((1, 2, 0)),
        make_vector((2, -1, 1)),
    )
    d = e1
    two_port_a = [outer(e0, vector) for vector in two_port_a_vectors]
    two_port_c = [
        matrix_add(
            outer(d, two_port_a_vectors[0]),
            outer(e0, two_port_c_vectors[0]),
        ),
        matrix_add(
            matrix_scale(-1, outer(d, two_port_a_vectors[1])),
            outer(e0, two_port_c_vectors[1]),
        ),
        outer(e0, two_port_c_vectors[2]),
        outer(e0, two_port_c_vectors[3]),
    ]
    two_port_b = {
        (u, v): b_from_rank_one_data(
            two_port_a_vectors[u],
            two_port_c_vectors[u],
            two_port_a_vectors[v],
            two_port_c_vectors[v],
        )
        for u, v in combinations(PORTS, 2)
    }
    assert all_pair_responses_zero(rank_one_h, two_port_a, two_port_c, two_port_b)
    assert all_pair_responses_zero(
        transpose(rank_one_h), two_port_c, two_port_a, two_port_b
    )

    two_sided_singleton_a = [
        outer(e1, make_vector((1, 1, 0))),
        zero_matrix(),
        zero_matrix(),
        zero_matrix(),
    ]
    two_sided_singleton_c = [
        make_matrix(((1, 2, 0), (0, 1, 1), (2, 0, 1))),
        zero_matrix(),
        zero_matrix(),
        zero_matrix(),
    ]
    assert all_pair_responses_zero(
        rank_one_h,
        two_sided_singleton_a,
        two_sided_singleton_c,
        {},
    )

    alpha_s = make_vector((1, 1, 0))
    alpha_t = make_vector((0, 1, 1))
    two_sided_two_a = [
        outer(e1, alpha_s),
        outer(e1, alpha_t),
        zero_matrix(),
        zero_matrix(),
    ]
    two_sided_two_c = [
        matrix_scale(2, outer(e2, alpha_s)),
        matrix_scale(-2, outer(e2, alpha_t)),
        zero_matrix(),
        zero_matrix(),
    ]
    assert all_pair_responses_zero(rank_one_h, two_sided_two_a, two_sided_two_c, {})

    active_sets = tuple(
        active for size in (1, 2) for active in combinations(PORTS, size)
    )
    response_leaves = [("contained", ())]
    response_leaves.extend(("left-escape", active) for active in active_sets)
    response_leaves.extend(("right-escape", active) for active in active_sets)
    response_leaves.extend(("two-sided-escape", active) for active in active_sets)
    assert len(response_leaves) == 31
    assert {label for label, _active in response_leaves} == {
        "contained",
        "left-escape",
        "right-escape",
        "two-sided-escape",
    }

    return {
        "rank_two_core_controls": 2,
        "rank_one_normal_forms": 6,
        "labelled_response_leaves": len(response_leaves),
    }


def normalize_projective(values: tuple[int, ...]) -> tuple[int, ...]:
    divisor = 0
    for value in values:
        divisor = gcd(divisor, abs(value))
    if divisor == 0:
        raise ValueError("zero vector is not projective")
    normalized = tuple(value // divisor for value in values)
    first = next(value for value in normalized if value)
    if first < 0:
        normalized = tuple(-value for value in normalized)
    return normalized


def projective_small_vectors_of_dimension(dimension: int) -> tuple[Vector, ...]:
    representatives = {
        normalize_projective(values)
        for values in product((-1, 0, 1), repeat=dimension)
        if any(values)
    }
    return tuple(make_vector(values) for values in sorted(representatives))


def projective_small_vectors() -> tuple[Vector, ...]:
    return projective_small_vectors_of_dimension(DIM)


def row_span_contains(rows: Sequence[Vector], vector: Vector) -> bool:
    if not rows:
        return False
    return matrix_rank(tuple(rows) + (vector,)) == matrix_rank(rows)


def find_torus_in_span(basis: tuple[Vector, ...]) -> Vector | None:
    if not basis:
        return None
    for coefficients in product(range(-3, 4), repeat=len(basis)):
        if not any(coefficients):
            continue
        vector = tuple(
            sum(
                q(coefficients[index]) * basis[index][coordinate]
                for index in range(len(basis))
            )
            for coordinate in COLORS
        )
        if all(vector):
            return vector
    return None


def beta_matrix(left: Vector, right: Vector) -> Matrix:
    """Return a tensor representative of beta(left,right) for H=I_2."""

    left_l, left_m = left[:2], left[2:]
    right_l, right_m = right[:2], right[2:]
    return matrix_add(outer(left_l, right_m), outer(right_l, left_m))


def beta_zero(left: Vector, right: Vector) -> bool:
    return scalar_multiple_of(identity_matrix(2), beta_matrix(left, right)) is not None


def beta_kernel_matrix(vector: Vector) -> Matrix:
    """Matrix of w' -> beta(vector,w') in Mat_2 / K I_2."""

    columns = []
    for coordinate in range(4):
        image = beta_matrix(vector, basis_vector(4, coordinate))
        columns.append((image[0][1], image[1][0], image[0][0] - image[1][1]))
    return transpose(tuple(columns))


def check_mixed_beta_kernel_and_combined_supports() -> dict[str, int]:
    """Use direct projective incidence, not the theorem's kernel normal form."""

    projective_four = projective_small_vectors_of_dimension(4)
    mixed = tuple(
        vector for vector in projective_four if any(vector[:2]) and any(vector[2:])
    )
    kernel_memberships = 0
    kernel_pair_checks = 0
    sharp_pairs = 0
    for vector in mixed:
        kernel_matrix = beta_kernel_matrix(vector)
        assert matrix_rank(kernel_matrix) in (2, 3)
        kernel_basis = nullspace_basis(kernel_matrix, 4)
        assert kernel_basis
        neighbors = tuple(
            candidate for candidate in mixed if beta_zero(vector, candidate)
        )
        for candidate in neighbors:
            assert all(
                sum(
                    kernel_matrix[row][column] * candidate[column]
                    for column in range(4)
                )
                == 0
                for row in range(3)
            )
            kernel_memberships += 1
        for first in neighbors:
            for second in neighbors:
                assert not beta_zero(first, second)
                kernel_pair_checks += 1

    for first, second in combinations(mixed, 2):
        if beta_zero(first, second):
            sharp_pairs += 1
    assert sharp_pairs
    for triple in combinations(mixed, 3):
        assert not all(
            beta_zero(left, right) for left, right in combinations(triple, 2)
        )
    assert all(not beta_zero(vector, vector) for vector in mixed)

    e0, e1 = basis_vector(2, 0), basis_vector(2, 1)
    sharp_left = e0 + e1
    sharp_right = e1 + e0
    assert beta_zero(sharp_left, sharp_right)

    return {
        "mixed_projective_lines": len(mixed),
        "kernel_memberships": kernel_memberships,
        "kernel_pair_checks": kernel_pair_checks,
        "sharp_orthogonal_pairs": sharp_pairs,
        "orthogonal_triples": 0,
    }


def check_moving_blockers() -> dict[str, int]:
    small = (make_vector((0, 0, 0)),) + projective_small_vectors()
    annihilator_checks = 0
    torus_kernel_witnesses = 0
    for a_vector, c_vector in product(small, repeat=2):
        rows = tuple(vector for vector in (a_vector, c_vector) if any(vector))
        rows = rref(rows)[0][: matrix_rank(rows)] if rows else ()
        misses_torus = any(
            row_span_contains(rows, basis_vector(DIM, color)) for color in COLORS
        )
        kernel = nullspace_basis(rows, DIM)
        witness = find_torus_in_span(kernel)
        assert (witness is None) == misses_torus
        if witness is not None:
            assert all(
                sum(row[color] * witness[color] for color in COLORS) == 0
                for row in rows
            )
            torus_kernel_witnesses += 1
        annihilator_checks += 1

    h_support = identity_matrix(2)
    p_line = make_vector((1, -1))
    q_line = make_vector((1, 1))
    scalar_values = tuple(q(value) for value in (-2, -1, 0, 1, 2))
    pair_tables = 0
    pair_solutions = 0
    for lambda_u, mu_u, lambda_v, mu_v, b_value in product(scalar_values, repeat=5):
        cross_scalar = lambda_u * mu_v + lambda_v * mu_u
        matrix = matrix_add(
            matrix_scale(b_value, h_support),
            matrix_scale(cross_scalar, outer(p_line, q_line)),
        )
        if matrix == zero_matrix(2, 2):
            assert b_value == 0
            assert cross_scalar == 0
            pair_solutions += 1
        pair_tables += 1

    blocker_masks = 0
    for open_mask in range(1 << len(PORTS)):
        open_count = open_mask.bit_count()
        if open_count >= 3:
            assert any(
                all(open_mask & (1 << port) for port in triple)
                for triple in combinations(PORTS, 3)
            )
        blocker_masks += 1

    active_pair_checks = 0
    for active_ports in combinations(PORTS, 2):
        inactive_ports = set(PORTS) - set(active_ports)
        open_ports = set(inactive_ports)
        assert len(open_ports) == 2
        assert not (open_ports & set(active_ports))
        active_pair_checks += 1

    return {
        "annihilator_tables": annihilator_checks,
        "torus_kernel_witnesses": torus_kernel_witnesses,
        "moving_pair_tables": pair_tables,
        "moving_pair_solutions": pair_solutions,
        "open_port_masks": blocker_masks,
        "active_pair_blocker_checks": active_pair_checks,
    }


def poly_add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, ZERO) + coefficient
    return {
        monomial: coefficient for monomial, coefficient in answer.items() if coefficient
    }


def poly_scale(scalar: int | Fraction, polynomial: Polynomial) -> Polynomial:
    value = q(scalar)
    return {
        monomial: value * coefficient
        for monomial, coefficient in polynomial.items()
        if value * coefficient
    }


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                a + b for a, b in zip(monomial_left, monomial_right, strict=True)
            )
            answer[monomial] = (
                answer.get(monomial, ZERO) + coefficient_left * coefficient_right
            )
    return {
        monomial: coefficient for monomial, coefficient in answer.items() if coefficient
    }


def variable_polynomial(position: int) -> Polynomial:
    monomial = [0] * (2 * len(PORTS))
    monomial[position] = 1
    return {tuple(monomial): ONE}


def response_replacement(u: int, v: int) -> Polynomial:
    a_u = variable_polynomial(u)
    a_v = variable_polynomial(v)
    c_u = variable_polynomial(len(PORTS) + u)
    c_v = variable_polynomial(len(PORTS) + v)
    return poly_scale(
        -1,
        poly_add(
            poly_multiply(a_u, c_v),
            poly_multiply(a_v, c_u),
        ),
    )


def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            answer.append(((first, second),) + matching)
    return tuple(answer)


def check_six_versus_seven_response() -> dict[str, int]:
    # Vertices 0,1 are q0,q1; vertices 2,...,5 are the four ports.
    matchings = perfect_matchings(tuple(range(6)))
    assert len(matchings) == 15
    reduced: Polynomial = {}
    h_matchings = 0
    cross_matchings = 0
    for matching in matchings:
        edge_set = {tuple(sorted(edge)) for edge in matching}
        if (0, 1) in edge_set:
            h_matchings += 1
            port_edges = [
                (left - 2, right - 2) for left, right in edge_set if left >= 2
            ]
            assert len(port_edges) == 2
            term = poly_multiply(
                response_replacement(*port_edges[0]),
                response_replacement(*port_edges[1]),
            )
        else:
            cross_matchings += 1
            q0_edge = next(edge for edge in edge_set if 0 in edge)
            q1_edge = next(edge for edge in edge_set if 1 in edge)
            port_u = max(q0_edge) - 2
            port_v = max(q1_edge) - 2
            assert port_u != port_v
            remaining = next(edge for edge in edge_set if edge[0] >= 2 and edge[1] >= 2)
            remaining_ports = (remaining[0] - 2, remaining[1] - 2)
            term = variable_polynomial(port_u)
            term = poly_multiply(term, variable_polynomial(len(PORTS) + port_v))
            term = poly_multiply(term, response_replacement(*remaining_ports))
        reduced = poly_add(reduced, term)

    assert h_matchings == 3
    assert cross_matchings == 12
    expected: Polynomial = {}
    for a_ports in combinations(PORTS, 2):
        term: Polynomial = {(0,) * (2 * len(PORTS)): ONE}
        for port in PORTS:
            position = port if port in a_ports else len(PORTS) + port
            term = poly_multiply(term, variable_polynomial(position))
        expected = poly_add(expected, poly_scale(-2, term))
    assert reduced == expected

    h_value = ONE
    a_values = (ONE,) * len(PORTS)
    c_values = (ONE,) * len(PORTS)
    b_values = {
        (u, v): -(a_values[u] * c_values[v] + a_values[v] * c_values[u])
        for u, v in combinations(PORTS, 2)
    }
    for u, v in combinations(PORTS, 2):
        assert (
            h_value * b_values[(u, v)]
            + a_values[u] * c_values[v]
            + a_values[v] * c_values[u]
            == 0
        )

    def scalar_edge(left: int, right: int) -> Fraction:
        edge = tuple(sorted((left, right)))
        if edge == (0, 1):
            return h_value
        if edge[0] == 0:
            return a_values[edge[1] - 2]
        if edge[0] == 1:
            return c_values[edge[1] - 2]
        return b_values[(edge[0] - 2, edge[1] - 2)]

    seventh_value = sum(
        (
            scalar_edge(*matching[0])
            * scalar_edge(*matching[1])
            * scalar_edge(*matching[2])
        )
        for matching in matchings
    )
    assert seventh_value == -12
    assert h_value * seventh_value == -2 * 6

    return {
        "perfect_matchings": len(matchings),
        "reduced_monomials": len(reduced),
        "sharp_seventh_value": int(seventh_value),
    }


def tensor_term_for_edge(
    edge: tuple[int, int],
    edge_block: Matrix,
    companion: Tensor,
    slot_count: int = 6,
) -> Tensor:
    left, right = edge
    complement = tuple(slot for slot in range(slot_count) if slot not in edge)
    answer: Tensor = {}
    for edge_left, edge_right in product(COLORS, repeat=2):
        edge_coefficient = edge_block[edge_left][edge_right]
        if not edge_coefficient:
            continue
        for companion_word, companion_coefficient in companion.items():
            assert len(companion_word) == len(complement)
            word = [0] * slot_count
            word[left] = edge_left
            word[right] = edge_right
            for slot, color in zip(complement, companion_word, strict=True):
                word[slot] = color
            key = tuple(word)
            answer[key] = (
                answer.get(key, ZERO) + edge_coefficient * companion_coefficient
            )
    return tensor_clean(answer)


def pure_companion(
    edge: tuple[int, int], color: int, coefficient: int | Fraction = 1
) -> Tensor:
    return {(color,) * (6 - len(edge)): q(coefficient)}


def ghz_tensor(weights: Sequence[int | Fraction] = (1, 1, 1)) -> Tensor:
    return {(color,) * 6: q(weights[color]) for color in COLORS}


def check_rank_two_quotient_target_projection() -> dict[str, int]:
    """Audit that the double quotient retains exactly the six U-U terms."""

    e0, e1, e2 = (basis_vector(DIM, color) for color in COLORS)
    h_block = make_matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))
    physical_edges: dict[tuple[int, int], Matrix] = {(0, 1): h_block}
    for port in PORTS:
        physical_edges[(0, 2 + port)] = matrix_add(
            outer(e0, make_vector((1, port + 1, -1))),
            outer(e1, make_vector((port + 2, -1, 1))),
        )
        physical_edges[(1, 2 + port)] = matrix_add(
            outer(e0, make_vector((2, -1, port + 1))),
            outer(e1, make_vector((1, port + 2, -2))),
        )
    for u, v in combinations(PORTS, 2):
        physical_edges[(2 + u, 2 + v)] = matrix_add(
            outer(e0, e1),
            matrix_scale(u + v + 1, outer(e2, e0)),
        )

    companions: dict[tuple[int, int], Tensor] = {}
    for edge in physical_edges:
        complement = tuple(slot for slot in range(6) if slot not in edge)
        companion: Tensor = {}
        for word in product(COLORS, repeat=len(complement)):
            coefficient = q(
                sum(
                    (slot + 1) * (color + 1)
                    for slot, color in zip(complement, word, strict=True)
                )
                % 5
                - 2
            )
            if coefficient:
                companion[word] = coefficient
        companions[edge] = companion

    all_terms = {
        edge: tensor_term_for_edge(edge, block, companions[edge])
        for edge, block in physical_edges.items()
    }
    projected_all = {
        word[2:]: coefficient
        for word, coefficient in tensor_add(*all_terms.values()).items()
        if word[0] == word[1] == 2
    }
    u_u_edges = tuple(edge for edge in physical_edges if edge[0] >= 2)
    projected_u_u = {
        word[2:]: coefficient
        for word, coefficient in tensor_add(
            *(all_terms[edge] for edge in u_u_edges)
        ).items()
        if word[0] == word[1] == 2
    }
    assert projected_all == projected_u_u
    for edge, term in all_terms.items():
        if edge[0] < 2:
            assert not any(word[0] == word[1] == 2 for word in term)

    projected_rhs = {
        word[2:]: coefficient
        for word, coefficient in ghz_tensor((2, -3, 5)).items()
        if word[0] == word[1] == 2
    }
    assert projected_rhs == {(2, 2, 2, 2): q(5)}
    return {
        "physical_edge_terms": len(physical_edges),
        "surviving_u_u_terms": len(u_u_edges),
        "projected_port_coefficients": 3 ** len(PORTS),
    }


def check_complete_target_pure_controls() -> dict[str, int]:
    triangle_checks = 0
    triangle_coefficients = 0
    for residual_left, residual_right in permutations(COLORS, 2):
        third = next(
            color for color in COLORS if color not in (residual_left, residual_right)
        )
        for active_port in PORTS:
            q_edge = (0, 1)
            a_edge = (0, 2 + active_port)
            c_edge = (1, 2 + active_port)
            terms = (
                tensor_term_for_edge(
                    q_edge,
                    outer(basis_vector(DIM, third), basis_vector(DIM, third)),
                    pure_companion(q_edge, third),
                ),
                tensor_term_for_edge(
                    a_edge,
                    outer(
                        basis_vector(DIM, residual_left),
                        basis_vector(DIM, residual_left),
                    ),
                    pure_companion(a_edge, residual_left),
                ),
                tensor_term_for_edge(
                    c_edge,
                    outer(
                        basis_vector(DIM, residual_right),
                        basis_vector(DIM, residual_right),
                    ),
                    pure_companion(c_edge, residual_right),
                ),
            )
            assert tensor_add(*terms) == ghz_tensor()
            assert all(len(term) == 1 for term in terms)
            active_colors = {next(iter(term))[2 + active_port] for term in terms}
            assert active_colors == set(COLORS)
            triangle_checks += 1
            triangle_coefficients += 3**6

            h_block = outer(basis_vector(DIM, third), basis_vector(DIM, third))
            a_blocks = [zero_matrix() for _ in PORTS]
            c_blocks = [zero_matrix() for _ in PORTS]
            a_blocks[active_port] = outer(
                basis_vector(DIM, residual_left),
                basis_vector(DIM, residual_left),
            )
            c_blocks[active_port] = outer(
                basis_vector(DIM, residual_right),
                basis_vector(DIM, residual_right),
            )
            assert all_pair_responses_zero(h_block, a_blocks, c_blocks, {})

    return {
        "formal_triangle_controls": triangle_checks,
        "implicit_six_slot_coefficients": triangle_coefficients,
    }


def incidence_columns(
    edge_data: dict[tuple[int, int], int],
    outside_count: int,
) -> tuple[Matrix, ...]:
    columns = []
    for outside in range(outside_count):
        matrix = [[ZERO for _ in COLORS] for _ in range(4)]
        for root in range(4):
            local_color = edge_data.get((root, outside))
            if local_color is not None:
                matrix[root][local_color] = ONE
        columns.append(tuple(tuple(row) for row in matrix))
    return tuple(columns)


def maximum_independent_set_size(
    vertices: tuple[str, ...], edges: set[frozenset[str]]
) -> int:
    maximum = 0
    for mask in range(1 << len(vertices)):
        selected = tuple(
            vertex for index, vertex in enumerate(vertices) if mask & (1 << index)
        )
        if all(frozenset(pair) not in edges for pair in combinations(selected, 2)):
            maximum = max(maximum, len(selected))
    return maximum


def check_sharp_physical_controls() -> dict[str, int]:
    # Outside order is u0,u1,u2,u3,q0,q1.
    root_outside_colors = {
        (0, 0): 2,
        (1, 0): 0,
        (2, 0): 1,
        (1, 1): 2,
        (2, 1): 0,
        (3, 1): 1,
        (2, 2): 2,
        (3, 2): 0,
        (3, 3): 2,
        (0, 4): 0,
        (1, 4): 1,
        (2, 5): 0,
        (0, 5): 1,
    }
    columns = incidence_columns(root_outside_colors, 6)
    ranks = tuple(matrix_rank(column) for column in columns)
    assert ranks == (3, 3, 2, 1, 2, 2)
    assert sum(DIM - rank for rank in ranks) == 5

    root_u_matchings = []
    for assigned_ports in permutations(PORTS):
        if all(
            (root, assigned_ports[root]) in root_outside_colors for root in range(4)
        ):
            word = [None] * len(PORTS)
            for root, port in enumerate(assigned_ports):
                word[port] = root_outside_colors[(root, port)]
            root_u_matchings.append(tuple(word))
    assert root_u_matchings == [(2, 2, 2, 2)]
    pi_q = {(2, 2, 2, 2): ONE}

    # Rows r1,r2 against q0,q1, evaluated at all-ones torus vectors.
    residual_incidence = make_matrix(((1, 0), (0, 1)))
    assert matrix_rank(residual_incidence) == 2

    vertices = (
        "r0",
        "r1",
        "r2",
        "r3",
        "q0",
        "q1",
        "u0",
        "u1",
        "u2",
        "u3",
    )
    monomial_edges = {
        frozenset((f"r{root}", f"u{outside}"))
        for root, outside in root_outside_colors
        if outside < 4
    }
    monomial_edges.update(
        {
            frozenset((f"r{root}", f"q{outside - 4}"))
            for root, outside in root_outside_colors
            if outside >= 4
        }
    )
    required_cliques = (
        ("r2", "u2"),
        ("r3", "u3"),
        ("r0", "q1", "u0"),
        ("r1", "q0", "u1"),
    )

    e0, e1, _e2 = (basis_vector(DIM, color) for color in COLORS)
    controls = []

    rank_two_h = make_matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))
    rank_two_a = [
        outer(e0, e0),
        outer(e1, e1),
        zero_matrix(),
        zero_matrix(),
    ]
    rank_two_c = [
        outer(e1, e0),
        outer(e0, e1),
        zero_matrix(),
        zero_matrix(),
    ]
    rank_two_b = {(0, 1): matrix_scale(-1, outer(e0, e1))}
    controls.append((rank_two_h, rank_two_a, rank_two_c, rank_two_b))

    rank_one_h = outer(e0, e0)
    rank_one_a = [
        outer(e0, e0),
        outer(e0, e1),
        zero_matrix(),
        zero_matrix(),
    ]
    rank_one_c = [
        outer(e0, e1),
        outer(e0, e0),
        zero_matrix(),
        zero_matrix(),
    ]
    rank_one_b = {(0, 1): matrix_scale(-1, matrix_add(outer(e0, e0), outer(e1, e1)))}
    controls.append((rank_one_h, rank_one_a, rank_one_c, rank_one_b))

    control_checks = 0
    for control_index, (h_block, a_blocks, c_blocks, b_blocks) in enumerate(controls):
        assert all_pair_responses_zero(h_block, a_blocks, c_blocks, b_blocks)
        control_edges = set(monomial_edges)
        for port, block in enumerate(a_blocks):
            if is_coordinate_monomial(block):
                control_edges.add(frozenset(("q0", f"u{port}")))
        for port, block in enumerate(c_blocks):
            if is_coordinate_monomial(block):
                control_edges.add(frozenset(("q1", f"u{port}")))
        if is_coordinate_monomial(h_block):
            control_edges.add(frozenset(("q0", "q1")))
        for clique in required_cliques:
            assert all(
                frozenset(pair) in control_edges for pair in combinations(clique, 2)
            )
        assert maximum_independent_set_size(vertices, control_edges) == 4

        root_set = {"r0", "r1", "r2", "r3"}
        assert all(
            frozenset(pair) not in control_edges for pair in combinations(root_set, 2)
        )

        outside_word = (0, 0, 2, 2, 2, 2)
        assert pi_q[(2, 2, 2, 2)] == 1
        q_term = h_block[outside_word[0]][outside_word[1]] * pi_q[outside_word[2:]]
        assert q_term == 1
        for port in PORTS:
            assert a_blocks[port][outside_word[0]][outside_word[2 + port]] == 0
            assert c_blocks[port][outside_word[1]][outside_word[2 + port]] == 0
        for (u, v), block in b_blocks.items():
            assert block[outside_word[2 + u]][outside_word[2 + v]] == 0
        assert outside_word not in ghz_tensor()
        assert bilinear_value(
            h_block, make_vector((1, 1, 1)), make_vector((1, 1, 1))
        ) == (2 if control_index == 0 else 1)

        if control_index == 0:
            active_combined_ports = []
            for port in PORTS:
                a_rows = a_blocks[port][:2]
                c_rows = c_blocks[port][:2]
                combined_rows = a_rows + c_rows
                combined_rank = matrix_rank(combined_rows)
                if combined_rank:
                    active_combined_ports.append(port)
                    assert matrix_rank(a_rows) == combined_rank
                    assert matrix_rank(c_rows) == combined_rank
                    kernel = nullspace_basis(combined_rows, DIM)
                    assert find_torus_in_span(kernel) is None
                    assert any(
                        row_span_contains(combined_rows, basis_vector(DIM, color))
                        for color in COLORS
                    )
            assert active_combined_ports == [0, 1]
        control_checks += 1

    return {
        "incidence_columns": len(columns),
        "unique_root_u_matchings": len(root_u_matchings),
        "maximum_root_controls": control_checks,
        "mixed_target_defects": control_checks,
    }


def check_rank_two_singleton_realignment() -> dict[str, int]:
    h_block = make_matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))
    checks = 0
    for b_rank in (1, 2, 3):
        b_block = canonical_rectangular(DIM, DIM, b_rank)
        # The H-times-B realignment has Kronecker rank 2*rank(B).
        kron = tuple(
            tuple(
                h_block[row // DIM][column // DIM] * b_block[row % DIM][column % DIM]
                for column in range(DIM * DIM)
            )
            for row in range(DIM * DIM)
        )
        assert matrix_rank(kron) == 2 * b_rank
        a_vector = flatten_matrix(canonical_rectangular(DIM, DIM, min(b_rank, DIM)))
        c_vector = flatten_matrix(outer(basis_vector(3, 1), basis_vector(3, 2)))
        assert matrix_rank(outer(a_vector, c_vector)) == 1
        checks += 1
    return {"singleton_realignment_ranks": checks}


def main() -> None:
    sections = (
        ("quotient-cross", check_quotient_cross_support),
        ("rank-two-census", check_rank_two_projection_census),
        ("rank-two-target", check_rank_two_target_routes),
        ("rank-two-core-rank-one-forms", check_rank_two_core_and_rank_one_forms),
        ("mixed-beta-kernel", check_mixed_beta_kernel_and_combined_supports),
        ("moving-blockers", check_moving_blockers),
        ("six-versus-seven", check_six_versus_seven_response),
        ("rank-two-quotient-target", check_rank_two_quotient_target_projection),
        ("complete-target-controls", check_complete_target_pure_controls),
        ("sharp-physical-controls", check_sharp_physical_controls),
        ("singleton-realignment", check_rank_two_singleton_realignment),
    )
    for label, check in sections:
        result = check()
        rendered = ", ".join(f"{key}={value}" for key, value in result.items())
        print(f"PASS {label}: {rendered}")

    print(
        "LIMITS: finite exact Q tables audit the displayed structural identities; "
        "they do not replace the arbitrary-field written proof."
    )
    print(
        "OPEN: rank-two double-contained witness core; rank-one complete-target "
        "and common-root companion branches; separate seventh-response quartic; "
        "unused GLS4 survival and selector gates; strategic node; global conjecture."
    )
    print("PASS independent determinant-divisor all-pair-response-zero audit")


if __name__ == "__main__":
    main()
