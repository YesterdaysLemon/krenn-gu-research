#!/usr/bin/env python3
"""Exact replay for the nonmonomial complete-target zero-pair localization.

The written theorem owns four analytic inputs: the order-three permanent-rank
obstruction, S2CK's two-transverse mixed-map lemma, S2CG's radical/zero-pair
classification, and the source-quotient geometry of a split two-source plane.
This deterministic SymPy script does not claim to prove those inputs.  It
replays the exact algebraic interfaces around them: graph coefficients and
gauge, the corrected cube, the structural-zero atlas, the correcting rank
fork, the one-survivor support census, perfect-pairing symmetry, and the final
retained-slice sign.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

Support = frozenset[int]


def unit(size: int, index: int) -> sp.Matrix:
    value = sp.zeros(size, 1)
    value[index] = 1
    return value


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    value = sp.zeros(x.rows * y.rows * z.rows, 1)
    for i, j, k in product(range(x.rows), range(y.rows), range(z.rows)):
        value[(i * y.rows + j) * z.rows + k] = x[i] * y[j] * z[k]
    return value


def matrix_tensor_vector(matrix: sp.Matrix, vector: sp.Matrix) -> sp.Matrix:
    value = sp.zeros(matrix.rows * matrix.cols * vector.rows, 1)
    for i, j, k in product(
        range(matrix.rows),
        range(matrix.cols),
        range(vector.rows),
    ):
        value[(i * matrix.cols + j) * vector.rows + k] = (
            matrix[i, j] * vector[k]
        )
    return value


def row(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return x.col_join(y).col_join(z)


def blocks(value: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    size = value.rows // 3
    return value[:size, :], value[size : 2 * size, :], value[2 * size :, :]


def polarized(u: sp.Matrix, v: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    split = (blocks(u), blocks(v), blocks(q))
    size = split[0][0].rows
    value = sp.zeros(size**3, 1)
    for sigma in permutations(range(3)):
        value += tensor3(
            split[sigma[0]][0],
            split[sigma[1]][1],
            split[sigma[2]][2],
        )
    return sp.simplify(value)


def permutation_sign(sigma: tuple[int, ...]) -> int:
    inversions = sum(
        sigma[i] > sigma[j]
        for i in range(len(sigma))
        for j in range(i + 1, len(sigma))
    )
    return -1 if inversions % 2 else 1


def alternating(rows: tuple[sp.Matrix, sp.Matrix, sp.Matrix]) -> sp.Matrix:
    split = tuple(blocks(value) for value in rows)
    size = split[0][0].rows
    value = sp.zeros(size**3, 1)
    for sigma in permutations(range(3)):
        value += permutation_sign(sigma) * tensor3(
            split[sigma[0]][0],
            split[sigma[1]][1],
            split[sigma[2]][2],
        )
    return sp.simplify(value)


def assert_zero(value: sp.Expr | sp.Matrix) -> None:
    if isinstance(value, sp.MatrixBase):
        assert all(sp.factor(entry) == 0 for entry in value)
    else:
        assert sp.factor(value) == 0


def assert_matrix_equal(left: sp.Matrix, right: sp.Matrix) -> None:
    assert left.shape == right.shape
    assert_zero(left - right)


def root_slices(value: sp.Matrix, size: int = 3) -> tuple[sp.Matrix, ...]:
    slices = tuple(sp.zeros(size, size) for _ in range(size))
    for i, j, k in product(range(size), repeat=3):
        slices[k][i, j] = value[(i * size + j) * size + k]
    return slices


def support(mask: int) -> Support:
    return frozenset(index for index in range(3) if mask & (1 << index))


def check_graph_coefficients_and_gauge() -> None:
    """Replay (8)--(12), including every tangent column and graph gauge."""

    t = 2
    e = tuple(unit(3, index) for index in range(3))
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    w = e[t]
    c_entries = sp.symbols("C0:9")
    residual = sp.Matrix(3, 3, c_entries)
    a = tuple(sp.Matrix(sp.symbols(f"a{s}_0:3")) for s in range(3))
    b = tuple(sp.Matrix(sp.symbols(f"b{s}_0:3")) for s in range(3))
    h = tuple(a[s] * y.T - x * b[s].T for s in range(3))
    u = tuple(
        matrix_tensor_vector(h[s], w)
        + matrix_tensor_vector(residual, e[s])
        for s in range(3)
    )

    target = tuple(unit(6, index) for index in range(3))
    source = tuple(unit(6, 3 + index) for index in range(3))
    l_rows = tuple(
        sum((a[s][i] * source[s] for s in range(3)), sp.zeros(6, 1))
        for i in range(3)
    )
    m_rows = tuple(
        sum((b[s][j] * source[s] for s in range(3)), sp.zeros(6, 1))
        for j in range(3)
    )

    coefficients: dict[tuple[int, int, int], sp.Matrix] = {}
    for i, j, k in product(range(3), repeat=3):
        diagonal = target[k] if i == j == k else sp.zeros(6, 1)
        tangent = w[k] * (y[j] * l_rows[i] - x[i] * m_rows[j])
        displayed = diagonal + tangent + residual[i, j] * source[k]
        direct = diagonal + sum(
            (u[s][9 * i + 3 * j + k] * source[s] for s in range(3)),
            sp.zeros(6, 1),
        )
        assert_matrix_equal(displayed, direct)
        coefficients[i, j, k] = displayed

    for k in range(3):
        for i, j in product(range(3), repeat=2):
            diagonal = target[k] if i == j == k else sp.zeros(6, 1)
            defect = coefficients[i, j, k] - diagonal
            if k != t:
                expected = residual[i, j] * source[k]
            else:
                expected = residual[i, j] * source[t] + sum(
                    (h[s][i, j] * source[s] for s in range(3)),
                    sp.zeros(6, 1),
                )
            assert_matrix_equal(defect, expected)

            if k == t:
                removed = defect - sum(
                    (
                        h[s][i, j] * source[s]
                        for s in range(3)
                        if s != t
                    ),
                    sp.zeros(6, 1),
                )
                assert_matrix_equal(
                    removed,
                    (residual[i, j] + h[t][i, j]) * source[t],
                )

    gauge = sp.symbols("gauge0:3")
    for s in range(3):
        shifted_a = a[s] + gauge[s] * x
        shifted_b = b[s] + gauge[s] * y
        assert_matrix_equal(shifted_a * y.T - x * shifted_b.T, h[s])


def check_incidence_and_alternating_interface() -> None:
    """Check the dimensions and basis covariance used at (13)--(16)."""

    zero3 = sp.zeros(3, 1)
    e = tuple(unit(3, index) for index in range(3))
    n = row(e[0], e[0], zero3)
    graph = (
        row(e[1], zero3, e[0]),
        row(e[2], e[1], e[1]),
        row(zero3, e[2], e[2]),
    )
    kernel_space = sp.Matrix.hstack(n, *graph)
    assert kernel_space.rank() == 4
    assert sp.Matrix.hstack(*(blocks(value)[0] for value in (n, *graph))).rank() == 3
    assert sp.Matrix.hstack(*(blocks(value)[1] for value in (n, *graph))).rank() == 3
    assert sp.Matrix.hstack(*(blocks(value)[2] for value in (n, *graph))).rank() == 3

    annihilator_n = sp.Matrix.hstack(*n.T.nullspace())
    annihilator_k = sp.Matrix.hstack(*kernel_space.T.nullspace())
    assert annihilator_n.rank() == 8
    assert annihilator_k.rank() == 5
    assert (n.T * annihilator_k) == sp.zeros(1, 5)

    # Restriction to K/N maps L=N^perp onto a three-space and has K^perp
    # as kernel.  The three pure third-root covectors map to its basis.
    restriction = kernel_space.T
    quotient_images = restriction[1:4, :] * annihilator_n
    assert quotient_images.rank() == 3
    assert restriction * annihilator_k == sp.zeros(4, 5)
    third_covectors = sp.Matrix.hstack(
        row(zero3, zero3, e[0]),
        row(zero3, zero3, e[1]),
        row(zero3, zero3, e[2]),
    )
    assert restriction[1:4, :] * third_covectors == sp.eye(3)

    # Alt(Q) != 0 is supplied analytically by the full sensor.  This fixture
    # checks its exact alternating convention and determinant covariance.
    z2 = sp.zeros(2, 1)
    f0 = unit(2, 0)
    q = (row(f0, z2, z2), row(z2, f0, z2), row(z2, z2, f0))
    alt_q = alternating(q)
    assert_matrix_equal(alt_q, tensor3(f0, f0, f0))
    change = sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    transformed = tuple(
        sum((change[i, j] * q[j] for j in range(3)), sp.zeros(6, 1))
        for i in range(3)
    )
    assert_matrix_equal(alternating(transformed), change.det() * alt_q)


def check_corrected_cube() -> None:
    """Contract the complete coefficient identity by two perpendicular rows."""

    t = 2
    e = tuple(unit(3, index) for index in range(3))
    x = sp.Matrix(sp.symbols("cx0:3"))
    y = sp.Matrix(sp.symbols("cy0:3"))
    c_entries = sp.symbols("cube_C0:9")
    residual = sp.Matrix(3, 3, c_entries)
    a = tuple(sp.Matrix(sp.symbols(f"cube_a{s}_0:3")) for s in range(3))
    b = tuple(sp.Matrix(sp.symbols(f"cube_b{s}_0:3")) for s in range(3))
    target = tuple(unit(6, index) for index in range(3))
    source = tuple(unit(6, 3 + index) for index in range(3))
    l_rows = tuple(
        sum((a[s][i] * source[s] for s in range(3)), sp.zeros(6, 1))
        for i in range(3)
    )
    m_rows = tuple(
        sum((b[s][j] * source[s] for s in range(3)), sp.zeros(6, 1))
        for j in range(3)
    )

    alpha = x.cross(sp.Matrix(sp.symbols("cube_u0:3")))
    beta = y.cross(sp.Matrix(sp.symbols("cube_v0:3")))
    assert_zero(alpha.dot(x))
    assert_zero(beta.dot(y))
    correction = (alpha.T * residual * beta)[0]

    for k in range(3):
        contracted = sp.zeros(6, 1)
        for i, j in product(range(3), repeat=2):
            diagonal = target[k] if i == j == k else sp.zeros(6, 1)
            tangent = e[t][k] * (
                y[j] * l_rows[i] - x[i] * m_rows[j]
            )
            contracted += alpha[i] * beta[j] * (
                diagonal + tangent + residual[i, j] * source[k]
            )
        assert_matrix_equal(
            contracted,
            alpha[k] * beta[k] * target[k] + correction * source[k],
        )


def check_structural_zero_atlas() -> None:
    """Exhaust the support split in (19) and replay the shores in (20)."""

    supports = tuple(support(mask) for mask in range(1, 8))
    disjoint_pairs = tuple(
        (left, right)
        for left, right in product(supports, repeat=2)
        if left.isdisjoint(right)
    )
    assert len(disjoint_pairs) == 12
    for left, right in disjoint_pairs:
        assert len(left) == 1 or len(right) == 1
        assert all(not (k in left and k in right) for k in range(3))

    x = sp.Matrix(sp.symbols("shore_x0:3"))
    y = sp.Matrix(sp.symbols("shore_y0:3"))
    alpha = sp.Matrix(sp.symbols("shore_alpha0:3"))
    beta = sp.Matrix(sp.symbols("shore_beta0:3"))
    c_entries = sp.symbols("shore_C0:9")
    residual = sp.Matrix(3, 3, c_entries)
    for index in range(3):
        coordinate = unit(3, index)
        first_shore = sp.Matrix.vstack(
            y.T,
            coordinate.T,
            residual.row(index),
        )
        assert_matrix_equal(
            first_shore * beta,
            sp.Matrix(
                [
                    y.dot(beta),
                    beta[index],
                    (coordinate.T * residual * beta)[0],
                ]
            ),
        )
        second_shore = sp.Matrix.vstack(
            x.T,
            coordinate.T,
            residual[:, index].T,
        )
        assert_matrix_equal(
            second_shore * alpha,
            sp.Matrix(
                [
                    x.dot(alpha),
                    alpha[index],
                    (alpha.T * residual * coordinate)[0],
                ]
            ),
        )

    nonempty_root_supports = tuple(support(mask) for mask in range(1, 8))
    shore_counts = {
        (x_support, y_support):
        (3 - len(x_support)) + (3 - len(y_support))
        for x_support, y_support in product(nonempty_root_supports, repeat=2)
    }
    assert max(shore_counts.values()) == 4
    assert all(count <= 4 for count in shore_counts.values())

    # A positive-dimensional displayed shore really gives a two-dimensional
    # partner plane.  S2CG's analytic radical bound is what excludes it.
    coordinate = unit(3, 0)
    positive_shore = sp.Matrix.vstack(
        coordinate.T,
        coordinate.T,
        coordinate.T,
    )
    shore_basis = sp.Matrix.hstack(*positive_shore.nullspace())
    assert shore_basis.rank() == 2
    injective_partner_map = sp.eye(3)
    assert (injective_partner_map * shore_basis).rank() == 2


def mode_flattening(value: sp.Matrix, mode: int) -> sp.Matrix:
    result = sp.zeros(3, 9)
    for i, j, k in product(range(3), repeat=3):
        indices = (i, j, k)
        other = tuple(indices[position] for position in range(3) if position != mode)
        result[indices[mode], 3 * other[0] + other[1]] = value[9 * i + 3 * j + k]
    return result


def check_correcting_rank_fork() -> None:
    """Replay (23)--(30); the P3 rank-four theorem remains analytic."""

    t = 2
    e = tuple(unit(3, index) for index in range(3))
    x = sp.Matrix(sp.symbols("fork_x0:3"))
    y = sp.Matrix(sp.symbols("fork_y0:3"))
    c_entries = sp.symbols("fork_C0:9")
    residual = sp.Matrix(3, 3, c_entries)
    a_columns = tuple(
        sp.Matrix(sp.symbols(f"fork_a{s}_0:3")) for s in range(3)
    )
    b_columns = tuple(
        sp.Matrix(sp.symbols(f"fork_b{s}_0:3")) for s in range(3)
    )
    h = tuple(
        a_columns[s] * y.T - x * b_columns[s].T for s in range(3)
    )
    u = tuple(
        matrix_tensor_vector(h[s], e[t])
        + matrix_tensor_vector(residual, e[s])
        for s in range(3)
    )
    mu = sp.symbols("mu0:3", nonzero=True)
    diagonal = sp.Matrix.hstack(
        *(tensor3(e[k], e[k], e[k]) for k in range(3))
    )
    source_substitution = sp.diag(*(-mu[k] for k in range(3)))
    from_complete_target = diagonal + sp.Matrix.hstack(*u) * source_substitution
    fork_columns = sp.Matrix.hstack(
        *(diagonal[:, k] - mu[k] * u[k] for k in range(3))
    )
    assert_matrix_equal(from_complete_target, fork_columns)

    # A diagonal three-target evaluation has all three mode ranks three and
    # a displayed length-three decomposition.  The contradictory rank four
    # of the order-three permanent tensor is an external exact theorem.
    weights = sp.symbols("rank_weight0:3", nonzero=True)
    diagonal_target = sum(
        (weights[k] * tensor3(e[k], e[k], e[k]) for k in range(3)),
        sp.zeros(27, 1),
    )
    for mode in range(3):
        assert mode_flattening(diagonal_target, mode).rank() == 3

    # If the vanishing fork colour s differs from t, the two third-root
    # slices separately force H_s=0 and actual C=nu E_ss.
    s = 0
    generic_h = sp.Matrix(3, 3, sp.symbols("fork_H0:9"))
    generic_c = sp.Matrix(3, 3, sp.symbols("fork_D0:9"))
    nu = sp.symbols("nu", nonzero=True)
    unequal_u = matrix_tensor_vector(generic_h, e[t])
    unequal_u += matrix_tensor_vector(generic_c, e[s])
    unequal_target = nu * tensor3(e[s], e[s], e[s])
    unequal_difference = root_slices(unequal_u - unequal_target)
    assert_matrix_equal(unequal_difference[t], generic_h)
    assert_matrix_equal(
        unequal_difference[s],
        generic_c - nu * (e[s] * e[s].T),
    )
    assert all(
        unequal_difference[k] == sp.zeros(3, 3)
        for k in range(3)
        if k not in {s, t}
    )

    # For s=t the only slice is C+H_t=nu E_tt.  Its restriction to the two
    # perpendicular planes is the diagonal coordinate pairing.
    a_t = sp.Matrix(sp.symbols("fork_at0:3"))
    b_t = sp.Matrix(sp.symbols("fork_bt0:3"))
    h_t = a_t * y.T - x * b_t.T
    same_u = matrix_tensor_vector(h_t, e[t])
    same_u += matrix_tensor_vector(nu * e[t] * e[t].T - h_t, e[t])
    assert_matrix_equal(same_u, nu * tensor3(e[t], e[t], e[t]))

    a = x.cross(sp.Matrix(sp.symbols("fork_au0:3")))
    b = y.cross(sp.Matrix(sp.symbols("fork_bv0:3")))
    alpha = x.cross(sp.Matrix(sp.symbols("fork_alphau0:3")))
    beta = y.cross(sp.Matrix(sp.symbols("fork_betav0:3")))
    actual_c = nu * e[t] * e[t].T - h_t
    assert_zero(a.dot(x))
    assert_zero(b.dot(y))
    assert_zero(alpha.dot(x))
    assert_zero(beta.dot(y))
    assert_zero((a.T * h_t * b)[0])
    assert_zero((alpha.T * h_t * beta)[0])
    assert_zero((a.T * actual_c * b)[0] - nu * a[t] * b[t])
    correction = (alpha.T * actual_c * beta)[0]
    assert_zero(correction - nu * alpha[t] * beta[t])

    corrected_values: list[sp.Expr] = []
    for k in range(3):
        corrected = a[k] * b[k]
        corrected -= (
            (a.T * actual_c * b)[0]
            * alpha[k]
            * beta[k]
            / correction
        )
        expected = a[k] * b[k]
        expected -= (
            alpha[k]
            * beta[k]
            * a[t]
            * b[t]
            / (alpha[t] * beta[t])
        )
        assert_zero(corrected - expected)
        corrected_values.append(expected)
    assert_zero(corrected_values[t])


def support_vector(support_set: Support, prefix: str) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.symbols(f"{prefix}{index}", nonzero=True)
            if index in support_set
            else 0
            for index in range(3)
        ]
    )


def marked_covector(vector: sp.Matrix, t: int) -> sp.Matrix:
    value = unit(3, t)
    for pivot in range(3):
        if pivot != t and vector[pivot] != 0:
            value[pivot] = -vector[t] / vector[pivot]
            assert_zero(value.dot(vector))
            assert value[t] == 1
            return value
    raise AssertionError("the excluded support {t} has no marked covector")


def restricted_bilinear_form(
    x: sp.Matrix,
    y: sp.Matrix,
    alpha: sp.Matrix,
    beta: sp.Matrix,
    colour: int,
    t: int,
) -> sp.Matrix:
    x_plane = sp.Matrix.hstack(*x.T.nullspace())
    y_plane = sp.Matrix.hstack(*y.T.nullspace())
    left_colour = x_plane[colour, :]
    right_colour = y_plane[colour, :]
    left_t = x_plane[t, :]
    right_t = y_plane[t, :]
    return sp.simplify(
        left_colour.T * right_colour
        - alpha[colour] * beta[colour] * left_t.T * right_t
    )


def swap_complement_colours(pair: tuple[Support, Support]) -> tuple[Support, Support]:
    def swap_one(value: Support) -> Support:
        return frozenset(
            1 - index if index in {0, 1} else index for index in value
        )

    return swap_one(pair[0]), swap_one(pair[1])


def check_one_survivor_census() -> None:
    """Check the exact B_k support criterion and the 14/20/2 split."""

    t = 2
    supports = tuple(
        support(mask) for mask in range(1, 8) if mask != (1 << t)
    )
    partitions: dict[int, set[tuple[Support, Support]]] = {
        0: set(),
        1: set(),
        2: set(),
    }
    for case_index, (x_support, y_support) in enumerate(
        product(supports, repeat=2)
    ):
        x = support_vector(x_support, f"census_x{case_index}_")
        y = support_vector(y_support, f"census_y{case_index}_")
        alpha = marked_covector(x, t)
        beta = marked_covector(y, t)
        zero_forms = 0
        for colour in (0, 1):
            form = restricted_bilinear_form(
                x,
                y,
                alpha,
                beta,
                colour,
                t,
            )
            expected_zero = (
                x_support == {colour}
                or y_support == {colour}
                or (
                    x_support <= {colour, t}
                    and y_support <= {colour, t}
                )
            )
            actual_zero = form == sp.zeros(2, 2)
            assert actual_zero == expected_zero
            if not expected_zero:
                assert any(
                    sp.factor(entry).is_zero is False
                    for entry in form
                    if entry != 0
                )
            zero_forms += int(expected_zero)
        partitions[zero_forms].add((x_support, y_support))

    assert {key: len(value) for key, value in partitions.items()} == {
        0: 14,
        1: 20,
        2: 2,
    }
    assert partitions[2] == {
        (frozenset({0}), frozenset({1})),
        (frozenset({1}), frozenset({0})),
    }

    # Root exchange and the swap of the two complementary colours give six
    # orbits in the exactly-one-zero census.
    unseen = set(partitions[1])
    orbits: list[set[tuple[Support, Support]]] = []
    while unseen:
        seed = next(iter(unseen))
        orbit: set[tuple[Support, Support]] = set()
        frontier = [seed]
        while frontier:
            current = frontier.pop()
            if current in orbit:
                continue
            orbit.add(current)
            frontier.append((current[1], current[0]))
            frontier.append(swap_complement_colours(current))
        orbits.append(orbit)
        unseen -= orbit
    assert sorted(len(orbit) for orbit in orbits) == [2, 2, 4, 4, 4, 4]

    expected_representatives = {
        (frozenset({0}), frozenset({0})),
        (frozenset({0}), frozenset({0, 1})),
        (frozenset({0}), frozenset({0, 2})),
        (frozenset({0}), frozenset({1, 2})),
        (frozenset({0}), frozenset({0, 1, 2})),
        (frozenset({0, 2}), frozenset({0, 2})),
    }
    assert all(
        any(representative_pair in orbit for representative_pair in expected_representatives)
        for orbit in orbits
    )

    # If both complementary forms survive at one pair, the Q-map has the
    # two transverse target columns.  S2CK analytically excludes this map.
    first, second = sp.symbols("survivor_first survivor_second", nonzero=True)
    mixed_map = sp.Matrix(
        [
            [first, 0, 0],
            [0, second, 0],
        ]
    )
    assert mixed_map.rank() == 2

    # If the sole survivor has rank one, its left kernel is a nonzero row
    # annihilating the whole opposite plane.  S2CG excludes that radical.
    left = sp.Matrix(sp.symbols("rank_one_left0:2"))
    right = sp.Matrix(sp.symbols("rank_one_right0:2"))
    rank_one = left * right.T
    left_kernel = sp.Matrix([-left[1], left[0]])
    assert_zero(left_kernel.T * rank_one)


def check_perfect_pairing_symmetry() -> None:
    """Replay the determinant argument forcing R=P=ker(lambda_l)."""

    b00, b01, b10, b11 = sp.symbols("pair_b00 pair_b01 pair_b10 pair_b11")
    l0, l1 = sp.symbols("pair_l0 pair_l1")
    pairing = sp.Matrix([[b00, b01], [b10, b11]])
    symmetry_conditions = sp.Matrix(
        [
            b00 * l1 - b10 * l0,
            b01 * l1 - b11 * l0,
        ]
    )
    determinant = pairing.det()
    assert_zero(
        b01 * symmetry_conditions[0]
        - b00 * symmetry_conditions[1]
        - l0 * determinant
    )
    assert_zero(
        b11 * symmetry_conditions[0]
        - b10 * symmetry_conditions[1]
        - l1 * determinant
    )
    # Thus symmetry_conditions=0 and det(B)!=0 force lambda|R=0.
    # Root exchange gives lambda|P=0; all three planes have dimension two.
    lambda_row = sp.Matrix([[0, 0, 1]])
    kernel_lambda = sp.Matrix.hstack(*lambda_row.nullspace())
    assert kernel_lambda.rank() == 2
    assert lambda_row * kernel_lambda == sp.zeros(1, 2)

    # Exact aligned split-plane fixture after S2CG's analytic classification.
    zero2 = sp.zeros(2, 1)
    x, y, z = unit(2, 0), unit(2, 0), unit(2, 0)
    pure_x = row(x, zero2, zero2)
    pure_y = row(zero2, y, zero2)
    q_l = row(zero2, zero2, z)
    split_plane = (pure_x, pure_y)
    split_pairing = sp.zeros(2, 2)
    target_l = tensor3(x, y, z)
    for i, j in product(range(2), repeat=2):
        value = polarized(split_plane[i], split_plane[j], q_l)
        if value == target_l:
            split_pairing[i, j] = 1
        else:
            assert_matrix_equal(value, sp.zeros(8, 1))
    assert split_pairing == sp.Matrix([[0, 1], [1, 0]])
    assert split_pairing.det() == -1
    conjugate_plus = pure_x + pure_y
    conjugate_minus = pure_x - pure_y
    assert_matrix_equal(
        polarized(conjugate_plus, conjugate_minus, q_l),
        sp.zeros(8, 1),
    )


def check_final_full_slice_quotient() -> None:
    """Replay (38)--(41), including the sign and actual-C conclusion."""

    zero2 = sp.zeros(2, 1)
    e0, e1 = unit(2, 0), unit(2, 1)
    pure_x = row(e0, zero2, zero2)
    pure_y = row(zero2, e0, zero2)
    q_coefficient = sp.symbols("quotient_q_coefficient")
    q_k = pure_x + q_coefficient * pure_y
    r = row(
        sp.Matrix(sp.symbols("quotient_rx0:2")),
        sp.Matrix(sp.symbols("quotient_ry0:2")),
        sp.Matrix(sp.symbols("quotient_rz0:2")),
    )
    p = row(
        sp.Matrix(sp.symbols("quotient_px0:2")),
        sp.Matrix(sp.symbols("quotient_py0:2")),
        sp.Matrix(sp.symbols("quotient_pz0:2")),
    )

    quotient = sp.zeros(1, 8)
    quotient[0, 7] = 1
    assert_zero(quotient * polarized(r, p, q_k))
    target_l = tensor3(e0, e0, e0)
    target_k = tensor3(e1, e1, e1)
    assert_zero(quotient * target_l)
    assert quotient * target_k == sp.ones(1, 1)

    # In a colour k distinct from t, the complete slice is
    # P^(k)-E_kk T_k=C S_k.  After quotient P^(k)=0 and T_k survives.
    root_e = tuple(unit(3, index) for index in range(3))
    k = 0
    root_diagonal = root_e[k] * root_e[k].T
    c_entries = sp.symbols("quotient_C0:9")
    residual = sp.Matrix(3, 3, c_entries)
    s_k = sp.symbols("quotient_s", nonzero=True)
    quotient_identity = -root_diagonal - s_k * residual
    solved_residual = -root_diagonal / s_k
    assert_matrix_equal(
        quotient_identity.subs(
            {
                residual[i, j]: solved_residual[i, j]
                for i, j in product(range(3), repeat=2)
            }
        ),
        sp.zeros(3, 3),
    )

    # With the correcting-zero notation S_k=-mu_k T_k, this same sign is
    # E_kk=mu_k C, hence actual C=mu_k^(-1)E_kk (not merely its tangent class).
    mu_k = sp.symbols("quotient_mu", nonzero=True)
    correcting_identity = quotient_identity.subs(s_k, -mu_k)
    actual_monomial = root_diagonal / mu_k
    assert_matrix_equal(
        correcting_identity.subs(
            {
                residual[i, j]: actual_monomial[i, j]
                for i, j in product(range(3), repeat=2)
            }
        ),
        sp.zeros(3, 3),
    )


def main() -> None:
    check_graph_coefficients_and_gauge()
    check_incidence_and_alternating_interface()
    check_corrected_cube()
    check_structural_zero_atlas()
    check_correcting_rank_fork()
    check_one_survivor_census()
    check_perfect_pairing_symmetry()
    check_final_full_slice_quotient()
    print("complete graph/full-slice coefficients and graph gauge: PASS")
    print("Alt/incidence and corrected-cube interfaces: PASS")
    print("structural-zero support union and <=4-shore census: PASS")
    print("correcting rank fork and one-survivor 14/20/2 census: PASS")
    print("perfect-pairing symmetry and retained-slice sign: PASS")
    print("analytic owners: P3 rank, S2CK, S2CG, source quotient geometry")


if __name__ == "__main__":
    main()
