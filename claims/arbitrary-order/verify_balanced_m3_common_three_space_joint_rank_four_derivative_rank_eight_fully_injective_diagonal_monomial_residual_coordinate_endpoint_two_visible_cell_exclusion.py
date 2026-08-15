#!/usr/bin/env python3
"""Exact replay for the diagonal two-visible-cell exclusion.

The written theorem owns the source-support classifications in the mixed-map
and zero-corner lemmas, as well as the S2CG zero-pair theorem.  This primary
SymPy replay checks their exact coordinate interfaces.  It also exhausts the
fourteen two-visible support masks and checks every perpendicular basis,
structural zero pair, correction-free condition, and selected target corner
in the ten-row boundary atlas.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

Support = frozenset[int]


def unit(size: int, index: int) -> sp.Matrix:
    value = sp.zeros(size, 1)
    value[index] = 1
    return value


def row(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return x.col_join(y).col_join(z)


def blocks(value: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    size = value.rows // 3
    return value[:size, :], value[size : 2 * size, :], value[2 * size :, :]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    x_size, y_size, z_size = x.rows, y.rows, z.rows
    value = sp.zeros(x_size * y_size * z_size, 1)
    for i, j, k in product(range(x_size), range(y_size), range(z_size)):
        value[(i * y_size + j) * z_size + k] = x[i] * y[j] * z[k]
    return value


def polarized(u: sp.Matrix, v: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    split = (blocks(u), blocks(v), blocks(q))
    value = sp.zeros(split[0][0].rows ** 3, 1)
    for sigma in permutations(range(3)):
        value += tensor3(
            split[sigma[0]][0],
            split[sigma[1]][1],
            split[sigma[2]][2],
        )
    return sp.simplify(value)


def assert_matrix_equal(left: sp.Matrix, right: sp.Matrix) -> None:
    assert sp.simplify(left - right) == sp.zeros(left.rows, left.cols)


def support(mask: int) -> Support:
    return frozenset(index for index in range(3) if mask & (1 << index))


def visible_zero(x_support: Support, y_support: Support) -> bool:
    return (
        x_support != {0}
        and y_support != {0}
        and (1 in x_support or 1 in y_support)
    )


def visible_one(x_support: Support, y_support: Support) -> bool:
    return (
        x_support != {1}
        and y_support != {1}
        and (0 in x_support or 0 in y_support)
    )


def vector_for_support(prefix: str, indices: Support) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.symbols(f"{prefix}{index}", nonzero=True)
            if index in indices
            else 0
            for index in range(3)
        ]
    )


def named_covector(vector: sp.Matrix, name: str) -> sp.Matrix:
    if name == "e0":
        return unit(3, 0)
    if name == "e1":
        return unit(3, 1)
    if name == "e2":
        return unit(3, 2)
    if name == "01":
        return sp.Matrix([vector[1], -vector[0], 0])
    if name == "02":
        return sp.Matrix([vector[2], 0, -vector[0]])
    if name == "12":
        return sp.Matrix([0, vector[2], -vector[1]])
    raise ValueError(name)


def corrected_cube(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    lam: sp.Expr,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    targets = tuple(unit(6, index) for index in range(3))
    sources = tuple(unit(6, 3 + index) for index in range(3))
    return tuple(
        sp.simplify(
            alpha[k] * beta[k] * targets[k]
            + lam * alpha[2] * beta[2] * sources[k]
        )
        for k in range(3)
    )


def assert_perpendicular_basis(
    vector: sp.Matrix,
    first: sp.Matrix,
    second: sp.Matrix,
) -> None:
    assert sp.expand(first.dot(vector)) == 0
    assert sp.expand(second.dot(vector)) == 0
    assert sp.Matrix.hstack(first, second).rank() == 2


def assert_zero_map(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    lam: sp.Expr,
) -> None:
    zero = sp.zeros(6, 1)
    for value in corrected_cube(alpha, beta, lam):
        assert_matrix_equal(value, zero)


def assert_target_line(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    target: int,
    lam: sp.Expr,
) -> None:
    assert sp.expand(alpha[2] * beta[2]) == 0
    products = tuple(sp.expand(alpha[k] * beta[k]) for k in range(3))
    assert products[target].is_zero is False
    assert all(products[k] == 0 for k in range(3) if k != target)
    values = corrected_cube(alpha, beta, lam)
    target_vector = unit(6, target)
    assert_matrix_equal(values[target], products[target] * target_vector)
    for k, value in enumerate(values):
        if k != target:
            assert_matrix_equal(value, sp.zeros(6, 1))


def check_fourteen_mask_partition() -> None:
    s0 = frozenset({0})
    s1 = frozenset({1})
    s01 = frozenset({0, 1})
    s02 = frozenset({0, 2})
    s12 = frozenset({1, 2})
    s012 = frozenset({0, 1, 2})
    supports = tuple(
        support(mask) for mask in range(1, 8) if mask != (1 << 2)
    )
    assert supports == (s0, s1, s01, s02, s12, s012)

    two_visible = {
        (x_support, y_support)
        for x_support, y_support in product(supports, repeat=2)
        if visible_zero(x_support, y_support)
        and visible_one(x_support, y_support)
    }
    central_factors = {s01, s012}
    central = {
        (x_support, y_support)
        for x_support, y_support in product(central_factors, repeat=2)
    }
    boundary = two_visible - central
    assert len(two_visible) == 14
    assert len(central) == 4
    assert len(boundary) == 10
    assert central.isdisjoint(boundary)
    assert central | boundary == two_visible

    expected_boundary = {
        (s01, s02),
        (s01, s12),
        (s02, s01),
        (s12, s01),
        (s02, s12),
        (s12, s02),
        (s02, s012),
        (s12, s012),
        (s012, s02),
        (s012, s12),
    }
    assert boundary == expected_boundary


def check_four_central_cubes() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    s01 = frozenset({0, 1})
    s012 = frozenset({0, 1, 2})
    targets = tuple(unit(6, index) for index in range(3))
    zero = sp.zeros(6, 1)

    for case_index, (x_support, y_support) in enumerate(
        product((s01, s012), repeat=2)
    ):
        x = vector_for_support(f"cx{case_index}_", x_support)
        y = vector_for_support(f"cy{case_index}_", y_support)
        alpha = named_covector(x, "01")
        beta = named_covector(y, "01")
        assert sp.expand(alpha.dot(x)) == 0
        assert sp.expand(beta.dot(y)) == 0
        assert alpha[2] == beta[2] == 0
        values = corrected_cube(alpha, beta, lam)
        assert_matrix_equal(values[0], x[1] * y[1] * targets[0])
        assert_matrix_equal(values[1], x[0] * y[0] * targets[1])
        assert_matrix_equal(values[2], zero)
        assert sp.Matrix.hstack(*values).rank() == 2


def check_ten_boundary_cubes() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    s01 = frozenset({0, 1})
    s02 = frozenset({0, 2})
    s12 = frozenset({1, 2})
    s012 = frozenset({0, 1, 2})
    cases = (
        (s01, s02, "e2", "01", "e1", "02", "Ad", 1, "AB", 0),
        (s01, s12, "e2", "01", "e0", "12", "Ad", 0, "AB", 1),
        (s02, s01, "e1", "02", "e2", "01", "cB", 1, "AB", 0),
        (s12, s01, "e0", "12", "e2", "01", "cB", 0, "AB", 1),
        (s02, s12, "e1", "02", "e0", "12", "Ad", 0, "cB", 1),
        (s12, s02, "e0", "12", "e1", "02", "Ad", 1, "cB", 0),
        (s02, s012, "e1", "02", "02", "01", "cB", 1, "AB", 0),
        (s12, s012, "e0", "12", "12", "01", "cB", 0, "AB", 1),
        (s012, s02, "02", "01", "e1", "02", "Ad", 1, "AB", 0),
        (s012, s12, "12", "01", "e0", "12", "Ad", 0, "AB", 1),
    )
    corner = {
        "Ad": (1, 0),
        "cB": (0, 1),
        "AB": (1, 1),
    }
    seen: set[tuple[Support, Support]] = set()

    for case_index, case in enumerate(cases):
        (
            x_support,
            y_support,
            c_name,
            a_name,
            d_name,
            b_name,
            first_name,
            first_target,
            second_name,
            second_target,
        ) = case
        x = vector_for_support(f"bx{case_index}_", x_support)
        y = vector_for_support(f"by{case_index}_", y_support)
        c = named_covector(x, c_name)
        a = named_covector(x, a_name)
        d = named_covector(y, d_name)
        b = named_covector(y, b_name)
        assert_perpendicular_basis(x, c, a)
        assert_perpendicular_basis(y, d, b)

        rows = (c, a)
        columns = (d, b)
        assert_zero_map(c, d, lam)
        assert_target_line(
            rows[corner[first_name][0]],
            columns[corner[first_name][1]],
            first_target,
            lam,
        )
        assert_target_line(
            rows[corner[second_name][0]],
            columns[corner[second_name][1]],
            second_target,
            lam,
        )
        assert {first_target, second_target} == {0, 1}
        seen.add((x_support, y_support))

    assert len(seen) == len(cases) == 10


def hyperdet_222(value: sp.Matrix) -> sp.Expr:
    def entry(i: int, j: int, k: int) -> sp.Expr:
        return value[4 * i + 2 * j + k]

    a000 = entry(0, 0, 0)
    a001 = entry(0, 0, 1)
    a010 = entry(0, 1, 0)
    a011 = entry(0, 1, 1)
    a100 = entry(1, 0, 0)
    a101 = entry(1, 0, 1)
    a110 = entry(1, 1, 0)
    a111 = entry(1, 1, 1)
    return sp.expand(
        a000**2 * a111**2
        + a001**2 * a110**2
        + a010**2 * a101**2
        + a100**2 * a011**2
        - 2
        * (
            a000 * a001 * a110 * a111
            + a000 * a010 * a101 * a111
            + a000 * a100 * a011 * a111
            + a001 * a010 * a101 * a110
            + a001 * a100 * a011 * a110
            + a010 * a100 * a011 * a101
        )
        + 4
        * (
            a000 * a011 * a101 * a110
            + a001 * a010 * a100 * a111
        )
    )


def assert_coordinate_support(
    value: sp.Matrix,
    forbidden: callable,
) -> None:
    for i, j, k in product(range(2), repeat=3):
        if forbidden(i, j, k):
            assert sp.expand(value[4 * i + 2 * j + k]) == 0


def check_mixed_map_interfaces() -> None:
    e0, e1 = unit(2, 0), unit(2, 1)
    zero = sp.zeros(2, 1)
    x, y, z = e0, e0, e0
    xi = e1
    vx = sp.Matrix(sp.symbols("mvx0:2"))
    vy = sp.Matrix(sp.symbols("mvy0:2"))
    vz = sp.Matrix(sp.symbols("mvz0:2"))
    qx = sp.Matrix(sp.symbols("mqx0:2"))
    qy = sp.Matrix(sp.symbols("mqy0:2"))
    qz = sp.Matrix(sp.symbols("mqz0:2"))
    q = row(qx, qy, qz)

    pure_x = row(x, zero, zero)
    generic_v = row(vx, vy, vz)
    assert_coordinate_support(
        polarized(pure_x, generic_v, q),
        lambda i, _j, _k: i == 1,
    )

    support_two = row(x, y, zero)
    assert_matrix_equal(
        polarized(support_two, generic_v, support_two),
        2 * tensor3(x, y, vz),
    )
    v_without_z = row(vx, vy, zero)
    fixed_xy = tensor3(x, vy, qz) + tensor3(vx, y, qz)
    assert_matrix_equal(polarized(support_two, v_without_z, q), fixed_xy)

    a, b, c = sp.symbols("ma mb mc")
    endpoint_v = row(a * x, b * y, c * z)
    endpoint_values = polarized(support_two, endpoint_v, q)
    assert_coordinate_support(
        endpoint_values,
        lambda i, j, _k: i == 1 and j == 1,
    )

    support_three = row(x, y, z)
    scaled_v = row(a * x, b * y, c * z)
    xyz = tensor3(x, y, z)
    assert_matrix_equal(
        polarized(support_three, support_three, scaled_v),
        2 * (a + b + c) * xyz,
    )
    kernel_v = scaled_v.subs(c, -a - b)
    tangent_values = polarized(support_three, kernel_v, q)
    assert_coordinate_support(
        tangent_values,
        lambda i, j, k: i + j + k >= 2,
    )

    t = sp.symbols("mt")
    shared_yz_v = row(a * x + t * xi, b * y, c * z)
    endpoint_tangent = polarized(
        support_three,
        support_three,
        shared_yz_v,
    )
    assert_coordinate_support(
        endpoint_tangent,
        lambda _i, j, k: j == 1 or k == 1,
    )
    endpoint_mixed = polarized(support_three, shared_yz_v, q)
    assert_coordinate_support(
        endpoint_mixed,
        lambda _i, j, k: j == 1 and k == 1,
    )

    secant_a, secant_b = sp.symbols("secant_a secant_b", nonzero=True)
    transverse_secant = secant_a * tensor3(e0, e0, e0)
    transverse_secant += secant_b * tensor3(e1, e1, e1)
    assert hyperdet_222(transverse_secant) == secant_a**2 * secant_b**2

    tangent_coefficients = sp.symbols("tau0:4")
    tangent = tangent_coefficients[0] * tensor3(e0, e0, e0)
    tangent += tangent_coefficients[1] * tensor3(e1, e0, e0)
    tangent += tangent_coefficients[2] * tensor3(e0, e1, e0)
    tangent += tangent_coefficients[3] * tensor3(e0, e0, e1)
    assert hyperdet_222(tangent) == 0


def linear_combination(
    coefficients: tuple[sp.Expr, sp.Expr, sp.Expr],
    basis: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    return sum(
        (coefficient * vector for coefficient, vector in zip(coefficients, basis)),
        sp.zeros(basis[0].rows, 1),
    )


def check_zero_corner_interfaces() -> None:
    e0 = unit(2, 0)
    zero = sp.zeros(2, 1)
    x, y, z = e0, e0, e0
    pure_x = row(x, zero, zero)
    pure_y = row(zero, y, zero)

    gx = sp.Matrix(sp.symbols("zgx0:2"))
    gy = sp.Matrix(sp.symbols("zgy0:2"))
    third = row(gx, gy, z)
    q_basis = (pure_x, pure_y, third)
    coefficients = tuple(
        tuple(sp.symbols(f"zq{row_index}_0:3"))
        for row_index in range(3)
    )
    generic_rows = tuple(
        linear_combination(coefficient_row, q_basis)
        for coefficient_row in coefficients
    )
    conjugate_plus = pure_x + pure_y
    conjugate_minus = pure_x - pure_y
    assert_matrix_equal(
        polarized(conjugate_plus, conjugate_minus, generic_rows[0]),
        sp.zeros(8, 1),
    )
    shared_omitted_factor = polarized(*generic_rows)
    assert_coordinate_support(
        shared_omitted_factor,
        lambda _i, _j, k: k == 1,
    )

    ax = sp.Matrix(sp.symbols("zax0:2"))
    bx = sp.Matrix(sp.symbols("zbx0:2"))
    qx = sp.Matrix(sp.symbols("zqx0:2"))
    qy = sp.Matrix(sp.symbols("zqy0:2"))
    qz = sp.Matrix(sp.symbols("zqz0:2"))
    q = row(qx, qy, qz)
    generic_a = row(ax, y, z)
    assert_matrix_equal(
        polarized(generic_a, pure_x, q),
        tensor3(x, y, qz) + tensor3(x, qy, z),
    )

    scale = sp.symbols("zt")
    kernel_b = row(bx, scale * y, -scale * z)
    assert_matrix_equal(
        polarized(generic_a, pure_x, kernel_b),
        sp.zeros(8, 1),
    )
    mixed_image = polarized(generic_a, kernel_b, q)
    assert_coordinate_support(
        mixed_image,
        lambda _i, j, k: j == 1 and k == 1,
    )

    source_scalar = sp.symbols("zs")
    q_y_line = row(qx, source_scalar * y, qz)
    a_without_y = row(ax, zero, z)
    b_without_y = row(bx, zero, sp.Matrix(sp.symbols("zbz0:2")))
    assert_matrix_equal(
        polarized(a_without_y, pure_x, q_y_line),
        source_scalar * tensor3(x, y, z),
    )
    assert_matrix_equal(
        polarized(a_without_y, pure_x, b_without_y),
        sp.zeros(8, 1),
    )
    assert_coordinate_support(
        polarized(a_without_y, b_without_y, q_y_line),
        lambda _i, j, _k: j == 1,
    )

    q_z_line = row(qx, qy, source_scalar * z)
    a_without_z = row(ax, y, zero)
    b_without_z = row(bx, sp.Matrix(sp.symbols("zby0:2")), zero)
    assert_matrix_equal(
        polarized(a_without_z, pure_x, q_z_line),
        source_scalar * tensor3(x, y, z),
    )
    assert_matrix_equal(
        polarized(a_without_z, pure_x, b_without_z),
        sp.zeros(8, 1),
    )
    assert_coordinate_support(
        polarized(a_without_z, b_without_z, q_z_line),
        lambda _i, _j, k: k == 1,
    )


def main() -> None:
    check_fourteen_mask_partition()
    check_four_central_cubes()
    check_ten_boundary_cubes()
    check_mixed_map_interfaces()
    check_zero_corner_interfaces()
    print("two-visible support atlas: PASS (14 = 4 central + 10 boundary)")
    print("corrected-cube covectors and corners: PASS")
    print("mixed-map algebraic interfaces: PASS")
    print("zero-corner algebraic interfaces: PASS")
    print("source-support classifications: owned by the written theorem")


if __name__ == "__main__":
    main()
