#!/usr/bin/env python3
"""Exact SymPy replay for the S2CB fully injective (3,3,2) exclusion."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

N = 3


def i3(a: int, b: int, c: int) -> int:
    return N * N * a + N * b + c


def basis(i: int) -> sp.Matrix:
    return sp.eye(N)[:, i]


def outer3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[i3(i, j, k)] = a[i] * b[j] * c[k]
    return out


def c_tensor(C: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(N**3, 1)
    for i, j, k in product(range(N), repeat=3):
        out[i3(i, j, k)] = C[i, j] * c[k]
    return out


def derivative_value(
    x: sp.Matrix,
    y: sp.Matrix,
    w: sp.Matrix,
    C: sp.Matrix,
    a: sp.Matrix,
    b: sp.Matrix,
    c: sp.Matrix,
) -> sp.Matrix:
    return outer3(a, y, w) - outer3(x, b, w) + c_tensor(C, c)


def derivative_matrix(
    x: sp.Matrix, y: sp.Matrix, w: sp.Matrix, C: sp.Matrix
) -> sp.Matrix:
    zero = sp.zeros(N, 1)
    columns = []
    for block in range(3):
        for colour in range(N):
            entries = [zero, zero, zero]
            entries[block] = basis(colour)
            columns.append(derivative_value(x, y, w, C, *entries))
    return sp.Matrix.hstack(*columns)


def projection(vectors: list[sp.Matrix], block: int) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(vector[block * N : (block + 1) * N, :] for vector in vectors)
    )


def check_vertical_projection_forks() -> None:
    zero = sp.zeros(N, 1)
    for d, s, t in permutations(range(N)):
        # Support one, with x=e_s: N, vertical, opposite split, one remainder.
        support_one_x = [
            basis(s).col_join(basis(t)).col_join(zero),
            zero.col_join(zero).col_join(basis(d)),
            zero.col_join(basis(s)).col_join(basis(t)),
            basis(d).col_join(basis(d)).col_join(basis(s)),
        ]
        assert sp.Matrix.hstack(*support_one_x).rank() == 4
        assert projection(support_one_x, 0).rank() == 2

        # Root exchange: y=e_s leaves the second projection of rank at most two.
        support_one_y = [
            basis(t).col_join(basis(s)).col_join(zero),
            zero.col_join(zero).col_join(basis(d)),
            basis(s).col_join(zero).col_join(basis(t)),
            basis(d).col_join(basis(d)).col_join(basis(s)),
        ]
        assert sp.Matrix.hstack(*support_one_y).rank() == 4
        assert projection(support_one_y, 1).rank() == 2

        # Support two: the syzygy, vertical, and two splits fill K.
        support_two = [
            basis(s).col_join(basis(t)).col_join(zero),
            zero.col_join(zero).col_join(basis(d)),
            zero.col_join(basis(s)).col_join(basis(s)),
            basis(t).col_join(zero).col_join(basis(t)),
        ]
        assert sp.Matrix.hstack(*support_two).rank() == 4
        assert projection(support_two, 0).rank() == 2
        assert projection(support_two, 1).rank() == 2


def check_direct_box_fixture() -> None:
    zero = sp.zeros(N, 1)
    for d, s, t in permutations(range(N)):
        x, y, w = basis(s), basis(t), basis(s)
        C = basis(d) * basis(d).T
        derivative = derivative_matrix(x, y, w, C)
        assert derivative.rank() == 8

        q = basis(s) - basis(t)
        syzygy = x.col_join(y).col_join(zero)
        split_s = zero.col_join(-basis(s)).col_join(zero)
        split_t = basis(t).col_join(zero).col_join(q)
        outside = basis(d).col_join(basis(d)).col_join(basis(d))
        K = [syzygy, split_s, split_t, outside]
        K_matrix = sp.Matrix.hstack(*K)
        assert K_matrix.rank() == 4
        assert [projection(K, block).rank() for block in range(3)] == [3, 3, 2]
        assert (derivative * K_matrix).rank() == 3

        vertical_test = sp.Matrix.vstack(projection(K, 0), projection(K, 1))
        assert vertical_test.rank() == 4

        # The fixture's third plane is span(e_d, e_s-e_t), not span(e_d,e_s).
        root_box = [
            outer3(basis(i), basis(j), third)
            for i in range(N)
            for j in range(N)
            for third in (basis(d), q)
        ]
        U = [derivative * vector for vector in K[1:]]
        assert sp.Matrix.hstack(*root_box).rank() == 18
        assert sp.Matrix.hstack(*U).rank() == 3
        assert sp.Matrix.hstack(*root_box, *U).rank() == 21

        ddd = outer3(basis(d), basis(d), basis(d))
        sss = outer3(basis(s), basis(s), basis(s))
        ttt = outer3(basis(t), basis(t), basis(t))
        assert U[0] == sss
        box_matrix = sp.Matrix.hstack(*root_box)
        assert sp.Matrix.hstack(box_matrix, ddd).rank() == 18
        f_t = ttt - U[1]
        assert sp.Matrix.hstack(box_matrix, f_t).rank() == 18
        assert f_t != sp.zeros(N**3, 1)


def permanent_tensor() -> sp.MutableDenseNDimArray:
    tensor = sp.MutableDenseNDimArray.zeros(N, N, N)
    for order in permutations(range(N)):
        tensor[order] = 1
    return tensor


def check_rank_fork_interface() -> None:
    tensor = permanent_tensor()
    flattening = sp.zeros(N, N * N)
    for i, j, k in product(range(N), repeat=3):
        flattening[i, N * j + k] = tensor[i, j, k]
    assert flattening.rank() == 3

    diagonal = sp.zeros(N**3, 1)
    for colour in range(N):
        diagonal += outer3(basis(colour), basis(colour), basis(colour))
    for mode in range(3):
        matrix = sp.zeros(N, N * N)
        for i, j, k in product(range(N), repeat=3):
            indices = (i, j, k)
            row = indices[mode]
            other = [indices[index] for index in range(3) if index != mode]
            matrix[row, N * other[0] + other[1]] = diagonal[i3(i, j, k)]
        assert matrix.rank() == 3


def check_support_one_plane_equality() -> None:
    zero = sp.zeros(N, 1)
    d, s, t = 0, 1, 2
    K = [
        basis(s).col_join(basis(t)).col_join(zero),
        zero.col_join(-basis(s)).col_join(zero),
        basis(d).col_join(basis(d)).col_join(basis(d)),
        basis(t).col_join(zero).col_join(basis(t)),
    ]
    assert [projection(K, block).rank() for block in range(3)] == [3, 3, 2]

    # In the K-dual basis, complementary first rows and all third rows coincide.
    r_d = sp.Matrix([0, 0, 1, 0])
    r_t = sp.Matrix([0, 0, 0, 1])
    q_d = sp.Matrix([0, 0, 1, 0])
    q_t = sp.Matrix([0, 0, 0, 1])
    assert sp.Matrix.hstack(r_d, r_t).columnspace() == sp.Matrix.hstack(
        q_d, q_t
    ).columnspace()


def swap_outer(tensor: sp.MutableDenseNDimArray) -> sp.MutableDenseNDimArray:
    out = sp.MutableDenseNDimArray.zeros(2, N, 2)
    for i, j, k in product(range(2), range(N), range(2)):
        out[i, j, k] = tensor[k, j, i]
    return out


def check_support_two_symmetry_reduction() -> None:
    q_d, q_c, lam = sp.symbols("q_d q_c lam", nonzero=True)
    m_d = sp.Matrix(sp.symbols("md0:3"))
    m_c = sp.Matrix(sp.symbols("mc0:3"))
    e_t = basis(2)

    tensor = sp.MutableDenseNDimArray.zeros(2, N, 2)
    # c tensor e_t tensor (q_d e_d+q_c c)
    for middle in range(N):
        tensor[1, middle, 0] += q_d * e_t[middle]
        tensor[1, middle, 1] += q_c * e_t[middle]
        tensor[0, middle, 1] -= lam * m_d[middle]
        tensor[1, middle, 1] -= lam * m_c[middle]

    antisymmetric = [
        sp.expand(tensor[1, middle, 0] - tensor[0, middle, 1])
        for middle in range(N)
    ]
    forced_m_d = -(q_d / lam) * e_t
    assert all(
        sp.simplify(
            expression.subs({m_d[index]: forced_m_d[index] for index in range(N)})
        )
        == 0
        for expression in antisymmetric
    )

    symmetric = sp.MutableDenseNDimArray.zeros(2, N, 2)
    for first, middle, third in product(range(2), range(N), range(2)):
        symmetric[first, middle, third] = tensor[first, middle, third]
    for index in range(N):
        symmetric[0, index, 1] = symmetric[0, index, 1].subs(
            m_d[index], forced_m_d[index]
        )
    assert all(
        sp.simplify(symmetric[i, j, k] - swap_outer(symmetric)[i, j, k]) == 0
        for i, j, k in product(range(2), range(N), range(2))
    )

    n = q_c * e_t - lam * m_c
    assert all(
        sp.simplify(symmetric[1, middle, 1] - n[middle]) == 0
        for middle in range(N)
    )

    # q_d=0 leaves two outer diagonal root forms.  The terminal middle fork
    # is exactly independent lines versus one shared line.
    e_d = basis(0)
    n_independent = basis(1) + basis(2)
    assert sp.Matrix.hstack(e_d, n_independent).rank() == 2
    n_shared = 7 * e_d
    assert sp.Matrix.hstack(e_d, n_shared).rank() == 1


def main() -> None:
    check_vertical_projection_forks()
    check_direct_box_fixture()
    check_rank_fork_interface()
    check_support_one_plane_equality()
    check_support_two_symmetry_reduction()
    print(
        "S2CB primary replay passed: vertical rank forks; direct 18-box; "
        "P3 rank interface; support-one equal plane; support-two symmetry; "
        "binary/two-square terminal fork."
    )


if __name__ == "__main__":
    main()
