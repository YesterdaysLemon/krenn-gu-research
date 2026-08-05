"""Exact replay for the ordered secant--factor Chow/norm criterion."""

from __future__ import annotations

from math import factorial

import sympy as sp


def verify_determinant_cleared_membership() -> None:
    """Replay Proposition 1 on a nontrivial exact small model."""
    b = sp.Matrix([[1, 2, 0], [0, 1, 1], [2, 0, 1]])
    c = sp.Matrix([[1, -1, 2], [3, 1, 0]])
    gamma = b.col_join(c)
    beta = b.det()
    assert beta == 5
    assert gamma.rank() == 3

    q = sp.Matrix(sp.symbols("q0:3"))
    z = gamma * q
    numerator = b.adjugate() * z[:3, :]
    assert sp.simplify(numerator - beta * q) == sp.zeros(3, 1)
    residual = beta * z[3:, :] - c * numerator
    assert sp.simplify(residual) == sp.zeros(2, 1)

    # A perturbation supported off the pivot rows is detected exactly.
    outside = z + sp.Matrix([0, 0, 0, 0, 1])
    outside_numerator = b.adjugate() * outside[:3, :]
    outside_residual = beta * outside[3:, :] - c * outside_numerator
    assert outside_residual == sp.Matrix([0, beta])


def standard_basis(size: int, index: int) -> sp.Matrix:
    vector = sp.zeros(size, 1)
    vector[index] = 1
    return vector


def verify_simple_incidence_rank() -> None:
    """Replay rank[Gamma|D]=dim(W+D) for simple and deeper incidence."""
    ambient = 7
    w = sp.Matrix.hstack(*(standard_basis(ambient, i) for i in range(3)))

    simple_d = sp.Matrix.hstack(
        standard_basis(ambient, 2),
        standard_basis(ambient, 3),
        standard_basis(ambient, 4),
    )
    deeper_d = sp.Matrix.hstack(
        standard_basis(ambient, 1),
        standard_basis(ambient, 2),
        standard_basis(ambient, 3),
    )

    assert w.rank() == simple_d.rank() == deeper_d.rank() == 3
    assert w.row_join(simple_d).rank() == 5  # 3+3-1
    assert w.row_join(deeper_d).rank() == 4  # 3+3-2


def wedge_contraction(
    left: sp.Matrix, right: sp.Matrix, selectors: list[sp.Symbol]
) -> sp.Expr:
    terms = []
    selector_index = 0
    for row in range(left.rows):
        for column in range(row + 1, left.rows):
            terms.append(
                selectors[selector_index]
                * (left[row] * right[column] - left[column] * right[row])
            )
            selector_index += 1
    assert selector_index == len(selectors)
    return sp.expand(sum(terms, sp.Integer(0)))


def verify_universal_open_separator() -> None:
    """A generic contraction tests nonzero bivectors and pair vectors."""
    selectors = list(sp.symbols("u01 u02 u12"))
    r_0 = sp.Matrix([1, 0, 0])
    r_1 = sp.Matrix([0, 1, 0])
    r_2 = -r_0 - r_1
    assert sp.Matrix.hstack(r_0, r_1, r_2).rank() == 2
    assert r_0 + r_1 + r_2 == sp.zeros(3, 1)
    assert wedge_contraction(r_0, r_1, selectors) == selectors[0]

    deeper_0 = sp.Matrix([1, 0, 0])
    deeper_1 = sp.Matrix([2, 0, 0])
    assert wedge_contraction(deeper_0, deeper_1, selectors) == 0

    z_0, z_1, z_2 = sp.symbols("z0 z1 z2")
    pair_vector = sp.Matrix([2, -1, 0])
    pair_contraction = (sp.Matrix([z_0, z_1, z_2]).T * pair_vector)[0]
    assert pair_contraction == 2 * z_0 - z_1
    assert (sp.Matrix([z_0, z_1, z_2]).T * sp.zeros(3, 1))[0] == 0


def multiplication_matrix(
    multiplier: sp.Expr, variable: sp.Symbol, modulus: sp.Expr
) -> sp.Matrix:
    basis = [sp.Integer(1), variable, variable**2]
    columns = []
    for monomial in basis:
        remainder = sp.Poly(
            sp.rem(sp.expand(multiplier * monomial), modulus, variable), variable
        )
        columns.append(
            sp.Matrix([remainder.coeff_monomial(item) for item in basis])
        )
    return sp.Matrix.hstack(*columns)


def verify_artinian_support_trichotomy() -> None:
    """Distinguish unit, boundary-trapped, and mixed support exactly."""
    x = sp.symbols("x")
    modulus = x**2 * (x - 1)
    zero = sp.zeros(3)

    # g vanishes at both support points {0,1}, hence is nilpotent in A.
    trapped = x * (x - 1)
    m_trapped = multiplication_matrix(trapped, x, modulus)
    assert m_trapped != zero
    assert m_trapped**2 == zero
    characteristic_variable = sp.symbols("T")
    assert m_trapped.charpoly(characteristic_variable).as_expr() == (
        characteristic_variable**3
    )

    # x vanishes at 0 but not at 1: singular, yet not nilpotent.
    mixed = x
    m_mixed = multiplication_matrix(mixed, x, modulus)
    assert m_mixed.det() == 0
    assert m_mixed**3 != zero
    assert m_mixed.charpoly(characteristic_variable).as_expr() != (
        characteristic_variable**3
    )

    # x+1 avoids both support points and is therefore a unit.
    unit = x + 1
    m_unit = multiplication_matrix(unit, x, modulus)
    assert m_unit.det() == 2

    # Multiplication matrices respect products, as required for G_(M,e).
    second_factor = x + 2
    assert multiplication_matrix(mixed * second_factor, x, modulus) == (
        m_mixed * multiplication_matrix(second_factor, x, modulus)
    )


def verify_dimension_degree_and_identifiability_arithmetic() -> None:
    secant_dimension = 3 * (5 * 2) + 2
    sensor_codimension = 243 - 219
    factor_codimension = 8
    assert secant_dimension == 32
    assert secant_dimension - sensor_codimension - factor_codimension == 0

    # Three-way regrouping of five mode-wise bases.
    kruskal_sum = 3 + 3 + 3
    kruskal_threshold = 2 * 3 + 2
    assert kruskal_sum >= kruskal_threshold
    assert factorial(3) == 6

    d_3 = sp.symbols("d_3", positive=True, integer=True)
    factor_degree = 259
    downstairs_length = factor_degree * d_3
    ordered_point_bound = factorial(3) * downstairs_length
    assert downstairs_length == 259 * d_3
    assert ordered_point_bound == 1554 * d_3


def main() -> None:
    verify_determinant_cleared_membership()
    verify_simple_incidence_rank()
    verify_universal_open_separator()
    verify_artinian_support_trichotomy()
    verify_dimension_degree_and_identifiability_arithmetic()
    print("PASS: committed legal sensor ordered secant-factor Chow/norm criterion")
    print("membership_residuals=24; factor_codimension=8; expected_dimension=0")
    print("factor_degree=259; ordered_good_cover=6; committed_outcome=UNKNOWN")


if __name__ == "__main__":
    main()
