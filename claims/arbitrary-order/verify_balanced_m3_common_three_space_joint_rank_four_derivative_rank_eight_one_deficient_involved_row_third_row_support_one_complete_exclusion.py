#!/usr/bin/env python3
"""Exact SymPy replay for the S2CA mixed support-one exclusion."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

N = 3
W_DIM = 3 * N


def i3(a: int, b: int, c: int) -> int:
    return N * N * a + N * b + c


def basis(i: int) -> sp.Matrix:
    return sp.eye(N)[:, i]


def source_basis(block: int, colour: int) -> sp.Matrix:
    out = sp.zeros(W_DIM, 1)
    out[block * N + colour] = 1
    return out


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


def projection_matrix(vectors: list[sp.Matrix], block: int) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(vector[block * N : (block + 1) * N, :] for vector in vectors)
    )


def polarized(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    vectors = (a, b, c)
    out = sp.zeros(N**3, 1)
    for order in permutations(range(3)):
        left = vectors[order[0]][0:N, :]
        middle = vectors[order[1]][N : 2 * N, :]
        right = vectors[order[2]][2 * N : 3 * N, :]
        out += outer3(left, middle, right)
    return out


def is_zero(vector: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in vector)


def check_mixed_four_space_and_direct_box() -> None:
    zero = sp.zeros(N, 1)
    for d, s, t in permutations(range(N)):
        x = basis(s)
        y = basis(d) + basis(t)
        b = basis(d) - basis(t)
        w = basis(s) + basis(t)
        C = basis(d) * basis(d).T + basis(t) * basis(s).T
        derivative = derivative_matrix(x, y, w, C)
        assert derivative.rank() == 8

        syzygy = x.col_join(y).col_join(zero)
        vertical = zero.col_join(zero).col_join(basis(d))
        split = zero.col_join(-basis(s)).col_join(zero)
        fourth = (2 * basis(t)).col_join(b).col_join(basis(t))
        K = [syzygy, vertical, split, fourth]
        K_matrix = sp.Matrix.hstack(*K)
        assert K_matrix.rank() == 4
        assert [projection_matrix(K, block).rank() for block in range(3)] == [
            2,
            3,
            2,
        ]
        assert (derivative * K_matrix).rank() == 3
        assert is_zero(derivative * syzygy)

        root_box = [
            outer3(basis(i), basis(j), basis(k))
            for i in (s, t)
            for j in range(N)
            for k in (d, t)
        ]
        U = [derivative * vector for vector in K[1:]]
        assert sp.Matrix.hstack(*root_box).rank() == 12
        assert sp.Matrix.hstack(*U).rank() == 3
        assert sp.Matrix.hstack(*root_box, *U).rank() == 15

        c_bar = basis(t) * basis(s).T
        rep_d = -c_tensor(c_bar, basis(d))
        rep_s = -outer3(basis(s), basis(s), basis(t))
        ddd = outer3(basis(d), basis(d), basis(d))
        sss = outer3(basis(s), basis(s), basis(s))
        assert is_zero(ddd - rep_d - U[0])
        assert is_zero(sss - rep_s - U[1])


def check_root_row_elimination() -> None:
    y_d, b_d, y_t, b_t = sp.symbols("y_d b_d y_t b_t")
    A, B = sp.symbols("A B")
    row_change = sp.Matrix([[y_d, b_d], [y_t, b_t]])
    assert sp.factor(row_change.det()) == b_t * y_d - b_d * y_t
    equations = row_change * sp.Matrix([A, B])
    recovered = row_change.inv() * equations
    assert all(sp.simplify(recovered[i] - (A, B)[i]) == 0 for i in range(2))

    cube = sp.symbols("cube", nonzero=True)
    after_first_face = sp.Matrix(
        [b_d * cube, b_t * cube]
    )
    assert after_first_face[0] == b_d * cube
    assert after_first_face[1] == b_t * cube
    # The tdt zero and nonzero ttt target force b_d=0 and b_t!=0.
    assert sp.solve(after_first_face[0], b_d) == [0]


def resonance_vectors(t: int) -> tuple[sp.Matrix, sp.Matrix, sp.Expr]:
    omega = (-1 + sp.sqrt(-3)) / 2
    assert sp.simplify(omega**2 + omega + 1) == 0
    x = source_basis(0, t)
    y = source_basis(1, t)
    z = source_basis(2, t)
    v = x + y + z
    u = x + omega * y + omega**2 * z
    return u, v, omega


def check_resonance_and_dual_row_collapse() -> None:
    for d, s, t in permutations(range(N)):
        del s
        u, v, omega = resonance_vectors(t)
        target_t = outer3(basis(t), basis(t), basis(t))
        target_d = outer3(basis(d), basis(d), basis(d))

        assert is_zero(polarized(u, v, v))
        assert is_zero(polarized(u, u, v))
        assert is_zero(polarized(v, v, v) - 6 * target_t)
        assert sp.simplify(1 + omega + omega**2) == 0
        assert sp.simplify(omega + omega**2 + omega**3) == 0

        tangent = sp.Matrix.hstack(
            *(polarized(source_basis(block, colour), v, v)
              for block in range(3)
              for colour in range(N))
        )
        first_map = [
            polarized(v, u, source_basis(block, colour))
            for block in range(3)
            for colour in range(N)
        ]
        second_map = [
            polarized(u, u, source_basis(block, colour))
            for block in range(3)
            for colour in range(N)
        ]
        assert tangent.rank() == 7
        assert sp.Matrix.hstack(tangent, *first_map, *second_map).rank() == 7
        assert sp.Matrix.hstack(tangent, target_d).rank() == 8

        stacked_columns = [
            first_map[index].col_join(second_map[index])
            for index in range(W_DIM)
        ]
        stacked = sp.Matrix.hstack(*stacked_columns)
        assert stacked.rank() == 8
        kernel = stacked.nullspace()
        assert len(kernel) == 1
        assert sp.Matrix.hstack(kernel[0], v).rank() == 1


def check_scalar_kernel_symbolically() -> None:
    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    gamma = -alpha - beta
    resonance = alpha**2 + alpha * beta + beta**2
    rows = sp.Matrix(
        [
            [alpha, beta, gamma],
            [beta * gamma, alpha * gamma, alpha * beta],
        ]
    )
    ones = sp.ones(3, 1)
    products = rows * ones
    assert sp.expand(products[0]) == 0
    assert sp.expand(products[1] + resonance) == 0
    minor = sp.factor(rows[:, :2].det())
    assert sp.simplify(minor - gamma * (alpha - beta) * (alpha + beta)) == 0


def main() -> None:
    check_mixed_four_space_and_direct_box()
    check_root_row_elimination()
    check_resonance_and_dual_row_collapse()
    check_scalar_kernel_symbolically()
    print(
        "S2CA primary replay passed: mixed four-space; direct 12-box; "
        "root-row elimination; exact cubic resonance; tangent separation; "
        "dual-row collapse."
    )


if __name__ == "__main__":
    main()
