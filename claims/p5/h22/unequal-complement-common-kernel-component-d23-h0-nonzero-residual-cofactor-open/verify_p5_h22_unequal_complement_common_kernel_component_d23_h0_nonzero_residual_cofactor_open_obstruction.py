#!/usr/bin/env python3
"""Close the cofactor open of component 22's h0-nonzero D23 residual."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
from verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_zero_residual_obstruction import (
    residual_polynomials,
)
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_"
    "H0_NONZERO_RESIDUAL_COFACTOR_OPEN_OBSTRUCTION.md"
)

A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
s = 2 * A + R
ROWS = (0, 1, 2, 3, 4, 5, 7, 8)


def mixed_matrix():
    alpha, canonical = component_rows(A, R, D)
    marked = shifted(canonical, alpha, (h0, h1, h2, h3))
    model = build_model(alpha, marked, x, "D23", "finite", rho)
    return sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in model["mixed"]]
    )


def cofactor_certificate():
    f2, f6, f7, f8, L, T, G, G2 = residual_polynomials()
    substitutions = {h1: 0, h3: s / 2}
    matrix = mixed_matrix().subs(substitutions, simultaneous=True)
    determinant = sp.factor(matrix.extract(ROWS, range(8)).det(method="domain-ge"))
    known = sp.factor(
        -8 * A * D * s**4 * (D - 1) * (D + 1) * rho * (rho - 1) * (rho + 1) * f6 * f7
    )
    quotient = sp.cancel(determinant / known)
    numerator, denominator = sp.fraction(quotient)
    assert denominator == 1
    polynomial = sp.factor(numerator)
    assert sp.factor(determinant - known * polynomial) == 0
    assert polynomial.free_symbols <= {A, R, D, h0, h2, rho}
    return polynomial, determinant, (f2, f6, f7, f8, L, T, G, G2)


def nonvacuity_certificate(polynomial, determinant, residual):
    f2, f6, f7, f8, L, T, G, G2 = residual
    radical = sp.sqrt(29665)
    point = {
        A: 2,
        R: 1,
        D: 3,
        rho: 2,
        h0: (-35 + radical) / 540,
        h1: 0,
        h2: (-199 - radical) / 1656,
        h3: sp.Rational(5, 2),
    }
    assert sp.simplify(G.subs(point)) == 0
    assert sp.simplify(G2.subs(point)) == 0
    open_factors = (
        h0,
        h2,
        f2,
        rho,
        rho - 1,
        rho + 1,
        f6,
        f7,
        f8,
        L,
        T,
        R * h2 - 1,
    )
    observed_factors = tuple(sp.factor(value.subs(point)) for value in open_factors)
    assert all(value != 0 for value in observed_factors)
    observed_polynomial = sp.factor(polynomial.subs(point))
    expected_polynomial = (-169645 + 5603 * radical) / 276
    assert sp.simplify(observed_polynomial - expected_polynomial) == 0
    assert 169645**2 - 5603**2 * 29665 != 0
    observed_determinant = sp.factor(determinant.subs(point))
    expected_determinant = -sp.Rational(20160000, 23) * (-169645 + 5603 * radical)
    assert sp.simplify(observed_determinant - expected_determinant) == 0
    assert observed_determinant != 0
    return {
        "field": "Q(sqrt(29665))",
        "point": {str(key): str(value) for key, value in point.items()},
        "open_factor_values": tuple(map(str, observed_factors)),
        "P_value": str(observed_polynomial),
        "minor_value": str(observed_determinant),
    }


def main():
    polynomial, determinant, residual = cofactor_certificate()
    point = nonvacuity_certificate(polynomial, determinant, residual)
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q(A,R,D)",
                "component": 22,
                "direction": "finite D23",
                "residual": "h1=0, 2*h3=2*A+R, G=G2=0",
                "mixed_minor_rows": ROWS,
                "mixed_minor_factorization": (
                    "-8*A*D*(2*A+R)^4*(D-1)*(D+1)*rho*(rho-1)*(rho+1)*f6*f7*P"
                ),
                "P_total_degree_in_residual_variables": sp.Poly(
                    polynomial, h0, h2, rho
                ).total_degree(),
                "P_term_count": len(sp.Poly(polynomial, h0, h2, rho).terms()),
                "nonempty_cofactor_open_point": point,
                "P_nonzero_residual_binary_empty": True,
                "remaining_residual": "h0!=0, P=0 on the displayed open factors",
                "finite_field_proof_used": False,
                "generic_weighted_H22_fibre_closed": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
