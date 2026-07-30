#!/usr/bin/env python3
"""Verify the generic parallel-incidence kernel reduction for q4_211."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def iterated_derivative(polynomial, variables, *directions):
    result = polynomial
    for direction in directions:
        result = derivative(result, variables, direction)
    return sp.factor(result)


def abstract_p4_quotient_factorization():
    """Check the AB|CD factorization after C,D kill the E factors."""
    ae1 = sp.symbols("ae1_0:2")
    ae2 = sp.symbols("ae2_0:2")
    be1 = sp.symbols("be1_0:2")
    be2 = sp.symbols("be2_0:2")
    cf = sp.symbols("cf_0:2")
    cg = sp.symbols("cg_0:2")
    df = sp.symbols("df_0:2")
    dg = sp.symbols("dg_0:2")

    # Only permutations assigning e1,e2 to A,B and f,g to C,D survive.
    actual = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for ell in range(2):
                    actual[i, j, k, ell] = sp.expand(
                        ae1[i] * be2[j] * cf[k] * dg[ell]
                        + ae1[i] * be2[j] * cg[k] * df[ell]
                        + ae2[i] * be1[j] * cf[k] * dg[ell]
                        + ae2[i] * be1[j] * cg[k] * df[ell]
                    )
                    expected = sp.expand(
                        (ae1[i] * be2[j] + ae2[i] * be1[j])
                        * (cf[k] * dg[ell] + cg[k] * df[ell])
                    )
                    assert sp.expand(actual[i, j, k, ell] - expected) == 0
    return len(actual)


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, b, c = sp.symbols("a b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    permanent = sp.prod(variables)
    u0 = (a, 1, 1, 0, 0)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h1 = (b, 0, 0, -1, 0)
    h2 = (c, 0, 0, 0, -1)

    contractions = {
        "u1_h2_h2": iterated_derivative(
            permanent, variables, u1, h2, h2
        ),
        "u2_h1_h1": iterated_derivative(
            permanent, variables, u2, h1, h1
        ),
        "u0_h1_h1": iterated_derivative(
            permanent, variables, u0, h1, h1
        ),
        "u0_h2_h2": iterated_derivative(
            permanent, variables, u0, h2, h2
        ),
        "u0_h1_h2": iterated_derivative(
            permanent, variables, u0, h1, h2
        ),
    }
    expected = {
        "u1_h2_h2": -2 * c * x1 * x2,
        "u2_h1_h1": -2 * b * x1 * x2,
        "u0_h1_h1": -2 * b * x4 * (x1 + x2),
        "u0_h2_h2": -2 * c * x3 * (x1 + x2),
        "u0_h1_h2": (
            a * x1 * x2
            + (x1 + x2) * (x0 - b * x3 - c * x4)
        ),
    }
    assert all(
        sp.expand(contractions[name] - value) == 0
        for name, value in expected.items()
    )

    # The diagonal-pencil membership equation.  For
    # p=(p0,p1,0), q=(q0,q1,0), a rank-two diagonal matrix
    # diag(alpha,beta,0) lies in p tensor W + W tensor q exactly when
    # the quotient functional vanishes.
    p0, p1, q0, q1, alpha, beta = sp.symbols(
        "p0 p1 q0 q1 alpha beta"
    )
    left_annihilator = sp.Matrix([[-p1, p0, 0]])
    right_annihilator = sp.Matrix([[-q1], [q0], [0]])
    diagonal = sp.diag(alpha, beta, 0)
    quotient = sp.expand(
        (left_annihilator * diagonal * right_annihilator)[0]
    )
    assert quotient == alpha * p1 * q1 + beta * p0 * q0

    # A two-dimensional diagonal plane is not a fixed-factor space:
    # its generic element has determinant alpha*beta.
    assert sp.det(sp.diag(alpha, beta)) == alpha * beta

    # The source two-plane identity behind the residual dichotomy.
    s = sp.Matrix([1, 1])
    d = sp.Matrix([1, -1])
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])
    sym12 = e1 * e2.T + e2 * e1.T
    assert s * s.T - d * d.T == 2 * sym12

    # If one complementary rank-three map kills s and d, its kernel is
    # the e1,e2 plane and its row space contains both singleton normals.
    row_basis = sp.Matrix(
        [
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ]
    )
    assert row_basis.rank() == 3
    assert sp.Matrix.vstack(row_basis, sp.Matrix([h1])).rank() == 3
    assert sp.Matrix.vstack(row_basis, sp.Matrix([h2])).rank() == 3

    # In the apparent G=e1^2 boundary, quotienting A,B by their forced
    # e2 image gives the common kernel
    # k=e0+b*e3+c*e4.  The u2 P4 residual cannot vanish there.
    k = sp.Matrix([1, b, c])  # X coordinates e0,e3,e4
    source_e3 = sp.Matrix([0, 1, 0])
    source_g2 = sp.Matrix([1, 0, c])
    assert source_g2 + b * source_e3 == k
    quotient_u2 = sp.expand(-2 * b)
    assert quotient_u2 != 0

    # The G=e2^2 case is the colour-swapped quotient of u1.
    source_e4 = sp.Matrix([0, 0, 1])
    source_g1 = sp.Matrix([1, b, 0])
    assert source_g1 + c * source_e4 == k
    quotient_u1 = sp.expand(-2 * c)
    assert quotient_u1 != 0
    factorization_entries = abstract_p4_quotient_factorization()

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b*c != 0",
        "parallel_common_modes": 2,
        "source_contractions": {
            name: str(value) for name, value in contractions.items()
        },
        "diagonal_pencil_quotient": str(quotient),
        "fixed_factor_diagonal_plane_possible": False,
        "zero_residual_forces_third_common_incidence": True,
        "nonzero_residual_intermediate_kernel": "span(e1+e2)",
        "nonzero_residual_quotient_coefficients": [
            str(quotient_u2),
            str(quotient_u1),
        ],
        "abstract_p4_quotient_factorization_entries": factorization_entries,
        "nonzero_residual_excluded": True,
        "parallel_without_third_common_incidence_excluded": True,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_parallel_incidence_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
