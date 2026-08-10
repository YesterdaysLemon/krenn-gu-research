#!/usr/bin/env python3
"""Verify component 25's sparse paired-D23 two-minor branch cover."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

started = time.perf_counter()
a, b, k, slope, p = sp.symbols("a b k lambda p")
w, z6 = sp.symbols("w z6")
u0, v0, u1, v1, z2, z3, z7 = sp.symbols("u0 v0 u1 v1 z2 z3 z7")
plus = slope + 1
minus = slope - 1

# In the first two modes replace (alpha_i,beta_i) by the equivalent sparse
# bases (beta_i,alpha_i-(a+b)beta_i).  The last two pairs are unchanged.
pairs = (
    ((1, 1, 0, u0), (0, 0, -p * plus, v0)),
    ((1, 1, k * minus, u1), (-p, p, -p * plus, v1)),
    ((1, -1, 0, z2), (1, 1, a * plus - k * minus, z6)),
    ((0, 0, minus, z3), (1 - b, 1 + b, b * plus, z7)),
)


def permanent_three(rows, omitted_column):
    columns = tuple(column for column in range(4) if column != omitted_column)
    return sp.expand(
        sum(
            sp.prod(rows[row][columns[permutation[row]]] for row in range(3))
            for permutation in itertools.permutations(range(3))
        )
    )


def cofactor_row(rows):
    return tuple(permanent_three(rows, column) for column in range(4))


def corner_minor(marked_mode, fixed_mode, fixed_bit):
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    variable_modes = tuple(mode for mode in other_modes if mode != fixed_mode)
    coefficient_rows = []
    for left_bit, right_bit in ((0, 0), (0, 1), (1, 0), (1, 1)):
        coefficient_rows.append(
            cofactor_row(
                (
                    pairs[fixed_mode][fixed_bit],
                    pairs[variable_modes[0]][left_bit],
                    pairs[variable_modes[1]][right_bit],
                )
            )
        )
    return sp.factor(sp.Matrix(coefficient_rows).det(method="domain-ge"))


# Mode 1: hold alpha_2 fixed and vary the sparse mode-0 and mode-3 pairs.
delta_1 = corner_minor(marked_mode=1, fixed_mode=2, fixed_bit=0)
delta_1_universal = (
    -8
    * b
    * p
    * z2
    * minus
    * plus
    * (b * u0 + z2)
    * (p * plus * z3 - minus * v0)
)
assert sp.expand(delta_1 - delta_1_universal) == 0

# Mode 3: hold beta_0 fixed and vary the sparse mode-1 and mode-2 pairs.
delta_3 = corner_minor(marked_mode=3, fixed_mode=0, fixed_bit=0)
delta_3_universal = (
    8
    * p
    * u0
    * plus
    * (a * plus - k * minus)
    * (a * p * z2 + a * v1 + p * u1 - p * z6)
    * (k * minus * u0 + plus * z2)
)
assert sp.expand(delta_3 - delta_3_universal) == 0

# Normalize s=1, so a=es and b=js.  Work in the exact quadratic component
# algebra Q(a,b,lambda,w,z6)[k]/(k^2-k2).
q = a + b
r = 1 + a * b
p_value = q**2 / r
k2 = p_value - a * b
component_relation = k**2 - k2
coefficient_field = sp.QQ.frac_field(a, b, slope, w, z6)
component_polynomial = sp.Poly(component_relation, k, domain=coefficient_field)


def vanishes_in_component_algebra(expression):
    numerator, _denominator = sp.together(sp.cancel(expression)).as_numer_denom()
    remainder = sp.Poly(numerator, k, domain=coefficient_field).rem(
        component_polynomial
    )
    return remainder.is_zero


inverse_k = k / k2
branch_denominator = minus * p_value - plus * q
z3_value = 1 / (2 * p_value * branch_denominator)
z2_value = minus * w
z4_value = -plus * w
z5_value = z6 - k * z3_value
z0_value = (
    p_value**2 * z3_value
    - sp.Rational(1, 2) / minus
    - q**2 * plus * k * w
) * inverse_k / q
z1_value = (
    q * z6
    - p_value * minus * w
    - b * (k**2 - a**2) * z3_value * inverse_k
)
v0_value = (
    p_value**2 * z3_value - sp.Rational(1, 2) / minus
) * inverse_k / q
v1_value = -p_value * minus * w + a * p_value * z3_value * inverse_k

# These are direct consequences of the already-certified branch extension.
assert vanishes_in_component_algebra(z0_value - q * z4_value - v0_value)
assert vanishes_in_component_algebra(z1_value - q * z5_value - v1_value)

substitution_1 = {
    p: p_value,
    u0: z4_value,
    v0: v0_value,
    z2: z2_value,
    z3: z3_value,
}
substitution_3 = {
    p: p_value,
    u0: z4_value,
    u1: z5_value,
    v1: v1_value,
    z2: z2_value,
    z3: z3_value,
}
t_bar = (1 - b) * slope - (1 + b)
special_factor = a * plus - k * minus
delta_1_factored = (
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
delta_3_factored = (
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
assert vanishes_in_component_algebra(
    delta_1.subs(substitution_1, simultaneous=True) - delta_1_factored
)
assert vanishes_in_component_algebra(
    delta_3.subs(substitution_3, simultaneous=True) - delta_3_factored
)

# On the residual intersection Tbar=A=0, b != 0,1 gives
# lambda=(1+b)/(1-b) and k=a/b.  Eliminate a from the remaining F,N equations.
a2 = (a + 1) * (b - 1) * (
    3 * a**2 * b**2
    + a**2 * b
    - a**2
    - a * b**3
    - 2 * a * b**2
    - a * b
    + b**3
)
a1 = -2 * (
    3 * a**3 * b**3
    - 2 * a**3 * b
    - a**2 * b**4
    + a**2 * b**2
    - a**2
    - a * b
    + b**4
)
a0 = (a - 1) * (b + 1) * (
    3 * a**2 * b**2
    - a**2 * b
    - a**2
    - a * b**3
    + 2 * a * b**2
    - a * b
    - b**3
)
exceptional_weight = a2 * slope**2 + a1 * slope + a0
residual_slope = (1 + b) / (1 - b)
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
assert sp.factor(
    b**2
    * (
        (a * b + (a / b) ** 2) * (1 + a * b)
        - (a + b) ** 2
    )
    - phi_f
) == 0
assert sp.factor(
    exceptional_weight.subs(slope, residual_slope)
    - 4 * (b + 1) * phi_n / (b - 1)
) == 0
sextic = 3 * b**6 - 3 * b**4 - 6 * b**2 - 2
expected_resultant = b**9 * (b - 1) ** 3 * (b + 1) ** 3 * sextic
assert sp.factor(sp.resultant(phi_f, phi_n, a)) == expected_resultant

# Marking beta_i -> beta_i+h_i alpha_i is an invertible row-basis change.
h = sp.symbols("h")
assert sp.Matrix(((1, 0), (h, 1))).det() == 1

print(
    json.dumps(
        {
            "status": "PASS",
            "normalization": {"a": "e*s", "b": "j*s", "s": 1},
            "marking_removed_by_invertible_row_change": True,
            "minor_modes": [1, 3],
            "mode_1_minor": str(delta_1_factored),
            "mode_3_minor": str(delta_3_factored),
            "necessary_rank_drop_cover": [
                "w=0",
                "k=1",
                "Tbar=0 and A=0",
            ],
            "Tbar": str(t_bar),
            "A": str(special_factor),
            "Tbar_A_residual_sextic": str(sextic),
            "residual_branches_closed": False,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
