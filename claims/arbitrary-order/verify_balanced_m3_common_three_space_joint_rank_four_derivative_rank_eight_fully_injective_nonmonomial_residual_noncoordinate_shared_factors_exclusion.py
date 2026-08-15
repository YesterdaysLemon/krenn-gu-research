#!/usr/bin/env python3
"""Exact replay for the noncoordinate structural-zero exclusion (S2CN).

The written proof owns the load-bearing analytic inputs: S2BQ's exhaustive
tangent-quotient atlas, S2CG's zero-pair support theorem, S2CI's exhaustive
two-cross incidence dichotomy, and S2CK's two-transverse mixed-map
obstruction.  This deterministic SymPy replay checks only the exact algebraic
interfaces between those results.  In particular, finite support tables and
normalized fixtures below do not replace any of the four analytic inputs.
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


def support(mask: int) -> Support:
    return frozenset(index for index in range(3) if mask & (1 << index))


def support_vector(support_set: Support) -> sp.Matrix:
    entries = (sp.Integer(2), sp.Integer(3), sp.Integer(5))
    return sp.Matrix(
        [entries[index] if index in support_set else 0 for index in range(3)]
    )


def complement(index: int) -> tuple[int, int]:
    values = tuple(value for value in range(3) if value != index)
    assert len(values) == 2
    return values[0], values[1]


def boundary_covector(vector: sp.Matrix, omitted: int) -> sp.Matrix:
    """Span ``vector^perp intersect ker(ev_omitted)`` exactly."""

    first, second = complement(omitted)
    value = sp.zeros(3, 1)
    value[first] = vector[second]
    value[second] = -vector[first]
    assert_zero(value.dot(vector))
    assert value[omitted] == 0
    return value


def full_partner_covector(vector: sp.Matrix, omitted: int) -> sp.Matrix:
    """Construct a perpendicular covector full off ``omitted``."""

    first, second = complement(omitted)
    value = sp.zeros(3, 1)
    value[first] = 1
    value[second] = 1
    if vector[omitted] != 0:
        value[omitted] = -(
            vector[first] + vector[second]
        ) / vector[omitted]
    else:
        value[first] = vector[second]
        value[second] = -vector[first]
    assert_zero(value.dot(vector))
    assert value[first] != 0 and value[second] != 0
    return value


def restricted_form(root: sp.Matrix, coordinate: int) -> sp.Matrix:
    basis = sp.Matrix.hstack(*root.T.nullspace())
    assert basis.shape == (3, 2)
    return basis[coordinate, :]


def check_kernel_singleton_gate() -> None:
    """Exhaust the finite support gate before the structural incidence split."""

    noncoordinate = tuple(
        support(mask) for mask in range(1, 8) if len(support(mask)) >= 2
    )
    singleton_cases: list[tuple[Support, int, int]] = []
    secant_cases = 0

    for root_support, d in product(noncoordinate, range(3)):
        root = support_vector(root_support)
        alpha = boundary_covector(root, d)
        alpha_support = {
            index for index in range(3) if alpha[index] != 0
        }
        if len(alpha_support) == 1:
            missing = next(iter(alpha_support))
            singleton_cases.append((root_support, d, missing))
            assert root_support == frozenset(complement(missing))
            assert d in root_support
        else:
            assert alpha_support == set(complement(d))
            for partner_support in noncoordinate:
                partner = support_vector(partner_support)
                beta = full_partner_covector(partner, d)
                first, second = complement(d)
                # Since alpha_d=0, every S2BQ quotient-monomial correction
                # lambda alpha_d beta_e vanishes for every e.  Both displayed
                # target coefficients are nonzero, which is precisely the
                # interface passed to S2CK.
                assert_zero(alpha[d])
                assert_nonzero(alpha[first] * beta[first])
                assert_nonzero(alpha[second] * beta[second])
                secant_cases += 1

    assert len(singleton_cases) == 6
    assert secant_cases == 24
    # Applying the same gate to both roots leaves 6 by 6 labelled choices.
    assert len(tuple(product(singleton_cases, repeat=2))) == 36


def check_one_sided_pure_row_table() -> None:
    """Replay the pure-row pencil and its one-factor slab consequences."""

    x0, y0, z0 = unit(2, 0), unit(2, 0), unit(2, 0)
    zero = sp.zeros(2, 1)
    u = row(x0, zero, zero)
    by, bz = sp.symbols("one_side_by one_side_bz", nonzero=True)
    qx0, qx1, qy0, qy1, qz0, qz1 = sp.symbols("one_side_q0:6")
    q = row(
        sp.Matrix([qx0, qx1]),
        sp.Matrix([qy0, qy1]),
        sp.Matrix([qz0, qz1]),
    )

    cases = (
        (row(zero, by * y0, zero), {"Z"}),
        (row(zero, zero, bz * z0), {"Y"}),
        (row(zero, by * y0, bz * z0), {"Y", "Z"}),
    )
    target_index = 0
    y_wall_index = 2  # X_0 tensor Y_1 tensor Z_0
    z_wall_index = 1  # X_0 tensor Y_0 tensor Z_1

    for b_row, fixed_projections in cases:
        value = polarized(u, b_row, q)
        expected = tensor3(x0, blocks(b_row)[1], blocks(q)[2])
        expected += tensor3(x0, blocks(q)[1], blocks(b_row)[2])
        assert_zero(value - expected)
        b_y = blocks(b_row)[1]
        b_z = blocks(b_row)[2]
        assert value[target_index] == b_y[0] * qz0 + b_z[0] * qy0
        if "Y" in fixed_projections:
            assert value[y_wall_index] == bz * qy1
        else:
            assert_zero(value[y_wall_index])
        if "Z" in fixed_projections:
            assert value[z_wall_index] == by * qz1
        else:
            assert_zero(value[z_wall_index])

    # Both missing components would make the supposedly visible map zero.
    assert_zero(polarized(u, row(zero, zero, zero), q))

    # Once one projection is fixed, every permanent of three Q rows lies in
    # the corresponding one-factor slab.  Here the fixed factor is Z_0.
    generic_rows = []
    for index in range(3):
        x_entries = sp.Matrix(sp.symbols(f"slab_x{index}_0:2"))
        y_entries = sp.Matrix(sp.symbols(f"slab_y{index}_0:2"))
        z_scalar = sp.symbols(f"slab_z{index}")
        generic_rows.append(row(x_entries, y_entries, z_scalar * z0))
    slab_value = polarized(*generic_rows)
    for i, j in product(range(2), repeat=2):
        assert_zero(slab_value[(i * 2 + j) * 2 + 1])


def physical_quotient_scalar(value: sp.Matrix) -> sp.Expr:
    """Quotient three two-spaces by their zeroth coordinate lines."""

    assert value.rows == 8
    return sp.factor(value[7])


def check_independent_zero_pair_interfaces() -> None:
    """Check normalized equal-plane and split-Q interfaces from S2CG."""

    x = row(unit(2, 0), sp.zeros(2, 1), sp.zeros(2, 1))
    y = row(sp.zeros(2, 1), unit(2, 0), sp.zeros(2, 1))
    z = row(sp.zeros(2, 1), sp.zeros(2, 1), unit(2, 0))
    target = tensor3(unit(2, 0), unit(2, 0), unit(2, 0))
    u = x + y
    v = x - y

    for q in (x, y, z):
        assert_zero(polarized(u, v, q))

    # Equal split plane: B has no omitted-source component, so Alt(Q) and
    # the analytic support argument put B in H=span(x,y).  The visible map
    # has kernel H, and any retained face with two H rows dies after the
    # target-factor quotient.
    b_equal = u
    equal_values = tuple(polarized(u, b_equal, q) for q in (x, y, z))
    assert_zero(equal_values[0])
    assert_zero(equal_values[1])
    assert_zero(equal_values[2] - 2 * target)
    arbitrary = row(
        sp.Matrix(sp.symbols("ind_rX0:2")),
        sp.Matrix(sp.symbols("ind_rY0:2")),
        sp.Matrix(sp.symbols("ind_rZ0:2")),
    )
    assert_zero(physical_quotient_scalar(polarized(arbitrary, u, v)))

    # Split Q: after the analytic rank-one equations remove H-shifts from
    # B, normalize B=z.  The whole Q^3 image is the single target line and
    # therefore dies in the same quotient.
    split_values = tuple(polarized(u, z, q) for q in (x, y, z))
    assert_zero(split_values[0] - target)
    assert_zero(split_values[1] - target)
    assert_zero(split_values[2])
    for q0, q1, q2 in product((x, y, z), repeat=3):
        assert_zero(physical_quotient_scalar(polarized(q0, q1, q2)))


def check_bilinear_slab_and_support_recovery() -> None:
    """Replay the slab coefficient comparison and its support consequence."""

    c_entries = sp.symbols("slab_C0:4")
    b_entries = sp.symbols("slab_b0:4")
    correction = sp.Matrix(2, 2, c_entries)
    bilinear = sp.Matrix(2, 2, b_entries)
    s0, s1 = sp.symbols("slab_S0 slab_S1")

    # In a quotient basis with Tbar=e_0 and Sbar=s0 e_0+s1 e_1,
    # coefficient comparison is b_ij+C_ij*s0=0 and C_ij*s1=0.
    # For every possible nonzero pivot of C, the following division-free
    # identity yields all 2 x 2 proportionality minors.
    for pivot, entry in enumerate(correction):
        pivot_equation = bilinear[pivot] + entry * s0
        for index, other in enumerate(correction):
            other_equation = bilinear[index] + other * s0
            assert_zero(
                entry * other_equation
                - other * pivot_equation
                - (entry * bilinear[index] - other * bilinear[pivot])
            )

    # The source coefficient orthogonal to Tbar is C_ij*s1.  A proved
    # nonzero pivot of C therefore forces that coefficient to vanish.
    nonzero_pivot = sp.symbols("slab_nonzero_pivot", nonzero=True)
    assert sp.solve(nonzero_pivot * s1, s1) == [0]

    scale = sp.symbols("slab_scale", nonzero=True)
    target_bar = unit(2, 0)
    source_bar = -scale * target_bar
    assert_zero(
        sp.kronecker_product(scale * correction, target_bar)
        + sp.kronecker_product(correction, source_bar)
    )

    noncoordinate = tuple(
        support(mask) for mask in range(1, 8) if len(support(mask)) >= 2
    )
    for a in range(3):
        t, k = complement(a)
        proportional_supports = []
        for root_support in noncoordinate:
            root = support_vector(root_support)
            forms = sp.Matrix.vstack(
                restricted_form(root, t),
                restricted_form(root, k),
            )
            if sp.factor(forms.det()) == 0:
                proportional_supports.append(root_support)
        assert proportional_supports == [frozenset((t, k))]

        root = support_vector(frozenset((t, k)))
        form_t = restricted_form(root, t)
        for coordinate in range(3):
            pair = sp.Matrix.vstack(
                form_t,
                restricted_form(root, coordinate),
            )
            assert (sp.factor(pair.det()) == 0) == (coordinate != a)


def quotient_correction(
    alpha: sp.Matrix,
    beta: sp.Matrix,
    d: int,
    e: int,
    scale: sp.Expr,
) -> sp.Expr:
    return sp.factor(scale * alpha[d] * beta[e])


def check_opposite_structural_corner() -> None:
    """Check every colour permutation of the repaired opposite shore."""

    quotient_scale = sp.symbols("opposite_lambda", nonzero=True)
    shift = sp.symbols("opposite_shift")
    for a, t, k in permutations(range(3)):
        x_t, x_k, y_t, y_k = sp.symbols(
            f"opp_x{t} opp_x{k} opp_y{t} opp_y{k}",
            nonzero=True,
        )
        x_root = sp.zeros(3, 1)
        y_root = sp.zeros(3, 1)
        x_root[t], x_root[k] = x_t, x_k
        y_root[t], y_root[k] = y_t, y_k
        alpha = sp.zeros(3, 1)
        beta = sp.zeros(3, 1)
        alpha[t], alpha[k] = x_k, -x_t
        beta[t], beta[k] = y_k, -y_t
        singleton = unit(3, a)
        assert_zero(alpha.dot(x_root))
        assert_zero(beta.dot(y_root))
        assert sp.Matrix.hstack(singleton, alpha).rank() == 2
        assert sp.Matrix.hstack(beta, singleton).rank() == 2

        for d, e in product((t, k), repeat=2):
            # Original structural shore (e_a,beta).
            assert_zero(quotient_correction(singleton, beta, d, e, quotient_scale))
            assert_zero(sp.Matrix([singleton[s] * beta[s] for s in range(3)]))
            # Opposite structural corner (alpha,e_a).
            assert_zero(quotient_correction(alpha, singleton, d, e, quotient_scale))
            assert_zero(sp.Matrix([alpha[s] * singleton[s] for s in range(3)]))
            # The remaining corner is exactly lambda_a tensor T_a.
            assert_zero(
                quotient_correction(singleton, singleton, d, e, quotient_scale)
            )
            products = sp.Matrix(
                [singleton[s] * singleton[s] for s in range(3)]
            )
            assert products == singleton

        # After scaling any off-kernel covector to have a-coordinate one,
        # it is e_a+shift*beta.  If p_beta=u, linearity gives p_b=p_a+shift*u;
        # in particular the Y/Z shores are unchanged because u is pure.
        off_kernel = singleton + shift * beta
        assert off_kernel[a] == 1
        assert_zero(off_kernel - singleton - shift * beta)


def check_s2ci_incidence_interfaces() -> None:
    """Replay normalized fixtures for both alternatives of S2CI."""

    zero = sp.zeros(2, 1)
    x = row(unit(2, 0), zero, zero)
    y = row(zero, unit(2, 0), zero)
    z = row(zero, zero, unit(2, 0))
    target = tensor3(unit(2, 0), unit(2, 0), unit(2, 0))

    # Split-Q alternative: the second cross pair is a Y/Z conjugate pair.
    u = x
    a_row = y + z
    p_a = y - z
    assert sp.Matrix.hstack(u, a_row).rank() == 2
    assert sp.Matrix.hstack(p_a, u).rank() == 2
    for q in (x, y, z):
        assert_zero(polarized(u, u, q))
        assert_zero(polarized(a_row, p_a, q))
    visible = tuple(polarized(u, p_a, q) for q in (x, y, z))
    assert_zero(visible[0])
    assert_zero(visible[1] + target)
    assert_zero(visible[2] - target)
    assert any(value != sp.zeros(8, 1) for value in visible)
    for q0, q1, q2 in product((x, y, z), repeat=3):
        assert_zero(physical_quotient_scalar(polarized(q0, q1, q2)))

    # Equal-plane alternative: R=P=H=span(X_0,Y_0), and the visible
    # functional has kernel H.  A retained q_ell in H makes its whole face
    # vanish even before quotienting.
    a_equal = y
    p_equal = y
    assert sp.Matrix.hstack(u, a_equal).rank() == 2
    assert sp.Matrix.hstack(p_equal, u).rank() == 2
    for q in (x, y, z):
        assert_zero(polarized(u, u, q))
        assert_zero(polarized(a_equal, p_equal, q))
    equal_visible = tuple(polarized(u, p_equal, q) for q in (x, y, z))
    assert_zero(equal_visible[0])
    assert_zero(equal_visible[1])
    assert_zero(equal_visible[2] - target)
    for r_row, p_row, q_row in product((x, y), repeat=3):
        assert_zero(polarized(r_row, p_row, q_row))


def check_retained_face_sign() -> None:
    """Check the tangent-free retained-face quotient and its exact sign."""

    for a, tangent_colour in product(range(3), repeat=2):
        retained = next(
            colour
            for colour in range(3)
            if colour not in {a, tangent_colour}
        )
        assert retained != a
        assert retained != tangent_colour
        diagonal = sp.zeros(3, 3)
        diagonal[retained, retained] = 1
        scale = sp.symbols(
            f"retained_scale_{a}_{tangent_colour}", nonzero=True
        )
        residual = diagonal / scale
        target_bar = unit(2, 0)
        source_bar = -scale * target_bar

        # Pbar=0 and the retained colour differs from w=e_t, so the complete
        # face is -E_ll*Tbar=C*Sbar with no tangent column.  The displayed
        # sign gives E_ll=scale*C, hence actual C is monomial.
        face_defect = -sp.kronecker_product(diagonal, target_bar)
        face_source = sp.kronecker_product(residual, source_bar)
        assert_zero(face_defect - face_source)
        assert_zero(diagonal - scale * residual)


def main() -> None:
    check_kernel_singleton_gate()
    check_one_sided_pure_row_table()
    check_independent_zero_pair_interfaces()
    check_bilinear_slab_and_support_recovery()
    check_opposite_structural_corner()
    check_s2ci_incidence_interfaces()
    check_retained_face_sign()
    print("S2BQ finite support/kernel singleton gate: PASS")
    print("pure-row one-sided table and one-factor slab: PASS")
    print("independent zero-pair equal/split interfaces: PASS")
    print("dependent slab proportionality and support recovery: PASS")
    print("opposite structural corner and S2CI fixtures: PASS")
    print("retained tangent-free full-face sign: PASS")
    print("analytic owners: S2BQ, S2CG, S2CI, and S2CK")


if __name__ == "__main__":
    main()
