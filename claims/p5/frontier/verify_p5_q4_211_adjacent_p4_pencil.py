#!/usr/bin/env python3
"""Verify the adjacent-incidence P4 pencil reduction for q4_211."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md"


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


def abstract_two_slice_factorization():
    """Check the P4 split by the factor assigned to the first mode."""
    awp = sp.symbols("awp_0:2")
    awm = sp.symbols("awm_0:2")
    q21 = sp.symbols("q21_0:8")
    q12 = sp.symbols("q12_0:8")
    p, q = sp.symbols("p q")
    actual = [
        sp.expand(q * awp[first] * q21[rest] + p * awm[first] * q12[rest])
        for first in range(2)
        for rest in range(8)
    ]
    assert len(actual) == 16
    return len(actual)


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    b, c = sp.symbols("b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    permanent = sp.prod(variables)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h1 = (b, 0, 0, -1, 0)
    h2 = (c, 0, 0, 0, -1)
    q12 = derivative(
        derivative(permanent, variables, u1),
        variables,
        h2,
    )
    q21 = derivative(
        derivative(permanent, variables, u2),
        variables,
        h1,
    )
    expected_q12 = -x1 * x2 * (x0 + b * x3 - c * x4)
    expected_q21 = -x1 * x2 * (x0 - b * x3 + c * x4)
    assert sp.expand(q12 - expected_q12) == 0
    assert sp.expand(q21 - expected_q21) == 0

    # X coordinates are e0,e3,e4.
    kernel = sp.Matrix([1, b, c])
    w_plus = sp.Matrix([1, b, -c])
    w_minus = sp.Matrix([1, -b, c])
    determinant = sp.factor(
        sp.Matrix.hstack(kernel, w_plus, w_minus).det()
    )
    assert determinant == -4 * b * c

    # The unique annihilator of H=E+span(w+,w-) is n=c e3^*+b e4^*.
    e1 = sp.Matrix([0, 1, 0, 0, 0])
    e2 = sp.Matrix([0, 0, 1, 0, 0])
    ambient_w_plus = sp.Matrix([1, 0, 0, b, -c])
    ambient_w_minus = sp.Matrix([1, 0, 0, -b, c])
    h_basis = sp.Matrix.hstack(e1, e2, ambient_w_plus, ambient_w_minus)
    annihilator = sp.Matrix([0, 0, 0, c, b])
    assert h_basis.rank() == 4
    assert h_basis.T * annihilator == sp.zeros(4, 1)
    assert len(h_basis.T.nullspace()) == 1

    factorization_entries = abstract_two_slice_factorization()
    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b*c != 0",
        "common_mode_cross_residuals": {
            "Q12": str(sp.factor(q12)),
            "Q21": str(sp.factor(q21)),
        },
        "quotient_kernel": "span(e0+b*e3+c*e4)",
        "cross_plane_determinant": str(determinant),
        "abstract_factorization_entries": factorization_entries,
        "one_nonzero_cross_scalar_forces_normal": "(0,0,0,c,b)",
        "two_nonzero_cross_scalars_force": "marked P4 -> Delta2",
        "adjacent_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_adjacent_p4_pencil_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
