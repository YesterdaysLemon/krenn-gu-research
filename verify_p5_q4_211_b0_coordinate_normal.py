#!/usr/bin/env python3
"""Verify the b=0 coordinate-normal boundary reduction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_B0_COORDINATE_NORMAL_REDUCTION.md"


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


def repeated_derivative(polynomial, variables, directions):
    result = polynomial
    for direction in directions:
        result = derivative(result, variables, direction)
    return sp.factor(result)


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, c = sp.symbols("a c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    source_permanent = sp.prod(variables)

    u0 = sp.Matrix([a, 1, 1, 0, 0])
    e3 = sp.Matrix([0, 0, 0, 1, 0])
    u2 = sp.Matrix([c, 0, 0, 0, 1])
    h2 = sp.Matrix([c, 0, 0, 0, -1])
    e1 = sp.eye(5)[:, 1]
    e2 = sp.eye(5)[:, 2]
    k = sp.Matrix([1, 0, 0, 0, c])
    s = e1 + e2
    d = e1 - e2
    w = sp.Matrix([1, 0, 0, 0, -c])

    coordinate_double = repeated_derivative(
        source_permanent, variables, (e3, e3)
    )
    mixed_p3 = repeated_derivative(
        source_permanent, variables, (u2, e3)
    )
    repeated_u2 = repeated_derivative(
        source_permanent, variables, (u2, u2)
    )
    propagated_kernel = repeated_derivative(
        source_permanent, variables, (u0, e3, h2, h2)
    )
    mixed_conic = repeated_derivative(
        source_permanent, variables, (u0, e3, h2)
    )
    assert coordinate_double == 0
    assert mixed_p3 == x1 * x2 * (x0 + c * x4)
    assert repeated_u2 == 2 * c * x1 * x2 * x3
    assert propagated_kernel == -2 * c * (x1 + x2)

    j_basis = sp.Matrix.hstack(e1, e2, k)
    j_annihilator = sp.Matrix.hstack(e3, h2)
    assert j_basis.T * j_annihilator == sp.zeros(3, 2)
    assert j_basis.rank() == 3
    assert j_annihilator.rank() == 2

    h_basis = sp.Matrix.hstack(s, d, w)
    conic_matrix = sp.Matrix(
        [
            [a / 2, 0, 1],
            [0, -a / 2, 0],
            [1, 0, 0],
        ]
    )
    assert sp.factor(conic_matrix.det()) == a / 2
    expected_conic = (
        a * x1 * x2 + (x1 + x2) * (x0 - c * x4)
    )
    assert sp.expand(mixed_conic + expected_conic) == 0

    g0, g1, g2 = sp.symbols("g0 g1 g2")
    quadratic_slice = sp.Matrix(
        [
            [0, g2, g1],
            [g2, 0, g0],
            [g1, g0, 0],
        ]
    )
    principal_minors = [
        sp.factor(
            quadratic_slice.extract(indices, indices).det()
        )
        for indices in ((0, 1), (0, 2), (1, 2))
    ]
    assert principal_minors == [-g2**2, -g1**2, -g0**2]
    binary_permanent = sp.Matrix([[0, 1], [1, 0]])
    assert binary_permanent.det() == -1

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "b=0, a*c != 0",
        "coordinate_normal_incidence_count": 2,
        "coordinate_normal_target_rows": ["C*e0^*", "C*e2^*"],
        "mixed_p3": str(mixed_p3),
        "repeated_u2": str(repeated_u2),
        "propagated_kernel_contraction": str(propagated_kernel),
        "mixed_conic": str(mixed_conic),
        "conic_determinant": str(sp.factor(conic_matrix.det())),
        "quadratic_slice_principal_minors": [
            str(value) for value in principal_minors
        ],
        "exact_disjoint_excluded": True,
        "exact_parallel_excluded": True,
        "remaining_incidence": (
            "h2 at B and C; either also A, or exactly B,C,D with A(s)=0"
        ),
        "b0_boundary_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_b0_coordinate_normal_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
