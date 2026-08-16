#!/usr/bin/env python3
"""Exact replay for the diagonal coordinate-endpoint full-target reduction."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def basis_vector(size: int, index: int) -> sp.Matrix:
    out = sp.zeros(size, 1)
    out[index] = 1
    return out


def tensor3(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 1)
    for i, j, k in product(range(3), repeat=3):
        out[9 * i + 3 * j + k] = u[i] * v[j] * w[k]
    return out


def polarized_product(
    u: sp.Matrix, v: sp.Matrix, w: sp.Matrix
) -> sp.Matrix:
    def blocks(row: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
        return row[:3, :], row[3:6, :], row[6:9, :]

    values = (blocks(u), blocks(v), blocks(w))
    out = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        out += tensor3(
            values[sigma[0]][0],
            values[sigma[1]][1],
            values[sigma[2]][2],
        )
    return sp.simplify(out)


def check_full_coefficient_identity() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    a = [
        sp.Matrix([sp.symbols(f"a{c}{i}") for i in range(3)])
        for c in range(3)
    ]
    b = [
        sp.Matrix([sp.symbols(f"b{c}{i}") for i in range(3)])
        for c in range(3)
    ]

    targets = [basis_vector(6, i) for i in range(3)]
    sources = [basis_vector(6, 3 + i) for i in range(3)]
    h_tensors = [a[c] * y.T - x * b[c].T for c in range(3)]

    p = [[[
        sp.zeros(6, 1) for _k in range(3)
    ] for _j in range(3)] for _i in range(3)]
    for i, j, k in product(range(3), repeat=3):
        value = sp.zeros(6, 1)
        if i == j == k:
            value += targets[i]
        if k == 0:
            for c in range(3):
                value += h_tensors[c][i, j] * sources[c]
        if i == 2 and j == 2:
            value += lam * sources[k]
        p[i][j][k] = value

        direct = sp.zeros(6, 1)
        if i == j == k:
            direct += targets[i]
        for c in range(3):
            tangent = int(k == 0) * (
                a[c][i] * y[j] - x[i] * b[c][j]
            )
            residual = lam * int(i == 2 and j == 2 and k == c)
            direct += (tangent + residual) * sources[c]
        assert sp.simplify(value - direct) == sp.zeros(6, 1)

    for c in range(3):
        t = sp.symbols(f"t{c}")
        shifted = (a[c] + t * x) * y.T - x * (b[c] + t * y).T
        assert sp.simplify(shifted - h_tensors[c]) == sp.zeros(3, 3)

    for i, j in product(range(3), repeat=2):
        expected_1 = (
            (targets[1] if i == j == 1 else sp.zeros(6, 1))
            + (lam * sources[1] if i == j == 2 else sp.zeros(6, 1))
        )
        expected_2 = (
            (targets[2] if i == j == 2 else sp.zeros(6, 1))
            + (lam * sources[2] if i == j == 2 else sp.zeros(6, 1))
        )
        assert sp.simplify(p[i][j][1] - expected_1) == sp.zeros(6, 1)
        assert sp.simplify(p[i][j][2] - expected_2) == sp.zeros(6, 1)

    assert sp.simplify(p[2][2][1] / lam - sources[1]) == sp.zeros(6, 1)
    assert sp.simplify(
        (p[2][2][2] - targets[2]) / lam - sources[2]
    ) == sp.zeros(6, 1)

    c_matrix = sp.zeros(3, 3)
    c_matrix[2, 2] = lam
    kappa = c_matrix + h_tensors[0]
    residual = [[sp.zeros(6, 1) for _j in range(3)] for _i in range(3)]
    for i, j in product(range(3), repeat=2):
        value = p[i][j][0]
        if i == j == 0:
            value -= targets[0]
        value -= h_tensors[1][i, j] * sources[1]
        value -= h_tensors[2][i, j] * sources[2]
        residual[i][j] = sp.simplify(value)
        assert sp.simplify(
            value - kappa[i, j] * sources[0]
        ) == sp.zeros(6, 1)

    for i, j, m, n in product(range(3), repeat=4):
        minor = (
            kappa[m, n] * residual[i][j]
            - kappa[i, j] * residual[m][n]
        )
        assert sp.simplify(minor) == sp.zeros(6, 1)


def check_retained_faces_and_omission_control() -> None:
    lam = sp.Rational(3)
    targets = [basis_vector(6, i) for i in range(3)]
    sources = [basis_vector(6, 3 + i) for i in range(3)]
    zero = sp.zeros(6, 1)

    faces = {
        1: [[zero.copy() for _j in range(3)] for _i in range(3)],
        2: [[zero.copy() for _j in range(3)] for _i in range(3)],
    }
    faces[1][1][1] = targets[1]
    faces[1][2][2] = lam * sources[1]
    faces[2][2][2] = targets[2] + lam * sources[2]

    recovered_1 = faces[1][2][2] / lam
    recovered_2 = (faces[2][2][2] - targets[2]) / lam
    assert recovered_1 == sources[1]
    assert recovered_2 == sources[2]

    retained = 0
    for k in (1, 2):
        for i, j in product(range(3), repeat=2):
            if (i, j) == (2, 2):
                continue
            expected = targets[k] if i == j == k else zero
            assert faces[k][i][j] == expected
            retained += 1
    assert retained == 16

    # At x=y=e_1 the perpendicular contraction forgets the (1,1) slot.
    # This negative control proves that the corrected cube cannot replace
    # the sixteen retained face equations.
    perturbation = sources[0]
    perturbed = {
        k: [[faces[k][i][j].copy() for j in range(3)] for i in range(3)]
        for k in (1, 2)
    }
    perturbed[1][1][1] += perturbation
    assert perturbed[1][2][2] / lam == recovered_1
    assert (perturbed[2][2][2] - targets[2]) / lam == recovered_2

    perpendicular = (basis_vector(3, 0), basis_vector(3, 2))
    for alpha, beta in product(perpendicular, repeat=2):
        delta = sum(
            (
                alpha[i]
                * beta[j]
                * (perturbed[1][i][j] - faces[1][i][j])
                for i, j in product(range(3), repeat=2)
            ),
            zero.copy(),
        )
        assert delta == zero
    assert perturbed[1][1][1] - targets[1] == perturbation


def check_flattening_pivot_converse() -> None:
    for pivot in range(9):
        kappa = list(sp.symbols(f"k{pivot}_0:9"))
        kappa[pivot] = sp.symbols(f"kp{pivot}", nonzero=True)
        for source_coordinate in range(3):
            residual = list(sp.symbols(f"r{pivot}_{source_coordinate}_0:9"))
            recovered = residual[pivot] / kappa[pivot]
            for index in range(9):
                minor = (
                    kappa[pivot] * residual[index]
                    - kappa[index] * residual[pivot]
                )
                scaled_error = kappa[pivot] * (
                    residual[index] - kappa[index] * recovered
                )
                assert sp.cancel(scaled_error - minor) == 0


def check_contracted_cube() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    u = sp.Matrix(sp.symbols("u0:3"))
    v = sp.Matrix(sp.symbols("v0:3"))
    alpha = x.cross(u)
    beta = y.cross(v)
    assert sp.expand(alpha.dot(x)) == 0
    assert sp.expand(beta.dot(y)) == 0

    targets = [basis_vector(6, i) for i in range(3)]
    sources = [basis_vector(6, 3 + i) for i in range(3)]
    a = [
        sp.Matrix([sp.symbols(f"aa{c}{i}") for i in range(3)])
        for c in range(3)
    ]
    b = [
        sp.Matrix([sp.symbols(f"bb{c}{i}") for i in range(3)])
        for c in range(3)
    ]

    for k in range(3):
        contracted = sp.zeros(6, 1)
        for i, j in product(range(3), repeat=2):
            value = sp.zeros(6, 1)
            if i == j == k:
                value += targets[k]
            if k == 0:
                for c in range(3):
                    value += (
                        a[c][i] * y[j] - x[i] * b[c][j]
                    ) * sources[c]
            if i == 2 and j == 2:
                value += lam * sources[k]
            contracted += alpha[i] * beta[j] * value
        expected = (
            alpha[k] * beta[k] * targets[k]
            + lam * alpha[2] * beta[2] * sources[k]
        )
        assert sp.simplify(contracted - expected) == sp.zeros(6, 1)

    h = basis_vector(4, 0)
    q = [basis_vector(4, 1 + c) for c in range(3)]
    r = [x[i] * h for i in range(3)]
    p = [y[j] * h for j in range(3)]
    for i in range(3):
        for c in range(3):
            r[i] += a[c][i] * q[c]
            p[i] += b[c][i] * q[c]
    r_alpha = sum((alpha[i] * r[i] for i in range(3)), sp.zeros(4, 1))
    p_beta = sum((beta[j] * p[j] for j in range(3)), sp.zeros(4, 1))
    assert sp.expand(r_alpha[0]) == 0
    assert sp.expand(p_beta[0]) == 0


def perpendicular_basis(vector: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix]:
    first = sp.Matrix((vector[1], -vector[0], 0))
    pivot = 0 if vector[0] != 0 else 1
    second = sp.zeros(3, 1)
    second[2] = 1
    second[pivot] = -sp.Rational(vector[2], vector[pivot])
    assert first != sp.zeros(3, 1)
    assert first.dot(vector) == 0
    assert second.dot(vector) == 0
    assert second[2] == 1
    return first, second


def is_coordinate(vector: sp.Matrix, coordinate: int) -> bool:
    return all(vector[i] == 0 for i in range(3) if i != coordinate)


def check_visibility_census() -> None:
    representatives = []
    for mask in range(1, 8):
        vector = sp.Matrix([int(bool(mask & (1 << i))) for i in range(3)])
        if vector != sp.Matrix((0, 0, 1)):
            representatives.append(vector)
    assert len(representatives) == 6

    for x, y in product(representatives, repeat=2):
        alpha = perpendicular_basis(x)
        beta = perpendicular_basis(y)
        visible = []
        for k in range(3):
            entries = (
                alpha[0][k] * beta[0][k],
                alpha[0][k] * beta[1][k],
                alpha[1][k] * beta[0][k],
            )
            visible.append(any(entry != 0 for entry in entries))

        expected_0 = (
            not is_coordinate(x, 0)
            and not is_coordinate(y, 0)
            and (x[1] != 0 or y[1] != 0)
        )
        expected_1 = (
            not is_coordinate(x, 1)
            and not is_coordinate(y, 1)
            and (x[0] != 0 or y[0] != 0)
        )
        assert visible == [expected_0, expected_1, False]


def check_two_radical_interface() -> None:
    a, b, u, v = sp.symbols("a b u v")
    c = -a - b
    w = -u - v
    q_left = sp.expand(a * b + a * c + b * c)
    q_right = sp.expand(u * v + u * w + v * w)
    assert q_left == -a**2 - a * b - b**2
    assert q_right == -u**2 - u * v - v**2

    polar = sp.expand(
        a * v + a * w + u * b + b * w + u * c + v * c
    )
    expected_polar = sp.expand(
        q_left.subs({a: a + u, b: b + v}, simultaneous=True)
        - q_left
        - q_right
    )
    assert sp.expand(polar - expected_polar) == 0
    gram = sp.hessian(q_left, (a, b))
    assert gram == sp.Matrix(((-2, -1), (-1, -2)))
    assert gram.det() == 3

    x0, x1, y0, y1 = sp.symbols("x0 x1 y0 y1")
    alpha_zero = sp.Matrix((x1, -x0, 0))
    beta_zero = sp.Matrix((y1, -y0, 0))
    assert alpha_zero[0] * beta_zero[0] == x1 * y1
    assert alpha_zero[1] * beta_zero[1] == x0 * y0
    assert alpha_zero[2] * beta_zero[2] == 0

    e0 = basis_vector(3, 0)
    pure_x = basis_vector(9, 0)
    pure_y = basis_vector(9, 3)
    generic_a = sp.Matrix(sp.symbols("ra0:9"))
    generic_b = sp.Matrix(sp.symbols("rb0:9"))

    # Support two: Phi(x+y,a,x+y)=2 x tensor y tensor a_Z.
    support_two = pure_x + pure_y
    expected_two = 2 * tensor3(e0, e0, generic_a[6:9, :])
    assert sp.simplify(
        polarized_product(support_two, generic_a, support_two)
        - expected_two
    ) == sp.zeros(27, 1)

    # Pure support and its crossed missing-factor equation.
    expected_square = 2 * tensor3(
        e0, generic_a[3:6, :], generic_a[6:9, :]
    )
    assert sp.simplify(
        polarized_product(pure_x, generic_a, generic_a)
        - expected_square
    ) == sp.zeros(27, 1)
    expected_cross = tensor3(
        e0, generic_a[3:6, :], generic_b[6:9, :]
    ) + tensor3(e0, generic_b[3:6, :], generic_a[6:9, :])
    assert sp.simplify(
        polarized_product(pure_x, generic_a, generic_b)
        - expected_cross
    ) == sp.zeros(27, 1)

    # In the application x_2=y_2=0, the common exceptional row has both
    # required cross-radical maps, while the two visible outputs have the
    # claimed transverse target coefficients.
    alpha_one = sp.Matrix((0, 0, 1))
    beta_one = sp.Matrix((0, 0, 1))
    for k in range(3):
        assert alpha_zero[k] * beta_one[k] == 0
        assert alpha_one[k] * beta_zero[k] == 0
    assert alpha_zero[0] * beta_zero[0] == x1 * y1
    assert alpha_zero[1] * beta_zero[1] == x0 * y0


def check_sharp_control() -> None:
    x0 = basis_vector(9, 0)
    y0 = basis_vector(9, 3)
    z0 = basis_vector(9, 6)
    zero = sp.zeros(27, 1)
    targets = [
        tensor3(basis_vector(3, i), basis_vector(3, i), basis_vector(3, i))
        for i in range(3)
    ]
    rows_r = (y0, z0)
    rows_p = (z0, y0)
    rows_q = (x0, y0, z0)
    lam = sp.Rational(3)
    sources = (targets[0] / lam, zero, -targets[2] / lam)
    coefficients = (
        (sp.Integer(1), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(1)),
    )

    nonzero_cells = []
    for a, b, k in product(range(2), range(2), range(3)):
        got = polarized_product(rows_r[a], rows_p[b], rows_q[k])
        expected = coefficients[k][a] * coefficients[k][b] * targets[k]
        if a == b == 1:
            expected += lam * sources[k]
        assert sp.simplify(got - expected) == zero
        if got != zero:
            nonzero_cells.append((a, b, k))
    assert nonzero_cells == [(0, 0, 0), (1, 1, 0)]
    assert sp.Matrix.hstack(*rows_q).rank() == 3
    assert sp.Matrix.hstack(*rows_r).rank() == 2
    assert sp.Matrix.hstack(*rows_p).rank() == 2


def main() -> None:
    check_full_coefficient_identity()
    check_retained_faces_and_omission_control()
    check_flattening_pivot_converse()
    check_contracted_cube()
    check_visibility_census()
    check_two_radical_interface()
    check_sharp_control()
    print("full coefficient identity and graph gauge: PASS")
    print("retained source faces and omission control: PASS")
    print("source-tensor elimination and flattening pivot converse: PASS")
    print("corrected third-row cube and support census: PASS")
    print("two-radical support and application interfaces: PASS")
    print("quotient-only sharpness control: PASS")


if __name__ == "__main__":
    main()
