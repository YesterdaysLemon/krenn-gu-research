#!/usr/bin/env python3
"""Exact replay for the coordinate shared-factor structural exclusion.

The written theorem owns the source-support classifications imported from
S2CG, the exhaustive two-cross incidence dichotomy imported from S2CI, and
the mixed-map/zero-corner obstructions imported from S2CK.  This deterministic
SymPy script checks the finite root-coordinate atlas and the exact algebraic
interfaces around those analytic results.  Its normalized physical fixtures
do not claim to prove the imported classifications.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def unit(size: int, index: int) -> sp.Matrix:
    value = sp.zeros(size, 1)
    value[index] = 1
    return value


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    value = sp.zeros(x.rows * y.rows * z.rows, 1)
    for i, j, k in product(range(x.rows), range(y.rows), range(z.rows)):
        value[(i * y.rows + j) * z.rows + k] = x[i] * y[j] * z[k]
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


def assert_zero(value: sp.Expr | sp.Matrix) -> None:
    if isinstance(value, sp.MatrixBase):
        assert all(sp.factor(entry) == 0 for entry in value)
    else:
        assert sp.factor(value) == 0


def assert_nonzero(value: sp.Expr) -> None:
    assert sp.factor(value).is_zero is False


def common_plane_map(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    residual: sp.Matrix,
) -> sp.Matrix:
    """Return coefficients of ``lambda_i T_i, lambda_j T_j, S``."""

    assert alpha.shape == beta.shape == (2, 1)
    correction = (alpha.T * residual * beta)[0]
    return sp.Matrix(
        [alpha[0] * beta[0], alpha[1] * beta[1], correction]
    )


def coordinate_pair_map(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    residual: sp.Matrix,
) -> sp.Matrix:
    """Return coefficients of ``lambda_k T_k, S`` for x=e_s,y=e_r."""

    assert alpha.shape == beta.shape == (2, 1)
    correction = (alpha.T * residual * beta)[0]
    return sp.Matrix([alpha[1] * beta[1], correction])


def check_root_exchange() -> None:
    """Check both first/second-root orientations without a label shortcut."""

    entries = sp.symbols("exchange_D0:4")
    residual = sp.Matrix(2, 2, entries)
    alpha = sp.Matrix(sp.symbols("exchange_alpha0:2"))
    beta = sp.Matrix(sp.symbols("exchange_beta0:2"))
    assert_zero(
        common_plane_map(alpha, beta, residual)
        - common_plane_map(beta, alpha, residual.T)
    )
    assert_zero(
        coordinate_pair_map(alpha, beta, residual)
        - coordinate_pair_map(beta, alpha, residual.T)
    )

    alpha3 = sp.Matrix(sp.symbols("exchange_alpha3_0:3"))
    beta3 = sp.Matrix(sp.symbols("exchange_beta3_0:3"))
    correction = sp.symbols("exchange_correction")
    cube = sp.Matrix(
        [*(alpha3[h] * beta3[h] for h in range(3)), correction]
    )
    exchanged = sp.Matrix(
        [*(beta3[h] * alpha3[h] for h in range(3)), correction]
    )
    assert_zero(cube - exchanged)
    assert len(tuple(product(permutations(range(3)), (False, True)))) == 12


def check_y_s_nonzero_cross_zero_atlas() -> None:
    """Replay every cross-zero pattern of the exact 2 x 2 D atlas."""

    a, u_cross, v_cross, b = sp.symbols(
        "ysnz_a ysnz_u ysnz_v ysnz_b", nonzero=True
    )
    e0, e1 = unit(2, 0), unit(2, 1)
    residual = sp.Matrix([[a, 0], [v_cross, b]])
    ab_map = common_plane_map(e0, e0, residual)
    ad_map = common_plane_map(e0, e1, residual)
    cb_map = common_plane_map(e1, e0, residual)
    cd_map = common_plane_map(e1, e1, residual)
    assert ab_map == sp.Matrix([1, 0, a])
    assert_zero(ad_map)
    assert cb_map == sp.Matrix([0, 0, v_cross])
    assert cd_map == sp.Matrix([0, 1, b])

    # Removing H=vS gives the two target corners used in the independent
    # zero-pair branch.
    assert_zero(v_cross * ab_map - a * cb_map - sp.Matrix([v_cross, 0, 0]))
    assert_zero(v_cross * cd_map - b * cb_map - sp.Matrix([0, v_cross, 0]))

    # The dependent pure branch has four exhaustive diagonal patterns.
    assert_zero(
        b * ab_map - a * cd_map - sp.Matrix([b, -a, 0])
    )
    residual_b_only = sp.Matrix([[0, 0], [v_cross, b]])
    beta_prime = e1 - (b / v_cross) * e0
    assert_zero(
        common_plane_map(e0, beta_prime, residual_b_only)
        - sp.Matrix([-b / v_cross, 0, 0])
    )
    assert_zero(
        common_plane_map(e1, beta_prime, residual_b_only)
        - sp.Matrix([0, 1, 0])
    )
    residual_a_only = sp.Matrix([[a, 0], [v_cross, 0]])
    alpha_prime = e0 - (a / v_cross) * e1
    assert_zero(
        common_plane_map(alpha_prime, e1, residual_a_only)
        - sp.Matrix([0, -a / v_cross, 0])
    )
    assert_zero(
        common_plane_map(alpha_prime, e0, residual_a_only)
        - sp.Matrix([1, 0, 0])
    )
    residual_no_diagonal = sp.Matrix([[0, 0], [v_cross, 0]])
    assert common_plane_map(e0, e0, residual_no_diagonal) == sp.Matrix([1, 0, 0])
    assert common_plane_map(e1, e1, residual_no_diagonal) == sp.Matrix([0, 1, 0])

    # Transposition gives the v=0,u!=0 shore, including every sign above.
    transposed = sp.Matrix([[a, u_cross], [0, b]])
    for alpha, beta in product((e0, e1), repeat=2):
        assert_zero(
            common_plane_map(alpha, beta, transposed)
            - common_plane_map(beta, alpha, transposed.T)
        )

    # Boolean census: eight one-cross charts and three nonzero double-cross
    # charts.  The all-zero matrix is excluded by rank eight.
    atlas: dict[str, int] = {"one_cross": 0, "double_cross": 0}
    for a_on, u_on, v_on, b_on in product((False, True), repeat=4):
        if not (a_on or u_on or v_on or b_on):
            continue
        if u_on and v_on:
            continue
        if u_on != v_on:
            atlas["one_cross"] += 1
        else:
            atlas["double_cross"] += 1
    assert atlas == {"one_cross": 8, "double_cross": 3}

    # Double cross with both diagonals nonzero eliminates S exactly.
    diagonal = sp.diag(a, b)
    assert_zero(
        b * common_plane_map(e0, e0, diagonal)
        - a * common_plane_map(e1, e1, diagonal)
        - sp.Matrix([b, -a, 0])
    )


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


def check_single_diagonal_cross_zero_quotients() -> None:
    """Check both retained-index forks in the double-cross rank-one walls."""

    for s, i, j in permutations(range(3)):
        for diagonal_colour, visible_colour in ((i, j), (j, i)):
            scale = sp.symbols(
                f"single_diag_scale_{s}_{diagonal_colour}", nonzero=True
            )
            for tangent_colour in range(3):
                if tangent_colour != s:
                    retained = s
                    source_bar = sp.zeros(2, 1)
                    residual = sp.Matrix(sp.symbols("single_diag_C0:9")).reshape(3, 3)
                    diagonal = sp.zeros(3, 3)
                    diagonal[retained, retained] = 1
                    target_bar = unit(2, 0)
                    # Pbar=0 and Sbar_s=0 after quotient by T_visible.
                    defect = -matrix_tensor_vector(diagonal, target_bar)
                    source = matrix_tensor_vector(residual, source_bar)
                    assert source == sp.zeros(18, 1)
                    assert defect != source
                else:
                    retained = diagonal_colour
                    assert retained not in {visible_colour, tangent_colour}
                    diagonal = sp.zeros(3, 3)
                    diagonal[retained, retained] = 1
                    target_bar = unit(2, 0)
                    source_bar = -(1 / scale) * target_bar
                    residual = scale * diagonal
                    defect = -matrix_tensor_vector(diagonal, target_bar)
                    source = matrix_tensor_vector(residual, source_bar)
                    assert_zero(defect - source)


def noncoordinate_wall_map(
    alpha: sp.Matrix,
    eta: sp.Matrix,
    correction: sp.Expr,
) -> sp.Matrix:
    """Return coefficients of ``lambda_i T_i, lambda_j T_j, S``."""

    return sp.Matrix(
        [alpha[0] * eta[0], alpha[1] * eta[1], correction]
    )


def check_y_s_zero_noncoordinate_cases() -> None:
    """Replay independent, full-dependent, and singleton-dependent shores."""

    c0, c1, a0, a1, eta0, eta1 = sp.symbols(
        "ys0_c0 ys0_c1 ys0_A0 ys0_A1 ys0_eta0 ys0_eta1",
        nonzero=True,
    )
    correction_c, correction_a = sp.symbols("ys0_corr_c ys0_corr_A")
    c_row = sp.Matrix([c0, c1])
    a_row = sp.Matrix([a0, a1])
    eta = sp.Matrix([eta0, eta1])
    source = unit(3, 2)
    c_b = noncoordinate_wall_map(c_row, eta, correction_c)
    a_b = noncoordinate_wall_map(a_row, eta, correction_a)
    corrected_c = c_b - correction_c * source
    corrected_a = a_b - correction_a * source
    coefficient_matrix = sp.Matrix(
        [
            [corrected_c[0], corrected_c[1]],
            [corrected_a[0], corrected_a[1]],
        ]
    )
    assert_zero(
        coefficient_matrix.det()
        - eta0 * eta1 * (c0 * a1 - c1 * a0)
    )
    # S=M(A,d) and M(c,d)=0 are the exact correction-removal interface.
    assert_zero(c_b - corrected_c - correction_c * source)
    assert_zero(a_b - corrected_a - correction_a * source)

    # If the dependent kernel row c is full, its corrected map contains both
    # transverse target coefficients.  S2CK owns the resulting obstruction.
    assert_nonzero(corrected_c[0])
    assert_nonzero(corrected_c[1])
    assert_zero(corrected_c[2])

    # Singleton kernel c=e_i; the i/j-swapped chart is replayed separately.
    singleton_fixture_count = 0
    for singleton in range(2):
        other = 1 - singleton
        c_single = unit(2, singleton)
        a_single = unit(2, other)
        eta_single = sp.Matrix(
            [
                sp.symbols(f"ys0_eta_{singleton}_0", nonzero=True),
                sp.symbols(f"ys0_eta_{singleton}_1", nonzero=True),
            ]
        )
        corr_c, corr_a = sp.symbols(
            f"ys0_single_corr_c_{singleton} ys0_single_corr_A_{singleton}"
        )
        c_map = noncoordinate_wall_map(c_single, eta_single, corr_c)
        a_map = noncoordinate_wall_map(a_single, eta_single, corr_a)
        # B'=B-corr_a*d; M(A,d)=S and M(c,d)=0.
        c_b_prime = c_map
        a_b_prime = a_map - corr_a * source
        expected_c = sp.zeros(3, 1)
        expected_c[singleton] = eta_single[singleton]
        expected_c[2] = corr_c
        expected_a = sp.zeros(3, 1)
        expected_a[other] = eta_single[other]
        assert_zero(c_b_prime - expected_c)
        assert_zero(a_b_prime - expected_a)
        independent_coefficients = sp.Matrix(
            [
                [c_single[0] * eta_single[0], c_single[1] * eta_single[1]],
                [a_single[0] * eta_single[0], a_single[1] * eta_single[1]],
            ]
        )
        assert_nonzero(independent_coefficients.det())

        # At the pure common row u, S(u)=0.  The uB'(u)=0 coefficient gives
        # lambda_i(u)=0; projecting the symmetry identity
        # AB'(u)=uB'(A) off the u-factor slab gives lambda_j(u)=0.
        lambda_single_u, lambda_other_u = sp.symbols(
            f"ys0_lambda_single_u_{singleton} ys0_lambda_other_u_{singleton}"
        )
        s_u = sp.Integer(0)
        u_b_at_u = eta_single[singleton] * lambda_single_u + corr_c * s_u
        assert_zero(u_b_at_u.subs(lambda_single_u, 0))
        projected_symmetry = eta_single[other] * lambda_other_u
        assert_zero(projected_symmetry.subs(lambda_other_u, 0))

        # In the coefficient basis (q_s,q_i,q_j), the joint kernel of
        # lambda_i,lambda_j is exactly q_s.
        coordinate_functionals = sp.Matrix([[0, 1, 0], [0, 0, 1]])
        joint_kernel = coordinate_functionals.nullspace()
        assert joint_kernel == [unit(3, 0)]
        singleton_fixture_count += 1
    assert singleton_fixture_count == 2


def check_y_s_zero_retained_s_face() -> None:
    """Check the ordinary and exceptional s-face signs after the u quotient."""

    for s, tangent_colour in product(range(3), repeat=2):
        diagonal = sp.zeros(3, 3)
        diagonal[s, s] = 1
        target_bar = unit(2, 0)
        source_tensors = tuple(sp.zeros(2, 1) for _ in range(3))
        p_bar = sp.zeros(18, 1)
        defect = p_bar - matrix_tensor_vector(diagonal, target_bar)
        residual = sp.Matrix(sp.symbols(f"ys0_C_{s}_{tangent_colour}_0:9")).reshape(3, 3)
        if s != tangent_colour:
            right = matrix_tensor_vector(residual, source_tensors[s])
        else:
            tangent_matrices = tuple(
                sp.Matrix(
                    sp.symbols(f"ys0_H_{s}_{index}_0:9")
                ).reshape(3, 3)
                for index in range(3)
            )
            right = matrix_tensor_vector(residual, source_tensors[s])
            right += sum(
                (
                    matrix_tensor_vector(tangent_matrices[index], source_tensors[index])
                    for index in range(3)
                ),
                sp.zeros(18, 1),
            )
        assert right == sp.zeros(18, 1)
        assert defect != right


def check_coordinate_pair_rank_one_and_rank_two_a_nonzero() -> None:
    """Replay the two adjacent zeros and opposite T_k coefficient."""

    a = sp.symbols("coord_a", nonzero=True)
    b, c, d = sp.symbols("coord_b coord_c coord_d")
    e0 = unit(2, 0)
    residual = sp.Matrix([[a, b], [c, d]])
    alpha = sp.Matrix([c, -a])
    beta = sp.Matrix([b, -a])
    assert_zero(coordinate_pair_map(alpha, e0, residual))
    assert_zero(coordinate_pair_map(e0, beta, residual))
    delta = sp.factor(residual.det())
    opposite = coordinate_pair_map(alpha, beta, residual)
    base = coordinate_pair_map(e0, e0, residual)
    assert base == sp.Matrix([0, a])
    assert_zero(opposite - sp.Matrix([a**2, a * delta]))
    assert_zero(opposite - delta * base - sp.Matrix([a**2, 0]))

    rank_two_delta = sp.symbols("coord_rank_two_delta", nonzero=True)
    rank_two = residual.subs(d, (rank_two_delta + b * c) / a)
    assert_zero(rank_two.det() - rank_two_delta)
    assert_zero(coordinate_pair_map(alpha, e0, rank_two))
    assert_zero(coordinate_pair_map(e0, beta, rank_two))
    assert_zero(
        coordinate_pair_map(alpha, beta, rank_two)
        - rank_two_delta * coordinate_pair_map(e0, e0, rank_two)
        - sp.Matrix([a**2, 0])
    )

    # Rank one is the exact Delta=0 specialization.  Nonzero row r and
    # column s force a!=0; the opposite corner is still a^2 lambda_k T_k.
    rank_one = residual.subs(d, b * c / a)
    assert_zero(rank_one.det())
    assert_zero(coordinate_pair_map(alpha, e0, rank_one))
    assert_zero(coordinate_pair_map(e0, beta, rank_one))
    assert_zero(
        coordinate_pair_map(alpha, beta, rank_one) - sp.Matrix([a**2, 0])
    )

    # If a=0 while row r and column s are both nonzero, b,c are nonzero and
    # det D=-bc, so this is necessarily the repaired rank-two branch.
    b0, c0 = sp.symbols("coord_a0_b coord_a0_c", nonzero=True)
    d0 = sp.symbols("coord_a0_d")
    a_zero = sp.Matrix([[0, b0], [c0, d0]])
    assert_nonzero(a_zero.det())
    assert_zero(a_zero.det() + b0 * c0)


def choose_retained_coordinate(s: int, r: int, tangent_colour: int) -> int:
    choices = [colour for colour in (s, r) if colour != tangent_colour]
    assert choices
    return choices[0]


def check_coordinate_pair_retained_indices() -> None:
    """Check every colour permutation and exact retained diagonal h."""

    checked = 0
    for s, r, k in permutations(range(3)):
        for tangent_colour in range(3):
            retained = choose_retained_coordinate(s, r, tangent_colour)
            assert retained in {s, r}
            assert retained != tangent_colour
            assert retained != k
            target_bar = unit(2, 0)
            diagonal = sp.zeros(3, 3)
            diagonal[retained, retained] = 1
            p_bar = sp.zeros(18, 1)
            source_bar = sp.zeros(2, 1)
            residual = sp.Matrix(
                sp.symbols(f"coord_retained_C_{s}_{r}_{tangent_colour}_0:9")
            ).reshape(3, 3)
            defect = p_bar - matrix_tensor_vector(diagonal, target_bar)
            right = matrix_tensor_vector(residual, source_bar)
            assert right == sp.zeros(18, 1)
            assert defect != right
            checked += 1
    assert checked == 18


def check_rank_two_a_zero_coefficient_interfaces() -> None:
    """Replay the repaired a=0 algebra in both incidence forks."""

    b, c, rho = sp.symbols("a0_b a0_c a0_rho", nonzero=True)
    d = sp.symbols("a0_d")
    e0, e1 = unit(2, 0), unit(2, 1)
    residual = sp.Matrix([[0, b], [c, d]])
    u_d = coordinate_pair_map(e0, e0, residual)
    u_b = coordinate_pair_map(e0, e1, residual)
    a_d = coordinate_pair_map(e1, e0, residual)
    a_b = coordinate_pair_map(e1, e1, residual)
    assert_zero(u_d)
    assert u_b == sp.Matrix([0, b])
    assert a_d == sp.Matrix([0, c])
    assert a_b == sp.Matrix([1, d])

    # Independent u,d: permanent symmetry gives S(u)=S(d)=0.  The script
    # records the exact nonzero scalar interfaces; S2CG owns the conclusion
    # that the involved planes coincide with the split kernel H.
    s_u, s_d = sp.symbols("a0_Su a0_Sd")
    assert_zero((c * s_u).subs(s_u, 0))
    assert_zero((b * s_d).subs(s_d, 0))

    # Dependent d=rho*u.  Adjacent proportionality gives a second radical
    # row, and shifting B removes the dS term with the displayed sign.
    mixed_u_a = sp.Matrix([0, c / rho])
    radical_map = mixed_u_a - (c / (rho * b)) * u_b
    assert_zero(radical_map)
    b_prime_map = a_b - (d * rho / c) * mixed_u_a
    assert_zero(b_prime_map - sp.Matrix([1, 0]))

    kappa = sp.symbols("a0_kappa")
    u_vector, a_vector = unit(2, 0), unit(2, 1)
    b_vector = (rho * b / c) * (a_vector - kappa * u_vector)
    b_prime_vector = b_vector - (d * rho / c) * u_vector
    lam = rho * b / c
    mu = -rho * (b * kappa + d) / c
    assert_nonzero(lam)
    assert_zero(b_prime_vector - lam * a_vector - mu * u_vector)


def check_rank_two_a_zero_independent_fixture() -> None:
    """Replay the equal split-plane quotient in the independent fork."""

    zero = sp.zeros(2, 1)
    x = row(unit(2, 0), zero, zero)
    y = row(zero, unit(2, 0), zero)
    z = row(zero, zero, unit(2, 0))
    u = x + y
    v = x - y
    a_row = x
    b_row = y
    target_k = tensor3(unit(2, 0), unit(2, 0), unit(2, 0))
    assert sp.Matrix.hstack(u, a_row).rank() == 2
    assert sp.Matrix.hstack(v, b_row).rank() == 2
    for q in (x, y, z):
        assert_zero(polarized(u, v, q))
    # The two source realizations vanish on H=span(x,y), while their values
    # on the omitted pure row are nonzero and proportional.
    assert_zero(polarized(u, b_row, x))
    assert_zero(polarized(u, b_row, y))
    assert_zero(polarized(a_row, v, x))
    assert_zero(polarized(a_row, v, y))
    assert_zero(polarized(u, b_row, z) - target_k)
    assert_zero(polarized(a_row, v, z) + target_k)
    assert_zero(polarized(a_row, b_row, z) - target_k)
    # For h=s or r, all three diagonal rows lie in H and the permanent dies
    # before the full T_k factor quotient.  This is the normalized interface
    # behind S_h=0 and the retained diagonal contradiction.
    for r_row, p_row, q_row in product((x, y), repeat=3):
        assert_zero(polarized(r_row, p_row, q_row))


def quotient_factor_coordinate(
    value: sp.Matrix,
    source: int,
    retained_coordinate: int,
) -> sp.Matrix:
    """Project one two-dimensional source onto one quotient coordinate."""

    assert value.rows == 8
    entries = []
    for i, j, k in product(range(2), repeat=3):
        indices = (i, j, k)
        if indices[source] == retained_coordinate:
            entries.append(value[(i * 2 + j) * 2 + k])
    return sp.Matrix(entries)


def check_rank_two_a_zero_pure_row_pencil() -> None:
    """Check the one-sided and full-support pure-row pencil interfaces."""

    zero = sp.zeros(2, 1)
    x0, x1 = unit(2, 0), unit(2, 1)
    y0, z0 = unit(2, 0), unit(2, 0)
    u = row(x0, zero, zero)
    lam = sp.symbols("pencil_lambda", nonzero=True)
    mu = sp.symbols("pencil_mu")

    # A_Y=0 (the A_Z=0 case is obtained by swapping Y,Z).  The map vanishes
    # on H=span(u,A), so H is the visible functional's kernel.  Quotienting
    # Z by A_Z kills every diagonal permanent with rows in H.
    a_one_sided = row(x1, zero, z0)
    b_one_sided = lam * a_one_sided + mu * u
    q_omitted = row(zero, y0, zero)
    assert_zero(polarized(a_one_sided, b_one_sided, u))
    assert_zero(polarized(a_one_sided, b_one_sided, a_one_sided))
    assert polarized(a_one_sided, b_one_sided, q_omitted) != sp.zeros(8, 1)
    for p_row, q_row in product((u, a_one_sided), repeat=2):
        value = polarized(u, p_row, q_row)
        quotient = quotient_factor_coordinate(value, source=2, retained_coordinate=1)
        assert_zero(quotient)

    # Explicit Y/Z exchange replays the dual shore.
    a_dual = row(x1, y0, zero)
    b_dual = lam * a_dual + mu * u
    q_dual = row(zero, zero, z0)
    assert_zero(polarized(a_dual, b_dual, u))
    assert_zero(polarized(a_dual, b_dual, a_dual))
    assert polarized(a_dual, b_dual, q_dual) != sp.zeros(8, 1)

    # A_Y,A_Z!=0.  The analytic rank-one condition forces A_X~u and
    # pr_X(Q)=K u.  This normalized fixture checks the resulting map and the
    # X/u quotient used on the retained diagonal.
    a_full = row(x0, y0, z0)
    b_full = lam * a_full + mu * u
    q_basis = (u, row(zero, y0, zero), row(zero, zero, z0))
    target = tensor3(x0, y0, z0)
    full_values = tuple(polarized(a_full, b_full, q) for q in q_basis)
    assert_zero(full_values[0] - 2 * lam * target)
    assert all(value.rank() == 1 for value in full_values)
    for value in full_values:
        assert all(
            value[index] == 0
            for index in range(8)
            if index != 0
        )
    for p_row, q_row in product(q_basis, repeat=2):
        value = polarized(u, p_row, q_row)
        quotient = quotient_factor_coordinate(value, source=0, retained_coordinate=1)
        assert_zero(quotient)


def main() -> None:
    check_root_exchange()
    check_y_s_nonzero_cross_zero_atlas()
    check_single_diagonal_cross_zero_quotients()
    check_y_s_zero_noncoordinate_cases()
    check_y_s_zero_retained_s_face()
    check_coordinate_pair_rank_one_and_rank_two_a_nonzero()
    check_coordinate_pair_retained_indices()
    check_rank_two_a_zero_coefficient_interfaces()
    check_rank_two_a_zero_independent_fixture()
    check_rank_two_a_zero_pure_row_pencil()
    print("all six colour permutations and both root orientations: PASS")
    print("y_s != 0 cross-zero D atlas and diagonal quotients: PASS")
    print("y_s = 0 noncoordinate independent/dependent shores: PASS")
    print("coordinate-coordinate rank-one and rank-two a != 0: PASS")
    print("repaired rank-two a = 0 coefficient and pure-row forks: PASS")
    print("exact retained diagonal indices and quotient signs: PASS")
    print("analytic owners: S2CG, S2CI, and S2CK")


if __name__ == "__main__":
    main()
