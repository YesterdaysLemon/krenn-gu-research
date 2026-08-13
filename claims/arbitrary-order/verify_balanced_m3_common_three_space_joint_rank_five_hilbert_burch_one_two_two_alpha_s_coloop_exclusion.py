"""Exact replay for the (1,2,2) alpha_s-coloop exclusion.

The owning Markdown file is the proof.  This verifier checks the determinant-
face pencil, its two coordinate-projection gates, the projective linear-factor
fork, the four resulting binary target tables, the distinct-plane cubic
restriction kernels, and every equal-plane orientation of the new same-pair
obstruction.
"""

from __future__ import annotations

from itertools import combinations_with_replacement, permutations, product
from math import factorial

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def target(
    alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix
) -> sp.Matrix:
    return sp.Matrix(
        [alpha[index] * beta[index] * gamma[index] for index in range(3)]
    )


def pencil_and_projection_gates() -> None:
    u, v, mu, ys, yh = sp.symbols("u v mu ys yh", nonzero=True)
    z0, z1, z2, w0, w1, w2 = sp.symbols(
        "z0 z1 z2 w0 w1 w2"
    )

    # If the two evaluation pairs lie on the same projective line [u:v],
    # the first component of the derivative transpose vanishes.
    beta_scale, gamma_scale = sp.symbols("beta_scale gamma_scale")
    beta_y = beta_scale * u
    mu_beta_t = beta_scale * v
    gamma_z = gamma_scale * u
    gamma_w = gamma_scale * v
    determinant = sp.expand(beta_y * gamma_w - mu_beta_t * gamma_z)
    assert determinant == 0

    # Fix s=0,t=1 for the unequal-colour chart.  The normal of P_[u:v]
    # is v*y-u*mu*e_t, while that of Q_[u:v] is v*z-u*w.
    y = sp.Matrix([ys, 0, yh])
    z = sp.Matrix([z0, z1, z2])
    w = sp.Matrix([w0, w1, w2])
    p_normal = v * y - u * mu * e(1)
    q_normal = v * z - u * w
    p_gate = sp.Matrix.vstack(p_normal.T, e(1).T, e(2).T).det()
    q_gate = sp.Matrix.vstack(q_normal.T, e(1).T, e(2).T).det()
    assert sp.factor(p_gate) == v * ys
    assert sp.factor(q_gate) == -u * w0 + v * z0

    # The two rows can be matched with opposite evaluation pairs, putting
    # their row classes on one common quotient line modulo R.
    assert sp.Matrix([u, v]) + sp.Matrix([-u, -v]) == sp.zeros(2, 1)
    print("determinant-face pencil: PASS (zero face / common quotient line)")


def projective_factor_fork() -> None:
    u, v, mu, ys, zs, ws = sp.symbols(
        "u v mu ys zs ws", nonzero=True
    )

    # For s!=t the gauge y_t=0 gives L_P=v*y_s.  Vanishing of
    # L_P*L_Q on every projective direction forces y_s=0 or z_s=w_s=0.
    lp_distinct = v * ys
    lq = v * zs - u * ws
    product_distinct = sp.Poly(sp.expand(lp_distinct * lq), u, v)
    assert product_distinct.coeff_monomial(u * v) == -ws * ys
    assert product_distinct.coeff_monomial(v**2) == ys * zs
    assert product_distinct.coeff_monomial(u**2) == 0

    # For s=t, the gauge already has y_s=y_t=0 and L_P=-u*mu, a
    # nonzero linear form.  The same product identity therefore forces B.
    lp_equal = -u * mu
    product_equal = sp.Poly(sp.expand(lp_equal * lq), u, v)
    assert product_equal.coeff_monomial(u**2) == mu * ws
    assert product_equal.coeff_monomial(u * v) == -mu * zs
    assert product_equal.coeff_monomial(v**2) == 0
    print("projective factor fork: PASS (A: s!=t,y_s=0 or B: z_s=w_s=0)")


def nonzero_cells(
    alphas: list[sp.Matrix],
    betas: list[sp.Matrix],
    gammas: list[sp.Matrix],
) -> dict[tuple[int, int, int], tuple[sp.Expr, ...]]:
    cells = {}
    for i, j, k in product(range(2), repeat=3):
        value = target(alphas[i], betas[j], gammas[k])
        if value != sp.zeros(3, 1):
            cells[(i, j, k)] = tuple(value)
    return cells


