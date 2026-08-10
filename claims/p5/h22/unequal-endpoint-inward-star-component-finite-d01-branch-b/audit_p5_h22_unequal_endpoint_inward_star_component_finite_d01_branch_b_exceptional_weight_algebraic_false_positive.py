#!/usr/bin/env python3
"""No-import audit of the exceptional B-weight algebraic false positive."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import time

import sympy as sp


def main():
    started = time.perf_counter()
    qq = sp.QQ
    relation_constant = qq(-5, 17)
    relation_linear = qq(42, 17)
    l_zero = (qq.zero, qq.zero)
    l_one = (qq.one, qq.zero)
    lam = (qq.zero, qq.one)

    def l_add(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def l_neg(value):
        return (-value[0], -value[1])

    def l_mul(left, right):
        return (
            left[0] * right[0] + relation_constant * left[1] * right[1],
            left[0] * right[1]
            + left[1] * right[0]
            + relation_linear * left[1] * right[1],
        )

    def l_scale(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

    def l_inverse(value):
        norm = (
            value[0] ** 2
            + relation_linear * value[0] * value[1]
            - relation_constant * value[1] ** 2
        )
        return (
            (value[0] + relation_linear * value[1]) / norm,
            -value[1] / norm,
        )

    def l_norm(value):
        return (
            value[0] ** 2
            + relation_linear * value[0] * value[1]
            - relation_constant * value[1] ** 2
        )

    def l_scalar(value):
        return (qq(value), qq.zero)

    # Elements of E=Q(lambda)[k]/(k^2+1).
    zero = (l_zero, l_zero)
    one = (l_one, l_zero)
    k = (l_zero, l_one)
    k2 = qq(-1)

    def add(left, right):
        return (l_add(left[0], right[0]), l_add(left[1], right[1]))

    def neg(value):
        return (l_neg(value[0]), l_neg(value[1]))

    def mul(left, right):
        return (
            l_add(l_mul(left[0], right[0]), l_scale(k2, l_mul(left[1], right[1]))),
            l_add(l_mul(left[0], right[1]), l_mul(left[1], right[0])),
        )

    def e_scale(coefficient, value):
        return (l_mul(coefficient, value[0]), l_mul(coefficient, value[1]))

    def e_scalar(value):
        return (l_scalar(value), l_zero)

    def e_lambda(value):
        return (value, l_zero)

    def field_norm(value):
        norm_over_k = l_add(
            l_mul(value[0], value[0]),
            l_neg(l_scale(k2, l_mul(value[1], value[1]))),
        )
        return l_norm(norm_over_k)

    # Verify the exceptional divisor and the component equation first.
    assert (
        l_add(l_add(l_scale(17, l_mul(lam, lam)), l_scale(-42, lam)), l_scalar(5))
        == l_zero
    )
    e, j, s = qq(1), qq(2), qq(2)
    p, q, r = qq(1), qq(3), qq(9)
    assert (e * j + k2) * r == q**2

    # Independently reconstruct N and separate it from every retained linear
    # factor at the chosen component point.
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
    defining = 17 * ell**2 - 42 * ell + 5
    assert sp.expand(leading * ell**2 + middle * ell + constant) == 9 * defining
    retained_factors = (ell, ell - 1, ell + 1, 3 * ell - 5, 3 * ell + 15)
    expected_resultants = (5, -20, 64, -160, 5760)
    assert (
        tuple(sp.resultant(defining, factor, ell) for factor in retained_factors)
        == expected_resultants
    )

    def row_sum(*rows):
        result = []
        for coordinate in range(4):
            value = zero
            for row in rows:
                value = add(value, row[coordinate])
            result.append(value)
        return tuple(result)

    def row_scale(coefficient, row):
        return tuple(e_scale(coefficient, value) for value in row)

    def row_multiply(value, row):
        return tuple(mul(value, entry) for entry in row)

    cap_a = tuple(map(e_scalar, (1, 1, 0, 0)))
    cap_b = tuple(map(e_scalar, (0, 0, 1, 1)))
    cap_c = tuple(map(e_scalar, (1, -1, 0, 0)))
    cap_d = tuple(map(e_scalar, (0, 0, 1, -1)))
    alpha = (
        row_sum(row_scale(l_scalar(q), cap_a), row_scale(l_scalar(-p), cap_b)),
        row_sum(
            row_scale(l_scalar(q), row_sum(cap_a, row_multiply(k, cap_d))),
            row_scale(l_scalar(-p), row_sum(cap_b, row_scale(l_scalar(s), cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        row_sum(cap_a, row_multiply(k, cap_d)),
        row_sum(
            cap_a,
            row_scale(l_scalar(e), cap_b),
            row_scale(l_scalar(-1), row_multiply(k, cap_d)),
        ),
        row_sum(
            cap_a,
            row_scale(l_scalar(-s * j), cap_c),
            row_scale(l_scalar(j), cap_b),
        ),
    )

    w = (l_zero, (qq(-29, 256), qq(-17, 1280)))
    z6 = (l_zero, (qq(-19, 320), qq(-51, 320)))
    extension = (
        (l_zero, (qq(119, 640), qq(391, 640))),
        (l_zero, (qq(61, 160), qq(-51, 160))),
        (l_zero, (qq(15, 128), qq(-17, 128))),
        ((qq(-127, 640), qq(17, 640)), l_zero),
        (l_zero, (qq(7, 64), qq(51, 320))),
        (l_zero, (qq(89, 640), qq(-119, 640))),
        z6,
        (l_zero, (qq(-21, 160), qq(51, 160))),
    )
    slope_minus_one = l_add(lam, l_scalar(-1))
    slope_plus_one = l_add(lam, l_one)
    assert extension[2] == e_scale(slope_minus_one, w)
    assert extension[4] == e_scale(l_neg(slope_plus_one), w)

    branch_denominator = l_add(
        l_mul(slope_minus_one, l_scalar(s * p)),
        l_neg(l_mul(slope_plus_one, l_scalar(q))),
    )
    assert (
        l_add(
            l_mul(l_scalar(2 * p), l_mul(branch_denominator, extension[3][0])),
            l_scalar(-s),
        )
        == l_zero
    )

    # Independently check the four solved extension equations.
    inverse_k = mul(k, e_scalar(1 / k2))
    asserted_z5 = add(z6, e_scale(l_neg(extension[3][0]), k))
    asserted_z1 = add(
        add(e_scale(l_scalar(q), z6), e_scale(l_scale(-p * s, slope_minus_one), w)),
        e_scale(l_scale(-j * (k2 - e**2), extension[3][0]), inverse_k),
    )
    asserted_z7_numerator = add(
        add(
            e_scale(l_scalar(p), z6), e_scale(l_scale(-k2 * q * s, slope_minus_one), w)
        ),
        e_scale(l_scalar(-e), asserted_z1),
    )
    asserted_z7 = e_scale(l_scalar(1 / (k2 - e**2)), asserted_z7_numerator)
    asserted_z0_numerator = add(
        e_lambda(
            l_add(
                l_mul(l_scalar(p**2), extension[3][0]),
                l_neg(l_mul(l_scalar(qq(1, 2)), l_inverse(slope_minus_one))),
            )
        ),
        e_scale(l_neg(l_mul(l_scalar(q**2), slope_plus_one)), mul(k, w)),
    )
    asserted_z0 = mul(asserted_z0_numerator, mul(k, e_scalar(1 / (k2 * q))))
    assert (asserted_z0, asserted_z1, asserted_z5, asserted_z7) == (
        extension[0],
        extension[1],
        extension[5],
        extension[7],
    )

    def project(row, extra, direction):
        if direction == "D01":
            return (
                add(e_scale(lam, row[0]), row[1]),
                row[2],
                row[3],
                extra,
            )
        return (
            row[0],
            row[1],
            add(e_scale(lam, row[2]), row[3]),
            extra,
        )

    def projected(direction):
        return (
            tuple(
                project(alpha[index], extension[index], direction) for index in range(4)
            ),
            tuple(
                project(beta[index], extension[index + 4], direction)
                for index in range(4)
            ),
        )

    # Deliberately use subset dynamic programming, not permutation expansion.
    def permanent_dp(rows):
        states = {0: one}
        for row in rows:
            next_states = {}
            for mask, coefficient in states.items():
                for column, entry in enumerate(row):
                    bit = 1 << column
                    if mask & bit:
                        continue
                    new_mask = mask | bit
                    term = mul(coefficient, entry)
                    next_states[new_mask] = add(next_states.get(new_mask, zero), term)
            states = next_states
        return states[15]

    alpha_01, beta_01 = projected("D01")
    marking = (
        zero,
        ((qq(-33, 160), qq(-17, 160)), l_zero),
        e_scalar(-2),
        (l_zero, (qq(3, 4), qq(-17, 4))),
    )
    for mode in range(4):
        singleton = permanent_dp(
            tuple(
                beta_01[index] if index == mode else alpha_01[index]
                for index in range(4)
            )
        )
        assert add(singleton, marking[mode]) == zero

    marked_01 = tuple(
        tuple(
            add(
                beta_01[index][coordinate],
                mul(marking[index], alpha_01[index][coordinate]),
            )
            for coordinate in range(4)
        )
        for index in range(4)
    )
    for word in itertools.product((0, 1), repeat=4):
        coefficient = permanent_dp(
            tuple(
                marked_01[index] if bit else alpha_01[index]
                for index, bit in enumerate(word)
            )
        )
        if word == (0, 0, 0, 0):
            assert coefficient == one
        elif word == (1, 1, 1, 1):
            assert coefficient == (l_zero, (qq(1, 10), qq(1, 10)))
        else:
            assert coefficient == zero

    alpha_23, beta_23 = projected("D23")
    marked_23 = tuple(
        tuple(
            add(
                beta_23[index][coordinate],
                mul(marking[index], alpha_23[index][coordinate]),
            )
            for coordinate in range(4)
        )
        for index in range(4)
    )
    ternary_words = tuple(itertools.product((0, 1), repeat=3))

    def one_marked_matrix(mode):
        matrix = []
        for row_index in (0, 1, 2, 3):
            chosen = []
            cursor = 0
            for index in range(4):
                if index == mode:
                    chosen.append(None)
                else:
                    chosen.append(
                        marked_23[index]
                        if ternary_words[row_index][cursor]
                        else alpha_23[index]
                    )
                    cursor += 1
            row = []
            for coordinate in range(4):
                basis = tuple(e_scalar(int(index == coordinate)) for index in range(4))
                row.append(
                    permanent_dp(
                        tuple(
                            basis if index == mode else chosen[index]
                            for index in range(4)
                        )
                    )
                )
            matrix.append(row)
        return matrix

    def determinant(matrix):
        total = zero
        for permutation in itertools.permutations(range(4)):
            inversions = sum(
                permutation[left] > permutation[right]
                for left in range(4)
                for right in range(left + 1, 4)
            )
            term = one
            for index in range(4):
                term = mul(term, matrix[index][permutation[index]])
            total = add(total, e_scale(l_scalar(-1 if inversions % 2 else 1), term))
        return total

    norms = tuple(field_norm(determinant(one_marked_matrix(mode))) for mode in range(4))
    assert norms == (
        qq(3346477548867590625, 321978368),
        qq(242198579941179669, 1710510080),
        qq(371804801417254836, 10440125),
        qq(1123047541391554692, 1305015625),
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "audit_independence": "no project imports; explicit section; subset-DP permanents",
                "exceptional_polynomial": "N=9*(17lambda^2-42lambda+5)",
                "retained_factor_resultants": list(expected_resultants),
                "component_equation_checked": True,
                "B_equation_and_four_extension_equations_checked": True,
                "normalized_binary_H22_coefficients_checked": 16,
                "nonzero_opposite_diagonal_checked": True,
                "D23_rank_four_modes": [0, 1, 2, 3],
                "counterexample": False,
                "finite_field_evidence_used": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
