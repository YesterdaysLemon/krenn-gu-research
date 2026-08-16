#!/usr/bin/env python3
"""Exact replay for the S2BX same-colour (2,2,3) exclusion."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

N = 3


def i2(a: int, b: int) -> int:
    return N * a + b


def i3(a: int, b: int, c: int) -> int:
    return N * N * a + N * b + c


def basis(i: int) -> sp.Matrix:
    return sp.eye(N)[:, i]


def outer3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.MutableDenseNDimArray:
    out = sp.MutableDenseNDimArray.zeros(N, N, N)
    for i, j, k in product(range(N), repeat=3):
        out[i, j, k] = a[i] * b[j] * c[k]
    return out


def add_tensor(
    left: sp.MutableDenseNDimArray,
    right: sp.MutableDenseNDimArray,
    scalar: sp.Expr | None = None,
) -> sp.MutableDenseNDimArray:
    if scalar is None:
        scalar = sp.Integer(1)
    out = sp.MutableDenseNDimArray.zeros(N, N, N)
    for index in product(range(N), repeat=3):
        out[index] = sp.expand(left[index] + scalar * right[index])
    return out


def tensor_equal(
    left: sp.MutableDenseNDimArray, right: sp.MutableDenseNDimArray
) -> bool:
    return all(
        sp.expand(left[index] - right[index]) == 0
        for index in product(range(N), repeat=3)
    )


def flatten(tensor: sp.MutableDenseNDimArray, mode: int) -> sp.Matrix:
    rows: list[list[sp.Expr]] = []
    for fixed in range(N):
        row: list[sp.Expr] = []
        for first in range(N):
            for second in range(N):
                index = [0, 0, 0]
                index[mode] = fixed
                free = [slot for slot in range(N) if slot != mode]
                index[free[0]] = first
                index[free[1]] = second
                row.append(tensor[tuple(index)])
        rows.append(row)
    return sp.Matrix(rows)


def permanent_tensor() -> sp.MutableDenseNDimArray:
    out = sp.MutableDenseNDimArray.zeros(N, N, N)
    for sigma in permutations(range(N)):
        out[sigma] += 1
    return out


def check_missing_row_correction() -> None:
    kappa = sp.symbols("kappa", nonzero=True)
    d, s, t = 0, 1, 2
    columns = []
    for c in (d, s, t):
        column = sp.zeros(N * N, 1)
        column[i2(d, c)] = kappa
        columns.append(column)
    contraction = sp.Matrix.hstack(*columns)
    target = sp.zeros(N * N, 1)
    target[i2(d, d)] = -1
    solution = sp.Matrix([-1 / kappa, 0, 0])
    assert contraction.rank() == 3
    assert contraction * solution == target
    assert contraction.gauss_jordan_solve(target)[0] == solution


def check_permanent_rank_interface() -> None:
    p3 = permanent_tensor()
    for mode in range(N):
        assert flatten(p3, mode).rank() == 3

    # The exact four-cube polarization of 6*x*y*z.
    signs = (
        (sp.Integer(1), sp.Matrix([1, 1, 1])),
        (sp.Integer(-1), sp.Matrix([1, 1, -1])),
        (sp.Integer(-1), sp.Matrix([1, -1, 1])),
        (sp.Integer(-1), sp.Matrix([-1, 1, 1])),
    )
    decomposition = sp.MutableDenseNDimArray.zeros(N, N, N)
    for coefficient, vector in signs:
        decomposition = add_tensor(
            decomposition, outer3(vector, vector, vector), coefficient / 4
        )
    assert tensor_equal(p3, decomposition)

    # Every matrix in the first slice space has this form.  Its three
    # principal 2x2 minors force x=y=z=0 if it has rank at most one.
    x, y, z = sp.symbols("x y z")
    slice_matrix = sp.Matrix([[0, z, y], [z, 0, x], [y, x, 0]])
    principal_minors = [
        slice_matrix.extract(rows, rows).det()
        for rows in ((0, 1), (0, 2), (1, 2))
    ]
    assert principal_minors == [-z**2, -y**2, -x**2]
    assert sp.groebner(principal_minors, x, y, z).is_zero_dimensional

    diagonal = sp.MutableDenseNDimArray.zeros(N, N, N)
    for colour, coefficient in enumerate((2, 3, 5)):
        diagonal[colour, colour, colour] = coefficient
    for mode in range(N):
        assert flatten(diagonal, mode).rank() == 3


def binary_value(a: int, b: int, c: int) -> sp.Matrix:
    """Coordinates on the two fully transverse target lines."""
    if a == b == c == 0:
        return sp.Matrix([1, 0])
    if a == b == c == 1:
        return sp.Matrix([0, 1])
    return sp.zeros(2, 1)


def check_binary_kernel_shifts() -> None:
    lam_0, lam_1 = sp.symbols("lam_0 lam_1")
    for a, b, c in product(range(2), range(2), range(2)):
        original = binary_value(a, b, c)
        kernel_value = sp.zeros(2, 1)
        shifted = original + (lam_0 if c == 0 else lam_1) * kernel_value
        assert shifted == original

    # q_d,q_0,q_1,h is an abstract basis of the four-space.  A line
    # ell=a*q_0+b*q_1+c*q_d belongs to the shifted plane exactly when
    # c=a*lambda_0+b*lambda_1.
    qd = sp.Matrix([1, 0, 0, 0])
    q0 = sp.Matrix([0, 1, 0, 0])
    q1 = sp.Matrix([0, 0, 1, 0])
    a, b, c = sp.symbols("a b c")
    shifted_0 = q0 + lam_0 * qd
    shifted_1 = q1 + lam_1 * qd
    ell = a * q0 + b * q1 + c * qd
    residual = sp.simplify(ell - a * shifted_0 - b * shifted_1)
    assert residual == (c - a * lam_0 - b * lam_1) * qd

    # Exact representatives of all three nonempty support masks for (a,b).
    for aa, bb, cc in ((2, 0, 3), (0, -2, 5), (2, -3, 7)):
        if aa:
            ll_0, ll_1 = sp.Rational(cc, aa), sp.Integer(0)
        else:
            ll_0, ll_1 = sp.Integer(0), sp.Rational(cc, bb)
        ell_value = aa * q0 + bb * q1 + cc * qd
        shifted_value = aa * (q0 + ll_0 * qd) + bb * (q1 + ll_1 * qd)
        assert ell_value == shifted_value
        assert sp.Matrix.hstack(
            q0 + ll_0 * qd, q1 + ll_1 * qd, ell_value
        ).rank() == 2

    # The endpoint mask a=b=0 is precisely the kernel line.
    endpoint = 11 * qd
    assert sp.Matrix.hstack(qd, endpoint).rank() == 1


def check_projection_dimensions() -> None:
    # Canonical four-space model for the dimension step only: Q is a
    # hyperplane and Q_0 a plane.  Any two-plane disjoint from Q_0 meets Q
    # in exactly one line.
    qd = sp.Matrix([1, 0, 0, 0])
    q0 = sp.Matrix([0, 1, 0, 0])
    q1 = sp.Matrix([0, 0, 1, 0])
    h = sp.Matrix([0, 0, 0, 1])
    q_space = sp.Matrix.hstack(qd, q0, q1)
    q_binary = sp.Matrix.hstack(q0, q1)
    for line in (qd, qd + 2 * q0 - 3 * q1):
        plane = sp.Matrix.hstack(line, h)
        assert plane.rank() == 2
        assert plane.row_join(q_binary).rank() == 4
        assert plane.row_join(q_space).rank() == 4
        assert plane.cols + q_space.cols - plane.row_join(q_space).rank() == 1


def main() -> None:
    check_missing_row_correction()
    check_permanent_rank_interface()
    check_binary_kernel_shifts()
    check_projection_dimensions()
    print(
        "S2BX primary replay passed: unique correction line; P3 rank-four "
        "interface; exact binary table shifts; four-space kernel-line trap."
    )


if __name__ == "__main__":
    main()
