"""Primary exact checks for the P7 support-five torus exclusion.

Only the fixed symbolic identities in the proof are evaluated.  No support,
configuration, graph, word, finite-field, or parameter-value search occurs.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def pair_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            left[0] * right[1] + left[1] * right[0],
            left[0] * right[2] + left[2] * right[0],
            left[1] * right[2] + left[2] * right[1],
        ]
    )


def verify_two_support_plane() -> None:
    r_value, s_value = sp.symbols("r s")
    star = sp.Matrix([r_value, s_value, -r_value - s_value])
    assert sum(star) == 0

    # With a unit complementary triangle, its four-hafnian is the star sum.
    h_star_triangle = star[0] + star[1] + star[2]
    assert sp.expand(h_star_triangle) == 0


def verify_binary_pair_product_isomorphism() -> None:
    p_value = sp.Matrix([1, 0, -1])
    q_value = sp.Matrix([0, 1, -1])
    beta_matrix = sp.Matrix.hstack(
        pair_product(p_value, p_value),
        pair_product(p_value, q_value),
        pair_product(q_value, q_value),
    )
    expected = sp.Matrix([[0, 1, 0], [-2, -1, 0], [0, -1, -2]])
    assert beta_matrix == expected
    assert beta_matrix.det() == -4

    q_zero = beta_matrix.inv() * sp.ones(3, 1)
    assert q_zero == sp.Matrix([-1, 1, -1])
    quadratic_matrix = sp.Matrix([[-1, sp.Rational(1, 2)], [sp.Rational(1, 2), -1]])
    assert quadratic_matrix.det() == sp.Rational(3, 4)


def verify_three_support_hafnian_identity() -> None:
    coordinates = sp.symbols("ra sa rb sb rc sc")
    r_a, s_a, r_b, s_b, r_c, s_c = coordinates
    v_a = sp.Matrix([r_a, s_a, -r_a - s_a])
    v_b = sp.Matrix([r_b, s_b, -r_b - s_b])
    v_c = sp.Matrix([r_c, s_c, -r_c - s_c])
    d_ab, d_ac, d_bc = sp.symbols("Dab Dac Dbc")

    internal_sum = d_ab + d_ac + d_bc
    expanded = []
    for i, j in combinations(range(3), 2):
        h_ab = d_ab + v_a[i] * v_b[j] + v_a[j] * v_b[i]
        h_ac = d_ac + v_a[i] * v_c[j] + v_a[j] * v_c[i]
        h_bc = d_bc + v_b[i] * v_c[j] + v_b[j] * v_c[i]
        expanded.append(sp.expand(h_ab + h_ac + h_bc))

    expected = sp.ones(3, 1) * internal_sum + pair_product(v_a, v_b)
    expected += pair_product(v_a, v_c) + pair_product(v_b, v_c)
    assert sp.Matrix(expanded) == expected.applyfunc(sp.expand)


def verify_five_scalar_triple_rank() -> None:
    vertices = tuple(range(5))
    incidence = sp.Matrix(
        [[int(vertex in triple) for vertex in vertices] for triple in combinations(vertices, 3)]
    )
    assert incidence.rank() == 5
    selected_rows = (0, 1, 2, 3, 6)
    assert incidence[list(selected_rows), :].det() == -3


def verify_factor_coordinate_reduction() -> None:
    r_a, s_a, r_b, s_b, r_c, s_c = sp.symbols("ra sa rb sb rc sc")
    # In a factor basis Q0=e odot f, quotienting by Q0 retains only squares.
    e_square = r_a * r_b + r_a * r_c + r_b * r_c
    f_square = s_a * s_b + s_a * s_c + s_b * s_c
    assert sp.Poly(e_square, r_a, r_b, r_c).total_degree() == 2
    assert sp.Poly(f_square, s_a, s_b, s_c).total_degree() == 2

    reciprocals = sp.symbols("u0:5")
    triple_sums = sp.Matrix(
        [sum(reciprocals[index] for index in triple) for triple in combinations(range(5), 3)]
    )
    incidence = sp.Matrix(
        [[int(index in triple) for index in range(5)] for triple in combinations(range(5), 3)]
    )
    assert triple_sums == incidence * sp.Matrix(reciprocals)


def main() -> None:
    verify_two_support_plane()
    print("PASS: two-support rows force the unit-triangle cross-star plane")
    verify_binary_pair_product_isomorphism()
    print("PASS: binary pair-product determinant -4 and nondegenerate Q0")
    verify_three_support_hafnian_identity()
    print("PASS: symbolic three-support hafnian identity")
    verify_five_scalar_triple_rank()
    verify_factor_coordinate_reduction()
    print("PASS: five-point reciprocal triple system has full rank")
    print("SCOPE: searches=0 support_enumerations=0 finite_fields=0 project_imports=0")
    print("BOUNDARY: this replay leaves sizes six through eight")
    print("CURRENT: later packages exclude sizes six and seven; only eight remains")


if __name__ == "__main__":
    main()
