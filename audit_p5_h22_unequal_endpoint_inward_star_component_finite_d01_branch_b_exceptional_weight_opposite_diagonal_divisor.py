#!/usr/bin/env python3
"""No-import audit of component 25's opposite-diagonal resultant divisor."""

from __future__ import annotations

import json
import time

import sympy as sp

started = time.perf_counter()
a, b, lam = sp.symbols("a b lambda")

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
n = a2 * lam**2 + a1 * lam + a0

g4 = (
    a**3 * (b - 1) ** 2
    + a**2 * (-b**3 + 3 * b - 2)
    - a * (b - 1) ** 2
    + b**3
    - 3 * b
    + 2
)
g3 = (
    2 * a**3 * b**2
    - 2 * a**3
    + 2 * a**2 * b**3
    + 4 * a**2 * b**2
    - 6 * a**2 * b
    - 6 * a * b**2
    + 8 * a * b
    - 2 * a
    - 2 * b**3
    - 2 * b
    + 4
)
g2 = (
    -6 * a**3 * b**2
    + 2 * a**3
    - 2 * a**2 * b**3
    - 2 * a**2 * b
    + 6 * a * b**2
    - 2 * a
    + 2 * b**3
    + 2 * b
)
g1 = (
    2 * a**3 * b**2
    - 2 * a**3
    + 2 * a**2 * b**3
    - 4 * a**2 * b**2
    - 6 * a**2 * b
    - 6 * a * b**2
    - 8 * a * b
    - 2 * a
    - 2 * b**3
    - 2 * b
    - 4
)
g0 = (
    a**3 * (b + 1) ** 2
    + a**2 * (-b**3 + 3 * b + 2)
    - a * (b + 1) ** 2
    + b**3
    - 3 * b
    - 2
)
g = g4 * lam**4 + g3 * lam**3 + g2 * lam**2 + g1 * lam + g0

# The reciprocal relation is audited directly from the displayed coefficients.
assert sp.factor(
    g
    + lam**4
    * g.subs({a: -a, b: -b, lam: 1 / lam}, simultaneous=True)
) == 0

u = (
    5 * a**6 * b**5
    - 5 * a**6 * b**3
    + a**6 * b
    - 4 * a**5 * b**6
    + 12 * a**5 * b**4
    - 10 * a**5 * b**2
    + 2 * a**5
    - a**4 * b**7
    - a**4 * b**5
    - 2 * a**4 * b**3
    + a**4 * b
    + 8 * a**3 * b**6
    - 14 * a**3 * b**4
    + 6 * a**3 * b**2
    + 2 * a**2 * b**7
    - 2 * a**2 * b**5
    + 3 * a**2 * b**3
    - 4 * a * b**6
    + 4 * a * b**4
    - b**7
)
expected_resultant = (
    64
    * a
    * (a - b) ** 3
    * (a + b) ** 5
    * (a - 1)
    * (a + 1)
    * (b - 1) ** 2
    * (b + 1) ** 2
    * u
)

# Build the 6 by 6 Sylvester matrix directly.  This does not call resultant.
f_coefficients = (a2, a1, a0)
g_coefficients = (g4, g3, g2, g1, g0)
sylvester_rows = []
for shift in range(4):
    sylvester_rows.append(
        [sp.S.Zero] * shift
        + list(f_coefficients)
        + [sp.S.Zero] * (3 - shift)
    )
for shift in range(2):
    sylvester_rows.append(
        [sp.S.Zero] * shift
        + list(g_coefficients)
        + [sp.S.Zero] * (1 - shift)
    )
sylvester_determinant = sp.factor(
    sp.Matrix(sylvester_rows).det(method="domain-ge")
)
assert sylvester_determinant == expected_resultant

factor_unit, factors = sp.factor_list(u)
assert factor_unit == 1
assert factors == [(u, 1)]
excluded_factors = (
    a,
    a - b,
    a + b,
    a - 1,
    a + 1,
    b - 1,
    b + 1,
)
assert all(sp.gcd(sp.Poly(u, a, b), sp.Poly(factor, a, b)) == 1 for factor in excluded_factors)

print(
    json.dumps(
        {
            "status": "PASS",
            "normalization": {"a": "e*s", "b": "j*s"},
            "exceptional_polynomial_degree_lambda": int(sp.degree(n, lam)),
            "opposite_factor_degree_lambda": int(sp.degree(g, lam)),
            "sylvester_matrix_size": [6, 6],
            "resultant_factorization": str(expected_resultant),
            "residual_hypersurface": "U(a,b)=0",
            "residual_hypersurface_irreducible": True,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
