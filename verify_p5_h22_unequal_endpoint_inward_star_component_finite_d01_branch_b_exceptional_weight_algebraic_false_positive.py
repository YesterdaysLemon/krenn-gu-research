#!/usr/bin/env python3
"""Verify an algebraic false positive on the exceptional B-weight divisor."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp


def main():
    started = time.perf_counter()
    rational = sp.QQ

    # L=Q(lambda), lambda^2=(42 lambda-5)/17.
    lambda_constant = rational(-5, 17)
    lambda_linear = rational(42, 17)
    l_zero = (rational.zero, rational.zero)
    l_one = (rational.one, rational.zero)
    lambda_element = (rational.zero, rational.one)

    def l_add(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def l_negate(value):
        return (-value[0], -value[1])

    def l_multiply(left, right):
        return (
            left[0] * right[0] + lambda_constant * left[1] * right[1],
            left[0] * right[1]
            + left[1] * right[0]
            + lambda_linear * left[1] * right[1],
        )

    def l_scale(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

    def l_inverse(value):
        norm = (
            value[0] ** 2
            + lambda_linear * value[0] * value[1]
            - lambda_constant * value[1] ** 2
        )
        return (
            (value[0] + lambda_linear * value[1]) / norm,
            -value[1] / norm,
        )

    def l_norm(value):
        return (
            value[0] ** 2
            + lambda_linear * value[0] * value[1]
            - lambda_constant * value[1] ** 2
        )

    def l_scalar(value):
        return (rational(value), rational.zero)

    # E=L(k), k^2=-1.  Elements are (a,b), meaning a+b*k.
    k_squared = rational(-1)
    zero = (l_zero, l_zero)
    one = (l_one, l_zero)
    k = (l_zero, l_one)

    def add(left, right):
        return (l_add(left[0], right[0]), l_add(left[1], right[1]))

    def negate(value):
        return (l_negate(value[0]), l_negate(value[1]))

    def subtract(left, right):
        return add(left, negate(right))

    def multiply(left, right):
        return (
            l_add(
                l_multiply(left[0], right[0]),
                l_scale(k_squared, l_multiply(left[1], right[1])),
            ),
            l_add(l_multiply(left[0], right[1]), l_multiply(left[1], right[0])),
        )

    def scale(coefficient, value):
        return (l_multiply(coefficient, value[0]), l_multiply(coefficient, value[1]))

    def inverse(value):
        norm = l_add(
            l_multiply(value[0], value[0]),
            l_negate(l_scale(k_squared, l_multiply(value[1], value[1]))),
        )
        inverse_norm = l_inverse(norm)
        return (
            l_multiply(value[0], inverse_norm),
            l_negate(l_multiply(value[1], inverse_norm)),
        )

    def divide(left, right):
        return multiply(left, inverse(right))

    def scalar(value):
        return (l_scalar(value), l_zero)

    def lambda_scalar(value):
        return (value, l_zero)

    def field_norm(value):
        k_norm = l_add(
            l_multiply(value[0], value[0]),
            l_negate(l_scale(k_squared, l_multiply(value[1], value[1]))),
        )
        return l_norm(k_norm)

    def display(value):
        return [str(coefficient) for part in value for coefficient in part]

    e = rational(1)
    j = rational(2)
    s = rational(2)
    q = rational(3)
    r = rational(9)
    p = rational(1)
    assert p * r == q**2

    # Reconstruct the corrected full-field exceptional polynomial and verify
    # that this point avoids every retained linear weight/chart divisor.
    ell = sp.Symbol("ell")
    E, J, S = map(sp.Integer, (1, 2, 2))
    leading = (
        (E * S + 1)
        * (J * S - 1)
        * (
            3 * E**2 * J**2 * S**2
            + E**2 * J * S
            - E**2
            - E * J**3 * S**2
            - 2 * E * J**2 * S
            - E * J
            + J**3 * S
        )
    )
    middle = -2 * (
        3 * E**3 * J**3 * S**4
        - 2 * E**3 * J * S**2
        - E**2 * J**4 * S**4
        + E**2 * J**2 * S**2
        - E**2
        - E * J
        + J**4 * S**2
    )
    constant = (
        (E * S - 1)
        * (J * S + 1)
        * (
            3 * E**2 * J**2 * S**2
            - E**2 * J * S
            - E**2
            - E * J**3 * S**2
            + 2 * E * J**2 * S
            - E * J
            - J**3 * S
        )
    )
    exceptional = sp.expand(leading * ell**2 + middle * ell + constant)
    defining = 17 * ell**2 - 42 * ell + 5
    assert exceptional == 9 * defining
    retained_factors = (ell, ell - 1, ell + 1, 3 * ell - 5, 3 * ell + 15)
    expected_resultants = (5, -20, 64, -160, 5760)
    assert (
        tuple(sp.resultant(defining, factor, ell) for factor in retained_factors)
        == expected_resultants
    )

    def row_add(*rows):
        result = []
        for coordinate in range(4):
            value = zero
            for row in rows:
                value = add(value, row[coordinate])
            result.append(value)
        return tuple(result)

    def row_scale(coefficient, row):
        return tuple(scale(coefficient, value) for value in row)

    def row_multiply(value, row):
        return tuple(multiply(value, entry) for entry in row)

    cap_a = tuple(map(scalar, (1, 1, 0, 0)))
    cap_b = tuple(map(scalar, (0, 0, 1, 1)))
    cap_c = tuple(map(scalar, (1, -1, 0, 0)))
    cap_d = tuple(map(scalar, (0, 0, 1, -1)))
    alpha = (
        row_add(row_scale(l_scalar(q), cap_a), row_scale(l_scalar(-p), cap_b)),
        row_add(
            row_scale(l_scalar(q), row_add(cap_a, row_multiply(k, cap_d))),
            row_scale(l_scalar(-p), row_add(cap_b, row_scale(l_scalar(s), cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        row_add(cap_a, row_multiply(k, cap_d)),
        row_add(
            cap_a,
            row_scale(l_scalar(e), cap_b),
            row_scale(l_scalar(-1), row_multiply(k, cap_d)),
        ),
        row_add(
            cap_a,
            row_scale(l_scalar(-s * j), cap_c),
            row_scale(l_scalar(j), cap_b),
        ),
    )

    slope_minus_one = l_add(lambda_element, l_scalar(-1))
    slope_plus_one = l_add(lambda_element, l_one)
    branch_denominator = l_add(
        l_multiply(slope_minus_one, l_scalar(s * p)),
        l_negate(l_multiply(slope_plus_one, l_scalar(q))),
    )
    z3 = l_multiply(
        l_scalar(s), l_inverse(l_multiply(l_scalar(2 * p), branch_denominator))
    )
    assert z3 == (rational(-127, 640), rational(17, 640))
    assert (
        l_add(
            l_multiply(l_scalar(2 * p), l_multiply(branch_denominator, z3)),
            l_scalar(-s),
        )
        == l_zero
    )

    def extensions(w, z6):
        z5 = add(z6, scale(l_negate(z3), k))
        z1 = add(
            add(scale(l_scalar(q), z6), scale(l_scale(-p * s, slope_minus_one), w)),
            scale(
                l_scale(-j * (k_squared - e**2), z3), multiply(k, scalar(1 / k_squared))
            ),
        )
        z7 = scale(
            l_scalar(1 / (k_squared - e**2)),
            add(
                add(
                    scale(l_scalar(p), z6),
                    scale(l_scale(-k_squared * q * s, slope_minus_one), w),
                ),
                scale(l_scalar(-e), z1),
            ),
        )
        z0 = multiply(
            add(
                lambda_scalar(
                    l_add(
                        l_multiply(l_scalar(p**2), z3),
                        l_negate(
                            l_multiply(
                                l_scalar(rational(1, 2)),
                                l_inverse(slope_minus_one),
                            )
                        ),
                    )
                ),
                scale(
                    l_negate(l_multiply(l_scalar(q**2), slope_plus_one)), multiply(k, w)
                ),
            ),
            multiply(k, scalar(1 / (k_squared * q))),
        )
        return (
            z0,
            z1,
            scale(slope_minus_one, w),
            lambda_scalar(z3),
            scale(l_negate(slope_plus_one), w),
            z5,
            z6,
            z7,
        )

    def project(row, extra, direction):
        if direction == "D01":
            return (
                add(scale(lambda_element, row[0]), row[1]),
                row[2],
                row[3],
                extra,
            )
        return (
            row[0],
            row[1],
            add(scale(lambda_element, row[2]), row[3]),
            extra,
        )

    def projected_rows(w, z6, direction):
        extension = extensions(w, z6)
        return (
            tuple(
                project(alpha[index], extension[index], direction) for index in range(4)
            ),
            tuple(
                project(beta[index], extension[index + 4], direction)
                for index in range(4)
            ),
        )

    def permanent(rows):
        total = zero
        for permutation in itertools.permutations(range(4)):
            term = one
            for index in range(4):
                term = multiply(term, rows[index][permutation[index]])
            total = add(total, term)
        return total

    def residuals(w, z6):
        alpha_rows, beta_rows = projected_rows(w, z6, "D01")

        def coefficient(word):
            return permanent(
                tuple(
                    beta_rows[index] if bit else alpha_rows[index]
                    for index, bit in enumerate(word)
                )
            )

        c0 = coefficient((0, 0, 0, 0))
        c1 = coefficient((0, 1, 0, 0))
        c2 = coefficient((0, 0, 1, 0))
        c3 = coefficient((0, 0, 0, 1))
        return (
            subtract(multiply(coefficient((0, 1, 0, 1)), c0), multiply(c1, c3)),
            subtract(multiply(coefficient((0, 0, 1, 1)), c0), multiply(c2, c3)),
            subtract(
                multiply(coefficient((0, 1, 1, 1)), multiply(c0, c0)),
                multiply(multiply(c1, c2), c3),
            ),
        )

    at_zero = residuals(zero, zero)
    at_w = residuals(one, zero)
    at_z6 = residuals(zero, one)
    a11 = subtract(at_w[0], at_zero[0])
    a12 = subtract(at_z6[0], at_zero[0])
    a21 = subtract(at_w[1], at_zero[1])
    a22 = subtract(at_z6[1], at_zero[1])
    determinant = subtract(multiply(a11, a22), multiply(a12, a21))
    assert field_norm(determinant) != 0
    rhs1 = negate(at_zero[0])
    rhs2 = negate(at_zero[1])
    w = divide(subtract(multiply(rhs1, a22), multiply(a12, rhs2)), determinant)
    z6 = divide(subtract(multiply(a11, rhs2), multiply(rhs1, a21)), determinant)
    assert residuals(w, z6) == (zero, zero, zero)
    assert w == (l_zero, (rational(-29, 256), rational(-17, 1280)))
    assert z6 == (l_zero, (rational(-19, 320), rational(-51, 320)))

    alpha_01, beta_01 = projected_rows(w, z6, "D01")
    assert permanent(alpha_01) == one
    marking = []
    for mode in range(4):
        marking.append(
            negate(
                permanent(
                    tuple(
                        beta_01[index] if index == mode else alpha_01[index]
                        for index in range(4)
                    )
                )
            )
        )
    expected_marking = (
        zero,
        ((rational(-33, 160), rational(-17, 160)), l_zero),
        scalar(-2),
        (l_zero, (rational(3, 4), rational(-17, 4))),
    )
    assert tuple(marking) == expected_marking

    marked_01 = tuple(
        tuple(
            add(
                beta_01[index][coordinate],
                multiply(marking[index], alpha_01[index][coordinate]),
            )
            for coordinate in range(4)
        )
        for index in range(4)
    )
    binary_coefficients = {}
    for word in itertools.product((0, 1), repeat=4):
        binary_coefficients[word] = permanent(
            tuple(
                marked_01[index] if bit else alpha_01[index]
                for index, bit in enumerate(word)
            )
        )
    assert binary_coefficients[(0, 0, 0, 0)] == one
    for word, value in binary_coefficients.items():
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1)):
            assert value == zero
    opposite_diagonal = binary_coefficients[(1, 1, 1, 1)]
    assert opposite_diagonal == (l_zero, (rational(1, 10), rational(1, 10)))
    assert field_norm(opposite_diagonal) == rational(256, 180625)

    alpha_23, beta_23 = projected_rows(w, z6, "D23")
    marked_23 = tuple(
        tuple(
            add(
                beta_23[index][coordinate],
                multiply(marking[index], alpha_23[index][coordinate]),
            )
            for coordinate in range(4)
        )
        for index in range(4)
    )
    bits = tuple(itertools.product((0, 1), repeat=3))

    def one_marked_matrix(mode):
        matrix = []
        for row_index in (0, 1, 2, 3):
            selected = []
            cursor = 0
            for index in range(4):
                if index == mode:
                    selected.append(None)
                else:
                    selected.append(
                        marked_23[index] if bits[row_index][cursor] else alpha_23[index]
                    )
                    cursor += 1
            row = []
            for coordinate in range(4):
                basis = tuple(scalar(int(index == coordinate)) for index in range(4))
                row.append(
                    permanent(
                        tuple(
                            basis if index == mode else selected[index]
                            for index in range(4)
                        )
                    )
                )
            matrix.append(row)
        return matrix

    def determinant_4(matrix):
        total = zero
        for permutation in itertools.permutations(range(4)):
            inversions = sum(
                permutation[left] > permutation[right]
                for left in range(4)
                for right in range(left + 1, 4)
            )
            term = one
            for index in range(4):
                term = multiply(term, matrix[index][permutation[index]])
            total = add(total, scale(l_scalar(-1 if inversions % 2 else 1), term))
        return total

    minors = tuple(determinant_4(one_marked_matrix(mode)) for mode in range(4))
    expected_norms = (
        rational(3346477548867590625, 321978368),
        rational(242198579941179669, 1710510080),
        rational(371804801417254836, 10440125),
        rational(1123047541391554692, 1305015625),
    )
    actual_norms = tuple(field_norm(value) for value in minors)
    assert actual_norms == expected_norms

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "Q[lambda,k]/(17lambda^2-42lambda+5,k^2+1)",
                "exceptional_polynomial": "N=9*(17*lambda^2-42*lambda+5)",
                "retained_factor_resultants": list(expected_resultants),
                "component_point": {"e": 1, "j": 2, "s": 2, "P": 1, "R": 9, "Q": 3},
                "B_section_w_basis_1_lambda_k_klambda": display(w),
                "B_section_z6_basis_1_lambda_k_klambda": display(z6),
                "marking_basis_1_lambda_k_klambda": [
                    display(value) for value in marking
                ],
                "normalized_D01_diagonals": ["1", "k*(1+lambda)/10"],
                "all_fourteen_mixed_D01_coefficients_zero": True,
                "D23_one_marked_minor_rows": [0, 1, 2, 3],
                "D23_minor_field_norms": list(map(str, actual_norms)),
                "all_four_D23_one_marked_ranks": 4,
                "weighted_H22_lift": False,
                "counterexample": False,
                "finite_field_evidence_used": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
