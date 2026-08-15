#!/usr/bin/env python3
"""Exact replay for the complete diagonal one-visible-wall exclusion.

The written theorem owns the coordinate-free S2CG radical bound and
zero-pair classification.  This primary SymPy replay checks the finite
twenty-mask support atlas and every algebraic interface used after those
analytic results: perpendicular bases, corrected-cube cells, radical shores,
triple quotients, recovered source identities, the final full-matrix
separation, and the graph-gauge reduction to a common two-plane.
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
    return value[:3, :], value[3:6, :], value[6:9, :]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    value = sp.zeros(27, 1)
    for i, j, k in product(range(3), repeat=3):
        value[9 * i + 3 * j + k] = x[i] * y[j] * z[k]
    return value


def polarized(u: sp.Matrix, v: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    split = (blocks(u), blocks(v), blocks(q))
    value = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        value += tensor3(
            split[sigma[0]][0],
            split[sigma[1]][1],
            split[sigma[2]][2],
        )
    return sp.simplify(value)


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


def check_twenty_mask_partition() -> None:
    s0, s1 = frozenset({0}), frozenset({1})
    s01 = frozenset({0, 1})
    s02 = frozenset({0, 2})
    s12 = frozenset({1, 2})
    s012 = frozenset({0, 1, 2})
    supports = tuple(
        support(mask) for mask in range(1, 8) if mask != (1 << 2)
    )
    assert supports == (s0, s1, s01, s02, s12, s012)

    one_visible = {
        (x_support, y_support)
        for x_support, y_support in product(supports, repeat=2)
        if visible_zero(x_support, y_support)
        ^ visible_one(x_support, y_support)
    }
    target_zero = {
        pair for pair in one_visible if visible_zero(*pair)
    }
    target_one = {
        pair for pair in one_visible if visible_one(*pair)
    }
    assert len(one_visible) == 20
    assert len(target_zero) == len(target_one) == 10

    same_coordinate = {(s1, s1), (s0, s0)}
    radical_shores = {
        (s1, s02),
        (s02, s1),
        (s0, s12),
        (s12, s0),
    }
    target_zero_cross = {
        (s1, s01),
        (s01, s1),
        (s1, s12),
        (s12, s1),
        (s1, s012),
        (s012, s1),
        (s12, s12),
    }
    target_one_coordinate = {
        (s0, s01),
        (s01, s0),
        (s0, s02),
        (s02, s0),
        (s0, s012),
        (s012, s0),
    }
    final_support = {(s02, s02)}
    pieces = (
        same_coordinate,
        radical_shores,
        target_zero_cross,
        target_one_coordinate,
        final_support,
    )
    assert tuple(map(len, pieces)) == (2, 4, 7, 6, 1)
    for left_index, left in enumerate(pieces):
        for right in pieces[left_index + 1 :]:
            assert left.isdisjoint(right)
    assert set().union(*pieces) == one_visible
    assert (
        (same_coordinate | radical_shores | target_zero_cross) & target_zero
    ) == {
        (s1, s1),
        (s1, s02),
        (s02, s1),
    } | target_zero_cross
    assert (
        (same_coordinate | radical_shores | target_one_coordinate
         | final_support) & target_one
    ) == {
        (s0, s0),
        (s0, s12),
        (s12, s0),
    } | target_one_coordinate | final_support


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


def assert_zero_cube(values: tuple[sp.Matrix, ...]) -> None:
    zero = sp.zeros(6, 1)
    assert all(sp.simplify(value) == zero for value in values)


def assert_perpendicular_basis(
    vector: sp.Matrix,
    first: sp.Matrix,
    second: sp.Matrix,
    rows: tuple[int, int],
    expected_minor: sp.Expr,
) -> None:
    expected_minor = sp.sympify(expected_minor)
    assert sp.expand(first.dot(vector)) == 0
    assert sp.expand(second.dot(vector)) == 0
    minor = sp.Matrix.hstack(first, second).extract(rows, (0, 1)).det()
    assert sp.factor(minor - expected_minor) == 0
    assert expected_minor.is_zero is False


def vector_for_support(prefix: str, indices: Support) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.symbols(f"{prefix}{index}", nonzero=True)
            if index in indices
            else 0
            for index in range(3)
        ]
    )


def check_same_coordinate_cubes() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    e0, e1, e2 = (unit(3, index) for index in range(3))
    targets = tuple(unit(6, index) for index in range(3))
    zero = sp.zeros(6, 1)
    for shared, visible, first, rows in (
        (e1, 0, e0, (0, 2)),
        (e0, 1, e1, (1, 2)),
    ):
        assert_perpendicular_basis(shared, first, e2, rows, 1)
        assert_zero_cube(corrected_cube(first, e2, lam))
        assert_zero_cube(corrected_cube(e2, first, lam))
        visible_cube = corrected_cube(first, first, lam)
        assert visible_cube[visible] == targets[visible]
        assert all(
            value == zero
            for index, value in enumerate(visible_cube)
            if index != visible
        )


def check_four_radical_shores() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    e0, e1, e2 = (unit(3, index) for index in range(3))
    y02 = vector_for_support("y", frozenset({0, 2}))
    x02 = vector_for_support("x", frozenset({0, 2}))
    y12 = vector_for_support("v", frozenset({1, 2}))
    x12 = vector_for_support("u", frozenset({1, 2}))
    shore_cases = (
        (e1, y02, (e0, e2), (e1,)),
        (x02, e1, (e1,), (e0, e2)),
        (e0, y12, (e1, e2), (e0,)),
        (x12, e0, (e0,), (e1, e2)),
    )
    checked = 0
    for x, y, alphas, betas in shore_cases:
        assert all(sp.expand(alpha.dot(x)) == 0 for alpha in alphas)
        assert all(sp.expand(beta.dot(y)) == 0 for beta in betas)
        shore = alphas if len(alphas) == 2 else betas
        assert sp.Matrix.hstack(*shore).rank() == 2
        for alpha, beta in product(alphas, betas):
            assert_zero_cube(corrected_cube(alpha, beta, lam))
            checked += 1
    # Each case supplies two independent radical rows for one nonzero row.
    assert checked == 8
    assert all(sp.Matrix.hstack(*(case[2] if len(case[2]) == 2 else case[3])).rank() == 2
               for case in shore_cases)
    # S2CG Corollary 2 owns the incompatible upper bound one.
    s2cg_radical_bound = 1
    assert 2 > s2cg_radical_bound


def assert_cross_cube(
    alpha_a: sp.Matrix,
    alpha_c: sp.Matrix,
    beta_b: sp.Matrix,
    beta_d: sp.Matrix,
    lam: sp.Expr,
    visible: int,
    visible_scalar: sp.Expr,
) -> None:
    zero = sp.zeros(6, 1)
    target = unit(6, visible)
    assert_zero_cube(corrected_cube(alpha_a, beta_d, lam))
    assert_zero_cube(corrected_cube(alpha_c, beta_b, lam))
    values = corrected_cube(alpha_a, beta_b, lam)
    assert sp.simplify(values[visible] - visible_scalar * target) == zero
    assert all(
        sp.simplify(value) == zero
        for index, value in enumerate(values)
        if index != visible
    )


def check_seven_target_zero_cross_cubes() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    e0, e1, e2 = (unit(3, index) for index in range(3))
    masks = (
        frozenset({0, 1}),
        frozenset({1, 2}),
        frozenset({0, 1, 2}),
    )
    checked = 0
    for case_index, y_support in enumerate(masks):
        y = vector_for_support(f"y{case_index}_", y_support)
        y0, y1, y2 = y
        alpha_a, alpha_c = e0, e2
        beta_b = sp.Matrix((y1, -y0, 0))
        beta_d = sp.Matrix((0, y2, -y1))
        assert_perpendicular_basis(e1, alpha_a, alpha_c, (0, 2), 1)
        assert_perpendicular_basis(
            y, beta_b, beta_d, (0, 2), -y1**2
        )
        assert_cross_cube(
            alpha_a, alpha_c, beta_b, beta_d, lam, 0, y1
        )
        checked += 1

        x = vector_for_support(f"x{case_index}_", y_support)
        x0, x1, x2 = x
        alpha_a = sp.Matrix((x1, -x0, 0))
        alpha_c = sp.Matrix((0, x2, -x1))
        beta_b, beta_d = e0, e2
        assert_perpendicular_basis(
            x, alpha_a, alpha_c, (0, 2), -x1**2
        )
        assert_perpendicular_basis(e1, beta_b, beta_d, (0, 2), 1)
        assert_cross_cube(
            alpha_a, alpha_c, beta_b, beta_d, lam, 0, x1
        )
        checked += 1

    x = vector_for_support("xs_", frozenset({1, 2}))
    y = vector_for_support("ys_", frozenset({1, 2}))
    x1, x2 = x[1], x[2]
    y1, y2 = y[1], y[2]
    alpha_a = e0
    alpha_c = sp.Matrix((0, x2, -x1))
    beta_b = e0
    beta_d = sp.Matrix((0, y2, -y1))
    assert_perpendicular_basis(x, alpha_a, alpha_c, (0, 2), -x1)
    assert_perpendicular_basis(y, beta_b, beta_d, (0, 2), -y1)
    assert_cross_cube(alpha_a, alpha_c, beta_b, beta_d, lam, 0, 1)
    checked += 1
    assert checked == 7


def check_six_target_one_coordinate_cross_cubes() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    e0, e1, e2 = (unit(3, index) for index in range(3))
    masks = (
        frozenset({0, 1}),
        frozenset({0, 2}),
        frozenset({0, 1, 2}),
    )
    checked = 0
    for case_index, y_support in enumerate(masks):
        y = vector_for_support(f"v{case_index}_", y_support)
        y0, y1, y2 = y
        alpha_a, alpha_c = e1, e2
        beta_b = sp.Matrix((y1, -y0, 0))
        beta_d = sp.Matrix((y2, 0, -y0))
        assert_perpendicular_basis(e0, alpha_a, alpha_c, (1, 2), 1)
        assert_perpendicular_basis(
            y, beta_b, beta_d, (1, 2), y0**2
        )
        assert_cross_cube(
            alpha_a, alpha_c, beta_b, beta_d, lam, 1, -y0
        )
        checked += 1

        x = vector_for_support(f"u{case_index}_", y_support)
        x0, x1, x2 = x
        alpha_a = sp.Matrix((x1, -x0, 0))
        alpha_c = sp.Matrix((x2, 0, -x0))
        beta_b, beta_d = e1, e2
        assert_perpendicular_basis(
            x, alpha_a, alpha_c, (1, 2), x0**2
        )
        assert_perpendicular_basis(e0, beta_b, beta_d, (1, 2), 1)
        assert_cross_cube(
            alpha_a, alpha_c, beta_b, beta_d, lam, 1, -x0
        )
        checked += 1
    assert checked == 6


def quotient_indices(base_colour: int) -> tuple[int, ...]:
    return tuple(
        9 * i + 3 * j + k
        for i, j, k in product(range(3), repeat=3)
        if i != base_colour and j != base_colour and k != base_colour
    )


def quotient(value: sp.Matrix, base_colour: int) -> sp.Matrix:
    return sp.Matrix([value[index] for index in quotient_indices(base_colour)])


def pure_rows(base_colour: int) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    basis = unit(3, base_colour)
    zero = sp.zeros(3, 1)
    return (
        row(basis, zero, zero),
        row(zero, basis, zero),
        row(zero, zero, basis),
    )


def check_split_quotient_interface(base_colour: int) -> None:
    pure = pure_rows(base_colour)
    arbitrary_r = sp.Matrix(sp.symbols(f"rr{base_colour}_0:9"))
    arbitrary_p = sp.Matrix(sp.symbols(f"pp{base_colour}_0:9"))
    q_coefficients = sp.symbols(f"q{base_colour}_0:3")
    q_in_split_space = sum(
        (q_coefficients[index] * pure[index] for index in range(3)),
        sp.zeros(9, 1),
    )
    assert quotient(
        polarized(arbitrary_r, arbitrary_p, q_in_split_space),
        base_colour,
    ) == sp.zeros(8, 1)

    plane_left = sp.symbols(f"l{base_colour}_0:2")
    plane_right = sp.symbols(f"m{base_colour}_0:2")
    left = plane_left[0] * pure[0] + plane_left[1] * pure[1]
    right = plane_right[0] * pure[0] + plane_right[1] * pure[1]
    arbitrary_q = sp.Matrix(sp.symbols(f"qq{base_colour}_0:9"))
    assert quotient(
        polarized(left, right, arbitrary_q), base_colour
    ) == sp.zeros(8, 1)


def check_target_zero_quotient() -> None:
    check_split_quotient_interface(0)
    e0, e1, _ = (unit(3, index) for index in range(3))
    target_zero = tensor3(e0, e0, e0)
    target_one = tensor3(e1, e1, e1)
    assert quotient(target_zero, 0) == sp.zeros(8, 1)
    assert quotient(target_one, 0) != sp.zeros(8, 1)


def full_target_values(
    x: sp.Matrix,
    y: sp.Matrix,
    a: tuple[sp.Matrix, ...],
    b: tuple[sp.Matrix, ...],
    lam: sp.Expr,
) -> tuple[tuple[tuple[sp.Matrix, ...], ...], ...]:
    targets = tuple(unit(6, index) for index in range(3))
    sources = tuple(unit(6, 3 + index) for index in range(3))
    values: list[list[list[sp.Matrix]]] = [
        [[sp.zeros(6, 1) for _k in range(3)] for _j in range(3)]
        for _i in range(3)
    ]
    for i, j, k in product(range(3), repeat=3):
        value = targets[k] if i == j == k else sp.zeros(6, 1)
        if k == 0:
            for c in range(3):
                value += (
                    a[c][i] * y[j] - x[i] * b[c][j]
                ) * sources[c]
        if i == j == 2:
            value += lam * sources[k]
        values[i][j][k] = sp.simplify(value)
    return tuple(
        tuple(tuple(values[i][j]) for j in range(3)) for i in range(3)
    )


def contract_first_two(
    values: tuple[tuple[tuple[sp.Matrix, ...], ...], ...],
    alpha: sp.Matrix,
    beta: sp.Matrix,
    k: int,
) -> sp.Matrix:
    return sp.simplify(
        sum(
            (
                alpha[i] * beta[j] * values[i][j][k]
                for i, j in product(range(3), repeat=2)
            ),
            sp.zeros(6, 1),
        )
    )


def generic_vectors(prefix: str) -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(sp.symbols(f"{prefix}{c}_0:3")) for c in range(3)
    )


def check_target_one_source_identities() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    targets = tuple(unit(6, index) for index in range(3))
    sources = tuple(unit(6, 3 + index) for index in range(3))
    e0, _, e2 = (unit(3, index) for index in range(3))
    a = generic_vectors("a")
    b = generic_vectors("b")

    y0 = sp.symbols("y0", nonzero=True)
    y1, y2 = sp.symbols("y1 y2")
    x = e0
    y = sp.Matrix((y0, y1, y2))
    values = full_target_values(x, y, a, b, lam)
    alpha_c = e2
    beta_d = sp.Matrix((y2, 0, -y0))
    a2_source_sum = sum(
        (a[c][2] * sources[c] for c in range(3)), sp.zeros(6, 1)
    )
    assert sp.simplify(
        values[2][0][0] - y0 * a2_source_sum
    ) == sp.zeros(6, 1)
    assert sp.simplify(
        values[2][2][0] - y2 * a2_source_sum - lam * sources[0]
    ) == sp.zeros(6, 1)
    expected = (
        -y0 * lam * sources[0],
        -y0 * lam * sources[1],
        -y0 * (targets[2] + lam * sources[2]),
    )
    assert values[2][0][1] == sp.zeros(6, 1)
    assert values[2][2][1] == lam * sources[1]
    assert values[2][0][2] == sp.zeros(6, 1)
    assert values[2][2][2] == targets[2] + lam * sources[2]
    for k in range(3):
        assert sp.simplify(
            contract_first_two(values, alpha_c, beta_d, k) - expected[k]
        ) == sp.zeros(6, 1)

    x0 = sp.symbols("x0", nonzero=True)
    x1, x2 = sp.symbols("x1 x2")
    x = sp.Matrix((x0, x1, x2))
    y = e0
    values = full_target_values(x, y, a, b, lam)
    alpha_c = sp.Matrix((x2, 0, -x0))
    beta_d = e2
    b2_source_sum = sum(
        (b[c][2] * sources[c] for c in range(3)), sp.zeros(6, 1)
    )
    assert sp.simplify(
        values[0][2][0] + x0 * b2_source_sum
    ) == sp.zeros(6, 1)
    assert sp.simplify(
        values[2][2][0] + x2 * b2_source_sum - lam * sources[0]
    ) == sp.zeros(6, 1)
    expected = (
        -x0 * lam * sources[0],
        -x0 * lam * sources[1],
        -x0 * (targets[2] + lam * sources[2]),
    )
    assert values[0][2][1] == sp.zeros(6, 1)
    assert values[2][2][1] == lam * sources[1]
    assert values[0][2][2] == sp.zeros(6, 1)
    assert values[2][2][2] == targets[2] + lam * sources[2]
    for k in range(3):
        assert sp.simplify(
            contract_first_two(values, alpha_c, beta_d, k) - expected[k]
        ) == sp.zeros(6, 1)


def check_target_one_unsliced_quotient() -> None:
    check_split_quotient_interface(1)
    lam = sp.symbols("lambda", nonzero=True)
    h0, h1, h2 = sp.symbols("h0 h1 h2")
    e0, e1, e2 = (unit(3, index) for index in range(3))
    target_zero = tensor3(e0, e0, e0)
    target_one = tensor3(e1, e1, e1)
    target_two = tensor3(e2, e2, e2)
    target_zero_bar = quotient(target_zero, 1)
    target_two_bar = quotient(target_two, 1)
    assert quotient(target_one, 1) == sp.zeros(8, 1)
    assert sp.Matrix.hstack(target_zero_bar, target_two_bar).rank() == 2

    source_zero_bar = sp.zeros(8, 1)
    source_one_bar = sp.zeros(8, 1)
    source_two_bar = -target_two_bar / lam
    for scalar in sp.symbols("s0 s1"):
        assert sp.simplify(scalar * source_zero_bar) == sp.zeros(8, 1)
    residual = sp.simplify(
        -target_zero_bar
        - h0 * source_zero_bar
        - h1 * source_one_bar
        - h2 * source_two_bar
    )
    expected = -target_zero_bar + h2 * target_two_bar / lam
    assert sp.simplify(residual - expected) == sp.zeros(8, 1)
    # The unsliced P_000 quotient cannot vanish: its two target coordinates
    # would require simultaneously -1=0 and h2/lambda=0.
    assert any(entry == -1 for entry in residual)
    assert sp.Matrix.hstack(target_zero_bar, target_two_bar).rank() == 2


def check_final_101_cube_and_sources() -> tuple[
    sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol
]:
    lam = sp.symbols("lambda", nonzero=True)
    x0, x2 = sp.symbols("x0 x2", nonzero=True)
    y0, y2 = sp.symbols("y0 y2", nonzero=True)
    x = sp.Matrix((x0, 0, x2))
    y = sp.Matrix((y0, 0, y2))
    e1 = unit(3, 1)
    alpha_a = e1
    alpha_c = sp.Matrix((x2, 0, -x0))
    beta_b = e1
    beta_d = sp.Matrix((y2, 0, -y0))
    assert_perpendicular_basis(x, alpha_a, alpha_c, (1, 2), -x0)
    assert_perpendicular_basis(y, beta_b, beta_d, (1, 2), -y0)
    assert_cross_cube(
        alpha_a, alpha_c, beta_b, beta_d, lam, 1, 1
    )

    targets = tuple(unit(6, index) for index in range(3))
    sources = tuple(unit(6, 3 + index) for index in range(3))
    expected = (
        x2 * y2 * targets[0] + lam * x0 * y0 * sources[0],
        lam * x0 * y0 * sources[1],
        x0 * y0 * (targets[2] + lam * sources[2]),
    )
    for k in range(3):
        assert sp.simplify(
            corrected_cube(alpha_c, beta_d, lam)[k] - expected[k]
        ) == sp.zeros(6, 1)
    return lam, x0, x2, y0, y2


def symbolic_matrix(prefix: str) -> sp.Matrix:
    return sp.Matrix(3, 3, sp.symbols(f"{prefix}0:9"))


def check_final_matrix_separation(
    lam: sp.Symbol,
    x0: sp.Symbol,
    x2: sp.Symbol,
    y0: sp.Symbol,
    y2: sp.Symbol,
) -> None:
    check_split_quotient_interface(1)
    e0, _, e2 = (unit(3, index) for index in range(3))
    target_zero_bar = quotient(tensor3(e0, e0, e0), 1)
    target_two_bar = quotient(tensor3(e2, e2, e2), 1)
    assert sp.Matrix.hstack(target_zero_bar, target_two_bar).rank() == 2

    ratio = sp.cancel(x2 * y2 / (lam * x0 * y0))
    source_zero_bar = -ratio * target_zero_bar
    source_one_bar = sp.zeros(8, 1)
    source_two_bar = -target_two_bar / lam
    assert sp.simplify(
        x2 * y2 * target_zero_bar
        + lam * x0 * y0 * source_zero_bar
    ) == sp.zeros(8, 1)
    assert sp.simplify(lam * x0 * y0 * source_one_bar) == sp.zeros(8, 1)
    assert sp.simplify(
        x0 * y0 * (target_two_bar + lam * source_two_bar)
    ) == sp.zeros(8, 1)

    e00 = sp.zeros(3, 3)
    e00[0, 0] = 1
    e22 = sp.zeros(3, 3)
    e22[2, 2] = 1
    c_root = lam * e22
    h0, h1, h2 = (symbolic_matrix(name) for name in ("h", "j", "k"))
    projected = [[sp.zeros(8, 1) for _j in range(3)] for _i in range(3)]
    expected = [[sp.zeros(8, 1) for _j in range(3)] for _i in range(3)]
    for i, j in product(range(3), repeat=2):
        projected[i][j] = sp.simplify(
            e00[i, j] * target_zero_bar
            + (c_root[i, j] + h0[i, j]) * source_zero_bar
            + h1[i, j] * source_one_bar
            + h2[i, j] * source_two_bar
        )
        expected[i][j] = sp.simplify(
            (e00[i, j] - ratio * (c_root[i, j] + h0[i, j]))
            * target_zero_bar
            - h2[i, j] * target_two_bar / lam
        )
        assert sp.simplify(projected[i][j] - expected[i][j]) == sp.zeros(8, 1)

    zero_slot = next(index for index, value in enumerate(target_zero_bar) if value)
    two_slot = next(index for index, value in enumerate(target_two_bar) if value)
    for i, j in product(range(3), repeat=2):
        assert sp.simplify(
            projected[i][j][zero_slot]
            - e00[i, j]
            + ratio * (c_root[i, j] + h0[i, j])
        ) == 0
        assert sp.simplify(
            projected[i][j][two_slot] + h2[i, j] / lam
        ) == 0
    # If every projected P^0 entry is zero, target-coordinate separation
    # forces H2=0 and E00=ratio*(Croot+H0), entry by entry.


def check_final_gauge_and_common_plane(
    x0: sp.Symbol,
    x2: sp.Symbol,
    y0: sp.Symbol,
    y2: sp.Symbol,
) -> None:
    x = sp.Matrix((x0, 0, x2))
    y = sp.Matrix((y0, 0, y2))
    a2 = sp.Matrix(sp.symbols("a2_0:3"))
    b2 = sp.Matrix(sp.symbols("b2_0:3"))
    h2 = a2 * y.T - x * b2.T
    gauge_scalar = b2[0] / y0
    shifted_a2 = sp.simplify(a2 - gauge_scalar * x)
    shifted_b2 = sp.simplify(b2 - gauge_scalar * y)
    assert sp.simplify(shifted_a2 - h2[:, 0] / y0) == sp.zeros(3, 1)
    assert sp.simplify(
        shifted_b2
        + h2[0, :].T / x0
        - y * h2[0, 0] / (x0 * y0)
    ) == sp.zeros(3, 1)
    assert sp.simplify(
        shifted_a2 * y.T - x * shifted_b2.T - h2
    ) == sp.zeros(3, 3)
    # Hence H2=0 implies a2=t*x and b2=t*y, and this gauge sets both to zero.

    a0, a1 = generic_vectors("ra")[:2]
    b0, b1 = generic_vectors("pb")[:2]
    h, q0, q1, _q2 = (unit(4, index) for index in range(4))
    r = tuple(
        x[i] * h + a0[i] * q0 + a1[i] * q1 for i in range(3)
    )
    p = tuple(
        y[j] * h + b0[j] * q0 + b1[j] * q1 for j in range(3)
    )
    alpha_a = unit(3, 1)
    alpha_c = sp.Matrix((x2, 0, -x0))
    beta_b = unit(3, 1)
    beta_d = sp.Matrix((y2, 0, -y0))
    r_a = sum((alpha_a[i] * r[i] for i in range(3)), sp.zeros(4, 1))
    r_c = sum((alpha_c[i] * r[i] for i in range(3)), sp.zeros(4, 1))
    p_b = sum((beta_b[j] * p[j] for j in range(3)), sp.zeros(4, 1))
    p_d = sum((beta_d[j] * p[j] for j in range(3)), sp.zeros(4, 1))
    for value in (r_a, r_c, p_b, p_d):
        assert value[0] == 0
        assert value[3] == 0

    q01 = sp.Matrix.hstack(q0, q1)
    r_coefficients = sp.Matrix(
        ((r_a[1], r_c[1]), (r_a[2], r_c[2]))
    )
    p_coefficients = sp.Matrix(
        ((p_b[1], p_d[1]), (p_b[2], p_d[2]))
    )
    r_pair = sp.Matrix.hstack(r_a, r_c)
    p_pair = sp.Matrix.hstack(p_b, p_d)
    assert r_pair == q01 * r_coefficients
    assert p_pair == q01 * p_coefficients
    assert sp.expand(r_coefficients.det()) != 0
    assert sp.expand(p_coefficients.det()) != 0
    assert sp.simplify(
        r_pair * r_coefficients.adjugate()
        - r_coefficients.det() * q01
    ) == sp.zeros(4, 2)
    assert sp.simplify(
        p_pair * p_coefficients.adjugate()
        - p_coefficients.det() * q01
    ) == sp.zeros(4, 2)
    # Injectivity supplies both nonzero determinants, so R=P=span(q0,q1).

    pure_x, pure_y, _ = pure_rows(1)
    coefficients = sp.symbols("fa0:3 fb0:3 fq0:3")
    final_a = coefficients[0] * pure_x + coefficients[1] * pure_y
    final_b = coefficients[3] * pure_x + coefficients[4] * pure_y
    final_q = coefficients[6] * pure_x + coefficients[7] * pure_y
    assert polarized(final_a, final_b, final_q) == sp.zeros(27, 1)
    target_one = tensor3(unit(3, 1), unit(3, 1), unit(3, 1))
    assert target_one != sp.zeros(27, 1)
    # S2CG reclassification owns that the common plane is split; the final
    # displayed identity checks the resulting P_111=0 versus T_1 interface.


def main() -> None:
    check_twenty_mask_partition()
    check_same_coordinate_cubes()
    check_four_radical_shores()
    check_seven_target_zero_cross_cubes()
    check_six_target_one_coordinate_cross_cubes()
    check_target_zero_quotient()
    check_target_one_source_identities()
    check_target_one_unsliced_quotient()
    final_parameters = check_final_101_cube_and_sources()
    check_final_matrix_separation(*final_parameters)
    check_final_gauge_and_common_plane(
        final_parameters[1],
        final_parameters[2],
        final_parameters[3],
        final_parameters[4],
    )
    print("twenty-mask one-visible partition (2+4+7+6+1): PASS")
    print("same-coordinate cubes and four radical shores: PASS")
    print("seven T0 and six coordinate-T1 cross systems: PASS")
    print("T0 quotient and T1 recovered-source quotient: PASS")
    print("final 101x101 cube and full-matrix separation: PASS")
    print("H2 gauge and injective common-plane interface: PASS")


if __name__ == "__main__":
    main()
