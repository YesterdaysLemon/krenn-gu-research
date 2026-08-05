#!/usr/bin/env python3
"""Independent audit of component 25's sparse paired-D23 minor cover."""

from __future__ import annotations

import json
import time

import sympy as sp

started = time.perf_counter()
a, b, k, slope, p = sp.symbols("a b k lambda p")
w, z6 = sp.symbols("w z6")
u0, v0, u1, v1, z2, z3, z7 = sp.symbols("u0 v0 u1 v1 z2 z3 z7")
plus = slope + 1
minus = slope - 1
pairs = (
    ((1, 1, 0, u0), (0, 0, -p * plus, v0)),
    ((1, 1, k * minus, u1), (-p, p, -p * plus, v1)),
    ((1, -1, 0, z2), (1, 1, a * plus - k * minus, z6)),
    ((0, 0, minus, z3), (1 - b, 1 + b, b * plus, z7)),
)


def permanent_dp(matrix):
    states = {0: sp.S.One}
    for row in matrix:
        new_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                new_states[new_mask] = new_states.get(new_mask, 0) + coefficient * entry
        states = new_states
    return sp.expand(states[(1 << len(matrix)) - 1])


def cofactor_row(rows):
    return tuple(
        permanent_dp(tuple(tuple(row[j] for j in range(4) if j != column) for row in rows))
        for column in range(4)
    )


def determinant_recursive(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    total = sp.S.Zero
    for column, entry in enumerate(matrix[0]):
        minor = tuple(
            tuple(row[j] for j in range(len(matrix)) if j != column)
            for row in matrix[1:]
        )
        total += (-1) ** column * entry * determinant_recursive(minor)
    return sp.expand(total)


def corner_minor(marked_mode, fixed_mode, fixed_bit):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    variable_modes = tuple(mode for mode in other_modes if mode != fixed_mode)
    rows = []
    for left_bit, right_bit in ((0, 0), (0, 1), (1, 0), (1, 1)):
        rows.append(
            cofactor_row(
                (
                    pairs[fixed_mode][fixed_bit],
                    pairs[variable_modes[0]][left_bit],
                    pairs[variable_modes[1]][right_bit],
                )
            )
        )
    return determinant_recursive(tuple(rows))


delta_1 = corner_minor(1, 2, 0)
delta_3 = corner_minor(3, 0, 0)
expected_1 = (
    -8
    * b
    * p
    * z2
    * minus
    * plus
    * (b * u0 + z2)
    * (p * plus * z3 - minus * v0)
)
expected_3 = (
    8
    * p
    * u0
    * plus
    * (a * plus - k * minus)
    * (a * p * z2 + a * v1 + p * u1 - p * z6)
    * (k * minus * u0 + plus * z2)
)
assert sp.expand(delta_1 - expected_1) == 0
assert sp.expand(delta_3 - expected_3) == 0

q = a + b
r = 1 + a * b
p_value = q**2 / r
k2 = p_value - a * b
inverse_k = k / k2
branch_denominator = minus * p_value - plus * q
z3_value = 1 / (2 * p_value * branch_denominator)
z2_value = minus * w
u0_value = -plus * w
u1_value = z6 - k * z3_value
v0_value = (
    p_value**2 * z3_value - sp.Rational(1, 2) / minus
) * inverse_k / q
v1_value = -p_value * minus * w + a * p_value * z3_value * inverse_k


def reduce_by_parity(expression):
    numerator, _denominator = sp.together(sp.cancel(expression)).as_numer_denom()
    polynomial = sp.Poly(numerator, k)
    even = sp.S.Zero
    odd = sp.S.Zero
    for (degree,), coefficient in polynomial.terms():
        if degree % 2:
            odd += coefficient * k2 ** ((degree - 1) // 2)
        else:
            even += coefficient * k2 ** (degree // 2)
    return sp.factor(even), sp.factor(odd)


def assert_component_zero(expression):
    even, odd = reduce_by_parity(expression)
    assert even == 0
    assert odd == 0


substitution_1 = {
    p: p_value,
    u0: u0_value,
    v0: v0_value,
    z2: z2_value,
    z3: z3_value,
}
substitution_3 = {
    p: p_value,
    u0: u0_value,
    u1: u1_value,
    v1: v1_value,
    z2: z2_value,
    z3: z3_value,
}
t_bar = (1 - b) * slope - (1 + b)
special_factor = a * plus - k * minus
factored_1 = (
    -8
    * b
    * p_value**2
    * z3_value
    * inverse_k
    * minus**2
    * plus**2
    * w**2
    * (k - 1)
    * t_bar
)
factored_3 = (
    8
    * p_value**2
    * z3_value
    * inverse_k
    * plus**3
    * minus
    * w**2
    * (k - 1)
    * (a**2 - k**2)
    * special_factor
)
assert_component_zero(delta_1.subs(substitution_1, simultaneous=True) - factored_1)
assert_component_zero(delta_3.subs(substitution_3, simultaneous=True) - factored_3)

# Audit the residual resultant without calling a resultant routine.
phi_f = (
    a**3 * b
    + a**2 * b**4
    - a**2 * b**2
    + a**2
    - a * b**3
    - b**4
)
phi_n = (
    3 * a**3 * b**3
    - a**3 * b
    - a**2 * b**4
    + a**2 * b**2
    - a**2
    - a * b**3
    - a * b
    + b**4
)
f_coefficients = tuple(sp.Poly(phi_f, a).all_coeffs())
n_coefficients = tuple(sp.Poly(phi_n, a).all_coeffs())
sylvester_rows = []
for shift in range(3):
    sylvester_rows.append(
        [sp.S.Zero] * shift + list(f_coefficients) + [sp.S.Zero] * (2 - shift)
    )
for shift in range(3):
    sylvester_rows.append(
        [sp.S.Zero] * shift + list(n_coefficients) + [sp.S.Zero] * (2 - shift)
    )
sylvester_determinant = sp.factor(sp.Matrix(sylvester_rows).det(method="domain-ge"))
sextic = 3 * b**6 - 3 * b**4 - 6 * b**2 - 2
assert sylvester_determinant == b**9 * (b - 1) ** 3 * (b + 1) ** 3 * sextic

print(
    json.dumps(
        {
            "status": "PASS",
            "independent_permanent_algorithm": "subset dynamic programming",
            "independent_determinant_algorithm": "recursive cofactor expansion",
            "component_reduction_algorithm": "even-odd parity reduction",
            "minor_modes": [1, 3],
            "necessary_rank_drop_cover": [
                "w=0",
                "k=1",
                "Tbar=0 and A=0",
            ],
            "residual_resultant_algorithm": "explicit 6x6 Sylvester determinant",
            "Tbar_A_residual_sextic": str(sextic),
            "residual_branches_closed": False,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
