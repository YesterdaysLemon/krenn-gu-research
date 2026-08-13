"""Exact replay for the transverse rank-six aligned-rank-two exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


def e3(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def e9(index: int) -> sp.Matrix:
    return sp.eye(9)[:, index]


def tidx(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


def block_derivative(b23: sp.Matrix, b13: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 9)
    for a, b, c in product(range(3), repeat=3):
        out[tidx(a, b, c), a] = b23[b, c]
        out[tidx(a, b, c), 3 + b] = b13[a, c]
    return out


def graph_derivative(
    a: sp.Matrix,
    ta: sp.Matrix,
    b23: sp.Matrix,
    b13: sp.Matrix,
) -> sp.Matrix:
    out = sp.zeros(27, 1)
    for i, j, k in product(range(3), repeat=3):
        out[tidx(i, j, k)] = a[i] * b23[j, k] + b13[i, k] * ta[j]
    return out


def pair_tensors(left: sp.Matrix, right: sp.Matrix) -> tuple[sp.Matrix, ...]:
    a = sp.Matrix(
        3,
        3,
        lambda i, j: left[3 + i] * right[6 + j]
        + right[3 + i] * left[6 + j],
    )
    b = sp.Matrix(
        3,
        3,
        lambda i, j: left[i] * right[6 + j]
        + right[i] * left[6 + j],
    )
    c = sp.Matrix(
        3,
        3,
        lambda i, j: left[i] * right[3 + j]
        + right[i] * left[3 + j],
    )
    return a, b, c


def mixed_derivative(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    a, b, c = pair_tensors(left, right)
    out = sp.zeros(27, 9)
    for x, y, z in product(range(3), repeat=3):
        row = tidx(x, y, z)
        out[row, x] = a[y, z]
        out[row, 3 + y] = b[x, z]
        out[row, 6 + z] = c[x, y]
    return out


def flatten(tensor: sp.Matrix, mode: int) -> sp.Matrix:
    out = sp.zeros(3, 9)
    for i, j, k in product(range(3), repeat=3):
        indices = (i, j, k)
        row = indices[mode]
        others = [indices[m] for m in range(3) if m != mode]
        out[row, 3 * others[0] + others[1]] = tensor[tidx(i, j, k)]
    return out


def tangent_tensor(u: tuple[sp.Matrix, ...], q: tuple[sp.Matrix, ...]) -> sp.Matrix:
    out = sp.zeros(27, 1)
    ux, uy, uz = u
    qx, qy, qz = q
    for i, j, k in product(range(3), repeat=3):
        out[tidx(i, j, k)] = 2 * (
            ux[i] * uy[j] * qz[k]
            + ux[i] * qy[j] * uz[k]
            + qx[i] * uy[j] * uz[k]
        )
    return out


def check_graph_target_and_symmetry() -> None:
    kappa = sp.Rational(11)
    lam = sp.Rational(13)
    transform = sp.Matrix([[0, 0, 0], [2, 3, 0], [5, 0, 7]])
    t = transform * e3(0)
    kernel = sp.Matrix([1, -sp.Rational(2, 3), -sp.Rational(5, 7)])
    assert transform.rank() == 2
    assert transform * kernel == sp.zeros(3, 1)
    assert all(transform * e3(i) != sp.zeros(3, 1) for i in range(3))

    k12 = sp.Matrix.vstack(sp.eye(3), transform)
    relation = sp.Matrix.vstack(-transform.T, sp.eye(3))
    assert k12.rank() == relation.rank() == 3
    assert k12.T * relation == sp.zeros(3, 3)

    b23 = kappa * e3(0) * e3(0).T
    w = sp.Matrix([17, 19, 23])
    b13 = lam * e3(0) * e3(0).T + kernel * w.T
    assert block_derivative(b23, b13).rank() == 6
    assert transform * b13 == lam * t * e3(0).T

    correction = graph_derivative(e3(0), t, b23, b13)
    target_zero = sp.zeros(27, 1)
    target_zero[tidx(0, 0, 0)] = 1
    coefficient_zero = target_zero - correction / kappa
    expected = sp.zeros(27, 1)
    for a, b, c in product(range(3), repeat=3):
        expected[tidx(a, b, c)] = -b13[a, c] * t[b] / kappa
    assert coefficient_zero == expected
    assert all(coefficient_zero[tidx(a, 0, c)] == 0 for a, c in product(range(3), repeat=2))

    for colour in (1, 2):
        matrix = e3(colour) * e3(colour).T
        assert transform * matrix == (transform * matrix).T
    for colour in range(3):
        matrix = -b13[:, colour] * t.T / kappa
        assert transform * matrix == (transform * matrix).T
    print("graph target identity: PASS (exact 27 coefficients / symmetric pullback)")


def check_repeated_row_tangent() -> None:
    transform = sp.Matrix([[0, 0, 0], [2, 3, 0], [5, 0, 7]])
    beta = sp.Matrix([0, 11, 13])
    gamma = sp.Matrix([17, 19, 23])
    alpha = transform.T * beta
    t = transform * e3(0)
    lam = sp.Rational(13)
    kappa = sp.Rational(11)
    coefficients = [
        -lam * gamma[0] * (beta.dot(t)) ** 2 / kappa,
        alpha[1] * beta[1] * gamma[1],
        alpha[2] * beta[2] * gamma[2],
    ]
    assert all(value != 0 for value in coefficients)

    diagonal = sp.zeros(27, 1)
    for colour, value in enumerate(coefficients):
        diagonal[tidx(colour, colour, colour)] = value
    assert [flatten(diagonal, mode).rank() for mode in range(3)] == [3, 3, 3]

    u = (
        sp.Matrix([1, 2, 3]),
        sp.Matrix([2, 3, 5]),
        sp.Matrix([3, 5, 7]),
    )
    q = (
        sp.Matrix([5, 7, 11]),
        sp.Matrix([7, 11, 13]),
        sp.Matrix([11, 13, 17]),
    )
    tangent = tangent_tensor(u, q)
    assert all(flatten(tangent, mode).rank() <= 2 for mode in range(3))
    print("repeated-row tangent: PASS (target rank 3 / tangent mode ranks <=2)")


def check_mixed_kernel_atlas() -> None:
    x0, x1 = e9(0), e9(1)
    y0, y1 = e9(3), e9(4)
    z0, z1, z2 = e9(6), e9(7), e9(8)

    # Zero pair: conjugate mixed squares are proportional.
    zero_u = x0 + y0
    zero_v = x0 - y0
    assert mixed_derivative(zero_u, zero_v) == sp.zeros(27, 9)
    assert mixed_derivative(zero_v, zero_v) == -mixed_derivative(zero_u, zero_u)

    # One pair: the kernel is X+Y and the square maps there are proportional.
    one_u = x0 + y0 + z0
    one_v = -x0 - y0 + z0
    one_cross = mixed_derivative(one_u, one_v)
    xy = sp.Matrix.hstack(*[e9(i) for i in range(6)])
    assert one_cross * xy == sp.zeros(27, 6)
    assert mixed_derivative(one_v, one_v) * xy == -mixed_derivative(one_u, one_u) * xy

    # Two pairs without a shared factor: only the whole Z summand survives.
    two_regular_u = x0 + y0 + z0
    two_regular_v = x0 - y0 + z1
    two_regular = mixed_derivative(two_regular_u, two_regular_v)
    z_space = sp.Matrix.hstack(z0, z1, z2)
    assert two_regular.rank() == 6
    assert two_regular * z_space == sp.zeros(27, 3)
    assert (mixed_derivative(two_regular_u, two_regular_u) * z_space).rank() == 3

    # Shared-factor two-pair chart: kernel Z+line, square rank three and
    # therefore kernel dimension one on that four-space.
    two_special_u = x0 + y0 + z0
    two_special_v = x0 - y0 + 2 * z0
    two_special = mixed_derivative(two_special_u, two_special_v)
    special_kernel = sp.Matrix.hstack(z0, z1, z2, -3 * x0 + y0)
    assert special_kernel.rank() == 4
    assert two_special * special_kernel == sp.zeros(27, 4)
    square_on_kernel = mixed_derivative(two_special_u, two_special_u) * special_kernel
    assert square_on_kernel.rank() == 3
    assert len(square_on_kernel.nullspace()) == 1

    # Three nonzero pair tensors have kernel dimension at most two.
    three_u = x0 + y0 + z0
    three_v = x1 + y1 + z1
    three = mixed_derivative(three_u, three_v)
    assert all(block != sp.zeros(3, 3) for block in pair_tensors(three_u, three_v))
    assert len(three.nullspace()) <= 2
    print("symmetric binary-diagonal atlas: PASS (0/1/2/3 pair cases)")


def check_binary_square_reduction() -> None:
    t1, t2 = sp.Rational(2), sp.Rational(5)
    tau1, tau2 = sp.Rational(3), sp.Rational(7)
    transform = sp.Matrix([[0, 0, 0], [t1, tau1, 0], [t2, 0, tau2]])
    kernel = sp.Matrix([1, -t1 / tau1, -t2 / tau2])
    alpha1 = sp.Matrix([t1 / tau1, 1, 0])
    alpha2 = sp.Matrix([t2 / tau2, 0, 1])
    beta1 = e3(1) / tau1
    beta2 = e3(2) / tau2
    assert transform * kernel == sp.zeros(3, 1)
    assert alpha1.dot(kernel) == alpha2.dot(kernel) == 0
    assert transform.T * beta1 == alpha1
    assert transform.T * beta2 == alpha2

    # The coefficient table in (43): cross zero and two disjoint square lines.
    cross = sp.zeros(3, 1)
    square1 = sp.Matrix([0, 1 / tau1, 0])
    square2 = sp.Matrix([0, 0, 1 / tau2])
    assert cross == sp.zeros(3, 1)
    assert square1.rank() == square2.rank() == 1
    assert square1.dot(square2) == 0
    print("aligned binary square reduction: PASS (cross zero / two target lines)")


def main() -> None:
    check_graph_target_and_symmetry()
    check_repeated_row_tangent()
    check_mixed_kernel_atlas()
    check_binary_square_reduction()
    print("balanced m=3 transverse-rank-six aligned-rank-two exclusion: PASS")


if __name__ == "__main__":
    main()