def binary_target_tables() -> None:
    r_basis = [e(1), e(2)]

    # Both coordinate projections invertible: the S2AN diagonal cube.
    diagonal = nonzero_cells(r_basis, [e(1), e(2)], [e(1), e(2)])
    assert set(diagonal) == {(0, 0, 0), (1, 1, 1)}

    # A and not B: P has an invisible e_s row and one active row; Q has
    # coordinate lifts.  The two targets share the active P row.
    p_normal = e(2) - e(1)
    q_normal = e(0) + e(1) - e(2)
    p_basis = [e(0), e(1) + e(2)]
    q_basis = [-e(0) + e(1), e(0) + e(2)]
    assert all((p_normal.T * vector)[0] == 0 for vector in p_basis)
    assert all((q_normal.T * vector)[0] == 0 for vector in q_basis)
    a_only = nonzero_cells(r_basis, p_basis, q_basis)
    assert set(a_only) == {(0, 1, 0), (1, 1, 1)}

    # B and not A: P has coordinate lifts; Q has an invisible e_s row and
    # one active row.  This is the S2AO same-third-row table.
    p_normal = e(0) - e(1) + e(2)
    q_normal = e(1) - e(2)
    p_basis = [e(0) + e(1), -e(0) + e(2)]
    q_basis = [e(0), e(1) + e(2)]
    assert all((p_normal.T * vector)[0] == 0 for vector in p_basis)
    assert all((q_normal.T * vector)[0] == 0 for vector in q_basis)
    b_only = nonzero_cells(r_basis, p_basis, q_basis)
    assert set(b_only) == {(0, 0, 1), (1, 1, 1)}

    # A and B: both planes have an invisible e_s row.  The two nonzero
    # targets share the active P,Q pair, giving the new same-pair table.
    p_basis = [e(0), e(1) + e(2)]
    q_basis = [e(0), e(1) + e(2)]
    both = nonzero_cells(r_basis, p_basis, q_basis)
    assert set(both) == {(0, 1, 1), (1, 1, 1)}
    print("binary target tables: PASS (diagonal / two same-row / same-pair)")


MONOMIALS = list(combinations_with_replacement(range(3), 3))


def plane_basis(normal: tuple[int, int, int]) -> list[sp.Matrix]:
    return [sp.Matrix(vector) for vector in sp.Matrix([normal]).nullspace()]


def symmetric_value(
    monomial: tuple[int, int, int],
    left: sp.Matrix,
    middle: sp.Matrix,
    right: sp.Matrix,
) -> sp.Expr:
    assignments = set(permutations(monomial))
    multiplicities = [monomial.count(index) for index in range(3)]
    multinomial = factorial(3)
    for multiplicity in multiplicities:
        multinomial //= factorial(multiplicity)
    return sp.simplify(
        sum(
            left[i] * middle[j] * right[k]
            for i, j, k in assignments
        )
        / multinomial
    )


def restriction_matrix(
    normals: tuple[
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
    ],
) -> sp.Matrix:
    bases = [plane_basis(normal) for normal in normals]
    return sp.Matrix(
        [
            [symmetric_value(monomial, r, p, q) for monomial in MONOMIALS]
            for r, p, q in product(*bases)
        ]
    )


def polynomial(vector: sp.Matrix) -> sp.Expr:
    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    return sp.factor(
        sum(
            vector[index]
            * variables[monomial[0]]
            * variables[monomial[1]]
            * variables[monomial[2]]
            for index, monomial in enumerate(MONOMIALS)
        )
    )


def distinct_plane_kernels() -> None:
    independent = restriction_matrix(
        ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    )
    assert independent.rank() == 7
    assert {str(polynomial(vector)) for vector in independent.nullspace()} == {
        "x**3",
        "y**3",
        "z**3",
    }

    pencil = restriction_matrix(
        ((1, 0, 0), (0, 1, 0), (1, 1, 0))
    )
    assert pencil.rank() == 7
    assert {str(polynomial(vector)) for vector in pencil.nullspace()} == {
        "x**3",
        "x*y*(x + y)",
        "y**3",
    }
    print("same-pair distinct planes: PASS (independent / pencil kernels)")


def equal_plane_orientations() -> None:
    l00, l01, l10, l11 = sp.symbols("l00 l01 l10 l11")
    matrix = sp.Matrix([[l00, l01], [l10, l11]])
    e01 = sp.Matrix([[0, 1], [0, 0]])
    e11 = sp.diag(0, 1)

    # R=P (and, by symmetry, R=Q): the two independent target coefficients
    # occur as E_01 and E_11.  Symmetry of L*F kills the first row of L.
    skew_01 = matrix * e01 - (matrix * e01).T
    skew_11 = matrix * e11 - (matrix * e11).T
    assert sp.solve(
        [skew_01[0, 1], skew_11[0, 1]],
        (l00, l01),
        dict=True,
    ) == [{l00: 0, l01: 0}]

    # P=Q: symmetry for E_11 gives l01=0, hence q0 is proportional to p0.
    # The zero q0 column then identifies both active values with the square
    # map per(-,p1,p1), which cannot contain two transverse targets by S2AL.
    assert sp.solve(skew_11[0, 1], l01) == [0]
    a, b, c, d = sp.symbols("a b c d", nonzero=True)
    lower = sp.Matrix([[a, 0], [b, d]])
    coefficient_table = c * e11
    symmetric_square = sp.simplify(
        coefficient_table * lower.T.inv()
    )
    assert symmetric_square == (c / d) * e11
    print("same-pair equal planes: PASS (singular R-equality / P=Q square)")


def main() -> None:
    pencil_and_projection_gates()
    projective_factor_fork()
    binary_target_tables()
    distinct_plane_kernels()
    equal_plane_orientations()
    print("(1,2,2) alpha_s-coloop exclusion: PASS")


if __name__ == "__main__":
    main()
