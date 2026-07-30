#!/usr/bin/env python3
"""Verify the generic disjoint-incidence conic-polarity reduction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md"


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


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, b, c = sp.symbols("a b c", nonzero=True)
    variables = (x0, x1, x2, x3, x4)
    permanent = sp.prod(variables)
    u0 = (a, 1, 1, 0, 0)
    h1 = (b, 0, 0, -1, 0)
    h2 = (c, 0, 0, 0, -1)

    mixed = derivative(
        derivative(
            derivative(permanent, variables, u0),
            variables,
            h1,
        ),
        variables,
        h2,
    )
    expected = (
        a * x1 * x2
        + (x1 + x2) * (x0 - b * x3 - c * x4)
    )
    assert sp.expand(mixed - expected) == 0

    matrix = sp.Matrix(
        [
            [a / 2, 0, 1],
            [0, -a / 2, 0],
            [1, 0, 0],
        ]
    )
    determinant = sp.factor(matrix.det())
    inverse = sp.simplify(matrix.inv())
    expected_inverse = sp.Matrix(
        [
            [0, 0, 1],
            [0, -2 / a, 0],
            [1, 0, -a / 2],
        ]
    )
    assert determinant == a / 2
    assert inverse == expected_inverse

    # H has basis s,d,w in ambient coordinates.  Its annihilator has
    # dimension two, and c*h1-b*h2 belongs to it.
    s = sp.Matrix([0, 1, 1, 0, 0])
    d = sp.Matrix([0, 1, -1, 0, 0])
    w = sp.Matrix([1, 0, 0, -b, -c])
    h_matrix = sp.Matrix.hstack(s, d, w).T
    assert h_matrix.rank() == 3
    assert len(h_matrix.nullspace()) == 2
    normal_difference = sp.Matrix(h1) * c - sp.Matrix(h2) * b
    assert h_matrix * normal_difference == sp.zeros(3, 1)
    assert sp.expand(sp.Matrix(h1).dot(w)) == 2 * b
    assert sp.expand(sp.Matrix(h2).dot(w)) == 2 * c

    sigma_i, delta_i, sigma_j, delta_j = sp.symbols(
        "sigma_i delta_i sigma_j delta_j"
    )
    kernel_i = sp.Matrix([sigma_i, delta_i, 0])
    kernel_j = sp.Matrix([sigma_j, delta_j, 0])
    polarity = sp.factor((kernel_i.T * inverse * kernel_j)[0])
    assert polarity == -2 * delta_i * delta_j / a

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a*b*c != 0",
        "incidence_type": "exact disjoint",
        "mixed_contraction": str(sp.factor(mixed)),
        "mixed_matrix_determinant": str(determinant),
        "mixed_matrix_inverse": [
            [str(value) for value in row] for row in inverse.tolist()
        ],
        "all_H_restriction_ranks": 2,
        "kernel_lines_lie_in": "span(e1+e2,e1-e2)",
        "cross_polarity_equation": str(polarity),
        "forced_common_kernel_pair": "AB or CD",
        "forced_common_kernel": "span(e1+e2)",
        "disjoint_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_disjoint_conic_polarity_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
