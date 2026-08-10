#!/usr/bin/env python3
"""Verify component 25's sparse paired-D23 w=0 obstruction."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

started = time.perf_counter()
a, b, k, slope = sp.symbols("a b k lambda")
p_symbol, z3_symbol, v0_symbol = sp.symbols("P z3 v0")
z6_symbol, z7_symbol = sp.symbols("z6 z7")
plus = slope + 1
minus = slope - 1

# For the mode-one one-marked map, use the sparse binary bases in the other
# modes.  On w=0, z2=z4=0.  The values z6,z7 remain arbitrary.
pairs = (
    (
        (1, 1, 0, 0),
        (0, 0, -p_symbol * plus, v0_symbol),
    ),
    (
        (1, -1, 0, 0),
        (1, 1, a * plus - k * minus, z6_symbol),
    ),
    (
        (0, 0, minus, z3_symbol),
        (1 - b, 1 + b, b * plus, z7_symbol),
    ),
)


def permanent_three(rows, omitted_column):
    columns = tuple(column for column in range(4) if column != omitted_column)
    return sp.expand(
        sum(
            sp.prod(rows[row][columns[permutation[row]]] for row in range(3))
            for permutation in itertools.permutations(range(3))
        )
    )


def cofactor_row(word):
    rows = tuple(pairs[index][bit] for index, bit in enumerate(word))
    return tuple(permanent_three(rows, column) for column in range(4))


primary_words = ((0, 1, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1))
primary_minor = sp.factor(
    sp.Matrix(tuple(cofactor_row(word) for word in primary_words)).det(
        method="domain-ge"
    )
)
x_minus_universal = p_symbol * plus * z3_symbol - minus * v0_symbol
x_plus_universal = p_symbol * plus * z3_symbol + minus * v0_symbol
assert sp.expand(
    primary_minor - 8 * x_minus_universal**2 * x_plus_universal
) == 0

# Insert the exact component-25 branch values and compute the quadratic norm.
q = a + b
r = 1 + a * b
p = q**2 / r
k2 = p - a * b
d0 = a**2 * b**2 - a**2 - a * b - b**2
chart_factor = plus * r - minus * q
branch_denominator = minus * p - plus * q
z3 = 1 / (2 * p * branch_denominator)
y0 = (p**2 * z3 - sp.Rational(1, 2) / minus) / (q * k2)
v0 = k * y0
x_minus = sp.cancel(p * plus * z3 - minus * v0)
x_plus = sp.cancel(p * plus * z3 + minus * v0)

assert sp.factor(d0 + r * k2) == 0
assert sp.factor(branch_denominator + q * chart_factor / r) == 0
assert sp.factor(x_minus.subs(k, -k) - x_plus) == 0

common_norm = sp.factor(
    sp.expand(x_minus * x_minus.subs(k, -k)).subs(k**2, k2)
)
expected_norm = (
    (a - 1)
    * (a + 1)
    * (b - 1)
    * (b + 1)
    * plus**2
    * r**2
    / (4 * q**2 * d0 * chart_factor**2)
)
assert sp.factor(common_norm - expected_norm) == 0
plus_norm = sp.factor(
    sp.expand(x_plus * x_plus.subs(k, -k)).subs(k**2, k2)
)
assert sp.factor(plus_norm - expected_norm) == 0

# Record why A0*A2 != 0 supplies all four numerator factors.
a2 = (a + 1) * (b - 1) * (
    3 * a**2 * b**2
    + a**2 * b
    - a**2
    - a * b**3
    - 2 * a * b**2
    - a * b
    + b**3
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
assert sp.denom(sp.cancel(a0 / ((a - 1) * (b + 1)))) == 1
assert sp.denom(sp.cancel(a2 / ((a + 1) * (b - 1)))) == 1

print(
    json.dumps(
        {
            "status": "PASS",
            "branch": "component 25 ordinary B=N=0, G!=0, A0*A2!=0, w=0",
            "marked_mode": 1,
            "sparse_row_words": ["".join(map(str, word)) for word in primary_words],
            "universal_minor": "8*X_minus^2*X_plus",
            "X_minus": "P*(lambda+1)*z3-(lambda-1)*v0",
            "X_plus": "P*(lambda+1)*z3+(lambda-1)*v0",
            "common_quadratic_norm": str(sp.factor(expected_norm)),
            "rank_four": True,
            "remaining_sparse_cover_branches": [],
            "projective_boundaries_closed": False,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
