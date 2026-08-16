#!/usr/bin/env python3
"""Exact replay for the lower-joint-rank transverse two-root theorem."""

from __future__ import annotations

import itertools

import sympy as sp

DIM = 3
ROOT_DIM = 9
TENSOR_DIM = DIM**3
S, T, U = 0, 1, 2


def e(index: int, size: int = DIM) -> sp.Matrix:
    return sp.eye(size)[:, index]


def root_tensor(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def split_sources(row: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return row[:DIM, :], row[DIM : 2 * DIM, :], row[2 * DIM :, :]


def permanent_rows(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    pieces = (split_sources(left), split_sources(middle), split_sources(right))
    total = sp.zeros(TENSOR_DIM, 1)
    for permutation in itertools.permutations(range(3)):
        total += root_tensor(
            pieces[permutation[0]][0],
            pieces[permutation[1]][1],
            pieces[permutation[2]][2],
        )
    return total


def transverse_derivative() -> sp.Matrix:
    # B_23=e_t tensor e_t and B_13=e_u tensor e_u.
    b_23 = sp.kronecker_product(e(T), e(T))
    columns = [sp.kronecker_product(e(i), b_23) for i in range(DIM)]
    columns += [root_tensor(e(U), e(i), e(U)) for i in range(DIM)]
    columns += [sp.zeros(TENSOR_DIM, 1) for _ in range(DIM)]
    return sp.Matrix.hstack(*columns)


def derivative_normal_form() -> None:
    derivative = transverse_derivative()
    assert derivative.shape == (TENSOR_DIM, ROOT_DIM)
    assert derivative.rank() == 6
    kernel = sp.Matrix.hstack(*derivative.nullspace())
    expected = sp.Matrix.vstack(sp.zeros(6, 3), sp.eye(3))
    assert kernel.columnspace() == expected.columnspace()
    print("transverse derivative: PASS (rank six, kernel A3)")


def model_k(rank_h: int, rank_q: int) -> sp.Matrix:
    assert rank_h in (3, 4) and rank_q in (1, 2)
    columns = [e(i, ROOT_DIM) for i in range(3)]
    if rank_h == 3:
        columns[0] += e(6, ROOT_DIM)
        if rank_q == 2:
            columns[1] += e(7, ROOT_DIM)
        return sp.Matrix.hstack(*columns)

    if rank_q == 2:
        columns[0] += e(7, ROOT_DIM)
    return sp.Matrix.hstack(*columns, e(6, ROOT_DIM))


def intersection_dimension(left: sp.Matrix, right: sp.Matrix) -> int:
    return left.rank() + right.rank() - sp.Matrix.hstack(left, right).rank()


def lower_rank_atlas() -> None:
    derivative = transverse_derivative()
    expected = {(3, 1): 1, (3, 2): 2, (4, 1): 0, (4, 2): 1}
    for (rank_h, rank_q), expected_intersection in expected.items():
        k = model_k(rank_h, rank_q)
        assert k.rank() == rank_h
        assert (derivative * k).rank() == 3

        top = k[:6, :]
        bottom = k[6:, :]
        assert top.rank() == 3
        assert rank_h - top.rank() == rank_h - 3
        assert bottom.rank() == rank_q

        # Restrictions of the first two and third root covectors to K live
        # in K^*.  Their images are the column spaces below.
        v_space = sp.Matrix.hstack(*top.T.columnspace())
        q_space = sp.Matrix.hstack(*bottom.T.columnspace())
        assert v_space.rank() == 3
        assert q_space.rank() == rank_q
        assert sp.Matrix.hstack(v_space, q_space).rank() == rank_h
        assert intersection_dimension(v_space, q_space) == expected_intersection

    print("lower-rank incidence atlas: PASS (four exact (r,q) cells)")


def support_boundary() -> None:
    coordinate_plane = sp.Matrix.hstack(e(1), e(2))
    assert all(vector[0] == 0 for vector in coordinate_plane.columnspace())

    # Up to coordinate permutation and nonzero diagonal rescaling, these are
    # the two noncoordinate normal directions.  Their kernels contain the
    # displayed fully supported vectors.
    support_two_normal = sp.Matrix([[1, 1, 0]])
    support_three_normal = sp.Matrix([[1, 1, 1]])
    assert support_two_normal * sp.Matrix([1, -1, 1]) == sp.zeros(1, 1)
    assert support_three_normal * sp.Matrix([1, 1, -2]) == sp.zeros(1, 1)

    for vector in (e(0), e(0) + e(1)):
        assert sum(entry != 0 for entry in vector) <= 2
    assert sum(entry != 0 for entry in sp.ones(3, 1)) == 3
    print("uninvolved-row support boundary: PASS")


def control_rows(rank_h: int) -> tuple[list[sp.Matrix], list[sp.Matrix], list[sp.Matrix]]:
    assert rank_h in (3, 4)
    x = e(0, ROOT_DIM)
    x_extra = x if rank_h == 3 else e(1, ROOT_DIM)
    y = e(3, ROOT_DIM)
    z = e(6, ROOT_DIM)

    v = x + z
    a = -x + z
    b = -x_extra + y
    q = sp.Rational(1, 2) * (x_extra + y)
    zero = sp.zeros(ROOT_DIM, 1)
    return [v, a, zero], [v, zero, b], [q, zero, zero]


def row_matrix(rank_h: int) -> sp.Matrix:
    root_one, root_two, root_three = control_rows(rank_h)
    return sp.Matrix.vstack(*(row.T for row in root_one + root_two + root_three))


def empty_tensor(rank_h: int) -> sp.Matrix:
    root_one, root_two, root_three = control_rows(rank_h)
    result = sp.zeros(TENSOR_DIM, TENSOR_DIM)
    for a, b, c in itertools.product(range(DIM), repeat=3):
        root_index = (a * DIM + b) * DIM + c
        result[root_index, :] = permanent_rows(
            root_one[a], root_two[b], root_three[c]
        ).T
    return result


def target_tensor() -> sp.Matrix:
    result = sp.zeros(TENSOR_DIM, TENSOR_DIM)
    for colour in range(DIM):
        index = (colour * DIM + colour) * DIM + colour
        result[index, index] = 1
    return result


def exact_control(rank_h: int) -> None:
    rows = row_matrix(rank_h)
    assert rows.rank() == rank_h
    # The displayed root rows are the rows of H: source coordinates are
    # columns, so no additional transpose is taken here.
    h_map = rows
    derivative = transverse_derivative()
    singleton = derivative * h_map
    assert singleton.rank() == 3

    d_t = root_tensor(e(T), e(T), e(T))
    d_u = root_tensor(e(U), e(U), e(U))
    mixed = root_tensor(e(S), e(T), e(T)) + root_tensor(e(U), e(S), e(U))
    expected_u = sp.Matrix.hstack(d_t, d_u, mixed)
    assert expected_u.rank() == 3
    assert sp.Matrix.hstack(singleton, expected_u).rank() == 3

    empty = empty_tensor(rank_h)
    expected_empty = sp.zeros(TENSOR_DIM, TENSOR_DIM)
    expected_empty[0, 0] = 1
    assert empty == expected_empty
    d_s = root_tensor(e(S), e(S), e(S))
    assert sp.Matrix.hstack(expected_u, d_s).rank() == 4

    target_difference = target_tensor() - empty
    assert target_difference.rank() == 2
    for column in target_difference.columnspace():
        assert sp.Matrix.hstack(expected_u, column).rank() == 3

    root_one, root_two, root_three = control_rows(rank_h)
    a = root_one[T]
    b = root_two[U]
    v = root_one[S]
    q = root_three[S]
    assert permanent_rows(v, v, q) == root_tensor(e(S), e(S), e(S))
    assert permanent_rows(a, v, q) == sp.zeros(TENSOR_DIM, 1)
    assert permanent_rows(v, b, q) == sp.zeros(TENSOR_DIM, 1)
    assert permanent_rows(a, b, q) == sp.zeros(TENSOR_DIM, 1)

    v_space = sp.Matrix.hstack(a, b, v)
    assert v_space.rank() == 3
    if rank_h == 3:
        assert sp.Matrix.hstack(v_space, q).rank() == 3
    else:
        assert sp.Matrix.hstack(v_space, q).rank() == 4

    print(f"joint-rank-{rank_h} physical pole control: PASS")


def rational_pair_identity(rank_h: int) -> None:
    xs, xt, xu, ys, yt, yu, zs, zt, zu = sp.symbols(
        "xs xt xu ys yt yu zs zt zu"
    )
    extra = xs if rank_h == 3 else xt
    g_x = sp.Matrix([-xs, -extra, xs])
    g_y = sp.Matrix([0, ys, 0])
    g_z = sp.Matrix([zs, 0, zs])
    sensor = sp.Matrix.hstack(g_x, g_y, g_z)
    assert sp.factor(sensor.det()) == -2 * xs * ys * zs

    target_t = xt * yt * zt
    target_u = xu * yu * zu
    c_x = -target_t / (2 * xs)
    c_z = target_t / (2 * zs)
    c_y = target_u / ys - extra * target_t / (2 * xs * ys)
    residual = sp.simplify(sensor * sp.Matrix([c_x, c_y, c_z]))
    assert residual == sp.Matrix([target_t, target_u, 0])
    assert xs in sp.denom(sp.together(c_x)).free_symbols
    assert zs in sp.denom(sp.together(c_z)).free_symbols
    assert ys in sp.denom(sp.together(c_y)).free_symbols
    print(f"joint-rank-{rank_h} rational pair lift: PASS (coordinate poles exposed)")


def main() -> None:
    derivative_normal_form()
    lower_rank_atlas()
    support_boundary()
    for rank_h in (3, 4):
        exact_control(rank_h)
        rational_pair_identity(rank_h)
    print("lower-joint-rank transverse two-root theorem: PASS")


if __name__ == "__main__":
    main()
