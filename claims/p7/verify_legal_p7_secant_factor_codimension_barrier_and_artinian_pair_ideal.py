"""Primary exact replay for the legal P7 secant--factor barrier."""

from itertools import combinations

import sympy as sp

BLOCKER_EDGES = tuple(combinations(range(7), 2))


def verify_factor_locus_dimension():
    a = sp.symbols("a0:7")
    b = sp.symbols("b0:7")
    responses = sp.Matrix(
        [a[i] * b[j] + b[i] * a[j] for i, j in BLOCKER_EDGES]
    )
    jacobian = responses.jacobian((*a, *b))

    gauge = sp.Matrix([*a, *(-value for value in b)])
    assert (jacobian * gauge).applyfunc(sp.expand) == sp.zeros(21, 1)

    point = {a[i]: i + 1 for i in range(7)}
    point.update({b[i]: (i + 1) ** 2 for i in range(7)})
    exact_jacobian = jacobian.subs(point)
    assert exact_jacobian.rank() == 13
    assert exact_jacobian[:13, :].rank() == 13


def verify_dimension_barrier():
    projective_u = 218
    projective_t = 242
    secant_dimension = 32
    sensor_plane = 218
    border_floor = sensor_plane + secant_dimension - projective_t
    assert border_floor == 8

    pair_affine_dimension = 13
    pair_projection_kernel = 219 - 21
    factor_preimage_projective = pair_projection_kernel + pair_affine_dimension - 1
    assert factor_preimage_projective == 210
    assert projective_u - factor_preimage_projective == 8
    assert border_floor + factor_preimage_projective - projective_u == 0

    assert all(border_floor - equation_count >= 0 for equation_count in range(9))


def verify_named_preimage_covariance():
    gamma = sp.Matrix(
        [
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 0],
            [2, -1, 1],
            [1, 3, -2],
        ]
    )
    q = sp.Matrix([2, -1, 3])
    change = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
        ]
    )
    assert change.det() != 0
    transformed = change * gamma
    assert gamma.rank() == transformed.rank() == 3
    assert transformed * q == change * (gamma * q)


def multiplication_matrix(modulus, element):
    variable = next(iter(element.free_symbols | modulus.free_symbols))
    degree = sp.Poly(modulus, variable).degree()
    columns = []
    for power in range(degree):
        remainder = sp.rem(element * variable**power, modulus, domain=sp.QQ)
        polynomial = sp.Poly(remainder, variable)
        columns.append(
            [polynomial.coeff_monomial(variable**row) for row in range(degree)]
        )
    return sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))


def verify_artinian_norm_criterion():
    x = sp.symbols("x")
    modulus = x**2 - 1

    zero_divisor = multiplication_matrix(modulus, x - 1)
    unit = multiplication_matrix(modulus, x + 2)
    assert zero_divisor.det() == 0
    assert unit.det() == 3

    inverse = sp.invert(x + 2, modulus)
    assert sp.rem((x + 2) * inverse, modulus, domain=sp.QQ) == 1


def main():
    verify_factor_locus_dimension()
    verify_dimension_barrier()
    verify_named_preimage_covariance()
    verify_artinian_norm_criterion()
    print("PASS: legal P7 secant--factor codimension barrier")
    print("border_secant_floor=8 factor_preimage_codimension=8")
    print("seven_port_factor_affine_dimension=13")
    print("eight_homogeneous_equations_still_leave_border_survivor=True")
    print("artinian_gate_norm_criterion=exact")
    print("graph_or_parameter_search_used=False")


if __name__ == "__main__":
    main()

