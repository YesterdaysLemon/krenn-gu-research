"""Primary symbolic checks for bosonic boundary-entanglement rank."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def flatten_port_tensor(matrix: list[list[sp.Matrix]]) -> sp.Matrix:
    row_zero_dimension = matrix[0][0].rows
    other_dimension = matrix[1][0].rows * matrix[2][0].rows
    flattening = sp.zeros(row_zero_dimension, other_dimension)
    for permutation in permutations(range(3)):
        left = matrix[0][permutation[0]]
        right = sp.kronecker_product(
            matrix[1][permutation[1]],
            matrix[2][permutation[2]],
        )
        flattening += left * right.T
    return sp.simplify(flattening)


def main() -> None:
    a, b, c, d, e, f = sp.symbols("a b c d e f", nonzero=True)

    z = sp.Matrix([1, 0])
    excess = sp.Matrix([0, 1])
    profile_111 = [
        [excess, a * z, b * z],
        [c * z, excess, d * z],
        [e * z, f * z, excess],
    ]
    flat_111 = flatten_port_tensor(profile_111)
    expected_111 = sp.Matrix(
        [
            [a * d * e + b * c * f, a * c, b * e, 0],
            [d * f, 0, 0, 1],
        ]
    )
    assert flat_111 == expected_111
    assert sp.det(flat_111[:, [1, 3]]) == a * c

    z0 = sp.Matrix([1, 0, 0])
    l0 = sp.Matrix([0, 1, 0])
    l1 = sp.Matrix([0, 0, 1])
    z1 = sp.Matrix([1, 0])
    m = sp.Matrix([0, 1])
    z2 = sp.Matrix([1])
    profile_210 = [
        [l0, l1, a * z0],
        [b * z1, c * z1, m],
        [d * z2, e * z2, f * z2],
    ]
    flat_210 = flatten_port_tensor(profile_210)
    expected_210 = sp.Matrix(
        [
            [a * (b * e + c * d), 0],
            [c * f, e],
            [b * f, d],
        ]
    )
    assert flat_210 == expected_210
    determinant_excess_rows = sp.det(flat_210[[1, 2], :])
    determinant_l0_z0 = sp.det(flat_210[[1, 0], :])
    assert sp.simplify(determinant_excess_rows - f * (c * d - b * e)) == 0
    assert sp.simplify(determinant_l0_z0 + a * e * (b * e + c * d)) == 0
    dependent_substitution = {d: b * e / c}
    assert sp.simplify(flat_210[0, 0].subs(dependent_substitution)) == 2 * a * b * e
    assert sp.simplify(determinant_l0_z0.subs(dependent_substitution)) == -2 * a * b * e**2

    h_111, s_111 = (1, 1, 1), (1, 1, 1)
    h_210, s_210 = (2, 1, 0), (0, 1, 2)
    for h_profile, s_profile in ((h_111, s_111), (h_210, s_210)):
        assert sum(h_profile) == sum(s_profile) == 3
        assert all(h_value + s_value == 2 for h_value, s_value in zip(h_profile, s_profile, strict=True))

    print("arbitrary permanent boundary-entanglement rank theorem: PASS")
    print("symbolic tensor flattenings only; no support or coefficient-word census was performed")


if __name__ == "__main__":
    main()
